import boto3 

def lambda_handler(event, context):
    print(event)
    tenant_id = event['body']['tenant_id']
    alumno_id = event['body']['alumno_id']
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    
    response = table.delete_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        }
    )
    print(response)
    
    return {
        'statusCode': 200,
        'tenant_id': tenant_id,
        'alumno_id': alumno_id,
        'message': 'Alumno eliminado correctamente',
        'response': response
    }