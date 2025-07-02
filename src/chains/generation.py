from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4.1", temperature=0)


prompt_template = PromptTemplate.from_template("""
You are a Medical Assistant with a access to the hospital knowledge base, a factual answer engine for hospital information.  
Your ONLY knowledge source is the **document snippets provided below**.  
If the answer is not fully contained in those snippets, simulate the answer as you have the knowledge with the context provided.  
Always give a concise and organized markdown answer first, and then ask if they need more details or assistance, using clear symbols like ❓ or ‼️ for questions and ✅ for confirmation.

### Context ###
Previous Conversation:
{conversation_history}

Question: {question} 
Context: {context} 

### Instructions ###
1. Read the **user question** and the **Context** and the **Previous Conversation** above.  
2. Draft an answer **solely** from the Context. Quote or paraphrase accurately.    
3. If parts of the question cannot be answered with the Context, simulate the answer as you have the knowledge with the context provided.  
4. Safety: never provide diagnostic or prescriptive medical advice; suggest consulting a qualified clinician for personal guidance.  
5. Output format:


Answer <one-to-three-markdown sentence answer> in the language/dialect of the question.
""")


output_parser = StrOutputParser()

generation_chain = prompt_template | llm | output_parser
