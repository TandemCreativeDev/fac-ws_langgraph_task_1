from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END, START
from typing import TypedDict

# Shared state across the graph


class CodeReviewState(TypedDict):
    input: str
    code: str
    review: str
    refactored_code: str


# LLM setup
llm = ChatOpenAI(model="gpt-4", api_key="YOUR API KEY HERE")

# Prompts
coder_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Coder. Write Python code based on the given requirements."),
    ("human", "{input}")
])

reviewer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Reviewer. Review the given code and suggest improvements."),
    ("human", "{code}")
])

refactorer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a Refactorer. Implement the suggested improvements in the code."),
    ("human", "Code:\n{code}\n\nReview:\n{review}")
])

# Agent functions


def coder_agent(state: CodeReviewState) -> CodeReviewState:
    response = llm.invoke(coder_prompt.format_messages(input=state["input"]))
    state["code"] = response.content
    return state


def reviewer_agent(state: CodeReviewState) -> CodeReviewState:
    response = llm.invoke(reviewer_prompt.format_messages(code=state["code"]))
    state["review"] = response.content
    return state


def refactorer_agent(state: CodeReviewState) -> CodeReviewState:
    response = llm.invoke(refactorer_prompt.format_messages(
        code=state["code"], review=state["review"]))
    state["refactored_code"] = response.content
    return state


# Build the graph
builder = StateGraph(CodeReviewState)
builder.add_node("coder", coder_agent)
builder.add_node("reviewer", reviewer_agent)
builder.add_node("refactorer", refactorer_agent)

builder.add_edge(START, "coder")
builder.add_edge("coder", "reviewer")
builder.add_edge("reviewer", "refactorer")
builder.add_edge("refactorer", END)

graph = builder.compile()

# Example usage
task = "Write a function that checks if a string is a palindrome"
initial_state = {"input": task}
final_state = graph.invoke(initial_state)

print("Initial Code:\n", final_state["code"])
print("\nReview Feedback:\n", final_state["review"])
print("\nRefactored Code:\n", final_state["refactored_code"])
