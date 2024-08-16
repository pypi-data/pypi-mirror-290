from pydantic import BaseModel, Field
from typing import List, Optional

class CSMAgentTaskMessage(BaseModel):
    sessionId: str = Field(description="The provided session id from the user prompt")
    title: str = Field(description="A concise title describing the task")
    assignedTeam: str = Field(description="""
    The team assigned to work on the task (csm or product).
    Assign to CSM team if the task involves:
    - Customer engagement, feedback, or relationship management
    - Strategic discussions or high-priority customer interactions
    - Complex technical issues requiring in-depth investigation
    - Initial product fixes or customization
    - Customer complaints needing detailed resolution
    Assign to Product team if the task involves:
    - Product development
    - Feature requests
    """)
    assigneeName: str = Field(description="""
    The person assigned to work on the task.
    For CSM team:
    - Assign to Gilbert Castro or Amor Baron (choose based on who is mentioned as the recipient)
    For Product team:
    - Always assign to Danielle Harris
    """)
    dueDate: str = Field(description="The due date for the task in the format 'MM-DD-YYYY' (1-5 days from the current date)")
    priority: str = Field(description="Task priority level")
    description: str = Field(description="A detailed description of the task")

class AIOperationsTaskMessage(BaseModel):
    sessionId: str = Field(description="The provided session id from the user prompt")
    title: str = Field(description="A clear, concise title task to improve the problematic agent")
    assignedTeam: str = Field(description="agents")
    assigneeName: str = Field(description="Ruben Madeja")
    dueDate: str = Field(description="The due date for the task in the format 'MM-DD-YYYY' (1-5 days from the current date)")
    priority: str = Field(description="Task priority level")
    description: str = Field(description="Detailed description of what should the AI Operation do to improve the problematic agent or the referee of the agent")

class TechnicalWriterTaskMessage(BaseModel):
    sessionId: str = Field(description="The provided session id from the user prompt")
    title: str = Field(description="A clear, concise title task for the technical writer.")
    assignedTeam: str = Field(description="agents")	
    assigneeName: str = Field(description="Technical Writer")
    dueDate: str = Field(description="The due date for the task in the format 'MM-DD-YYYY' (1-5 days from the current date)")
    priority: str = Field(description="Task priority level")
    description: str = Field(description="Brief description what should the technical writer do. If the Article Issue Type is incorrect technical writer needs to update the article, if it's missing, technical writer needs to create an article")

class SlackMessageTaskMessage(BaseModel):
    sessionId: str = Field(description="The provided session id from the user prompt")
    title: str = Field(description="A clear, concise title task to improve the problematic agent")
    assignedTeam: str = Field(description="agents")
    assigneeName: str = Field(description="Ruben Madeja")
    dueDate: str = Field(description="The due date for the task in the format 'MM-DD-YYYY' (1-5 days from the current date)")
    priority: str = Field(description="Task priority level")
    description: str = Field(description="Detailed description of what should the AI Operation do to improve the problematic agent or the referee of the agent")

def get_task_message_model(task_type: str):
    if task_type == "AI Operations":
        return AIOperationsTaskMessage
    elif task_type == "CSM Agent":
        return CSMAgentTaskMessage
    elif task_type == "Technical Writer":
        return TechnicalWriterTaskMessage
    elif task_type == "Slack Message":
        return SlackMessageTaskMessage
    else:
        raise ValueError(f"Invalid task_type: {task_type}")