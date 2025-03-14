#!/bin/bash

# Variables
RESOURCE_GROUP="ncassonetRG"                   # Nom du groupe de ressources
CONTAINER_NAME="prediction-service-container" # Nom du conteneur
ACR_NAME="nicocassoregistry"                 # Nom de ton Azure Container Registry
ACR_IMAGE="prediction-service-image"        # Nom de l'image dans le ACR
ACR_URL="$ACR_NAME.azurecr.io"             # URL du registre
CPU="1"                                   # Nombre de CPUs
MEMORY="4"                               # Mémoire (RAM)
PORT="3100"                             # Port exposé
#PROBE_PORT="8001"   
#PROBE_NAME="nicocasso-probe"                          
IP_ADDRESS="Public"                    # Type d'IP (Public ou Private)
DNS_LABEL="nicocasso-prediction-service"
#LOAD_BALANCER_NAME="nicocasso-load-balancer"
#LOAD_BALANCER_RULE="nicocasso-rule"
#FRONTEND_NAME="nicocasso-frontend"
#BACKEND_NAME="nicocasso-backend"
OS_TYPE="Linux"                      # Type d'OS (Linux ou Windows)                 

# Récupération dynamique des identifiants du ACR
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query "username" -o tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query "passwords[0].value" -o tsv)

# Suppression du conteneur existant
az container delete --name $CONTAINER_NAME --resource-group $RESOURCE_GROUP -y

# Récupération des variables d'environnement
source .env


# Créer une adresse IP publique statique
# az network public-ip create \
#     --resource-group $RESOURCE_GROUP \
#     --name $PUBLIC_STATIC_IP \
#     --allocation-method Static

# Associer l'adresse IP à votre conteneur ou service
# (Cette étape dépend de la manière dont votre conteneur est déployé, par exemple via un équilibreur de charge ou directement)

# Déploiement du conteneur sur Azure
echo "Déploiement du conteneur sur Azure..."
az container create \
  --name $CONTAINER_NAME \
  --resource-group $RESOURCE_GROUP \
  --image $ACR_URL/$ACR_IMAGE \
  --cpu $CPU \
  --memory $MEMORY \
  --registry-login-server $ACR_URL \
  --registry-username $ACR_USERNAME \
  --registry-password $ACR_PASSWORD \
  --ports $PORT \
  --ip-address $IP_ADDRESS \
  --os-type $OS_TYPE \
  --dns-name-label $DNS_LABEL

echo "Déploiement terminé."

#   az network lb create \
#     --resource-group $RESOURCE_GROUP \
#     --name $LOAD_BALANCER_NAME \
#     --public-ip-address $PUBLIC_STATIC_IP \
#     --frontend-ip-name $FRONTEND_NAME \
#     --backend-pool-name $BACKEND_NAME

# echo "Réseau d'équlibrage de charge créé."

# az network lb address-pool create \
#     --resource-group $RESOURCE_GROUP \
#     --lb-name $LOAD_BALANCER_NAME \
#     --name $BACKEND_NAME

# echo "Pool de thread configuré."

# az network lb probe create \
#     --resource-group $RESOURCE_GROUP \
#     --lb-name $LOAD_BALANCER_NAME \
#     --name $PROBE_NAME \
#     --protocol HTTP \
#     --port $PROBE_PORT

# echo "Sonde d'intégrité configurée"

# az network lb rule create \
#     --resource-group $RESOURCE_GROUP \
#     --lb-name $LOAD_BALANCER_NAME \
#     --name $LOAD_BALANCER_RULE \
#     --protocol HTTP \
#     --frontend-port $PORT \
#     --backend-port $BACKEND_NAME \
#     --frontend-ip-name $FRONTEND_NAME \
#     --backend-pool-name $BACKEND_NAME \
#     --probe-name $PROBE_NAME

# echo "Regle d'équilibrage créée"