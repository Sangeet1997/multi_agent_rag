from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
import json

# Initialize Groq LLM
# Define the task breakdown prompt
def child_list(problem_statement):
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        temperature=0.7
    )

    # Define the expected JSON output structure
    parser = JsonOutputParser(pydantic_object={
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "role": {"type": "string"},
                "task": {"type": "string"}
            },
            "required": ["role", "task"]
        }
    })

    # Create the structured breakdown prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
    Task: Break down the problem(2 to 3 subtasks)
    Generate roles for child agents, each with a corresponding sub-task.
    Structure response as an array of JSON objects in this format(ONLY RESPOND WITH THIS ARRAY):
    [
    {{"role": "role1", "task": "task1"}},
    {{"role": "role2", "task": "task2"}},
    ...
    ]
    """),("user", "{input}")
    ])

    # Create the chain for processing task breakdowns
    chain = prompt | llm | parser
        
    result = chain.invoke({"input": problem_statement})
    return result
    # print(json.dumps(result, indent=2))
    # print(result)


# description = """Plan a surprise birthday party for a friend, including venue, catering, invitations, entertainment, and gifts."""
# child_list(description)