import json
import boto3
import os

ddb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
table = ddb.Table(os.environ['tableName'])

def handler(event, context):
    print(event)
    body = {}
    statusCode = 200
    headers = {
        "Content-Type": "application/json"
    }

    try:
        if event['routeKey'] == "GET /movies":
            body = table.scan()
            body = body["Items"]
            print("ITEMS----")
            print(body)
            responseBody = []
            for items in body:
                responseItems = [
                    {'id': items['id'], 'title': items['title'], 'releaseYear': items['releaseYear'], 'director': items['director']}]
                responseBody.append(responseItems)
            body = responseBody
        elif event['routeKey'] == "GET /movies/{releaseYear}":
            body = table.scan()
            body = body["Items"]
            responseBody = []
            for items in body:
                if items['releaseYear'] == event['pathParameters']['releaseYear']:
                    responseItems = [
                    {'id': items['id'], 'title': items['title'], 'releaseYear': items['releaseYear'], 'director': items['director']}]
                    responseBody.append(responseItems)
            body = responseBody
    except KeyError:
        statusCode = 400
        body = 'Unsupported route: ' + event['routeKey']
    body = json.dumps(body)
    res = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": body
    }
    return res