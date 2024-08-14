import logging
from typing import Any, Dict, List, Union, Callable

from .._client import SGPClient
from .._models import BaseModel
from ..types.shared.test_case import TestCase
from ..types.application_test_case_output_batch_params import (
    Body as _ApplicationTestCaseOutputPayload,
    BodyOutput as _Output,
)

log: logging.Logger = logging.getLogger("scale_gp")


class ExternalApplicationOutputCompletion(BaseModel):
    generation_output: str


class Chunk(BaseModel):
    metadata: Dict[str, Any] = {}
    text: str


class ExternalApplicationOutputContextChunks(ExternalApplicationOutputCompletion):
    chunks: List[Chunk] = []


class ExternalApplicationOutputContextString(ExternalApplicationOutputCompletion):
    info: str = ""


ExternalApplicationOutput = Union[
    ExternalApplicationOutputCompletion, ExternalApplicationOutputContextChunks, ExternalApplicationOutputContextString
]


ExternalApplicationCallable = Callable[[str], ExternalApplicationOutput]


class ExternalApplication:
    def __init__(self, client: SGPClient):
        self.client = client
        self._initialized = False

    def initialize(self, *, application_variant_id: str, application: ExternalApplicationCallable):
        application_variant = self.client.application_variants.retrieve(application_variant_id)

        if application_variant.version != "OFFLINE":
            raise ValueError(f"Application variant {application_variant_id} is not an external application.")

        self.application_variant = application_variant
        self.application = application

        output_schema_type = application_variant.configuration.output_schema_type

        if output_schema_type == "completion_only":
            self._output_model = ExternalApplicationOutputCompletion
        elif output_schema_type == "context_chunks":
            self._output_model = ExternalApplicationOutputContextChunks
        elif output_schema_type == "context_string":
            self._output_model = ExternalApplicationOutputContextString
        elif output_schema_type is None:
            self._output_model = None
        else:
            raise ValueError(f"Unknown application output schema type: {output_schema_type}")

        self._initialized = True
        return self

    def generate_outputs(self, *, evaluation_dataset_id: str, evaluation_dataset_version: int):
        self._check_initialized()

        test_cases = self._retrieve_test_cases_to_run(evaluation_dataset_id, evaluation_dataset_version)
        test_case_id_to_output: Dict[str, ExternalApplicationOutput] = {}

        for test_case in test_cases:
            prompt = test_case.test_case_data.input
            log.info(f'\nRunning test case {test_case.id}\nPrompt: "{prompt}"')

            output = self._format_output(self.application(prompt))
            log.info(f'\nApplication responded with:\n"{output.generation_output}"')

            test_case_id_to_output[test_case.id] = output

        if test_case_id_to_output:
            self._create_outputs(evaluation_dataset_version, test_case_id_to_output)

        log.info(
            f"Created {len(test_case_id_to_output)} outputs on evaluation dataset {evaluation_dataset_id} version {evaluation_dataset_version} for application variant {self.application_variant.id}"
        )

    def _retrieve_test_cases_to_run(self, evaluation_dataset_id: str, version: int) -> List[TestCase]:
        existing_outputs_response = self.client.application_test_case_outputs.list(
            application_variant_id=self.application_variant.id,
            evaluation_dataset_id=evaluation_dataset_id,
            evaluation_dataset_version_num=version,
            limit=10_000,
        )

        existing_outputs = {output.test_case_id for output in existing_outputs_response.items}

        test_case_history_response = self.client.evaluation_datasets.test_cases.history.list(
            str(version),
            evaluation_dataset_id=evaluation_dataset_id,
            limit=10_000,
        )

        return [test_case for test_case in test_case_history_response.items if test_case.id not in existing_outputs]

    def _format_output(self, output: Any) -> ExternalApplicationOutput:
        if self._output_model is not None and not isinstance(output, self._output_model):
            return self._output_model.model_validate(output)
        return output

    def _create_outputs(
        self,
        evaluation_dataset_version: int,
        test_case_id_to_output: Dict[str, ExternalApplicationOutput],
    ):
        outputs: List[_ApplicationTestCaseOutputPayload] = []

        def get_output_dict(output: ExternalApplicationOutput) -> _Output:
            if isinstance(output, ExternalApplicationOutputContextChunks):
                return {
                    "generation_output": output.generation_output,
                    "generation_extra_info": {
                        "chunks": [
                            {
                                "metadata": chunk.metadata,
                                "text": chunk.text,
                            }
                            for chunk in output.chunks
                        ],
                        "schema_type": "CHUNKS",
                    },
                }
            elif isinstance(output, ExternalApplicationOutputContextString):
                return {
                    "generation_output": output.generation_output,
                    "generation_extra_info": {
                        "info": output.info,
                        "schema_type": "STRING",
                    },
                }
            else:
                return {
                    "generation_output": output.generation_output,
                }

        for test_case_id, output in test_case_id_to_output.items():
            outputs.append(
                {
                    "account_id": self.application_variant.account_id,
                    "application_variant_id": self.application_variant.id,
                    "evaluation_dataset_version_num": evaluation_dataset_version,
                    "output": get_output_dict(output),
                    "schema_type": "GENERATION",
                    "test_case_id": test_case_id,
                }
            )

        self.client.application_test_case_outputs.batch(
            body=outputs,
        )

    def _check_initialized(self):
        if not self._initialized:
            raise ValueError(f"{self} is not initialized.")
