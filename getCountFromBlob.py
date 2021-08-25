from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, blockblobservice
import json
import datetime
import os
import re
import pytz

def updateData():
    blob_client = container_client.get_blob_client(latest_modified_filename)
    streamdownloader = blob_client.download_blob()

    #download a file to the dataFromBlob\data directory
    dir_path = os.path.join("'", os.getcwd(),"dataFromBlob")
    if not (os.path.isdir(dir_path)):
        os.makedirs(dir_path)
        print("created folder : ", dir_path)


    dest_path = dest_path = os.path.join(dir_path, "data")    
    with open(dest_path, "wb") as my_blob:
           download_stream = blob_client.download_blob()
           my_blob.write(download_stream.readall())

    with open(dest_path, "r") as f:
           data = f.read()
           if (not (data.endswith("]"))):
               data = data + "]"


    json_data = json.loads(data)


    if len(json_data) > 0 and json_data[-1].get('count') is not None:
        dataTimeStamp = json_data[-1]['@timestamp']
        print(json_data[-1]['count'],dataTimeStamp)
        timeList = (re.split(r'[-T:.Z]',dataTimeStamp))
        #remove empty element
        timeList = list(filter(None, timeList))
        for i in range(0, len(timeList)):
            timeList[i] = int(timeList[i])
        
        b = datetime.datetime(timeList[0], timeList[1], timeList[2], timeList[3], timeList[4], timeList[5])
        if(checkValidTime(b)):
            count = int(json_data[-1]['count'])
        else:
            count = 0
        
    else:
        print("no valid data")
    return(count)

def checkValidTime(timeToCheck):
    validTime = True
    currentTime = datetime.datetime.now()
    #this is the time in China time zone
    dataTime = timeToCheck + datetime.timedelta(hours=8)
    print(currentTime, dataTime)
    difference = abs(currentTime - dataTime)
    #if the data is not updated since 9 seconds ago, assume that there is no people detected for the
    #past 9 seconds
    if (difference > datetime.timedelta(minutes=0.15)):
        validTime = False
        #if no data is received for the last 3 minutes, alert the user to check if there is connection error
        if (difference > datetime.timedelta(minutes=3)):
            print("There is no valid data since 3 minutes ago, please check if your device connected to the cloud and the stream analytics job is running!")
    return validTime

def getCountData():
    counts=updateData()
    return counts

count = 0
#date of today
now = datetime.datetime. now(). strftime("%Y/%m/%d")


container_name="datapoints"
constr = "DefaultEndpointsProtocol=https;AccountName=smartsdcsa;AccountKey=2jXDMI53MdEKST1ZWiyI6DacC+zw6iowIrkfjw0BM/ooYwcKDkZFIFBF2uXJbLUTn5p4NEtHHJtwOydYzAEvsA==;EndpointSuffix=core.windows.net"

blob_service_client = BlobServiceClient.from_connection_string(constr)
container_client = blob_service_client.get_container_client(container_name)
# load today's file from blob container
blobs_list = container_client.list_blobs(name_starts_with = now)

#find the last modified file of today
latest_modified_time = datetime.datetime(2001,1,1,0,0,0, tzinfo=pytz.UTC)
latest_modified_filename = ""
for blob in blobs_list:
    modified_time = blob.last_modified
    if(modified_time>latest_modified_time):
        latest_modified_filename = blob
        latest_modified_time = modified_time
print("blobs in the datapoints container:" + '\n' + latest_modified_filename.name + '\n')
    
if(latest_modified_filename == ""):
    print("There is no valid data in the datapoint container for the last 24 hours")







