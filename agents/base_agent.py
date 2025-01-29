class ProblemSolver:
    def __init__(self, recursion_depth=0, max_depth=3):

        self.recursion_depth = recursion_depth
        self.max_depth = max_depth

    def solve(self, problem: str) -> str:

        if self.recursion_depth >= self.max_depth:
            return f"Solution of Class A at depth {self.recursion_depth}"

        sub_problem = f"Subproblem of '{problem}' at depth {self.recursion_depth}"
        print(f"Solving: {sub_problem}")

        # Recursive call for subproblem
        sub_solver = ProblemSolver(self.recursion_depth + 1, self.max_depth)
        sub_solution = sub_solver.solve(sub_problem)

        # Combine or return solution
        return f"Solution of Class A at depth {self.recursion_depth} with sub-solution: [{sub_solution}]"