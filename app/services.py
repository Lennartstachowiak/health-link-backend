from app.schemas import ChatRequest
from app.mistral import ask_question


def get_message_response(chat_request: ChatRequest):
    message = chat_request.message
    answer = ask_question(message)

    return answer
