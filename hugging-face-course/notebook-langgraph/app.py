from smolagents import CodeAgent,DuckDuckGoSearchTool, HfApiModel,load_tool,tool
import datetime
import requests
import pytz
import yaml
from tools.final_answer import FinalAnswerTool

from Gradio_UI import GradioUI

# Below is an example of a tool that does nothing. Amaze us with your creativity !
@tool
def my_custom_tool(arg1:str, arg2:int)-> str: #it's import to specify the return type
    #Keep this format for the description / args / args description but feel free to modify the tool
    """A tool that does nothing yet 
    Args:
        arg1: the first argument
        arg2: the second argument
    """
    return "What magic will you build ?"

@tool
def get_current_time_in_timezone(timezone: str) -> str:
    """A tool that fetches the current local time in a specified timezone.
    Args:
        timezone: A string representing a valid timezone (e.g., 'America/New_York').
    """
    try:
        # Create timezone object
        tz = pytz.timezone(timezone)
        # Get current time in that timezone
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        return f"The current local time in {timezone} is: {local_time}"
    except Exception as e:
        return f"Error fetching time for timezone '{timezone}': {str(e)}"


final_answer = FinalAnswerTool()

# If the agent does not answer, the model is overloaded, please use another model or the following Hugging Face Endpoint that also contains qwen2.5 coder:
# model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud' 

from smolagents import LiteLLMModel

model = LiteLLMModel(
    model_id="ollama_chat/qwen2:7b",  # Or try other Ollama-supported models
    api_base="http://127.0.0.1:11434",  # Default Ollama local server
    num_ctx=8192,
)

# Import tool from Hub
try:
    image_generation_tool = load_tool("agents-course/text-to-image", trust_remote_code=True)
    print("✅ Image generation tool loaded successfully")
except Exception as e:
    print(f"❌ Failed to load image tool: {e}")
    # Create a working ASCII art image tool as fallback
    @tool
    def ascii_image_generator(prompt: str) -> str:
        """Generate ASCII art based on the prompt"""
        if 'cat' in prompt.lower():
            return '''🐱 ASCII Cat Generated:
    /\\_/\\  
   ( o.o ) 
    > ^ <  
  __|___|__
'''
        elif 'dog' in prompt.lower():
            return '''🐶 ASCII Dog Generated:
    / \\   / \\
   (   o_o   )
    \\  <_>  /
     )     (
    /       \\
   (  (o) (o)  )
'''
        elif 'house' in prompt.lower():
            return '''🏠 ASCII House Generated:
      /\\    
     /  \\   
    /____\\  
    |    |  
    | [] |  
    |____|  
'''
        else:
            return f'''🎨 ASCII Art for "{prompt}":
    ┌─────────────┐
    │   *  o  *   │
    │  o  ┌─┐  o  │
    │  *  │ │  *  │
    │     └─┘     │
    └─────────────┘
'''
    image_generation_tool = ascii_image_generator

print("🔧 Note: If the remote image tool loaded successfully, it creates PIL images")
print("   The agent might need to be instructed to use 'image_generation_tool' instead of 'image_generator'")

with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)
    
# Add custom instruction for image handling
custom_prompt = """
When generating images:
1. Use image_generation_tool(prompt="your description") to generate images
2. Pass the generated image directly to final_answer(image) 
3. Do NOT try to save images to files or create metadata
4. Do NOT use image_generator() function directly

Example:
```python
image = image_generation_tool(prompt="a cute cat")
final_answer(image)
```
"""

# Update the prompt templates to include image handling instructions
if 'run' in prompt_templates:
    prompt_templates['run'] = prompt_templates['run'] + "\n\n" + custom_prompt

agent = CodeAgent(
    model=model,
    tools=[final_answer, image_generation_tool, get_current_time_in_timezone], ## add your tools here (don't remove final answer)
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name=None,
    description=None,
    prompt_templates=prompt_templates,
    # Add authorized imports to fix numpy/PIL import errors
    additional_authorized_imports=[
        'numpy', 'PIL', 'matplotlib', 'pandas', 'requests', 'base64', 'io', 
        'cv2', 'torch', 'transformers', 'scipy', 'sklearn'
    ]
)


GradioUI(agent).launch()