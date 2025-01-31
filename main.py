import gradio as gr
from llm_interface.ollama_api import query_ollama
from llm_interface.ollama_api import query_rag
from llm_interface.ollama_api import query_groq
from agents.base_agent import base_agent
import os
from vectorization.create_database import create_collection
from PyPDF2 import PdfReader, PdfWriter


def solve_problem_groq(problem_statement):

    return query_groq(problem_statement)


def solve_problem(problem_statement):

    return query_ollama(problem_statement)
    # return "0"

def solve_problem_RAG(problem_statement):

    return query_rag(problem_statement)

# Process uploaded PDF file and add to ChromaDB
def process_pdf(pdf_file):
    # Save uploaded file temporarily
    temp_path = "temp.pdf"

    reader = PdfReader(pdf_file)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    with open(temp_path, "wb") as output_pdf:
        writer.write(output_pdf)

    
    try:
        result = create_collection(temp_path)
        os.remove(temp_path)  # Clean up
        return result
    except Exception as e:
        os.remove(temp_path)  # Clean up even if error occurs
        return f"Error processing PDF: {str(e)}"


# UI Setup
with gr.Blocks() as interface:
    # File upload section
    with gr.Tab("PDF Upload & Processing"):
        pdf_file = gr.File(label="Upload PDF", file_types=[".pdf"], interactive=True)
        process_pdf_button = gr.Button("Process PDF")
        pdf_output = gr.Textbox(label="PDF Processing Result", interactive=False)
        process_pdf_button.click(process_pdf, inputs=pdf_file, outputs=pdf_output)

    # Problem-solving sections
    with gr.Tab("Problem Solving"):
        problem_input = gr.Textbox(label="Enter Problem Statement")
        solve_button = gr.Button("Solve Without RAG")
        output = gr.Markdown(label="Reasoning Process & Solution")
        solve_button.click(solve_problem, inputs=problem_input, outputs=output)

    # Problem-solving sections
    with gr.Tab("Problem Solving Groq"):
        problem_input = gr.Textbox(label="Enter Problem Statement")
        solve_button = gr.Button("Solve Without RAG")
        output = gr.Markdown(label="Reasoning Process & Solution")
        solve_button.click(solve_problem_groq, inputs=problem_input, outputs=output)

    with gr.Tab("Problem Solving with RAG"):
        problem_input_rag = gr.Textbox(label="Enter Problem Statement")
        solve_rag_button = gr.Button("Solve With RAG")
        output_rag = gr.Markdown(label="Reasoning Process & Solution")
        solve_rag_button.click(solve_problem_RAG, inputs=problem_input_rag, outputs=output_rag)

interface.launch()