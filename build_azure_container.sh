#mistral ai
#!/bin/bash

# Variables
RESOURCE_GROUP="ncassonetRG"
ACR_NAME="nicocassoregistry"
IMAGE_NAME="prediction-service-image"
TAG="latest"
CONTAINER_NAME="prediction-service-container"
DNS_LABEL="nicocassoregistry.azurecr.io/prediction-service-image"

# Connexion à Azure
# echo "Connexion à Azure..."
# az login

# Connexion au registre de conteneurs Azure
# echo "Connexion au registre de conteneurs Azure..."
# az acr login --name $ACR_NAME



# Construction de l'image Docker et push vers ACR
echo "Construction de l'image Docker et push vers ACR..."

# az acr build \
#   --registry $ACR_NAME \
#   --image ${ACR_NAME}.azurecr.io/${IMAGE_NAME}:${TAG} . 

echo "Construction de l'image Docker ..."
# docker build -t nicocassoregistry.azurecr.io/prediction-service-image .
docker build -t $DNS_LABEL .

echo "Push vers ACR..."
#docker push nicocassoregistry.azurecr.io/prediction-service-image
docker push $DNS_LABEL

# docker run --rm -p 3100:3100 nicocassoregistry.azurecr.io/prediction-service-image
# ./deploy_azure_container.sh
