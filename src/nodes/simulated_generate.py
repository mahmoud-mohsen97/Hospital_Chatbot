from typing import Any, Dict

from src.chains.simulated_generation import simulated_generation_chain
from src.state import GraphState


def simulated_generate(state: GraphState) -> Dict[str, Any]:
    """
    Generate answer using simulated hospital knowledge and capabilities.
    
    This node replaces web search by acting as if it has access to comprehensive
    hospital information systems and can perform various hospital-related actions.
    """
    print("---SIMULATED KNOWLEDGE GENERATION---")
    question = state["question"]
    documents = state.get("documents", [])
    conversation_history = state.get("conversation_history", [])
    
    # Use available context if any, otherwise rely on simulated knowledge
    context = documents if documents else "No specific context available - using comprehensive hospital knowledge base"
    
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
    
    generation = simulated_generation_chain.invoke({
        "context": context, 
        "question": question,
        "conversation_history": formatted_history
    })
    
    
    # Ensure documents is always a list for state consistency
    if not documents:
        documents = []
    
    return {
        "documents": documents, 
        "question": question, 
        "generation": generation
    } 