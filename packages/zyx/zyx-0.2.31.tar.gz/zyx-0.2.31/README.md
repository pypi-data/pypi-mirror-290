
## **hammad dev** - *Fun stuff I've made?*
</br>
### zyx - Super duper fast, litellm, instructor tool calling & executing abstraction*

**Install**
```bash
pip install zyx
```

**Completion**
```python
import zyx

class ResponseModel(BaseModel):
    # some_fields....

def some_tool():
    # some function....

zyx.completion(
    "hello!",
    model = "ollama/llama3.1",
    tools = [some_tool], # Handles Raw Python functions
    response_model = ResponseModel, # With Optionsl Instructor Parsing
    run_tools = True # Choose to automatically execute tools
)
```

**Textual CLI Chat Interface**
Launches a nice looking CLI interface, with color customization. 
Built using Textual.
```python
import zyx

zyx.cli() # Takes in any argument .completion() can take

# or define your own
zyx.app()
```

    