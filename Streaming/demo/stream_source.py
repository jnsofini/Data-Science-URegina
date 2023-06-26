import json
import datetime
import random
import boto3
# import psutil

session = boto3.Session(
    # Using local profile
    # aws_access_key_id = "keys",
    # aws_secret_access_key="secret_key",
    region_name = "us-west-2"
)
client = session.client("kinesis")
STREAM_NAME = "demo-temperature"

def get_data(device_name, lower_bound, upper_bound):
    data = {
        "device_name": device_name,
        "temperatue": random.randint(lower_bound, upper_bound),
        "time": str(datetime.datetime.now())
    }

    return data

def main():
    for temp in range(100):
        random_number = random.random()
        if random_number < 0.1:
            data = json.dumps(
                get_data(
                device_name="demo_sensor",
                lower_bound=100,
                upper_bound=120
                )
            )
            print("=================Anomaly Temperature============")
        else:
            data = json.dumps(
                get_data(
                device_name="demo_sensore",
                lower_bound=10,
                upper_bound=20
                )
            )
        
        client.put_record(
                StreamName=STREAM_NAME,
                Data=data,
                PartitionKey=str(1)
            )

        print(data, datetime.datetime.now())
        # print("temperature", psutil.sensors_temperatures(fahrenheit=False))

if __name__ == "__main__":
    main()

