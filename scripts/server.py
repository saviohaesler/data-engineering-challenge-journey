from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json

server = Flask(__name__)

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

@server.route('/')
def index():
    print(request.method)
    return 'Hello world'

@server.route('/data', methods=['POST'])
def sensor_logger():
    try:
        data = json.loads(request.data)
        print(data)
    
        for entry in data["payload"]:
            topic = entry['name']
    
            payload = {
                "time": entry['time'],
                "values": entry['values']
            }
    
            producer.send(topic=topic, value=json.dumps(payload).encode('utf-8'))
        producer.flush()
    
        return jsonify({"message": "Successfully written to Kafka.", "topic": topic}), 200
    except Exception as e:
        return jsonify({"error": e}), 500

# Entry point to this script
if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000)
