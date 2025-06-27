from typing import Any, Dict

from src.chains.retrieval_grader import retrieval_grader
from src.state import GraphState


def grade_documents(state: GraphState) -> Dict[str, Any]:
    """
    Determines whether the retrieved documents are relevant to the question
    If all documents are not relevant, we will set a flag to run simulated generation

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Filtered out irrelevant documents and updated simulated_generation state
    """

    print("---CHECK DOCUMENT RELEVANCE TO QUESTION---")
    question = state["question"]
    documents = state["documents"]

    filtered_docs = []
    for i, d in enumerate(documents):
        score = retrieval_grader.invoke(
            {"question": question, "document": d.page_content}
        )
        grade = score.binary_score
        
        if grade.lower() == "yes":
            print("---GRADE: DOCUMENT RELEVANT---")
            filtered_docs.append(d)
        else:
            print("---GRADE: DOCUMENT NOT RELEVANT---")
            continue
    
    # Set simulated_generation to True only if ALL documents are not relevant (filtered_docs is empty)
    simulated_generation = len(filtered_docs) == 0
    
    return {"documents": filtered_docs, "question": question, "simulated_generation": simulated_generation}
