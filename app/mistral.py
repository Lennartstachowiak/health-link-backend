from haystack import Pipeline
from haystack.dataclasses import ChatMessage
from haystack.components.builders import ChatPromptBuilder
from haystack_integrations.document_stores.weaviate import WeaviateDocumentStore, AuthApiKey
from haystack import Document
from haystack_integrations.components.embedders.mistral.document_embedder import MistralDocumentEmbedder
from haystack_integrations.components.embedders.mistral.text_embedder import MistralTextEmbedder
from haystack_integrations.components.retrievers.weaviate import WeaviateEmbeddingRetriever
from haystack_integrations.components.generators.mistral import MistralChatGenerator
from haystack.components.generators.utils import print_streaming_chunk
from haystack.dataclasses import ChatMessage
from dotenv import load_dotenv
import os
import json

load_dotenv()


WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

auth_client_secret = AuthApiKey()

WEAVIATE_URL = os.getenv("WEAVIATE_URL")  # need to check this
document_store = WeaviateDocumentStore(url=WEAVIATE_URL,
                                       auth_client_secret=auth_client_secret)


def load_local_dataset(directory_path):
    documents = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".txt") or file.endswith(".md"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    content = f.read()
                documents.append(Document(content=content, meta={"filename": file}))
    return documents


# Load your dataset
local_dataset_path = "./processed_data/patient_1"
documents = load_local_dataset(local_dataset_path)

Mistral_doc_embedder = MistralDocumentEmbedder(model="mistral-embed")

embedder = MistralTextEmbedder(model="mistral-embed")

# Initialize the Weaviate retriever
retriever = WeaviateEmbeddingRetriever(document_store=document_store)


technical_template = [
    ChatMessage.from_user(
        """
Please provide a detailed and technical answer to the following question based on the medical information available:

Question: {{ question }}

Context:
{% for document in documents %}
    {{ document.content }}
{% endfor %}

Technical Details:
        """
    )
]

technical_prompt_builder = ChatPromptBuilder(template=technical_template)


simplification_template = [
    ChatMessage.from_user(
        """
Now, let's translate the medical information into simpler terms for better understanding. Here's the detailed answer to your query:

Technical Answer: {{ technical_response }}

*Here’s what you need to know*:  
[Act as the AI medical doctor treating the patient and as if you are having a conversation with the patient directly right now. Provide a simple, easy-to-understand explanation of the answer. Always refer to the patient in the 2nd person singular (you). Make sure you are friendly and approachable, but do not overwhelm the patient with information. Try to keep the conversation going by pointing to things the patient might want to ask and get to know. No answer needs to be completely comprehensive, but can rather point to what might be relevant next. The goal is to have a free-flowing fast-paced conversation with the patient.]

*What you can do next* [This should be optional and highly dependent on context - only provide this information if it genuinely makes sense based on what the patient asked! When patients ask a quick question about something basic make sure your answer is similarly short and to the point.]:  

- *Medications*: [Provide clear, actionable advice about medications, if this only exist in the medical record e.g., "Take your insulin as prescribed, and make sure to monitor your blood sugar levels regularly."]  
- *Activities*: [Suggest practical activities, if this only exist in the medical record e.g., "Try to go for a 20-minute walk every day—it’s great for your health!"]  
- *Dietary Tips*: [Offer simple dietary advice, if this only exist in the medical record e.g., "Include more leafy greens and whole grains in your meals, and try to avoid sugary snacks."]  
        """
    )
]

simplification_prompt_builder = ChatPromptBuilder(template=simplification_template)


technical_llm = MistralChatGenerator(streaming_callback=print_streaming_chunk)  # LLM for technical response
simplification_llm = MistralChatGenerator(streaming_callback=print_streaming_chunk)  # LLM for simplified respon


basic_rag_pipeline = Pipeline()

# Add components to your pipeline
basic_rag_pipeline.add_component("text_embedder", embedder)
basic_rag_pipeline.add_component("retriever", retriever)
basic_rag_pipeline.add_component("technical_prompt_builder", technical_prompt_builder)
basic_rag_pipeline.add_component("technical_llm", technical_llm)
basic_rag_pipeline.add_component("simplification_prompt_builder", simplification_prompt_builder)
basic_rag_pipeline.add_component("simplification_llm", simplification_llm)

# Connect the components
basic_rag_pipeline.connect("text_embedder.embedding", "retriever.query_embedding")
basic_rag_pipeline.connect("retriever.documents", "technical_prompt_builder.documents")
basic_rag_pipeline.connect("technical_prompt_builder.prompt", "technical_llm.messages")
basic_rag_pipeline.connect("technical_llm.replies", "simplification_prompt_builder.technical_response")
basic_rag_pipeline.connect("simplification_prompt_builder.prompt", "simplification_llm.messages")

# Define a function to run the pipeline


def ask_question(question):
    results = basic_rag_pipeline.run(
        {
            "text_embedder": {"text": question},  # Embed the question
            "technical_prompt_builder": {"question": question},  # Build the technical prompt
        }
    )
    # Ensure `results["simplification_llm"]["replies"][0]` is JSON serializable
    reply = results["simplification_llm"]["replies"][0]

    # Return the reply as JSON
    return reply.text
