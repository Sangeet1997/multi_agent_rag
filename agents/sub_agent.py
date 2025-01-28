from .base_agent import BaseAgent

class SubAgent(BaseAgent):
    def run(self):
        return f"Solution for {self.problem_statement}"
