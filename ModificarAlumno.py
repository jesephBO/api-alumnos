import boto3  # import Boto3

def lambda_handler(event, context):
    print(event)
    tenant_id = event['body']['tenant_id']
    alumno_id = event['body']['alumno_id']
    alumno_datos = event['body']['alumno_datos']
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    response = table.update_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        },
        UpdateExpression="SET alumno_datos = :datos",
        ExpressionAttributeValues={
            ':datos': alumno_datos
        },
        ReturnValues="UPDATED_NEW"
    )
    print(response)
    
    return {
        'statusCode': 200,
        'tenant_id': tenant_id,
        'alumno_id': alumno_id,
        'response': response
    }