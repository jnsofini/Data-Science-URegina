# Lambda Kinesis Demo

In this project, we will demonstrate how to use a Lambda function to process streaming data from a Kinesis stream. We will simulate the data source using the `stream_source.py` script, and the Lambda function responsible for processing the data is `monitor.py`.

## Step 1: Setup Streaming Data

To set up the streaming data, we need to create a Kinesis stream in AWS. Follow these steps:

1. Go to the **Amazon Kinesis** service and select **Data streams**.
2. Click **Create data stream** and provide a name for the stream, such as "_server-data_".
3. Configure the desired number of shards based on your requirements.
4. Once the stream is created, you should see it listed with the status "Active".

Here is an example of the stream creation process:

![Filling the info](images/kinesis-console-start.png)
![Running service](images/kinesis-console-active.png)

To generate the simulated data for the stream, we provide a script called `stream_source.py`. Before running the script, make sure you have completed the following requirements:

- Set up the Python environment and install all the necessary requirements.
- Configure your AWS credentials. You can either directly add the access key and ID or use a profile configured via `aws configure --profile`.

It's not necessary to start generating data until we configure the consumer of the streaming data, which in this case is our Lambda function.

## Step 2: Setup Consumer

Our consumer is a Lambda function named `temperature-monitor`. Follow these steps to set it up:

1. Go to the **Lambda** service and click **Create function**.
2. Provide a name for the function, select **Python 3.10** as the runtime, and choose **Use an existing role**.
3. In a new AWS IAM window, go to **Roles** and create a role with the following configuration:
   - Select **AWS service** as the trusted entity.
   - Choose **Lambda** as the service that will use this role.
   - Search for and select **AWSLambdaKinesisExecutionRole** as the policy.
   - Give the policy a name, such as "_lambda-kinesis-role_".
4. Once the role is created, go back to the Lambda function configuration page and select the role from the dropdown menu.
5. With the role attached, the Lambda function can now read from the Kinesis stream. However, we still need to add a trigger to initiate the data processing.

### 1. Provide Consumer with Roles

Before attaching the role to the Lambda function, follow these steps:

1. Open a new AWS IAM window and go to **Roles**.
2. Create a new role and select **AWS service** as the trusted entity.
3. Choose **Lambda** as the service that will use this role.
4. Search for **AWSLambdaKinesisExecutionRole** and select it as the policy.
5. Proceed to the next steps and name the policy as "_lambda-kinesis-role_" or any desired name.

### 2. Setup Lambda

Once the role is created, return to the Lambda function configuration page and follow these steps:

1. Select the newly created role from the dropdown menu.
2. The Lambda function can now read from the Kinesis stream.

### 3. Event Trigger

To trigger the Lambda function to read from the Kinesis stream, follow these steps:

1. Go to the Lambda function page and click on **Add trigger**.
2. Select **Kinesis** as the trigger type.
3. In the provided window, select the **server-data** stream from the Kinesis stream dropdown.
4. Optionally, you can adjust the **batch size** (e.g., 10

) to determine the number of events the Lambda function can pull.
5. Leave the **starting position** as **Latest** to process only the latest data. You can choose to process the entire stream by selecting a trim horizon or specifying a time range.
6. Set the **batch window** to 5 seconds (or your desired value).
7. Finish the trigger setup.

Here is an example of a finished Lambda function console:

![](images/lambda-console-finished.png)

## Step 3: Generate Events

To generate the streaming data, run the `stream_source.py` script using the command `python stream_source.py`. This script will push events to the Kinesis stream.

To monitor the incoming data in the Lambda function, follow these steps:

1. Go to the Lambda function page and select **Monitor**.
2. View the CloudWatch logs by clicking on the log group associated with the Lambda function.
3. Inspect the logs to see the output of the Lambda function.

Make sure to observe the CloudWatch logs to verify that the Lambda function is successfully processing the streaming data.
