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
• Output "vectorstore" **only when the user is requesting factual information that is explicitly documented within hospital records**. The vector store contains structured data in the following categories:
    1. **Clinic & Specialty Information**
        * Details on available clinics and specialties
        * Information about doctors, including their availability by day of the week and working hours
    2. **Consultation & Surgery Prices**
        * Standard fees for available consultations and surgical procedures
    3. **Insurance Details**
        * List of accepted insurance providers
        * Procedures for applying or using insurance
    4. **Lab & Radiology Information**
        * Available laboratory and radiology tests
        * Descriptions and details about each test
    5. **Department Information**
        * Comprehensive list of hospital departments
        * Relevant details about each department


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
