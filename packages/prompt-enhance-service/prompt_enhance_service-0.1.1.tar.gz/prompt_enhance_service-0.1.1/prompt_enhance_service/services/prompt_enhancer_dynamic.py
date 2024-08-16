from src.genai_framework import ChatLLMBuilder
from src.genai_framework import ChatLLMWithMemoryBuilder
from schemas.prompt_request import PromptRequest
from dotenv import load_dotenv
from typing import Dict, Any
from firestore_test import get_questions_from_db

load_dotenv()

# Store sessions
sessions: Dict[str, Any] = {}

def prompt_enhancer_dynamic(session_id, user_message, domain):
    if session_id not in sessions:
        questions = get_questions_from_db(domain)  # Fetch questions based on the domain
        response = initialize_dynamic_session(session_id, user_message, questions)
    else:
        response = continue_dynamic_session(session_id, user_message)
    
    return response

def initialize_dynamic_session(session_id, initial_prompt, questions):
    builder = ChatLLMWithMemoryBuilder()
    
    # Initialize a new session with the relevant questions
    chat_session = builder.llm_chat.chat_google_vertexai()
    sessions[session_id] = {
        "chat_session": chat_session,
        "current_question_index": 0,
        "responses": {},
        "initial_prompt": initial_prompt,
        "questions": questions  # Store questions in the session
    }

    return get_next_question(session_id)

def continue_dynamic_session(session_id, user_response):
    session = sessions[session_id]
    session["responses"][session["questions"][session["current_question_index"]]] = user_response
    session["current_question_index"] += 1

    if session["current_question_index"] < len(session["questions"]):
        return get_next_question(session_id)
    else:
        return build_final_enhanced_prompt(session_id)

def get_next_question(session_id):
    session = sessions[session_id]
    next_question = session["questions"][session["current_question_index"]]
    return {"question": next_question}

def build_final_enhanced_prompt(session_id):
    session = sessions[session_id]
    responses = session["responses"]
    initial_prompt = session["initial_prompt"]

    enhanced_prompt = f'''
    Enhance the below prompt by comprehensively analyzing the following parameters to ensure better outcomes:
                    prompt: "{initial_prompt}"
                    with the below questions answered by the user:
    Define Role: {responses.get("What is the role involved?", "Not Provided")}
    Type of Data: {responses.get("What type of data are you referring to?", "Not Provided")}
    Relationship: {responses.get("What is the relationship between data elements?", "Not Provided")}
    Constraints: {responses.get("Are there any constraints?", "Not Provided")}
    Steps for Analysis: {responses.get("What are the steps for analysis?", "Not Provided")}
    Output Instructions: {responses.get("What are the output instructions?", "Not Provided")}
    Restrictions: {responses.get("Are there any restrictions?", "Not Provided")}
    Data Organizations: {responses.get("How is the data organized?", "Not Provided")}
    If any of these parameters are understandable or have existing information, do not make assumptions but instead, enhance the prompt by including them explicitly to ensure clarity and precision. The goal is to create a prompt that is fully detailed and comprehensive, facilitating accurate and insightful analysis. All enhancements should be integrated into a single, comprehensive paragraph.
    '''
    print(enhanced_prompt)
    
    builder = ChatLLMBuilder()  # Reinitialize the builder for final prompt enhancement
    response2 = (builder.set_prompt(enhanced_prompt, initial_prompt=initial_prompt, responses=responses)
                         .llm_chat.chat_google_vertexai().build())

    del sessions[session_id]  # Clean up session
    return response2
