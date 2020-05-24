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

def add_order(table_service, req_body):
    row_key = get_rows(table_service) + 1
    print(row_key)
    order = Entity()
    order.PartitionKey = req_body.get('PartitionKey')
    order.RowKey = '00' + str(row_key)
    order.customer = req_body.get('customer')
    order.po = req_body.get('po')
    order.podate = req_body.get('poDate')
    order.deldate = req_body.get('delDate')
    order.qty = req_body.get('qty')
    order.presentation = req_body.get('presentation')
    order.order = req_body.get('order')
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

def get_order(table_service, RowKey):
    order = table_service.get_entity('ordertable', 'ordersSTC', RowKey)
    order_json = json.dumps(order,indent=4, sort_keys=True, default=str)
    return order_json

def get_orders(table_service):
    aList = []
    orders = table_service.query_entities(
    'ordertable', filter="PartitionKey eq 'ordersSTC'")
    for order in orders:
        aList.append(order)
    payload = json.dumps(aList,indent=4, sort_keys=True, default=str)
    #i = iter(orders)
    #payload = dict(zip(i,1))
    return payload

def get_rows(table_service):
    orders = table_service.query_entities(
    'ordertable', filter="PartitionKey eq 'ordersSTC'", select='RowKey')
    cnt = 0
    for order in orders:
        cnt = cnt + 1
    return cnt 

def delete_order(table_service, RowKey):
    table_service.delete_entity('ordertable', 'ordersSTC', RowKey)

def delete_table():
    table_service.delete_table('ordertable')

def main(data):
    table_service = TableService(account_name=data['storage'], account_key=data['skey'])
    #create_table(table_service)
    #add_order(table_service)
    query_set(table_service)

def az_storage(req_body):
    configFile = os.path.sep + 'config_cosmos.json'
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    data = {}

    with open(__location__ + configFile) as config_file:
        data = json.load(config_file)
    print(req_body)
    table_service = TableService(account_name=data['storage'], account_key=data['skey'])
    db_op = req_body.get('db_op')

    if db_op == 'get_rows':
        payload = get_rows(table_service)
        return payload
    elif db_op == 'add_order':
        add_order(table_service, req_body)
        return 'Successful order'
    elif db_op == 'delete_order':
        delete_order(table_service, req_body.get('RowKey'))
        return 'Order Deleted'
    elif db_op == 'get_orders':
        payload = get_orders(table_service)
        return payload
    elif db_op == 'get_order':
        payload = get_order(table_service, req_body.get('RowKey'))
        return payload



if __name__ == "__main__":
    configFile = os.path.sep + 'config_cosmos.json'
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    data = {}

    with open(__location__ + configFile) as config_file:
        data = json.load(config_file)

    main(data)