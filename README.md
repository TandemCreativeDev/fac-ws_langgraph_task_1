# LangGraph Code Review Workshop

A hands-on tutorial for building a multi-agent code review system using LangGraph.

## Workshop Overview

This workshop teaches you to build a LangGraph application that:

1. Generates code based on requirements
2. Reviews the generated code
3. Refactors the code based on review feedback

## Prerequisites

- Python 3.8+
- OpenAI API key
- Basic understanding of Python and AI concepts

## Installation

```bash
pip install langchain-openai langgraph
```

## Step-by-Step Tutorial

### Step 1: Import Dependencies

**Checkpoint: Basic imports**

Add the required imports to `main.py`:

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END, START
from typing import TypedDict
```

**What you should have:** A file with the basic LangGraph and LangChain imports.

---

### Step 2: Define the Shared State

**Checkpoint: State definition**

Create a TypedDict to define the state that will be shared across all agents:

```python
class CodeReviewState(TypedDict):
    input: str
    code: str
    review: str
    refactored_code: str
```

**What you should have:** A state class that tracks input requirements, generated code, review feedback, and refactored code.

---

### Step 3: Setup the LLM

**Checkpoint: LLM configuration**

Initialize the OpenAI model:

```python
llm = ChatOpenAI(model="gpt-4", api_key="YOUR API KEY HERE")
```

**Note:** Replace `"YOUR API KEY HERE"` with your actual OpenAI API key.

**What you should have:** An LLM instance ready to use in your agents.

---

### Step 4: Create Agent Prompts

**Checkpoint: Prompt templates**

Define prompts for each agent role:

```python
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
```

**What you should have:** Three distinct prompt templates for coder, reviewer, and refactorer roles.

---

### Step 5: Implement Agent Functions

**Checkpoint: Agent implementations**

Create the three agent functions:

```python
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
```

**What you should have:** Three functions that each take the state, call the LLM with appropriate prompts, and update the state.

---

### Step 6: Build the Graph

**Checkpoint: Graph construction**

Create the LangGraph workflow:

```python
builder = StateGraph(CodeReviewState)
builder.add_node("coder", coder_agent)
builder.add_node("reviewer", reviewer_agent)
builder.add_node("refactorer", refactorer_agent)

builder.add_edge(START, "coder")
builder.add_edge("coder", "reviewer")
builder.add_edge("reviewer", "refactorer")
builder.add_edge("refactorer", END)

graph = builder.compile()
```

**What you should have:** A compiled graph that defines the workflow: START → coder → reviewer → refactorer → END.

---

### Step 7: Test the System

**Checkpoint: Working application**

Add the example usage:

```python
task = "Write a function that checks if a string is a palindrome"
initial_state = {"input": task}
final_state = graph.invoke(initial_state)

print("======================================")
print("INITIAL CODE")
print("======================================")
print("\nInitial Code:\n", final_state["code"])

print("\n======================================")
print("CODE REVIEW")
print("======================================")
print("\nReview Feedback:\n", final_state["review"])

print("\n======================================")
print("REFACTORED CODE")
print("======================================")
print("\nRefactored Code:\n", final_state["refactored_code"])
```

**What you should have:** A complete working application that generates, reviews, and refactors code.

---

## Running the Application

```bash
python main.py
```

## Common Issues & Debugging

### Issue: ImportError

**Solution:** Ensure all packages are installed: `pip install langchain-openai langgraph`

### Issue: API Key Error

**Solution:** Set your OpenAI API key in the code or as an environment variable

### Issue: Graph doesn't execute

**Solution:** Check that all edges are properly connected and the graph is compiled

### Issue: Agent functions not working

**Solution:** Verify each agent function returns the updated state

## Workshop Checkpoints Summary

- ✅ **Step 1:** Imports added
- ✅ **Step 2:** State class defined
- ✅ **Step 3:** LLM configured
- ✅ **Step 4:** Prompts created
- ✅ **Step 5:** Agent functions implemented
- ✅ **Step 6:** Graph built and compiled
- ✅ **Step 7:** Application tested

## Next Steps

- Experiment with different prompts
- Add error handling
- Implement conditional logic in the graph
- Add human-in-the-loop interactions
- Extend with additional agents (e.g., tester, documentation writer)

## Support

If you're stuck at any step, reference the step number and checkpoint description for targeted help.
