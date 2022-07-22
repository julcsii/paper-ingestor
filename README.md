# paper-ingestor

## Run locally
### Requirements
* AWS credentials

### Install dependencies for local development
* Create a new virtual environment with [virtualenv](https://virtualenv.pypa.io/en/latest/) inside directory `venv`: `virtualenv -p python3 venv`
* Activate the virtual environment: `source venv/bin/activate`
* Install developer dependencies: `pip install -r requirements.txt`

### Run main
```
python -m paper_ingestor.main
```

## Run remotely
### Requirements
* Docker
* AWS credentials
* AWS cli
* kubectl

### Connect to remote cluster
```
# optional: switch to aws profile export AWS_PROFILE=personal
aws eks --region eu-central-1 update-kubeconfig --name elicit-stg
```

### Deploy rct service
```
kubectl apply -f deployment/rct-score-svc.yaml
```

### Deploy new version of paper-ingestor

1. Set env variables
```
export CODE_PATH='paper_ingestor'
export IMAGE_NAME='elicit-paper-ingestor'
export IMAGE_TAG='latest' # this is going to override the mutable image in ECR
export ECR_HOST="067892212219.dkr.ecr.eu-central-1.amazonaws.com"
export LOCAL_IMAGE_URL=$IMAGE_NAME:$IMAGE_TAG
export ECR_IMAGE_URL=$ECR_HOST/$LOCAL_IMAGE_URL
```

2. Build new Docker image
```
docker build -t $LOCAL_IMAGE_URL . -f $CODE_PATH/Dockerfile
```
3. Push to ECR
```
aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin $ECR_HOST&&\
docker tag $LOCAL_IMAGE_URL $ECR_IMAGE_URL &&\
docker push $ECR_IMAGE_URL
```
4. Deploy cron job to EKS 
```bash
kubectl apply -f deployment/paper-ingestor-cronjob.yaml
```


