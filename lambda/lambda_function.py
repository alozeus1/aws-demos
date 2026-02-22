import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Students')


def _response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps(body)
    }


def lambda_handler(event, context):
    method = event.get('httpMethod')
    path = (event.get('resource') or event.get('path') or '').lower()

    if method == "GET" and path.endswith("/health"):
        return _response(200, {"status": "ok"})

    if method == "POST":
        body = json.loads(event['body'])
        table.put_item(Item=body)
        return _response(200, "Student registered successfully")

    if method == "GET":
        path_parameters = event.get('pathParameters') or {}
        student_id = path_parameters.get('studentID')
        if not student_id:
            return _response(400, "studentID is required")

        response = table.get_item(Key={'studentID': student_id})
        item = response.get('Item')
        if item:
            return _response(200, item)
        return _response(404, "Student not found")

    return _response(400, "Unsupported method")
