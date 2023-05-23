# RSS To Telegram Bot Using Google Cloud Run
## Deployment To Google Cloud Run
1. Google Cloud CLI Authentication
```
gcloud auth login
```
2. Choose Google Cloud project
```
gcloud config set project [PROJECT_ID]
```
3. Clone the GitHub repository that contains your Dockerfile
```
git clone https://github.com/xilverkamui/rss-to-telegram-bot-gcr.git
```
4. Change into the directory that contains the Dockerfile
```
cd rss-to-telegram-bot-gcr
```
5. Use the docker build command to build the Docker image, replacing [IMAGE_NAME] with the desired name for the image
```
docker build -t [IMAGE_NAME] .
```
6. Push Docker image to Google Container Registry
```
docker tag [IMAGE_NAME] gcr.io/[PROJECT_ID]/[IMAGE_NAME]
docker push gcr.io/[PROJECT_ID]/[IMAGE_NAME]
```
7. Deploy Docker image to Google Cloud Run
```
gcloud run deploy [SERVICE_NAME] --image gcr.io/[PROJECT_ID]/[IMAGE_NAME]  --platform managed --set-env-vars-from-file=config.env
```

Note: Replace [PROJECT_ID], [IMAGE_NAME], and [SERVICE_NAME] with your project and application information. Also make sure to run these commands from the directory that contains your Dockerfile
