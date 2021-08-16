# pip install boto3
# pip install awscli
# aws configure

# **contact admin(Xavier Wells) for credentials** 
# OR 
# if youre the new team create a bucket named 
# identidocdocumentclassifier(or change BUCKETNAME to name of your bucket) in AWS s3.

# After doing that, setup an IAM user with the perms you need.

import boto3
import logging
from botocore.exceptions import ClientError


s3 = boto3.resource('s3')
BUCKETNAME = 'identidocdocumentclassifier'
BUCKET = s3.Bucket(BUCKETNAME)

def download_file(object_name, file_name=None):
    """Download a file

    :param object_name: S3 object name to download
    :param file_name: name of local file. If not specified then file_name is used
    :return: True if file was downloaded, else False
    """
    
    # If S3 object_name was not specified, use file_name
    if file_name is None:
        file_name = object_name
    
    #download the file
    try:
        BUCKET.download_file(object_name, file_name)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
            return False
        else:
            raise
            return False
    return True

def upload_file(file_name, object_name=None):
    """Upload a file

    :param file_name: File to upload
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, BUCKETNAME, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def delete_file(object_name):
    """delete a file

    :param object_name: S3 object name.
    :return: True always due to aws not having proper response to delete
    """
    
    s3.Object(BUCKETNAME, object_name).delete()
    return True

def list_files():
    """List of all files
    
    :return: list of s3 objects
    """
    
    listOfObjects = []
    for obj in BUCKET.objects.all():
        if obj is None:
            continue
        else:
            listOfObjects.append(obj)
        
    return listOfObjects