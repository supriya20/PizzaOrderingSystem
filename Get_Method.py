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
    response = table.get_item(
            Key={
                'orderId' : event.get('orderId')
            }
        )
    #print (response['Item'])
    format1 = response['Item']
    menuId = format1['menuId']
    #print (menuId)
    orderId = format1['orderId']
    #print (orderId)
    customer_name = format1['customer_name']
    #print (customer_name)
    customer_email = format1['customer_email']
    #print(customer_email)
    order_status = format1['order_status']
    #print(order_status)
    selection = format1['selection']
    #print (selection)
    size = format1['size']
    #print (size)
    costs = format1['costs']
    #print (costs)
    order_time = format1['order_time']
    #print (order_time)



    return{
        "menuId" : menuId,
        "oderId" : orderId,
        "customer_name" : customer_name,
        "customer_email" :  customer_email,
        "order_status" : order_status,
        "order" : {
            "selection" : selection,
            "size" : size,
            "costs" : costs,
            "order_time" : order_time
        }

    }