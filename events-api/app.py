import json
import boto3
from boto3.dynamodb.conditions import Key, And
from functools import reduce
from flask_lambda import FlaskLambda
from flask import request


app = FlaskLambda(__name__)
ddb = boto3.resource('dynamodb')
table = ddb.Table('event')


@app.route('/')
def index():
    return json_response({"message": "Event API!"})


@app.route('/events', methods=['GET', 'PUT'])
def put_list_event():
    if request.method == 'GET':
        data = request.form.to_dict()
        data['eventID'] = int(data['eventID'])
        events = table.scan()['Items']
        return json_response(events)
    elif request.method == "PUT":
        table.put_item(Item=request.form.to_dict())
        return json_response({"message": "Event entry created"})
    else:
        return json_response({"message": "Method not supported"})


@app.route('/events/<id>', methods=['GET', 'PATCH', 'DELETE'])
def get_patch_delete_event(id):
    key = {'eventID': id}
    if request.method == 'GET':
        event = table.get_item(Key=key).get('Item')
        if event:
            return json_response(event)
        else:
            return json_response({"message": "Event not found"}, 404)
    elif request.method == 'PATCH':
        attribute_updates = {key: {'Value': value, 'Action': 'PUT'}
                             for key, value in request.form.items()}
        table.update_item(Key=key, AttributeUpdates=attribute_updates)
        return json_response({"message": "Event entry updated"})
    elif request.method == 'DELETE':
        table.delete_item(Key=key)
        return json_response({"message": "Event entry deleted"})
    else:
        return json_response({"message": "Method not supported"})

@app.route('/events/eventType/<eventType>', methods=['GET'])
def get_by_event_eventType(eventType):
    if request.method == 'GET':
        events = table.scan(FilterExpression=Key('eventType').eq(eventType))['Items']
        return json_response(events)
    else:
        return json_response({"message": "Method not supported"})

@app.route('/events/deviceID/<deviceID>', methods=['GET'])
def get_by_event_deviceID(deviceID):
    if request.method == 'GET':
        events = table.scan(FilterExpression=Key('deviceID').eq(deviceID))['Items']
        return json_response(events)
    else:
        return json_response({"message": "Method not supported"})

@app.route('/events/userID/<userID>', methods=['GET'])
def get_by_event_userID(userID):
    if request.method == 'GET':
        events = table.scan(FilterExpression=Key('userID').eq(userID))['Items']
        return json_response(events)
    else:
        return json_response({"message": "Method not supported"})



def json_response(data, response_code=200):
    return json.dumps(data,  response_code})


#{"eventID": "10001","eventType": "FaceDetection","eventDate": "2020-06-25 12:00 AM +900","deviceID": "DEBXYZ_1","userID": "user1","eventMessage": "sample text message"}
