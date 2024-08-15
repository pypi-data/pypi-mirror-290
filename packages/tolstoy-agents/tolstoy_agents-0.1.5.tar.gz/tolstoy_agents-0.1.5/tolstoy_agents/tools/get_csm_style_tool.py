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

@handle_exceptions
def get_csm_style(human_csm_email: str,
                ) -> str:
    
    function_name = f"tolstoy-ai-data-{os.environ['env']}-getCSMWritingStyle"
    payload = json.dumps({"body": json.dumps({"humanCsmEmail": human_csm_email})})
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


def get_csm_style_factory() -> StructuredTool:
    return StructuredTool.from_function(
        func=get_csm_style,
        name="get_csm_style",
        description= (
            "Use this tool to match the human CSM's communication style for a consistent, personalized experience"
        ),
        args_schema=ToolInput,
        return_direct=False
    )
