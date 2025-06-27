from typing import List, TypedDict, Optional


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: question
        generation: LLM generation
        simulated_generation: whether to add simulated generation
        documents: list of documents
        conversation_history: previous conversation messages for context
        generation_retry_count: number of times generation has been retried due to hallucinations
        max_generation_retries: maximum allowed retries for generation (default: 3)
    """

    question: str
    generation: str
    simulated_generation: bool
    documents: List[str]
    conversation_history: Optional[List[dict]]
    generation_retry_count: Optional[int]
    max_generation_retries: Optional[int]
