# Import the SDK
import boto3
import uuid
s3 = boto3.resource('s3')
bucket_name = 'sound-ai'
bucket = bucket = s3.Bucket(bucket_name)
# print('Uploading some data to {} with key: {}'.format(
#     bucket_name, object_key))
    
# s3client.put_object(Bucket=bucket_name, Key=object_key, Body=b'Hello World!')
# pageresponse = paginator.paginate(Bucket=bucket_name)
# Boto 3
# for key in bucket.objects.all():
#     key.name
# for key in bucket.objects.get('fold4'):
#     print(dir(key))
import os
import shutil
dest = 'data/'
def upload(directories):
    """
    directories are arrays
    """
    for directory in directories:
        directory_path= dest+directory
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
        for key in bucket.objects.filter(Prefix=directory+'/'):
            sound_file = dest+key.key
            try:
                fh = open(sound_file,'r')
            except:
            # if file does not exist, create it
                fh = open(sound_file,'w')
            bucket.download_file(key.key, sound_file)

def delete_dirs(directories):
    for directory in directories:
        directory_path= dest+directory
        shutil.rmtree(directory_path)