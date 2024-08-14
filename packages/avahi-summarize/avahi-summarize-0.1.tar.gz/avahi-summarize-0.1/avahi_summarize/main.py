def hello():
    print("The package function call is working!")
    
def get_bedrock_client():
    import os
    import boto3
    """Configure and return a Bedrock client using environment variables."""
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region = os.getenv('AWS_REGION')

    if not all([aws_access_key_id, aws_secret_access_key, region]):
        raise ValueError("AWS credentials and region must be set as environment variables.")

    return boto3.client(
        service_name="bedrock-runtime",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region
    )

def summarize_text(text):
    import json 
    """Summarize the provided text using AWS Bedrock."""
    bedrock = get_bedrock_client()
    
    body = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": f"You have been provided with below text\n{text}\n\n------------------------------------------\nSummarize above article in 3-5 lines"}]
            }
        ],
        "max_tokens": 4000,
        "top_p": 0.2,
        "temperature": 0,
        "anthropic_version": "bedrock-2023-05-31"
    })

    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    accept = "application/json"
    content_type = "application/json"

    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept=accept,
        contentType=content_type
    )
    
    result = json.loads(response.get('body').read())['content'][0]['text']
    return result