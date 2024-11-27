import boto3
import time
import random
import uuid
import logging

# import os
import json

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    write_client = boto3.client("timestream-write")

    # database_name = os.environ["TIMESTREAM_DATABASE_NAME"]
    database_name = "sampleDB"
    # table_name = os.environ["TIMESTREAM_TABLE_NAME"]
    table_name = "uplinkDB"

    # AI-generated: Load machines from JSON file
    try:
        with open("machines.json", "r") as f:
            machines = json.load(f)
    except Exception as err:
        logger.error(f"Failed to load machines.json: {err}")
        return {
            "statusCode": 500,
            "body": f"Error loading machines configuration: {str(err)}",
        }

    current_time = int(time.time() * 1000)
    records = []

    # AI-generated: Generate records for each machine
    for machine in machines:
        machine_id = machine.get("id", str(uuid.uuid4()))
        # AI-generated: Generate random value within machine's specified range
        min_value = machine.get("min_value", 0)
        max_value = machine.get("max_value", 100)
        current_value = random.uniform(min_value, max_value)

        records.append(
            {
                "Dimensions": [
                    {"Name": "id", "Value": machine_id},
                    {"Name": "name", "Value": machine.get("name", "unknown")},
                    {"Name": "type", "Value": machine.get("type", "default")},
                ],
                "MeasureName": "a_rms",
                "MeasureValue": f"{int(current_value)}",
                "MeasureValueType": "BIGINT",
                "Time": str(current_time),
            }
        )

    try:
        result = write_client.write_records(
            DatabaseName=database_name, TableName=table_name, Records=records
        )
        print(
            "WriteRecords Status: [%s]" % result["ResponseMetadata"]["HTTPStatusCode"]
        )
    except Exception as err:
        print("Error:", err)

    return {"statusCode": 200, "body": f"Data written for {len(records)} machines"}
