from typing import List, Dict, Any, Optional, Union
from ..types import (
    TaskIntent,
    TaskDelegation,
    SupervisorResponse,
    WorkerResponse,
    AgentParams
)

class Agents:
    def __init__(self, **kwargs):
        from .main import Client
        import networkx as nx
        
        self.client = Client()
        self.agent_graph = nx.DiGraph()
        self.agent_graph.add_node("supervisor", agent=AgentParams(agent_id="supervisor", agent_type="supervisor"))
        self.default_completion_args = kwargs

    def add_worker(self, agent_id: str, tools: List[Any] = [], instructions: Optional[str] = None, **completion_params):
        from .main import Agent
        try:
            worker = Agent(agent_id=agent_id, agent_type="worker", tools=tools, instructions=instructions, completion_params=completion_params)
            self.agent_graph.add_node(agent_id, agent=worker)
            self.agent_graph.add_edge("supervisor", agent_id)
        except Exception as e:
            print(f"Error adding agent {agent_id}: {str(e)}")

    def process_user_message(self, user_message: str, **kwargs) -> Optional[SupervisorResponse]:
        try:
            supervisor_prompt = f"""
            As a supervisor agent, analyze the following user message and break it down into specific intents or delegations:
            
            User Message: {user_message}
            
            If delegation is needed, provide a list of TaskIntent objects, each containing:
            - intent: A short description of the task
            - description: A detailed explanation of what needs to be done
            - priority: An integer from 1 (lowest) to 5 (highest)
            
            If no delegation is needed, write a response message directly.
            """
            
            completion_args = {**self.default_completion_args, **kwargs}
            response = self.client.completion(
                messages=supervisor_prompt,
                response_model=SupervisorResponse,
                **completion_args
            )
            return response
        except Exception as e:
            print(f"Error processing user message: {str(e)}")
            return None

    def delegate_tasks(self, supervisor_response: Optional[SupervisorResponse]) -> Dict[str, TaskDelegation]:
        delegations = {}
        try:
            if supervisor_response is None or not supervisor_response.delegations:
                return delegations
            worker_agents = list(self.agent_graph.neighbors("supervisor"))
            if not worker_agents:
                print("No worker agents available.")
                return delegations
            for i, delegation in enumerate(supervisor_response.delegations):
                assigned_worker = worker_agents[i % len(worker_agents)]
                delegation.assigned_worker = assigned_worker
                delegations[delegation.task_id] = delegation
        except Exception as e:
            print(f"Error delegating tasks: {str(e)}")
        return delegations

    def execute_worker_task(self, worker_id: str, task: TaskDelegation, **kwargs) -> Optional[WorkerResponse]:
        try:
            worker = self.agent_graph.nodes[worker_id]["agent"]
            
            worker_prompt = f"""
            You are a worker agent with the following tools and instructions:
            Tools: {worker.tools}
            Instructions: {worker.instructions}
            
            Execute the following task:
            Intent: {task.intent.intent}
            Description: {task.intent.description}
            
            Provide your response as a WorkerResponse object.
            """
            
            completion_args = {**worker.completion_params, **kwargs}
            response = self.client.completion(
                messages=worker_prompt,
                tools=worker.tools,
                response_model=WorkerResponse,
                **completion_args
            )
            return response
        except Exception as e:
            print(f"Error executing worker task: {str(e)}")
            return None

    def run(self, user_message: Union[str, List[dict]], **kwargs) -> str:
        try:
          
            if isinstance(user_message, str):
                user_message = [{"role": "user", "content": user_message}]
            elif isinstance(user_message, list):
                user_message = self.client.format_messages(user_message)

            supervisor_response = self.process_user_message(user_message, **kwargs)
            if supervisor_response is None:
                return "Failed to process user message."
            
            if not supervisor_response.delegations:
                return supervisor_response.message
            
            delegations = self.delegate_tasks(supervisor_response)
            if not delegations:
                return supervisor_response.message
            
            final_results = []
            for task_id, delegation in delegations.items():
                worker_response = self.execute_worker_task(delegation.assigned_worker, delegation, **kwargs)
                if worker_response:
                    delegation.status = worker_response.status
                    delegation.result = worker_response.result
                    final_results.append(f"Task: {delegation.intent.intent}\nResult: {worker_response.result}")
                else:
                    final_results.append(f"Task: {delegation.intent.intent}\nResult: Task execution failed.")
            
            summary_prompt = "Summarize the results of the following tasks:\n\n"
            summary_prompt += "\n\n".join(final_results)
            summary_prompt += "\n\nProvide a concise summary for the user."
            
            completion_args = {**self.default_completion_args, **kwargs}
            summary_response = self.client.completion(
                messages=summary_prompt,
                **completion_args
            )
            
            if summary_response and summary_response.choices:
                return summary_response.choices[0].message
            else:
                return "Failed to generate summary. Here are the raw results:\n" + "\n".join(final_results)
        except Exception as e:
            return f"An error occurred while running the multi-agent system: {str(e)}"

    def get_state(self) -> Dict[str, Any]:
        try:
            return {
                "agents": [node for node in self.agent_graph.nodes()],
                "delegations": self.delegate_tasks(self.process_user_message("Get current state"))
            }
        except Exception as e:
            print(f"Error getting state: {str(e)}")
            return {"agents": [], "delegations": {}}

# Example usage
if __name__ == "__main__":
    try:
        # Initialize the state manager with default completion arguments
        state_manager = Agents(
            model="gpt-4o-mini",
            temperature=0.7,
            max_tokens=150
        )
        
        # Add worker agents with individual completion params
        state_manager.add_worker("researcher", instructions="Research and summarize information on given topics.", model="gpt-3.5-turbo", temperature=0.5)
        state_manager.add_worker("writer", instructions="Create well-written, engaging content based on provided information.", model="gpt-4", temperature=0.6)
        state_manager.add_worker("analyst", instructions="Analyze information, identify trends, and provide insights.", model="gpt-4o-mini", temperature=0.7)

        # Example user message
        user_message = "Prepare a report on the impact of artificial intelligence in healthcare."

        # Run the multi-agent system with custom completion arguments
        result = state_manager.run(
            user_message,
            temperature=0.5,  # Override the default temperature
            top_p=0.9         # Add a new completion argument
        )
        
        print("Multi-Agent System Result:")
        print(result)

        # Get and print the current state
        current_state = state_manager.get_state()
        print("\nCurrent State:")
        print(f"Agents: {current_state['agents']}")
        print("Delegations:")
        for task_id, delegation in current_state['delegations'].items():
            print(f"  Task: {delegation.intent.intent}")
            print(f"  Assigned to: {delegation.assigned_worker}")
            print(f"  Status: {delegation.status}")
            print("---")

        # Dynamically add a new agent
        state_manager.add_worker("healthcare_specialist", instructions="Provide expert insights on healthcare topics and medical advancements.", model="gpt-4", temperature=0.8)
        print("\nAdded new agent: healthcare_specialist")

        # Print updated state
        updated_state = state_manager.get_state()
        print("\nUpdated Agents:", updated_state['agents'])

    except Exception as e:
        print(f"An error occurred in the main execution: {str(e)}")
