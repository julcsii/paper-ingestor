# paper-ingestor

## Run localally

### Requirements
* Docker

### Build image and run container
```bash

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
### Deploy new version of paper-ingestor

1. Run unit tests
```
```
2. Build new Docker image
```
```
3. Push to ECR
```
```
4. Deploy cron job to EKS 
```bash
kubectl apply -f deployment/cronjob.yaml
```

