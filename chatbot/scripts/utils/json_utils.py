import json
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from typing import Any

class ChatbotJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (HumanMessage, AIMessage, SystemMessage)):
            return {"type": obj.__class__.__name__, "content": obj.content}
        return super().default(obj)


def pretty_print_json(*, obj: Any) -> str:
    return json.dumps(obj, indent=2, cls=ChatbotJSONEncoder)
