# zyx ==============================================================================

__all__ = ["_tailwind"]

from typing import Optional, List, Union, Tuple


class TailwindManager:
    """
    A manager class for handling Tailwind CSS and React client integration in Jupyter notebooks.
    """

    initialized = False

    def __init__(self, className: Optional[str] = None):
        self.className = className if className is not None else ""
        if not TailwindManager.initialized:
            self.setup_environment()
            TailwindManager.initialized = True

    def setup_environment(self):
        """
        Set up Tailwind CSS and custom fonts. This method ensures that Tailwind CSS is loaded only once.
        It also checks for an existing React client.
        """
        setup_scripts = """
        <!DOCTYPE html>
        <html>
        <head>
            <script>
                if (!window.React) {
                    var reactScript = document.createElement('script');
                    reactScript.src = 'https://unpkg.com/react/umd/react.development.js';
                    document.head.appendChild(reactScript);

                    var reactDomScript = document.createElement('script');
                    reactDomScript.src = 'https://unpkg.com/react-dom/umd/react-dom.development.js';
                    document.head.appendChild(reactDomScript);
                }
            </script>
            <script src="https://cdn.tailwindcss.com"></script>
            <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Lexend:wght@400;500;600;700&family=Lora:wght@400;500;600;700&family=Playfair+Display:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
            <style>
                body {{ font-family: 'DM Sans', sans-serif; }}
                h1, h2, h3, h4, h5, h6 {{ font-family: 'Lexend', sans-serif; }}
                p {{ font-family: 'Lora', serif; }}
                code, pre {{ font-family: 'JetBrains Mono', monospace; }}
                .playfair {{ font-family: 'Playfair Display', serif; }}
                .dm-sans {{ font-family: 'DM Sans', sans-serif; }}
                .lexend {{ font-family: 'Lexend', sans-serif; }}
                .lora {{ font-family: 'Lora', serif; }}
                .jetbrains-mono {{ font-family: 'JetBrains Mono', monospace; }}
            </style>
        </head>
        </html>
        """
        try:
            from IPython.display import display, HTML
        except ImportError:
            raise ImportError("""This module requires IPython to be installed, which is not included in the 'zyx' base package
                      Please install it by running :
                      '! pip install IPython' -- in your notebook
                      'pip install ipython' -- in your terminal
                      """)
        display(HTML(setup_scripts))

    def display(
        self,
        content: str,
        className: Optional[str] = "",
        component: Optional[str] = "div",
    ):
        """
        Display the HTML element with the specified content, component type, and Tailwind CSS class.
        """
        element = f"<{component} class='{className}'>{content}</{component}>"
        if self.className:
            content = f"<div class='{self.className}'>{element}</div>"
        else:
            content = element
        html = f"<!DOCTYPE html><html><body>{content}</body></html>"
        try:
            from IPython.display import display, HTML
        except ImportError:
            raise ImportError("""This module requires IPython to be installed, which is not included in the 'zyx' base package
                      Please install it by running :
                      '! pip install IPython' -- in your notebook
                      'pip install ipython' -- in your terminal
                      """)
        display(HTML(html))

    def display_components(
        self,
        components: List[Union[str, Tuple[str, str]]],
        className: Optional[str] = "",
    ):
        """
        Display multiple components inside a div with the specified Tailwind CSS class.
        """
        elements = []
        for component in components:
            if isinstance(component, str):
                content = component
                component_className = ""
            else:
                content, component_className = component
            element = f"<div class='{component_className}'>{content}</div>"
            elements.append(element)

        content = "\n".join(elements)
        div_className = f"{self.className} {className}".strip()
        html = f"<!DOCTYPE html><html><body><div class='{div_className}'>{content}</div></body></html>"
        try:
            from IPython.display import display, HTML
        except ImportError:
            raise ImportError("""This module requires IPython to be installed, which is not included in the 'zyx' base package
                      Please install it by running :
                      '! pip install IPython' -- in your notebook
                      'pip install ipython' -- in your terminal
                      """)
        display(HTML(html))


# Singleton Tailwind manager instance
_tailwind_manager = None


def _tailwind(
    components: List[Union[str, Tuple[str, str]]], className: Optional[str] = ""
):
    """
    A function to add and display components using Tailwind CSS. It ensures that Tailwind CSS is set up only once.

    Args:
        components (List[Union[str, Tuple[str, str]]]): A list of components to be displayed.
            Each component can be either a string (content) or a tuple (content, className).
        className (str, optional): The Tailwind CSS class name for the outer div. Defaults to an empty string.
    """
    global _tailwind_manager
    if _tailwind_manager is None:
        _tailwind_manager = TailwindManager()

    _tailwind_manager.display_components(components, className=className)
