import uuid
from llm_interface.ollama_api import query_ollama
from prompt_templates.child_json_template import child_list
from llm_interface.ollama_api import query_groq
import os
import json



class base_agent:
    def __init__(self, parent_id=None, config=None):
        config = config or {}
        
        # Core Identifiers
        self.agent_UUID = str(uuid.uuid4())
        self.parent_id = parent_id

        # Agent Configuration
        self.role = config.get('role', 'general_agent')
        
        # Depth Management
        self.overall_depth = config.get('overall_depth', 3)
        self.current_depth = config.get('current_depth', 1)
        self.num_branches = config.get('num_branches', 2)

        # Prompt Configuration
        self.task_prompt = config.get('task_prompt', 'General')

        #problem statement
        self.problem_statement = config.get('problem_statement', None)

        # output
        self.json_file = "solutions.json"

    def get_role(self):
        return self.role

    def call_llm(self, prompt):
        return query_groq(prompt)
    

    # Solve the problem at the current agent level if maximum depth is reached.
    def solve_problem(self):
        solution_prompt = (
            f"Overall Problem: {self.problem_statement}\n"
            f"This is your role: {self.role}\n"
            f"This is your task: {self.task_prompt}\n"
            "Provide a solution in 100 words or less."
        )
        solution = self.call_llm(solution_prompt)
        
        # Load existing data if the file exists
        data = []
        if os.path.exists(self.json_file):
            with open(self.json_file, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    pass  # Handle empty or malformed JSON

        # Append new solution data
        data.append({
            "agent_id": self.agent_UUID,
            "parent": self.parent_id,
            "role": self.role,
            "task": self.task_prompt,
            "solution": solution
            })

        # Write updated data back to the JSON file
        with open(self.json_file, "w") as file:
            json.dump(data, file, indent=4)

        print(self.role, solution)
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
        solutions = ""

        for child in children:
            solution = child.run()
            role = child.get_role()
            solutions = solutions + "\n" +role + ": " + solution
        prompt = (
            f"Overall Problem: {self.problem_statement}\n"
            f"Your role is:{self.role}"
            f"Your Task:{self.task_prompt}"
            f"Solutions from your sub agents: {solutions}"
            f"Compile the solutions of these agents summarize it and give your solution, precise and to the point in 100 words or less."
        )
        response = self.call_llm(prompt)

        data = []
        if os.path.exists(self.json_file):
            with open(self.json_file, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    pass  
        data.append({
            "agent_id": self.agent_UUID,
            "parent": self.parent_id,
            "role": self.role,
            "task": self.task_prompt,
            "solution": response
            })
        with open(self.json_file, "w") as file:
            json.dump(data, file, indent=4)

        print(self.role, response)
        return response


# testing

# test1
# config1 = {
#     'role': 'research_agent',
#     'expertise': 'quantum physics',
#     'overall_depth': 3,
#     'problem_statement': 'Explore the applications of quantum entanglement in communication.'
# }
# agent1 = base_agent(config=config1)
# agent1.run()

# test2
# config1 = {
#     'role': 'Parents',
#     'expertise': 'Every Day Life',
#     'overall_depth': 3,
#     'problem_statement': 'Plan a surprise birthday party for your son, including venue, catering, invitations, entertainment, and gifts.'
# }

# agent1 = base_agent(config=config1)
# agent1.run()

