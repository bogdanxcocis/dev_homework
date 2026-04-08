import json
import os

import chromadb
from chromadb.utils import embedding_functions


def load_books() -> list:
    try:
        with open('../data/books.json', 'r', encoding='utf-8') as file:
            file_data = json.load(file)
        return file_data
    except json.JSONDecodeError:
        print('Error: Failed to decode JSON from the file.')
        return []
    except FileNotFoundError:
        print('Error: The file was not found.')
        return []


def create_embedding_function():
    openai_key = os.getenv('OPENAI_API_KEY')
    openai_embedding_function = embedding_functions.OpenAIEmbeddingFunction(
        api_key=openai_key,
        model_name='text-embedding-3-small'
    )
    return openai_embedding_function


def is_collection_empty():
    openai_embedding_function = create_embedding_function()
    client = chromadb.PersistentClient(path='../chroma_db')
    collection = client.get_or_create_collection(
        name='book_summaries',
        embedding_function=openai_embedding_function
    )
    data = collection.get()
    return len(data['documents']) == 0


def insert_books_into_db():
    books = load_books()
    openai_embedding_function = create_embedding_function()
    client = chromadb.PersistentClient(path='../chroma_db')
    collection = client.get_or_create_collection(
        name='book_summaries',
        embedding_function=openai_embedding_function
    )

    ids = []
    chromadb_documents = []
    metadata = []

    for index, book in enumerate(books):
        ids.append(f'book_{index}')
        chromadb_documents.append(book['summary'])
        metadata.append({
            'title': book['title'],
            'full_summary': book['full_summary']
        })

    collection.add(ids=ids, documents=chromadb_documents, metadatas=metadata)
