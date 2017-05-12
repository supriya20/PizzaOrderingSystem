# -*- coding: utf-8 -*-

from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

# Helper class to convert a DynamoDB item to JSON.
def handler(event, context): 
    
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')

    table = dynamodb.Table('order')
    menuId="store1"
    response = table.put_item(
    Item={'menuId' : menuId,
        'orderId': event.get('orderId'),
            'customer_name': event.get('customer_name'),
            'customer_email': event.get('customer_email')
        }
    )

    dynamodb2 = boto3.resource('dynamodb', region_name='eu-west-1')
    table1 = dynamodb2.Table('PizzaMenu')

    try:
        response2 = table1.get_item(
            Key={
                'menuId' : menuId
            },
            ProjectionExpression = 'selection'
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        item = response2['Item']
        sel = (item['selection'])
        a =  len(sel)
        print (a)
        if (a == 3):
            format1 =  "Hi " + event.get('customer_name') + ", please choose one of these selection: 1. " + sel[0] +" 2. " + sel[1] + " 3. " + sel[2]
        elif (a == 2):
            format1 =  "Hi " + event.get('customer_name') + ", please choose one of these selection: 1. " + sel[0] +" 2. " + sel[1]
        #print(json.dumps(format1, indent=4, cls=DecimalEncoder))
        return {
        "statusCode": "200 OK",
        "Message": format1
    }

