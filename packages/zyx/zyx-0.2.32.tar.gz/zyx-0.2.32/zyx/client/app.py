__all__ = ["app", "cli"]

# --- zyx ----------------------------------------------------------------

from textual.app import App, ComposeResult
from textual.widgets import Input, RichLog
from textual.containers import VerticalScroll
from typing import Any, Union, Optional, List, Callable, Literal
from ..types import ClientModeParams
from ..core.ext import BaseModel

COLOR_MAP = {
    "deep_blue": "#001f3f",
    "ocean_blue": "#0074D9",
    "sunset_orange": "#FF851B",
    "twilight_purple": "#6F42C1",
    "forest_green": "#2ECC40",
    "midnight_black": "#111111",
    "crimson_red": "#DC143C",
    "royal_gold": "#FFD700",
    "peach": "#FFDAB9",
    "lavender": "#E6E6FA",
    "teal": "#008080",
    "coral": "#FF7F50",
    "mustard_yellow": "#FFDB58",
    "powder_blue": "#B0E0E6",
    "sage_green": "#B2AC88",
    "blush": "#FF6F61",
    "steel_grey": "#7A8B8B",
    "ice_blue": "#AFEEEE",
    "burnt_sienna": "#E97451",
    "plum": "#DDA0DD",
}

ColorName = Literal[
    "deep_blue",
    "ocean_blue",
    "sunset_orange",
    "twilight_purple",
    "forest_green",
    "midnight_black",
    "crimson_red",
    "royal_gold",
    "peach",
    "lavender",
    "teal",
    "coral",
    "mustard_yellow",
    "powder_blue",
    "sage_green",
    "blush",
    "steel_grey",
    "ice_blue",
    "burnt_sienna",
    "plum",
]


class ChatApp(App):
    def __init__(
        self,
        messages: Union[str, list[dict]] = None,
        model: Optional[str] = "gpt-4o-mini",
        tools: Optional[List[Union[Callable, dict, BaseModel]]] = None,
        run_tools: Optional[bool] = True,
        response_model: Optional[BaseModel] = None,
        mode: Optional[ClientModeParams] = "tools",
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        organization: Optional[str] = None,
        top_p: Optional[float] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_retries: Optional[int] = 3,
        verbose: Optional[bool] = False,
        background: Optional[Union[str, ColorName]] = "midnight_black",
        text: Optional[Union[str, ColorName]] = "steel_grey",
        input_field: Optional[Union[str, ColorName]] = "ocean_blue",
        **kwargs,
    ):
        try:
            from .main import Client

            super().__init__()
            self.client = Client()
            self.chat_history = (
                self.client.format_messages(messages) if messages else []
            )
            self.model = model
            self.tools = tools
            self.run_tools = run_tools
            self.response_model = response_model
            self.mode = mode
            self.base_url = base_url
            self.api_key = api_key
            self.organization = organization
            self.top_p = top_p
            self.temperature = temperature
            self.max_tokens = max_tokens
            self.max_retries = max_retries
            self.verbose = verbose
            self.background = COLOR_MAP.get(background, background)
            self.text = COLOR_MAP.get(text, text)
            self.input_field = COLOR_MAP.get(input_field, input_field)
            self.kwargs = kwargs
        except Exception as e:
            print(f"Error initializing ChatApp: {e}")

    def compose(self) -> ComposeResult:
        try:
            self.CSS = f"""
            ChatApp {{
                background: {self.background};
            }}
            
            RichLog#chat_display {{
                border: round $primary;
                background: #2e2e2e;
                color: {self.text};
                padding: 1 2;
            }}
        
            Input#input_field {{
                border: round $primary;
                background: {self.input_field};
                color: $text;
                padding: 1 2;
            }}
            """

            with VerticalScroll():
                yield RichLog(id="chat_display")
                yield Input(placeholder="Type your message...", id="input_field")
        except Exception as e:
            print(f"Error composing ChatApp: {e}")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        try:
            from rich.text import Text

            user_message = event.value.strip()
            if user_message:
                self.chat_history.append({"role": "user", "content": user_message})

                user_text = Text()
                user_text.append("User: ", style="bold blue")
                user_text.append(f"{user_message}\n")

                # Write the styled text to RichLog
                self.query_one("#chat_display", RichLog).write(user_text)

                response = self.client.completion(
                    messages=self.chat_history,
                    model=self.model,
                    tools=self.tools,
                    run_tools=self.run_tools,
                    response_model=self.response_model,
                    mode=self.mode,
                    base_url=self.base_url,
                    api_key=self.api_key,
                    organization=self.organization,
                    top_p=self.top_p,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    max_retries=self.max_retries,
                    verbose=self.verbose,
                    **self.kwargs,
                )

                assistant_reply = response.choices[0].message["content"]
                self.chat_history.append(
                    {"role": "assistant", "content": assistant_reply}
                )

                assistant_text = Text()
                assistant_text.append("Assistant: ", style="bold green")
                assistant_text.append(f"{assistant_reply}\n")

                self.query_one("#chat_display", RichLog).write(assistant_text)

                self.query_one("#input_field", Input).value = ""
        except Exception as e:
            print(f"Error processing input: {e}")


