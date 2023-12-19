import boto3
import settings

settings.DB_SETTINGS['_s3']['ACCESS_KEY_ID']
settings.DB_SETTINGS['_s3']['ACCESS_SECRET_KEY']
settings.DB_SETTINGS['_s3']['BUCKET_NAME']

s3 = boto3.client('s3', aws_access_key_id=settings.DB_SETTINGS['_s3']['ACCESS_KEY_ID'],
                  aws_secret_access_key=settings.DB_SETTINGS['_s3']['ACCESS_SECRET_KEY'])
bucket_name = settings.DB_SETTINGS['_s3']['BUCKET_NAME']

def extract(route, con_str, con_str2=None):
    '''
    route: str, text routh which you want to extract
    con_str: str, text which you want to contain in file name
    con_str2: str, text which you want to contain in file name
    '''
    # List all files
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=route)

    txt_lst = []
    for obj in response['Contents']:
        if con_str in obj['Key'] and (con_str2 in obj['Key'] if con_str2 else True):
            file_key = obj['Key'] # Make Variable For Get Text
        
            txt_lst.append(file_key)
    print('<<<<< Txt List >>>>>')
    print(txt_lst)

    response = s3.get_object(Bucket=bucket_name, Key=file_key)
    result = response['Body'].read().decode('utf-8')
    
    return result

def get_most_recent_file(prefix):
    objects = s3.list_objects_v2(Bucket=bucket_name)['Contents']

    # Filter objects in the 'user/transcript/' path
    relevant_objects = [obj for obj in objects if obj['Key'].startswith(prefix)]

    # Sort objects by last modified date/time in descending order
    sorted_objects = sorted(relevant_objects, key=lambda obj: obj['LastModified'], reverse=True)

    # Get the most recent object
    most_recent_object = sorted_objects[0]

    return most_recent_object['Key']


