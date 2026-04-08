import json
import os

import chromadb
from chromadb.utils import embedding_functions
from openai import OpenAI


def get_books_collection():
    openai_key = os.getenv("OPENAI_API_KEY")
    openai_embedding_function = embedding_functions.OpenAIEmbeddingFunction(
        api_key=openai_key,
        model_name="text-embedding-3-small"
    )
    client = chromadb.PersistentClient(path="../chroma_db")
    collection = client.get_collection(
        name="book_summaries",
        embedding_function=openai_embedding_function
    )
    return collection


def is_valid_input(user_input: str) -> bool:
    cleaned_input = user_input.strip()
    if len(cleaned_input) == 0:
        print("Input cannot be empty.")
        return False
    return True


def get_summary_by_title(title: str) -> str:
    collection = get_books_collection()
    result = collection.get()
    for metadata in result["metadatas"]:
        if metadata["title"].strip().lower() == title.strip().lower():
            return metadata["full_summary"]
    return "Full summary not found for the given title."


def search_books_by_query(user_query: str):
    collection = get_books_collection()
    results = collection.query(
        query_texts=[user_query],
        n_results=1
    )
    return results


def build_recommendation(user_query: str):
    results = search_books_by_query(user_query)
    if not results["documents"] or not results["documents"][0]:
        return None
    title = results["metadatas"][0][0]["title"]
    summary = results["documents"][0][0]
    return {
        "title": title,
        "summary": summary
    }


def generate_ai_response(user_query: str, recommendation: dict) -> str:
    client = OpenAI()
    title = recommendation["title"]
    summary = recommendation["summary"]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_summary_by_title",
                "description": "Return the full summary of a book for an exact title.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The exact title of the recommended book."
                        }
                    },
                    "required": ["title"]
                }
            }
        }
    ]

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful librarian assistant. "
                "You will receive a user request, a recommended book title, and a short summary. "
                "First, recommend the book in a natural and conversational way. "
                "Then call the tool get_summary_by_title to retrieve the full summary of that exact book. "
                "Use only the information you receive. "
                "Do not invent facts. "
                "Always answer in the same language as the user's request."
            )
        },
        {
            "role": "user",
            "content": (
                f'User request: "{user_query}"\n'
                f'Recommended book title: "{title}"\n'
                f'Short summary: "{summary}"'
            )
        }
    ]

    first_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice={
            "type": "function",
            "function": {"name": "get_summary_by_title"}
        },
        temperature=0.7
    )

    first_message = first_response.choices[0].message
    messages.append(first_message)

    if first_message.tool_calls:
        for tool_call in first_message.tool_calls:
            if tool_call.function.name == "get_summary_by_title":
                arguments = json.loads(tool_call.function.arguments)
                requested_title = arguments["title"]

                full_summary = get_summary_by_title(requested_title)

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": full_summary
                    }
                )

        final_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7
        )

        return final_response.choices[0].message.content

    return first_message.content or "No response was generated."
