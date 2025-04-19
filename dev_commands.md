# Launch uvicorn locally directly
```bash
uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

# Build the dockerfile
```bash
docker build -t my-chainlit-app . 
```

# Run the container locally
First Setup the `.env.list` file with `GEMINI_API_KEY=YOURAPIKEY`
```bash
docker run --env-file ./.env.list -p 8000:8000 my-chainlit-app
```
