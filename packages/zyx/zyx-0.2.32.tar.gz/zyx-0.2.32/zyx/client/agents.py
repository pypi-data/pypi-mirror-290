__all__ = ["Agents"]

# --- zyx ----------------------------------------------------------------

from ..core.ext import BaseModel, Field
from typing import List, Dict, Any, Optional, Union, Callable
from uuid import uuid4
from ..types import ClientParams

class TaskIntent(BaseModel):
    intent: str
    description: str
    priority: int = Field(default=1, ge=1, le=5)

class TaskDelegation(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid4()))
    intent: TaskIntent
    assigned_worker: Optional[str] = None
    status: str = "pending"
    result: Optional[Any] = None

class SupervisorResponse(BaseModel):
    message: str
    delegations: List[TaskDelegation]

class WorkerResponse(BaseModel):
    task_id: str
    status: str
    result: Any
    message: Optional[str] = None

class Agent(BaseModel):
    agent_id: str
    agent_type: str
    tools: List[Any] = []
    instructions: Optional[str] = None

class Agents:
    def __init__(
        self,
        instructions: Optional[str] = None,
        model: Optional[str] = None,
        messages: Union[str, list[dict]] = None,
        tools: Optional[List[Union[Callable, dict, BaseModel]]] = None,
        run_tools: Optional[bool] = True,
        response_model: Optional[BaseModel] = None,
        mode: Optional[str] = "tools",
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        organization: Optional[str] = None,
        top_p: Optional[float] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_retries: Optional[int] = 3,
        **kwargs
    ):
        """Initialize the multi-agent system with the specified parameters.
        
        Parameters:
            model (str): The model to use for completions.
            messages (Union[str, list[dict]]): The messages to send to the model.
            tools (Optional[List[Union[Callable, dict, BaseModel]]]): The tools to use for completions.
            run_tools (Optional[bool]): Whether to run the tools.
            response_model (Optional[BaseModel]): The response model to use for completions.
            mode (Optional[str]): The mode to use for completions.
            base_url (Optional[str]): The base URL for the API.
            api_key (Optional[str]): The API key to use for the API.
            organization (Optional[str]): The organization to use for the API.
            top_p (Optional[float]): The top-p value for completions.
            temperature (Optional[float]): The temperature value for completions.
            max_tokens (Optional[int]): The maximum number of tokens for completions.
            max_retries (Optional[int]): The maximum number of retries for completions.
            supervisor_instructions (Optional[str]): Additional instructions for the supervisor agent.
            **kwargs: Additional keyword arguments for the completion    
        """
        from .main import Client
        import networkx as nx
        
        self.client = Client()
        self.agent_graph = nx.DiGraph()
        self.agent_graph.add_node("supervisor", agent=Agent(agent_id="supervisor", agent_type="supervisor"))
        
        self.params = ClientParams(
            model=model,
            messages=messages,
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
            **kwargs
        )
        
        self.supervisor_instructions = instructions or "Analyze user messages and delegate tasks efficiently."

    def worker(self, agent_id: str, tools: List[Any] = [], instructions: Optional[str] = None):
        try:
            worker = Agent(agent_id=agent_id, agent_type="worker", tools=tools, instructions=instructions)
            self.agent_graph.add_node(agent_id, agent=worker)
            self.agent_graph.add_edge("supervisor", agent_id)
        except Exception as e:
            print(f"Error adding worker agent {agent_id}: {str(e)}")

    def process_user_message(self, user_message: str, **kwargs) -> Optional[SupervisorResponse]:
        try:
            supervisor_prompt = f"""
            As a supervisor agent with the following instructions: {self.supervisor_instructions}
            
            Analyze the following user message and break it down into specific intents or delegations:
            
            User Message: {user_message}
            
            Provide a list of TaskIntent objects, each containing:
            - intent: A short description of the task
            - description: A detailed explanation of what needs to be done
            - priority: An integer from 1 (lowest) to 5 (highest)
            
            Also, provide a brief summary message for the user.
            """
            
            completion_args = {**self.params.dict(), **kwargs}
            response = self.client.completion(
                messages=supervisor_prompt,
                response_model=SupervisorResponse,
                **completion_args
            )
            return response
        except Exception as e:
            print(f"Error processing user message: {str(e)}")
            return None

    # ... [rest of the code remains unchanged]

# Example usage
if __name__ == "__main__":
    try:
        # Initialize the Agents with default completion arguments and supervisor instructions
        agents = Agents(
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=150,
            supervisor_instructions="Prioritize tasks based on their potential impact and delegate efficiently."
        )
        
        # Add worker agents using the new .worker() method
        agents.worker("researcher", instructions="Research and summarize information on given topics.")
        agents.worker("writer", instructions="Create well-written, engaging content based on provided information.")
        agents.worker("analyst", instructions="Analyze information, identify trends, and provide insights.")

        # Example user message
        user_message = "Prepare a report on the impact of artificial intelligence in healthcare."

        # Run the multi-agent system with custom completion arguments
        result = agents.run(
            user_message,
            temperature=0.5,  # Override the default temperature
            top_p=0.9         # Add a new completion argument
        )
        
        print("Multi-Agent System Result:")
        print(result)

        # Get and print the current state
        current_state = agents.get_state()
        print("\nCurrent State:")
        print(f"Agents: {current_state['agents']}")
        print("Delegations:")
        for task_id, delegation in current_state['delegations'].items():
            print(f"  Task: {delegation.intent.intent}")
            print(f"  Assigned to: {delegation.assigned_worker}")
            print(f"  Status: {delegation.status}")
            print("---")

        # Dynamically add a new agent using .worker()
        agents.worker("healthcare_specialist", instructions="Provide expert insights on healthcare topics and medical advancements.")
        print("\nAdded new agent: healthcare_specialist")

        # Print updated state
        updated_state = agents.get_state()
        print("\nUpdated Agents:", updated_state['agents'])

    except Exception as e:
        print(f"An error occurred in the main execution: {str(e)}")