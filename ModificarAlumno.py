import boto3

def lambda_handler(event, context):
    print(event)
    tenant_id = event['body']['tenant_id']
    alumno_id = event['body']['alumno_id']
    nuevos_datos = event['body']['alumno_datos'] 
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('t_alumnos')
    
    response_get = table.get_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        }
    )
    alumno_existente = response_get.get('Item', None)
    
    if not alumno_existente:
        return {
            'statusCode': 404,
            'message': 'Alumno no encontrado'
        }
    
    datos_actuales = alumno_existente.get('alumno_datos', {})
    for key, value in nuevos_datos.items():
        if isinstance(value, dict) and key in datos_actuales and isinstance(datos_actuales[key], dict):
            datos_actuales[key].update(value)
        else:
            datos_actuales[key] = value

    response = table.update_item(
        Key={
            'tenant_id': tenant_id,
            'alumno_id': alumno_id
        },
        UpdateExpression="SET alumno_datos = :datos",
        ExpressionAttributeValues={
            ':datos': datos_actuales
        },
        ReturnValues="UPDATED_NEW"
    )
    print(response)
    
    return {
        'statusCode': 200,
        'tenant_id': tenant_id,
        'alumno_id': alumno_id,
        'message': 'Alumno modificado exitosamente',
        'response': response
    }