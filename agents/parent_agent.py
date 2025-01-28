from .base_agent import BaseAgent
from .sub_agent import SubAgent

class ParentAgent(BaseAgent):
    def run(self):
        self.decompose_problem()
        # Create sub-agents based on sub-problems
        results = [SubAgent(problem).run() for problem in self.sub_problems]
        final_output = self.refine_conclusion(results)
        return final_output

    def decompose_problem(self):
        # Decompose complex problem
        self.sub_problems = ["subproblem 1", "subproblem 2"]  # Example

    def refine_conclusion(self, results):
        # Combine results from sub-agents
        return "\n".join(results)
