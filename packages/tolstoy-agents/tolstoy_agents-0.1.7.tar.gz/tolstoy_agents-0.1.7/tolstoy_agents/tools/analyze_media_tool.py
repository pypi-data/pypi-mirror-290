import os
import json
import functools
from pydantic import BaseModel, Field
import boto3

from langchain.tools import StructuredTool

from tolstoy_agents.utils import (
    handle_exceptions
    )

lambda_client = boto3.client('lambda')

class ToolInput(BaseModel):
    human_csm_email: str = Field(description="Email of the CSM")
    messageId: str = Field(description="messageId of the message")
    mediaType: str = Field(description="image or video")

@handle_exceptions
def analyze_media(human_csm_email: str,
                  messageId: str,
                  mediaType: str
                ) -> str:
    
    function_name = f"tolstoy-ai-data-{os.environ['env']}-getMedia"
    
    payload = json.dumps({"body": json.dumps({"gmailUser": human_csm_email, "messageId": messageId, "mediaType": mediaType})})
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',
        Payload=payload
    )
    
    if response.get('StatusCode') == 200:
        response_payload = json.loads(response['Payload'].read())
        return response_payload.get('body')
    else:
        return ""


def analyze_media_factory() -> StructuredTool:
    return StructuredTool.from_function(
        func=analyze_media,
        name="analyze_media",
        description= (
            " This tool checks if there are attached media in the email. The response should be interpreted as if you have seen the media, not just read text"
        ),
        args_schema=ToolInput,
        return_direct=False
    )
