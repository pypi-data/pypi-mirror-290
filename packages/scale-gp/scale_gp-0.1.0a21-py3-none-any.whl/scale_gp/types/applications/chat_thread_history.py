# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel
from ..chat_thread import ChatThread
from .application_interaction import ApplicationInteraction
from .chat_threads.chat_thread_feedback import ChatThreadFeedback

__all__ = ["ChatThreadHistory", "Message"]


class Message(BaseModel):
    entry: ApplicationInteraction

    feedback: Optional[ChatThreadFeedback] = None


class ChatThreadHistory(BaseModel):
    messages: List[Message]

    thread: ChatThread