def cli(
    messages: Union[str, list[dict]] = None,
    model: Optional[str] = "gpt-4o-mini",
    tools: Optional[List[Union[Callable, dict, BaseModel]]] = None,
    run_tools: Optional[bool] = True,
    response_model: Optional[BaseModel] = None,
    mode: Optional[ClientModeParams] = "tools",
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    top_p: Optional[float] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    max_retries: Optional[int] = 3,
    verbose: Optional[bool] = False,
    background: Optional[Union[str, ColorName]] = "midnight_black",
    text: Optional[Union[str, ColorName]] = "steel_grey",
    input_field: Optional[Union[str, ColorName]] = "ocean_blue",
    **kwargs,
):
    try:
        ChatApp(
            messages=messages,
            model=model,
            tools=tools,
            run_tools=run_tools,
            response_model=response_model,
            mode=mode,
            base_url=base_url,
            api_key=api_key,
            organization=organization,
            top_p=top_p,
            temperature=temperature,
            max_tokens=max_tokens,
            max_retries=max_retries,
            verbose=verbose,
            background=background,
            text=text,
            input_field=input_field,
            **kwargs,
        ).run()
    except Exception as e:
        print(f"Error running ChatApp: {e}")


# --- zyx ----------------------------------------------------------------


class CustomChatApp(App):
    def __init__(
        self,
        input_handler: Callable[[str], Any],
        output_handler: Callable[[Any], str],
        background: Optional[Union[str, ColorName]] = "midnight_black",
        text: Optional[Union[str, ColorName]] = "steel_grey",
        input_field: Optional[Union[str, ColorName]] = "ocean_blue",
    ):
        try:
            super().__init__()
            self.input_handler = input_handler
            self.output_handler = output_handler
            self.background = COLOR_MAP.get(background, background)
            self.text = COLOR_MAP.get(text, text)
            self.input_field = COLOR_MAP.get(input_field, input_field)
        except Exception as e:
            print(f"Error initializing CustomChatApp: {e}")

    def compose(self) -> ComposeResult:
        try:
            self.CSS = f"""
            CustomChatApp {{
                background: {self.background};
            }}
            
            RichLog#chat_display {{
                border: round $primary;
                background: #2e2e2e;
                color: {self.text};
                padding: 1 2;
            }}
        
            Input#input_field {{
                border: round $primary;
                background: {self.input_field};
                color: $text;
                padding: 1 2;
            }}
            """
            with VerticalScroll():
                yield RichLog(id="chat_display")
                yield Input(placeholder="Type your message...", id="input_field")
        except Exception as e:
            print(f"Error composing CustomChatApp: {e}")

    def on_input_submitted(self, event: Input.Submitted) -> None:
        try:
            from rich.text import Text

            user_message = event.value.strip()
            if user_message:
                user_text = Text()
                user_text.append("User: ", style="bold blue")
                user_text.append(f"{user_message}\n")
                self.query_one("#chat_display", RichLog).write(user_text)

                processed_input = self.input_handler(user_message)

                response = self.output_handler(processed_input)

                assistant_text = Text()
                assistant_text.append("Assistant: ", style="bold green")
                assistant_text.append(f"{response}\n")
                self.query_one("#chat_display", RichLog).write(assistant_text)

                self.query_one("#input_field", Input).value = ""
        except Exception as e:
            print(f"Error processing input in CustomChatApp: {e}")


def app(
    input_handler: Callable[[str], Any],
    output_handler: Callable[[Any], str],
    background: Optional[Union[str, ColorName]] = "midnight_black",
    text: Optional[Union[str, ColorName]] = "steel_grey",
    input_field: Optional[Union[str, ColorName]] = "ocean_blue",
):
    """
    Creates and runs a custom chat application with user-defined input and output handlers.

    Parameters:
    - input_handler: A function that takes a string (user input) and returns any type of data.
    - output_handler: A function that takes the result of input_handler and returns a string (assistant's response).
    - background: Background color of the app.
    - text: Text color in the chat display.
    - input_field: Color of the input field.

    Example usage:
    def custom_input_handler(user_input: str) -> dict:
        return {"user_message": user_input}

    def custom_output_handler(processed_input: dict) -> str:
        return f"Received: {processed_input['user_message']}"

    app(custom_input_handler, custom_output_handler)
    """
    try:
        CustomChatApp(
            input_handler=input_handler,
            output_handler=output_handler,
            background=background,
            text=text,
            input_field=input_field,
        ).run()
    except Exception as e:
        print(f"Error running CustomChatApp: {e}")
