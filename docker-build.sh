IMAGE_NAME=badgering
HUB_NAME=newtondotcom/badgering:0.0.1
docker build . -f Dockerfile -t $IMAGE_NAME
docker tag $IMAGE_NAME $HUB_NAME
docker push $HUB_NAME