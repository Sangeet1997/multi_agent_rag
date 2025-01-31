import gradio as gr
from llm_interface.ollama_api import query_ollama
from agents.base_agent import ProblemSolver


def solve_problem(problem_statement):

    ps = ProblemSolver()
    result = ps.solve(problem_statement)
    return result

    # return query_ollama(problem_statement)


# UI Setup
with gr.Blocks() as interface:
    problem_input = gr.Textbox(label="Enter Problem Statement")
    output = gr.Markdown(label="Reasoning Process & Solution")
    solve_button = gr.Button("Solve")
    
    solve_button.click(fn=solve_problem, inputs=[problem_input], outputs=[output])

interface.launch()
