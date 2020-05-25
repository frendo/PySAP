#!/bin/bash

RG="AZRGSTC"
SUB="CC_Sandbox_Enterprise Dev/Test"
PLAN="AZPLANSTC"
STOR="azstoragestc"
FUNC="FuncSTC"
LOC="westeurope"
STORSKU="Standard_LRS"
TAGN="GSW"
TAGV="STC"
DB="stcdb"
USER="graemestewart.watt@chemours.com"
# Select the Azure subscription that contains the resource group.

az account set --subscription "$SUB" 
echo $RG
#if az group exists -n $RG; then
    echo "Exists"
    az group delete -n $RG
    #az group wait --deleted --resource-group $RG
#else
    echo "Creating group...."
    az group create -l $LOC -n $RG --tags $TAGN=$TAGV --managed-by $USER
    az group wait -n $RG --created
#fi
az appservice plan create -g $RG -n $PLAN
az storage account create -n $STOR -g $RG -l $LOC --sku $STORSKU
az functionapp create -g $RG  -p $PLAN -n $FUNC -s $STOR --functions-version 2 --runtime dotnet
#az cosmosdb create --name $DB --resource-group $RG --subscription $SUB
# Provide an endpoint for handling the events.
#myEndpoint="<endpoint URL>"

# Provide the name of the resource group to subscribe to.
#myResourceGroup="<resource group name>"

# Select the Azure subscription that contains the resource group.
#az account set --subscription "CC_Sandbox_Enterprise Dev/Test"
#az functionapp deployment source config-zip -g {myRG} -n {myAppName} --src {zipFilePathLocation}