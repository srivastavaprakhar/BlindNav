from services.local_llm import generate_local_response
from models.elements import PageElements

def generate_description(elements: PageElements) -> str:
    prompt = f"""
You are a helpful AI assistant for blind users. Please describe this webpage clearly.

Headings: {elements.headings}
Buttons: {elements.buttons}
Links: {elements.links}
Inputs: {elements.inputs}
Forms: {elements.forms}

Describe the structure and purpose of the page in plain English. Mention what buttons do, what forms expect, and ask if the user wants to take any action.
"""

    return generate_local_response(prompt)
