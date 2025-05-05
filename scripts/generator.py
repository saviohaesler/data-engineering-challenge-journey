from csv import reader
import time
import requests

ts = int(time.time()*1000)

path = '/home/bfh/def2/challenge-journey-savio/data/'

kafka_topics = ["light", "barometer", "pedometer", "location"]

def get_payload(row: list[str], kafka_topic: str) -> dict:
    if kafka_topic == "light":
        time = str(float(float(row[0])/1000+(float(ts))/1000)) # transform the timestamp
        values = {
            "lx": row[1]
        }
    elif kafka_topic == "barometer":
        time = row[-1]
        values = {
            "relativeAltitude": row[0],
            "pressure": row[1]
        }
    elif kafka_topic == "pedometer":
        time = row[-1]
        values = {
            "steps": row[0]
        }
    elif kafka_topic == "location":
        time = row[-1]
        values = {
            "altitude": row[0],
            "speedAccuracy": row[1],
            "bearingAccuracy": row[2],
            "latitude": row[3],
            "altitudeAboveMeanSeaLevel": row[4],
            "bearing": row[5],
            "horizontalAccuracy": row[6],
            "verticalAccuracy": row[7],
            "longitude": row[8],
            "speed": row[9]
        }
    else:
        raise ValueError(f"Unsupported kafka topic: '{kafka_topic}'. Supported topics are: {kafka_topics}")
    return {
        "name": kafka_topic,
        "time": time,
        "values": values
    }

for kafka_topic in kafka_topics:
    with open(path + f"{kafka_topic}.csv", 'r') as data:
        csv_reader = reader(data)
        header_to_skip = next(csv_reader)
        if header_to_skip != None: # File is not empty
            for row in csv_reader:
                print(row)
                data = {
                    "payload": [get_payload(row, kafka_topic)]
                }
                print(data)
    
                # send to server
                response = requests.post('http://10.248.16.132:5000/data', json=data)
    
                print(response.status_code)