class BaseAgent:
    def __init__(self, problem_statement):
        self.problem_statement = problem_statement
    
    def decompose_problem(self):
        raise NotImplementedError
    
    def generate_hypotheses(self):
        raise NotImplementedError
    
    def refine_conclusion(self):
        raise NotImplementedError
