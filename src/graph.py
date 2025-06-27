from dotenv import load_dotenv
from langgraph.graph import END, StateGraph

from src.chains.answer_grader import answer_grader
from src.chains.hallucination_grader import hallucination_grader
from src.chains.router import RouteQuery, question_router
from src.nodes import generate, grade_documents, retrieve, simulated_generate
from src.state import GraphState

load_dotenv()

RETRIEVE = "retrieve"
GRADE_DOCUMENTS = "grade_documents"
GENERATE = "generate"
SIMULATED_GENERATE = "simulated_generate"


def decide_to_generate(state):
    print("---ASSESS GRADED DOCUMENTS---")

    if state["simulated_generation"]:
        print(
            "---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, USING SIMULATED GENERATION---"
        )
        return SIMULATED_GENERATE
    else:
        print("---DECISION: GENERATE---")
        return GENERATE


def grade_generation_grounded_in_documents_and_question(state: GraphState) -> str:
    print("---CHECK HALLUCINATIONS---")
    question = state["question"]
    documents = state["documents"]
    generation = state["generation"]
    retry_count = state.get("generation_retry_count", 0)
    max_retries = state.get("max_generation_retries", 3)  # Default max retries: 3

    score = hallucination_grader.invoke(
        {"documents": documents, "generation": generation}
    )

    if hallucination_grade := score.binary_score:
        print("---DECISION: GENERATION IS GROUNDED IN DOCUMENTS---")
        print("---GRADE GENERATION vs QUESTION---")
        score = answer_grader.invoke({"question": question, "generation": generation})
        if answer_grade := score.binary_score:
            print("---DECISION: GENERATION ADDRESSES QUESTION---")
            return "useful"
        else:
            print("---DECISION: GENERATION DOES NOT ADDRESS QUESTION---")
            return "not useful"
    else:
        if retry_count >= max_retries:
            print(f"---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, BUT MAX RETRIES ({max_retries}) REACHED---")
            print("---FALLING BACK TO SIMULATED GENERATION---")
            return "not useful"  # This will trigger simulated generation
        else:
            print(f"---DECISION: GENERATION IS NOT GROUNDED IN DOCUMENTS, RE-TRY ({retry_count + 1}/{max_retries})---")
            return "not supported"


def route_question(state: GraphState) -> str:
    print("\n\n---ROUTE QUESTION---")
    question = state["question"]
    conversation_history = state.get("conversation_history", [])
    
    # Format conversation history for the router
    formatted_history = ""
    if conversation_history:
        for msg in conversation_history[-6:]:  # Last 6 messages for context
            role = msg.get("role", "")
            content = msg.get("content", "")
            if role == "user":
                formatted_history += f"User: {content}\n"
            elif role == "assistant":
                formatted_history += f"Assistant: {content}\n"
    else:
        formatted_history = "No previous conversation."
    
    source: RouteQuery = question_router.invoke({
        "question": question,
        "conversation_history": formatted_history
    })
    
    if source.datasource == "simulated_generation":
        print("---ROUTE QUESTION TO SIMULATED GENERATION---")
        return SIMULATED_GENERATE
    elif source.datasource == "vectorstore":
        print("---ROUTE QUESTION TO RAG---")
        return RETRIEVE


workflow = StateGraph(GraphState)

workflow.add_node(RETRIEVE, retrieve)
workflow.add_node(GRADE_DOCUMENTS, grade_documents)
workflow.add_node(GENERATE, generate)
workflow.add_node(SIMULATED_GENERATE, simulated_generate)

workflow.set_conditional_entry_point(
    route_question,
    {
        SIMULATED_GENERATE: SIMULATED_GENERATE,
        RETRIEVE: RETRIEVE,
    },
)
workflow.add_edge(RETRIEVE, GRADE_DOCUMENTS)
workflow.add_conditional_edges(
    GRADE_DOCUMENTS,
    decide_to_generate,
    {
        SIMULATED_GENERATE: SIMULATED_GENERATE,
        GENERATE: GENERATE,
    },
)

workflow.add_conditional_edges(
    GENERATE,
    grade_generation_grounded_in_documents_and_question,
    {
        "not supported": GENERATE,
        "useful": END,
        "not useful": SIMULATED_GENERATE,
    },
)
workflow.add_edge(SIMULATED_GENERATE, END)
workflow.add_edge(GENERATE, END)

app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")
