from dotenv import load_dotenv
import os
import boto3
import json

load_dotenv()

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)

body = json.dumps({
    "messages": [{"role": "user", "content": [{"text": "Say: Nova is working!"}]}],
    "inferenceConfig": {"maxTokens": 50}
})

response = bedrock.invoke_model(
    modelId="amazon.nova-lite-v1:0",
    body=body,
    contentType="application/json",
    accept="application/json"
)

result = json.loads(response["body"].read())
print(result["output"]["message"]["content"][0]["text"])