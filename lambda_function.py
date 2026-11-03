import boto3, os

r53 = boto3.client("route53")

def lambda_handler(event, context):
    auth = event.get("headers", {}).get("authorization", "")
    if auth != "Bearer " + os.environ["TOKEN"]:
        return {
           "statusCode": 403,
            "headers": {"Content-Type": "application/json"},
            "body": '{"error": "forbidden"}',
}

    ip = event["requestContext"]["http"]["sourceIp"]
    r53.change_resource_record_sets(
        HostedZoneId=os.environ["ZONE_ID"],
        ChangeBatch={"Changes": [{
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": os.environ["RECORD"],
                "Type": "A",
                "TTL": 60,
                "ResourceRecords": [{"Value": ip}],
            },
        }]},
    )
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": '{"ip": "' + ip + '"}',
}
