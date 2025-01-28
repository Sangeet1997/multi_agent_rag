import gradio as gr
from agents.parent_agent import ParentAgent

def solve_problem(problem_statement):
    agent = ParentAgent(problem_statement)
    result = agent.run()
    return result

# UI Setup
with gr.Blocks() as interface:
    problem_input = gr.Textbox(label="Enter Problem Statement")
    output = gr.Markdown(label="Reasoning Process & Solution")
    solve_button = gr.Button("Solve")
    
    solve_button.click(fn=solve_problem, inputs=[problem_input], outputs=[output])

interface.launch()
