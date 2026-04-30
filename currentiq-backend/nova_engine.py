import boto3
import json
import re
import asyncio
from functools import partial
from config import (
    AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION,
    NOVA_MODEL_DIGEST, NOVA_MODEL_MCQ, NOVA_MODEL_EVAL
)

# Bedrock client
bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

def _invoke_nova_sync(prompt, model_id, max_tokens=2000, temperature=0.7):
    body = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": [{"text": prompt}]
            }
        ],
        "inferenceConfig": {
            "maxTokens": max_tokens,
            "temperature": temperature,
            "topP": 0.9
        }
    })

    response = bedrock_client.invoke_model(
        modelId=model_id,
        body=body,
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())

    usage = result.get("usage", {})
    print(
        f"[Nova] model={model_id} | "
        f"in={usage.get('inputTokens','?')} | "
        f"out={usage.get('outputTokens','?')} tokens"
    )

    return result["output"]["message"]["content"][0]["text"]


async def call_nova(prompt, model_id=None, expect_json=False, max_tokens=2000):
    if model_id is None:
        model_id = NOVA_MODEL_DIGEST

    if expect_json:
        prompt += (
            "\n\nCRITICAL INSTRUCTION: Your response must be ONLY valid JSON. "
            "No markdown code fences. No backticks. No preamble or explanation. "
            "Start your response directly with { and end with }."
        )

    loop = asyncio.get_event_loop()
    fn = partial(_invoke_nova_sync, prompt, model_id, max_tokens)
    result = await loop.run_in_executor(None, fn)
    return result


async def call_nova_digest(prompt, expect_json=True):
    return await call_nova(prompt, model_id=NOVA_MODEL_DIGEST,
                           expect_json=expect_json, max_tokens=2500)

async def call_nova_mcq(prompt, expect_json=True):
    return await call_nova(prompt, model_id=NOVA_MODEL_MCQ,
                           expect_json=expect_json, max_tokens=2000)

async def call_nova_eval(prompt, expect_json=True):
    return await call_nova(prompt, model_id=NOVA_MODEL_EVAL,
                           expect_json=expect_json, max_tokens=3000)


def parse_nova_json(raw):
    # Strip markdown fences if present
    clean = re.sub(r'```(?:json)?\s*|\s*```', '', raw).strip()

    # Try direct parse
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        pass

    # Find first { ... } block
    match = re.search(r'\{[\s\S]*\}', clean)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    # If all else fails
    print(f"[Nova] JSON parse failed. Raw: {raw[:300]}")
    return {"error": "Failed to parse Nova response", "raw": raw[:200]}