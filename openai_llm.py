import os
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI 
from numpy import dot
from numpy.linalg import norm

openai_api_key = os.environ.get("OPENAI_API_KEY")

embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key, model='text-embedding-ada-002')

llm = ChatOpenAI(openai_api_key=openai_api_key, model='gpt-3.5-turbo-1106', temperature=0.5)

def generate_tasks(event_description: str, user_description: str):
    context = 'Here is a description and list of tasks of the volunteering event: \n' + event_description + '\n\n' + "Here is the user's list of skills, description of his interests and past volunteer experiences : " + user_description + '\n\n'
    query = 'Can you generate 3 to 5 personalized tasks for the user that are tailored to the event? Try not to repeat tasks that are already in the event description. Do not use any lists, keep the response in a single paragraph.'

    prompt = context + '\n\n' + query
    return llm.predict(prompt)

def get_embeddings(text: str):
    return embeddings.embed_query(text)

def get_cosine_similarity(embedding1, embedding2):
    return dot(embedding1, embedding2)/(norm(embedding1)*norm(embedding2))