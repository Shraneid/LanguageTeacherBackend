# FastAPI + Chainlit + LangChain + Vertex AI Integration

A simple project demonstrating how to integrate FastAPI with Chainlit and LangChain using Google Vertex AI (Gemini) as the language model.

## Features

- FastAPI backend with proper Chainlit integration using `mount_chainlit`
- Web-based chat interface powered by Chainlit
- Google Vertex AI (Gemini) integration via LangChain
- LangChain conversation chains for maintaining context
- Environment-based configuration
- Dual access methods: chat UI and direct API endpoints

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd <repository-directory>
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
```bash
cp .env.example .env
```

5. Edit the `.env` file and set your Google Cloud credentials:
   - Set `GOOGLE_APPLICATION_CREDENTIALS` to the path of your service account key file
   - Set `GOOGLE_CLOUD_PROJECT` to your Google Cloud project ID

## Vertex AI Setup

1. Create a Google Cloud Project if you don't already have one
2. Enable the Vertex AI API in your project
3. Create a service account with the required permissions for Vertex AI
4. Download the service account key as JSON
5. Set the path to this JSON file in your `.env` file

## Running the Application

The application combines FastAPI and Chainlit into a single server:

```bash
python app.py
```

This will start the server at http://localhost:8000 with:
- The Chainlit chat interface at the root URL (http://localhost:8000)
- FastAPI endpoints at http://localhost:8000/api/...
- API documentation at http://localhost:8000/docs

## Project Structure

- `main.py`: FastAPI application that mounts the Chainlit UI
- `my_cl_app.py`: Chainlit application logic with Vertex AI integration
- `requirements.txt`: Project dependencies
- `.env.example`: Example environment variables file
- `chainlit.md`: Chainlit UI documentation

## How It Works

1. FastAPI serves as the backend framework
2. Chainlit is mounted as a sub-application using the official `mount_chainlit` function
3. The Chainlit UI is accessible at the root path
4. Google Vertex AI provides the language model capabilities via Gemini-Pro
5. LangChain handles the conversation logic and integration with Vertex AI
6. The API endpoints are available at /api/... for programmatic access

## API Usage

You can also interact with the application programmatically:

```python
import requests

response = requests.post(
    "http://localhost:8000/api/conversation",
    json={
        "query": "Hello, can you help me practice French?",
        "conversation_id": None  # Optional, for continuing conversations
    }
)

print(response.json())
```

## License

MIT
