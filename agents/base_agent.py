import uuid
from llm_interface.ollama_api import query_ollama
from prompt_templates.child_json_template import child_list
from llm_interface.ollama_api import query_groq



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
        self.task_prompt = config.get('task_prompt', 'Perform your task effectively')

        #problem statement
        self.problem_statement = config.get('problem_statement', None)


    def call_llm(self, prompt):
        return query_groq(prompt)
    

    # Solve the problem at the current agent level if maximum depth is reached.
    def solve_problem(self):
        solution_prompt = f"Overall Problem: {self.problem_statement}\nThis is your role: {self.role}\nThis is your task: {self.task_prompt}\nProvide a solution."
        solution = self.call_llm(solution_prompt)
        print(solution)
        return solution or "No solution generated."
    

    # Create a single child agent.
    def create_child(self, child_config):
        child = base_agent(parent_id=self.agent_UUID, config=child_config)
        return child


    # Generate child agents by breaking down the problem statement.
    def generate_children(self):
        if self.current_depth >= self.overall_depth:
            return [self.solve_problem()]


        response = child_list(self.task_prompt)

        # Parse breakdown response into tasks
        child_agents = []

        for i, item in enumerate(response):
            role = item.get('role', f'child_agent_{i}')
            task = item.get('task', 'No task provided')

            child_config = {
                "role": role,
                "overall_depth": self.overall_depth,
                "current_depth": self.current_depth + 1,
                "num_branches": self.num_branches,
                "task_prompt": task,
                "problem_statement": self.problem_statement
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



