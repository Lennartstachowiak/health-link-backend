from app.schemas import ChatRequest


def get_text(chat_request: ChatRequest):
    text = chat_request.text
    return text
