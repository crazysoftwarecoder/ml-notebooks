from typing import Any, Optional
from smolagents.tools import Tool
from smolagents.agent_types import AgentImage

class FinalAnswerTool(Tool):
    name = "final_answer"
    description = "Provides a final answer to the given problem. For images, pass the image directly."
    inputs = {'answer': {'type': 'any', 'description': 'The final answer - can be text, number, image, etc.'}}
    output_type = "any"

    def forward(self, answer: Any) -> Any:
        # Handle different types of answers
        if hasattr(answer, 'save') and hasattr(answer, 'size'):
            # It's a PIL image - convert to AgentImage for proper display
            try:
                return AgentImage(answer)
            except:
                return f"Generated image (PIL format): {answer.size[0]}x{answer.size[1]}"
        elif isinstance(answer, dict) and 'filename' in answer:
            # It's metadata about an image - extract meaningful info
            return f"Image generated: {answer.get('filename', 'image file')}"
        else:
            # Regular text/number answer
            return answer

    def __init__(self, *args, **kwargs):
        self.is_initialized = False
