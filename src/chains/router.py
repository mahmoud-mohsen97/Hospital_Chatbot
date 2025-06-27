from typing import Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field


class RouteQuery(BaseModel):
    """Route a user query to the most relevant datasource."""

    datasource: Literal["vectorstore", "simulated_generation"] = Field(
        ...,
        description="Given a user question choose to route it to simulated generation or a vectorstore.",
    )


llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)
structured_llm_router = llm.with_structured_output(RouteQuery)

system = """
You are *Router-LLM*, a context-aware classifier.  
Your task: read the user's message and conversation history, then output **ONLY** a "vectorstore" or "simulated_generation".

Decision rule (mutually exclusive):
• Output "vectorstore" if the user is seeking factual information that exists in hospital documents. The vector store ONLY contains:
    * **Clinic & Specialty Information** – Doctors, clinic types, days of the week availability, and working hours.
    * **Consultation & Surgery Prices** – Standard fees for various services.
    * **Insurance Details** – List of accepted insurance companies and application procedures.

• Otherwise output "simulated_generation" for tasks or open-ended conversation. Examples:
    * **booking**
    * **rescheduling**
    * **cancelling**
    * **result notifications**
    * **ambulance or complaint requests**
    * **medication/appointment reminders**
    * **pre-procedure instructions**
    * **or any follow-up requiring confirmation or multi-turn flow**
    * **follow-up questions to previous responses**

### Context Considerations ###
- If the conversation history shows the user is in the middle of a booking/scheduling flow, prefer "simulated_generation"
- If asking for specific details after receiving general information, prefer "vectorstore" for factual lookup
- Consider the flow: factual questions → vectorstore, action requests → simulated_generation

### Examples ###
1. Q: "How much is a knee replacement surgery?"  
   → "vectorstore"

2. Q: "Can you book me with Dr. Ibrahim next Monday morning?"  
   → "simulated_generation"

3. Q: "Which insurance companies do you accept?"  
   → "vectorstore"

4. Q: "I need an ambulance at 5 AM tomorrow"  
   → "simulated_generation"

5. Previous: "We have cardiology on Mon, Wed, Fri" | Current: "Can you book me with the cardiologist?"
   → "simulated_generation"

### Now classify the next user message considering the conversation context. REMEMBER: Output JSON only – no prose. ###
"""


route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "Previous conversation:\n{conversation_history}\n\nCurrent question: {question}"),
    ]
)

question_router = route_prompt | structured_llm_router
