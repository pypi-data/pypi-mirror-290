
## **hammad-dev** - *A collection of fun things I've made*

### **zyx** - *Super Duper Lightweight AI functions, built on LiteLLM & Instructor*

**Install**
```bash
pip install zyx
```

</br>

**Chat Completions w/ Pydantic Outputs & Tool Calling**
```python
import zyx
from pydantic import BaseModel

# Send a standard completion
zyx.completion("Hello how are you?")

# Send a completion with a Pydantic output
class Response(BaseModel):
    response: str

zyx.completion("Hello how are you?", response_model = Response)

# Call a tool
zyx.completion(
    "Hello how are you?,
    model = "ollama/llama3.1
    response_model = Response,
    tools = [some_tool()],

    # Optionally Run Tool Execution as well
    # This parameter will result in more than 1 LLM completion, for tool interpretation
    run_tools = True
)
```