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
PATH="./Archive.zip"
#myEndpoint="<endpoint URL>"

# Select the Azure subscription that contains the resource group.
az account set --subscription "$SUB"
az functionapp deployment source config-zip -g $RG -n $FUNC --src $PATH 