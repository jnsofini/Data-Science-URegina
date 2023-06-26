import json
import base64

def lambda_handler(event, context):

    print(event)
    predictions_events = []
    for record in event['Records']:
        encoded_data = record['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        temperature_event = json.loads(decoded_data)
        print(temperature_event)

def get_data():
    with open("kinesis_data.json", 'r') as fout:
        data = json.load(fout)
    return data

def main():
    data = get_data()
    print(data)
    lambda_handler(data, None)

if __name__ == "__main__":
    main()