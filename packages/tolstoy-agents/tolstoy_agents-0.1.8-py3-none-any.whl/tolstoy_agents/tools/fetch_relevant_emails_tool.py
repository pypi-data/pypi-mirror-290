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
    tolstoy_user_email: str = Field(description="Email of user")
    threadId: str = Field(description="image or video")

@handle_exceptions
def fetch_relevant_emails(human_csm_email: str,
                  tolstoy_user_email: str,
                  threadId: str
                ) -> str:
    
    function_name = f"tolstoy-ai-data-{os.environ['env']}-getCSMRelevantEmails"
    payload = json.dumps({
        "body": json.dumps({
            "humanCsmEmail": human_csm_email,
            "senderEmail": tolstoy_user_email,
            "threadId": threadId
        })
    })
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


def fetch_relevant_emails_factory() -> StructuredTool:
    return StructuredTool.from_function(
        func=fetch_relevant_emails,
        name="fetch_relevant_emails",
        description= (
            "Use this tool to retrieve relevant email threads/messages between the human CSM and the Tolstoy user when you believe the context or answer to the current email might be found in previous conversations. Reasons to use this tool include:\n"
            "- The current email refers to a previous conversation with the human CSM.\n"
            "- The user mentions something that may have been discussed in earlier emails with the Human CSM.\n"
            "- You need more context about the user's situation or problem to provide an accurate response."
        ),
        args_schema=ToolInput,
        return_direct=False
    )


