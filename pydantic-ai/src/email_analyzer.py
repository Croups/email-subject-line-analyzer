
from typing import List, Optional
import nest_asyncio
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel


from convert_to_md import to_markdown

nest_asyncio.apply()

model = OpenAIModel("gpt-4o")

# -----------------     -----------------
#!              SIMPLE AGENT
# -----------------     -----------------


agent1 = Agent(
    model=model,
    system_prompt="You are an expert email subject line analyzer. Your task is to analyze the given subject lines and extract key information."
)

# Example usage of basic agent
response = agent1.run_sync("Code Review Needed for project #1234 ASAP")
print(response.data)
print(response.all_messages())
print(response.cost())

# -----------------     -----------------
#!      AGENT WITH STRUCTURE OUTPUT
# -----------------     -----------------

class ResponseModel(BaseModel):
    category: str        # urgent, general, spam risk, newsletter, personal
    priority: int = Field(description= "1-5 Scale")   
    sentiment: str = Field(description="Customer sentiment analysis")
    action_required: bool 
    keywords: List[str] 
    
agent2 = Agent(
    model=model,
    result_type=ResponseModel,
    system_prompt=(
        "You are an expert email subject line analyzer. Your task is to analyze the given subject lines and extract key information. Be concise and focus on priority, sentiment, required actions, and main keywords. Be conservative with urgency.",
        "Analyze queries carefully and provide structured responses."
    ),
)

response = agent2.run_sync("Code Review Needed for project #1234 ASAP")
print(response.data.model_dump_json(indent=2))


# -----------------     -----------------
#!        AGENT WITH DEPENDENCIES
# -----------------     -----------------

# Email context model
class EmailContext(BaseModel):
    """Structure for email context details."""
    sender_email: str
    sender_name: str
    department: Optional[str] = None

# Response model
class ResponseModel(BaseModel):
    category: str        
    priority: int        
    sentiment: str       
    action_required: bool 
    keywords: List[str]  

# Agent with context
agent3 = Agent(
    model=model,
    result_type=ResponseModel,
    deps_type=EmailContext,  # Dependencies
    retries=3,              # Number of retries
    system_prompt=(
        "You are an expert email subject line analyzer. "
        "Consider the sender's context and department when analyzing. "
        "Analyze carefully and provide structured analysis."
    )
)

@agent3.system_prompt
async def add_customer_name(ctx: RunContext[EmailContext]) -> str:
    return f"Customer details: {to_markdown(ctx.deps)}"  


email = EmailContext(
    sender_email="sample@gmail.com",
    sender_name="John Doe",
    department="software"
)
        
result = agent3.run_sync(
    user_prompt="Code Review Needed for project #1234 ASAP",
    deps=email
)

print(result.data.model_dump_json(indent=2))
