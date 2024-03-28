from typing import Any, Dict, List
from uuid import UUID
from langchain.callbacks.base import BaseCallbackHandler
from langchain_core.messages import BaseMessage


class StreamingHandler(BaseCallbackHandler):
    def __init__(self, queue):
        self.queue = queue
        self.streaming_run_ids = set()

    def on_chat_model_start(self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], run_id: UUID, **kwargs) -> Any:
        if serialized["kwargs"]["streaming"]:
            self.streaming_run_ids.add(run_id)

    def on_llm_new_token(self, token):
        self.queue.put(token)

    def on_llm_end(self, run_id: UUID, **kwargs):
        if run_id in self.streaming_run_ids:
            self.queue.put(None)
            self.streaming_run_ids.remove(run_id)

    def on_llm_error(self):
        self.queue.put(None)
