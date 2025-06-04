# LangGraph Code Review Workshop

<p align="center">
  <img src="https://github.com/user-attachments/assets/885d196b-e9b8-47ee-84de-d4533c42f3b7" width="300">
</p>

A hands-on tutorial for building a multi-agent code review system using LangGraph.

## Workshop Overview

This workshop teaches you to build a LangGraph application that:

1. Generates code based on requirements
2. Reviews the generated code
3. Refactors the code based on review feedback

## Prerequisites

- Python 3.12+
- OpenAI API key
- Basic understanding of Python and AI concepts

## Environment Manager Installation (Skip this step if you already use Conda or Venv)

**Checkpoint: Install environment manager**

- Mac/Linux:
  - Install Conda (or can use venv if preferred)
- Windows:
  - Skip this step. You can just use global `pip` package manager.

**What you should have**: An environment manager

## Project Setup

- Create a new directory called `langgraph-task-1` with a file called `main.py` inside it
- Conda users (Mac/Linux), use `conda create -n langgraph-task-1`, then `conda activate langgraph-task-1` inside the directory
  > - Venv users, setup an environment for this project as you normally would

**What you should have**: An environment to work in

## Package Installation

Inside your project directory, run:

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
```

**What you should have:** A file with the basic LangGraph and LangChain imports.

---

### Step 2: Setup the LLM

**Checkpoint: LLM configuration**

Initialize the OpenAI model:

```python
llm = ChatOpenAI(model="gpt-4", api_key="YOUR API KEY HERE")
```

**Note:** Replace `"YOUR API KEY HERE"` with your actual OpenAI API key.

**What you should have:** An LLM instance ready to use in your agents.

---

### Step 3: Create Agent Prompts

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

### Step 4: Implement Agent Functions

**Checkpoint: Agent implementations**

Create the three agent functions:

```python
def coder_agent(state):
    response = llm.invoke(coder_prompt.format_messages(input=state["input"]))
    state["code"] = response.content
    return state

def reviewer_agent(state):
    response = llm.invoke(reviewer_prompt.format_messages(code=state["code"]))
    state["review"] = response.content
    return state

def refactorer_agent(state):
    response = llm.invoke(refactorer_prompt.format_messages(
        code=state["code"], review=state["review"]))
    state["refactored_code"] = response.content
    return state
```

**What you should have:** Three functions that each take the state, call the LLM with appropriate prompts, and update the state.

---

### Step 5: Build the Graph

**Checkpoint: Graph construction**

Create the LangGraph workflow:

```python
builder = StateGraph(dict)
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

### Step 6: Test the System

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

## Next Steps

- Experiment with different prompts
- Add error handling
- Implement conditional logic in the graph
- Add human-in-the-loop interactions
- Extend with additional agents (e.g., tester, documentation writer)

## Support

If you're stuck at any step, reference the step number and checkpoint description for targeted help.
