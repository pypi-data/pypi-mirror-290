from genai_framework import ChatLLMBuilder
from dotenv import load_dotenv

load_dotenv()

def prompt_enhancer_static(initial_prompt):
    builder = ChatLLMBuilder()
    template = '''Enhance the below prompt by comprehensively analyzing the following parameters to ensure better outcomes:
                    prompt: "{initial_prompt}"
                    Role: Identify the specific roles involved in the scenario and their responsibilities.
                    Type of Data: Specify the types of data being used or analyzed.
                    Relationship: Describe the relationships between different data elements.
                    Constraints: Outline any constraints or limitations that need to be considered.
                    Steps for Analysis: Detail the steps required for analyzing the data.
                    Output Instructions: Provide clear instructions on the expected output.
                    Restrictions: Mention any restrictions or specific rules that must be followed.
                    Data Organization: Explain how the data is organized or structured.
                If any of these parameters are understandable or have existing information, do not make assumptions but instead, enhance the prompt by including them explicitly to ensure clarity and precision. The goal is to create a prompt that is fully detailed and comprehensive, facilitating accurate and insightful analysis.All enhancements should be integrated into a single, comprehensive paragraph.'''
    response = (builder.set_prompt(template, initial_prompt=initial_prompt).llm_chat.chat_google_vertexai().build())
    return response