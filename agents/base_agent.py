import uuid
from llm_interface.ollama_api import query_ollama

class base_agent:
    def __init__(self, parent_id=None, config=None):
        config = config or {}
        
        # Core Identifiers
        self.agent_UUID = str(uuid.uuid4())
        self.parent_id = parent_id

        # Agent Configuration
        self.role = config.get('role', 'general_agent')
        self.expertise = config.get('expertise', 'general')
        
        # Depth Management
        self.overall_depth = config.get('overall_depth', 3)
        self.current_depth = config.get('current_depth', 1)
        self.num_branches = config.get('num_branches', 2)

        # Prompt Configuration
        self.system_prompt = config.get('system_prompt', 'You are a helpful assistant')
        self.task_prompt = config.get('task_prompt', 'Perform your task effectively')

        #problem statement
        self.problem_statement = config.get('problem_statement', None)


    def call_ollama(self, prompt):
        return query_ollama(prompt)
    

    # Solve the problem at the current agent level if maximum depth is reached.
    def solve_problem(self):
        solution_prompt = f"{self.system_prompt}\nTask: {self.task_prompt}\nProblem: {self.problem_statement}\nProvide a solution."
        solution = self.call_ollama(solution_prompt)
        # task : exception handling and reprompting
        return solution or "No solution generated."
    

    # Create a single child agent.
    def create_child(self, child_config):
        child = base_agent(parent_id=self.agent_UUID, config=child_config)
        return child


    # Generate child agents by breaking down the problem statement.
    def generate_children(self):
        if self.current_depth >= self.overall_depth:
            return [self.solve_problem()]

        # Request problem breakdown from Ollama
        breakdown_prompt = (
            f"{self.system_prompt}\nTask: Break down the problem\n"
            f"Problem: {self.problem_statement}\n"
            f"Generate {self.num_branches} roles for each child agent. And give each of them a sub-task"
            f"Generate response in this format |role1| , |task1|, |role2|, |task2| ... "
            f"DONT RETURN ANYTHING ELSE."
        )
        breakdown_response = self.call_ollama(breakdown_prompt)
        
        if not breakdown_response:
            print("Failed to generate problem breakdown.")
            return []

        # Parse breakdown response into tasks
        subtasks = [task.strip() for task in breakdown_response.split("\n") if task.strip()]
        child_agents = []

        for i, task in enumerate(subtasks[:self.num_branches]):
            child_config = {
                "role": f"child_agent_{i}",
                "expertise": "specialized",
                "overall_depth": self.overall_depth,
                "current_depth": self.current_depth + 1,
                "num_branches": self.num_branches,
                "system_prompt": self.system_prompt,
                "task_prompt": f"Handle sub-task: {task}",
                "problem_statement": task
            }
            child_agents.append(self.create_child(child_config))

        return child_agents
    

    # Execute the agent's logic, creating children if needed or solving the problem.
    def run(self):
        if self.current_depth >= self.overall_depth:
            return self.solve_problem()

        children = self.generate_children()
        solutions = []

        for child in children:
            solution = child.run()
            solutions.append(solution)

        return solutions



