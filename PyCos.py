#!/usr/bin/python
import json
import os
from azure.cosmos import CosmosClient, PartitionKey, exceptions

def main(data):
    client = CosmosClient(data['uri'], credential=data['pkey'])
    db = client.get_database_client(data['db'])
    container = db.get_container_client(data['container'])
    query = 'SELECT * FROM c WHERE c.id="1"'
    for item in container.query_items(query=query, enable_cross_partition_query=True):
        payload = json.dumps(item, indent=True)
        print(type(payload))
        print(payload['Customer'])
if __name__ == "__main__":
    configFile = '\\config_cosmos.json'
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    data = {}

    with open(__location__ + configFile) as config_file:
        data = json.load(config_file)

    main(data)