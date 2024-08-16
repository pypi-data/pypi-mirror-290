from prompt_enhance_service.services.prompt_enhancer_static import prompt_enhancer_static
from prompt_enhance_service.services.prompt_enhancer_dynamic import prompt_enhancer_dynamic
from prompt_enhance_service.schemas.prompt_request import PromptRequest
from prompt_enhance_service.schemas.domain_questions import DomainQuestions
#from firestore_test import get_questions_from_db


def enhance(prompt_request: PromptRequest):
    # Retrieve fields from the request
    user_message = prompt_request.message
    session_id = getattr(prompt_request, 'session_id', None)
    customization = getattr(prompt_request, 'customization', None)
    domain = getattr(prompt_request, 'domain', None)

    if not customization:
        # No customization, handle with static enhancer
        response = prompt_enhancer_static(user_message)
    else:
        # Customization is provided, ensure mandatory fields are present
        if session_id is None or domain is None:
            raise ValueError("Both session_id and domain are required when customization is provided.")
        
        response = prompt_enhancer_dynamic(session_id, user_message, domain)

    return response


# Define the questions_dict dictionary
questions_dict = {}
def domain_questions(domain_questions: DomainQuestions):
    domain_name = domain_questions.domain
    questions = domain_questions.questions

    # Check if domain_name already exists in the dictionary
    if domain_name in questions_dict:
        return "Domain name already exists"

    # Add the questions to the dictionary
    questions_dict[domain_name] = questions

    # Print success message
    response = "Questions updated successfully"
    return response

'''def get_questions(domain_name: str):
    # Fetch questions from Firestore
    questions = get_questions_from_db(domain_name)
    
    # Check if questions were found
    if not questions:
        return f"No questions found for domain: {domain_name}"
    
    return {"domain": domain_name, "questions": questions}'''