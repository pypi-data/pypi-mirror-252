import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def s3event_extract(event):
    
    if type(event) != dict:
        raise TypeError(f"El event_message pasado no es de tipo dict, si no de tipo {type(event)}")
    if len(event) == 0:
        raise ValueError("El evento introducido está vacío")
     
    raw_message = json.loads(event['Records'][0]['body'])['Message']
    event_message = json.loads(raw_message)['Records'][0]

    s3_meta = event_message["s3"]

    key = s3_meta["object"]["key"]
    bucket_name = s3_meta["bucket"]["name"]

    uri = "s3://" + bucket_name + '/' + key
    return uri, bucket_name, key


def dynamodb_loader(msg_content, s3_bucket_name, file_name, file_URI):
    # Carga la tabla de dynamodb con metadatos operativos de seguimiento de 
    # una ejecución del appflow (Primary Key es un ID deEjecución de ese 
    # servicio)
    try:
        dynamo_client = boto3.client('dynamodb')
        dynamo_client.put_item(TableName=os.environ['dynamodb_name']
                            , Item={'id':{'S':msg_content['s3']['object']['eTag']}
                            ,'TimeStamp':{'S':msg_content['eventTime']}
                            ,'event_name':{'S':msg_content['eventName']}
                            ,'event_source':{'S':msg_content['eventSource']}
                            ,'aws_region':{'S':msg_content['awsRegion']}
                            ,'s3_bucket_name':{'S':s3_bucket_name}
                            ,'DocumentName':{'S':file_name}
                            ,'DocumentSize':{'N':msg_content['s3']['object']['size']}
                            ,'DocumentURI':{'S':file_URI}
                            ,'DocumentLayer':{'S':'Raw'}
                            })
        print(f"Tabla {os.environ['dynamodb_name']} de DynamoDB actualizada correctamente.")

    except Exception as exp:
        logger.info(f'Error subiendo archivo a DynamoDB')
        exception_type, exception_value, exception_traceback = sys.exc_info()
        traceback_string = traceback.format_exception(exception_type, exception_value, exception_traceback)
        err_msg = json.dumps({
            "errorType": exception_type.__name__,
            "errorMessage": str(exception_value),
            "stackTrace": traceback_string
        })
        logger.error(err_msg)
