# Build the dockerfile
```bash
docker build -t my-chainlit-app . 
```

# Run the container locally
First Setup the `.env.list` file with `GEMINI_API_KEY=MYAPIKEY`
```bash
docker run --env-file ./.env.list -p 8000:8000 my-chainlit-app
```

# Tag the container to GCP
```bash
docker tag my-chainlit-app shranei/languageteacherbackend
```

# Push container to DockerHub
```bash
docker push shranei/languageteacherbackend
```