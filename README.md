# Chatbot that can recommend books based on user preferences

This project is a CLI-based AI chatbot that recommends books based on user interests using semantic search with ChromaDB and OpenAI embeddings. After recommending a book, the chatbot uses OpenAI function calling to retrieve the full summary of the recommended title.

## Features

- Stores books with short and full summaries
- Uses ChromaDB as a vector database
- Uses OpenAI embeddings (`text-embedding-3-small`) for semantic search
- Recommends books based on user interests
- Uses OpenAI GPT (`gpt-4o-mini`) to generate conversational responses
- Uses tool calling with `get_summary_by_title(title)`
- Provides a CLI interface

## Installation and Setup

Follow these steps to set up and run the project locally.

### 1. Clone the Repository

If using Git:

```bash
git clone https://github.com/bogdanxcocis/dev_homework.git
cd dev_homework
```

### 2. Create a Virtual Environment
```bash
 python -m venv .venv
```

### 3. Activate the Virtual Environment
```bash
.venv\Scripts\Activate.ps1
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Set Environment Variables
You must set your OpenAI API key before running the project.
```bash
$env:OPENAI_API_KEY="your_api_key_here"
```

## Build and Run

### 1. Run the Application
```aiignore
python main.py
```

### 2. Initial Setup
On first run:

* The application checks if the ChromaDB collection is empty
* If empty, it loads data from data/books.json
* It then creates embeddings and stores them in chroma_db/

### 3. Use the CLI

After starting the app, choose one of the options:
```aiignore
1. Get full summary by title
2. Get book recommendation
```

Option 1:
* Enter a book title to retrieve its full summary.

Option 2:
* Describe what kind of book you want (e.g.):
```aiignore
I want a book about freedom and control
```

The system will:

1. Perform semantic search using ChromaDB
2. Select the best matching book
3. Use OpenAI GPT to generate a response
4. Call the tool get_summary_by_title(title)
5. Return a recommendation with the full summary
