# -*- coding: utf-8 -*-

from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import datetime
from datetime import datetime
from datetime import datetime as dt

# Helper class to convert a DynamoDB item to JSON.
def handler(event, context): 
    #connect to the DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    #create a object to the table order
    table = dynamodb.Table('order')
    #create a object to the table table1
    table1 = dynamodb.Table('PizzaMenu')
    menuId = "store1"

    #Query the order table
    response1 = table.query(KeyConditionExpression=Key('orderId').eq(event.get('orderId')))

    resp =  response1['Items']
    for table_col in resp:
        format_resp = table_col.keys()

#INSERTING SIZE TO THE TABLE
        if ('selection' in format_resp):
            size = event.get('size')
            response5 = table1.get_item(
            Key={
                'menuId' : menuId
            },
            ProjectionExpression = 'size'
        )
            item = response5['Item']
            #print (item)
            sel = (item['size'])
            #print (sel.keys())
            size_list = []
            for sel_size in sel:
                size_list.append(sel_size)
            size_sel = size_list[int(size)-1]

            response2 = table.update_item(
                Key = {'orderId':event.get('orderId')},
                UpdateExpression="set size = :val1",
                ExpressionAttributeValues={':val1': size_sel},
                ReturnValues="UPDATED_NEW"
            )
            response3 = table1.get_item(Key={'menuId' : menuId},ProjectionExpression = 'size')
            item = response3['Item']
            #print (item)
            sel = (item['size'])
            #print (sel[size_sel])
        
            response6 = table.get_item(
            Key={
                'orderId' : event.get('orderId')
            },
            ProjectionExpression = 'size'
        )
            bill = sel[size_sel]


            #print (datetime.today().strftime('%m-%d-%Y %H:%M:%S %p'))
            date = datetime.today().strftime('%m-%d-%Y @ %H:%M:%S %p')

            orderstatus = "processing"
            response10 = table.update_item(
            Key = {'orderId':event.get('orderId')},
                UpdateExpression="set costs = :val2, order_time = :val3, order_status = :val4",
                ExpressionAttributeValues={':val2': bill, ':val3':date, ':val4':orderstatus},
                ReturnValues="UPDATED_NEW"
            )

            return{"Message" : "Your order costs $" +  str(bill) + ". We will email you when the order is ready. Thank you!"}



#INSERTING SELECTION TO THE TABLE
        elif ('selection' not in format_resp):
            selection = event.get('selection')

            response5 = table1.get_item(
            Key={
                'menuId' : menuId
            },
            ProjectionExpression = 'selection'
        )
            item = response5['Item']
            #print (item)
            sel = (item['selection'])
            print (sel)
            selection_list = []
            for sel_sel in sel:
                selection_list.append(sel_sel)
            selection_sel = selection_list[int(selection)-1]

            response4 = table.update_item(
                Key = {'orderId':event.get('orderId')},
                UpdateExpression="set selection = :val",
                ExpressionAttributeValues={':val': selection_sel},
                ReturnValues="UPDATED_NEW"
            )
            response5 = table1.get_item(
            Key={ 'menuId' : menuId},
            ProjectionExpression = 'size')
            
            item = response5['Item']
            #print (item)
            sel = (item['size'])
            #print (sel.keys())
            size_list = []
            for sel_size in sel:
                size_list.append(sel_size)
            size_str = str(size_list)
            return {
        "statusCode": "200 OK",
        "Message": "Which size do you want? 1 . " + size_list[0] + " 2. " + size_list[1] + " 3. " + size_list[2] + " 4. " + size_list[3] + " 5. " + size_list[4]
        }