from typing import Any, Dict

from src.chains.generation import generation_chain
from src.state import GraphState


def generate(state: GraphState) -> Dict[str, Any]:
    print("---GENERATE---")
    question = state["question"]
    documents = state["documents"]
    conversation_history = state.get("conversation_history", [])
    retry_count = state.get("generation_retry_count", 0)
    max_retries = state.get("max_generation_retries", 3)
    
    # Format conversation history for the prompt
    formatted_history = ""
    if conversation_history:
        for msg in conversation_history[-6:]:  # Last 6 messages for context
            role = msg.get("role", "")
            content = msg.get("content", "")
            if role == "user":
                formatted_history += f"User: {content}\n"
            elif role == "assistant":
                formatted_history += f"Assistant: {content}\n"
    
    if not formatted_history:
        formatted_history = "No previous conversation."

    generation = generation_chain.invoke({
        "context": documents, 
        "question": question,
        "conversation_history": formatted_history
    })
    
    # Increment retry count for next iteration if this gets retried
    new_retry_count = retry_count + 1
    
    return {
        "documents": documents, 
        "question": question, 
        "generation": generation,
        "generation_retry_count": new_retry_count,
        "max_generation_retries": max_retries
    }
