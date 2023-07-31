IMAGE_NAME=foodstock
HUB_NAME=newtondotcom/foodstock:latest
docker build . -f Dockerfile -t $IMAGE_NAME
docker tag $IMAGE_NAME $HUB_NAME
docker push $HUB_NAME