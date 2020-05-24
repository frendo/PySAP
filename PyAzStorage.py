import json
import os
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity
from azure.cosmosdb.table.tablebatch import TableBatch

def create_table(table_service):
    table_service.create_table('ordertable')
    #order = {'PartitionKey': 'ordersSTC', 'RowKey': '001',
    #    'customer': 'Bismark', 'po': '200', 'poDate': '05/20/2020', 
    #    'delDate':'05/20/2020', 'qty':'100', 
    #    'presentation':'Flobin', 'order':'8500687926'}
    #table_service.insert_entity('ordertable', order)
    #table_service.insert_or_replace_entity('ordertable', order)

def add_order(table_service):
    order = Entity()
    order.PartitionKey = 'ordersSTC'
    order.RowKey = '002'
    order.customer = 'Bismark'
    order.po = '200'
    order.podate = '05/20/2020'
    order.deldate = '05/24/2020'
    order.qty = '800'
    order.presentation = 'Flobin'
    order.order = '8500687926'
    table_service.insert_entity('ordertable', order)

def update_order():
    order = {'PartitionKey': 'ordersSeattle', 'RowKey': '001',
            'description': 'Take out the garbage', 'priority': 250}
    table_service.update_entity('ordertable', order)

def batch_entry():
    batch = TableBatch()
    order004 = {'PartitionKey': 'ordersSeattle', 'RowKey': '004',
            'description': 'Go grocery shopping', 'priority': 400}
    order005 = {'PartitionKey': 'ordersSeattle', 'RowKey': '005',
            'description': 'Clean the bathroom', 'priority': 100}
    batch.insert_entity(order004)
    batch.insert_entity(order005)
    table_service.commit_batch('ordertable', batch)

    order006 = {'PartitionKey': 'ordersSeattle', 'RowKey': '006',
            'description': 'Go grocery shopping', 'priority': 400}
    order010 = {'PartitionKey': 'ordersSeattle', 'RowKey': '007',
            'description': 'Clean the bathroom', 'priority': 100}

    with table_service.batch('ordertable') as batch:
        batch.insert_entity(order006)
        batch.insert_entity(order007)

def get_order():
    order = table_service.get_entity('ordertable', 'ordersSeattle', '001')
    print(order.description)
    print(order.priority)

def filter_orders():
    orders = table_service.query_entities(
    'ordertable', filter="PartitionKey eq 'ordersSeattle'")
    for order in orders:
        print(order.customer)
        print(order.priority)

def query_set(table_service):
    orders = table_service.query_entities(
    'ordertable', filter="PartitionKey eq 'ordersSTC'", select='RowKey')
    for order in orders:
        print(order.RowKey)
    cnt = int(order.RowKey)
    print(cnt)

def delete_order():
    table_service.delete_entity('ordertable', 'ordersSeattle', '001')

def delete_table():
    table_service.delete_table('ordertable')

def main(data):
    table_service = TableService(account_name=data['storage'], account_key=data['skey'])
    #create_table(table_service)
    #add_order(table_service)
    query_set(table_service)

if __name__ == "__main__":
    configFile = os.path.sep + 'config_cosmos.json'
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    data = {}

    with open(__location__ + configFile) as config_file:
        data = json.load(config_file)

    main(data)