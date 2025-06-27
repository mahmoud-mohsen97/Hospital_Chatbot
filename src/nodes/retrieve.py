from typing import Any, Dict

from src.state import GraphState
from src.ingestion import retriever


def retrieve(state: GraphState) -> Dict[str, Any]:
    print("---RETRIEVE---")
    question = state["question"]

    documents = retriever.invoke(question)
    
    return {"documents": documents, "question": question}
