# `agent-memory-systems`

## Why This Repository Exists

Most “agent memory” implementations conflate **state** with **capability**.

They equate memory with:

* chat history
* vector databases
* unbounded accumulation of prior context

These approaches *appear* to work in short demos but obscure a more basic question:

> **What does it even mean for an agent to be stateful across sessions?**

This repository exists to isolate and study **memory as a system mechanism**, not as a performance enhancement.

This is **not** a chatbot memory demo.
It is a **controlled implementation of agent state across executions**.

---

## The Question

> **Can an agent carry forward state across sessions in a controlled, inspectable way?**

This repository investigates **only**:

* how state is written
* how state is retrieved
* how state is constrained
* how state can be forgotten

It does **not** attempt to prove that memory improves correctness, quality, or intelligence.

---

## What This Repository Explicitly Does NOT Do

This system deliberately avoids:

* Claims of improved answer quality
* Claims of improved agent performance
* Human-like or persona-based memory
* Unlimited conversation replay
* Production-grade vector database optimization
* Automated grading of “memory usefulness”

If you are looking for proof that memory *helps*, that is **out of scope for this repo**.

---

## System Contract

**Inputs**

* Task sequences spanning multiple runs
* Optional static documents (unchanged from prior weeks)

**Outputs**

* Agent actions
* Explicit memory writes
* Explicit memory reads
* Artifacts showing when state was accessed

**Invariant**

> If state is persisted or retrieved, that interaction must be explicitly logged.

---

## Memory Is a First-Class Mechanism (Not a Capability)

Memory is treated as a **constrained subsystem** with:

* explicit interfaces
* explicit routing
* explicit persistence rules

This repository makes **no claim** that memory is beneficial.
It only establishes the **conditions under which memory exists at all**.

---

## Memory Taxonomy (Implementation Scope)

This repository implements **three distinct memory mechanisms**.

### 1. Working Context (Session-Local)

**Stores**

* Current plan
* Temporary assumptions
* Scratchpad state

**Properties**

* Exists only during execution
* Never persisted
* Fully discarded at session end

**Purpose**

* Enable intra-session reasoning
* Prevent accidental cross-session leakage

---

### 2. Episodic Memory (Persisted, Event-Level)

**Stores**

* Past tasks
* Tool outcomes
* Execution events

**Properties**

* Time-indexed
* Append-only
* Subject to decay rules
* Not queried automatically

**Purpose**

* Preserve a trace of prior events without asserting correctness or usefulness

---

### 3. Semantic Memory (Persisted, Curated)

**Stores**

* Abstracted facts
* Stable constraints
* Explicitly approved invariants

**Properties**

* Written only through gating rules
* Deduplicated
* Retrieved only via explicit request

**Purpose**

* Represent long-lived state **without claiming long-term correctness**

---

## Architectural Overview

```
User Task
   ↓
Planner
   ↓
Executor
   ↓
Memory Router
   ├── Working Context (ephemeral)
   ├── Episodic Store (persisted, decaying)
   └── Semantic Store (persisted, gated)
```

**Non-negotiable rule**

Planner and Executor **cannot access memory directly**.
All state interaction occurs through a routing layer.

---

## File Structure

```
agent-memory-systems/
│
├── README.md
├── requirements.txt
├── main.py
│
├── runtime/
│   └── run.py                # orchestrates agent + memory lifecycle
│
├── planner/
│   ├── planner.py
│   └── plan_schema.py
│
├── executor/
│   └── executor.py
│
├── decision/
│   ├── decide.py
│   └── schema.py
│
├── memory/
│   ├── episodic.py           # persisted, decaying events
│   ├── semantic.py           # persisted, gated abstractions
│   ├── working.py            # in-memory session context
│   ├── router.py             # explicit read/write control
│   └── schemas.py
│
├── policies/
│   ├── forgetting.py         # decay mechanics
│   ├── write_filter.py       # persistence gating
│   └── retrieval_policy.py
│
├── tools/
│   ├── ingest.py
│   ├── retrieve_tool.py
│   └── reranker_core.py
│
├── logs/
│   └── traces.jsonl          # observability only
│
├── artifacts/
│   ├── memory/
│   │   ├── episodic.jsonl
│   │   ├── semantic.json
│   │   └── snapshots/
│   ├── plans/
│   └── runs/
│
└── data/
    └── input_pdfs/
```

---

## Observability vs State (Hard Boundary)

* **Logs** explain *what happened*
* **Artifacts** define *what persists*

Logs are **never** treated as memory.
Memory is **never** reconstructed from logs.

---

## Expected Failure Modes (Declared, Not Resolved)

This system is expected to exhibit failures such as:

* State accumulation without relevance
* Persisted assumptions becoming stale
* Memory retrieval interfering with planning
* Forgetting removing still-useful context

These failures are **not mitigated here**.
They are **surfaced for future analysis**.

---

## What This Repository Establishes

This repository establishes that:

* Agent state can persist across sessions
* That persistence can be constrained and inspected
* Memory access can be routed and logged
* Forgetting can be implemented as a mechanism

It does **not** establish that memory improves outcomes.

---

## What This Repository Does NOT Establish

* That memory improves correctness
* That memory improves planning quality
* That memory improves agent performance
* That more memory is beneficial

Those questions are deferred.

---

## How to Run (Minimal)

```bash
pip install -r requirements.txt
python main.py
```

All state interactions are materialized in `artifacts/`.

---

## Evaluation Artifacts

This repository produces:

* Memory write records
* Memory read traces
* Session-to-session state carryover
* Concrete evidence of persisted vs discarded state

No scoring or optimization metrics are claimed.

---

## Relationship to Other Repositories

This repository builds directly on:

* [`agent-tool-retriever`](https://github.com/Arnav-Ajay/agent-tool-retriever) — tool-using decisions
* [`agent-planner-executor`](https://github.com/Arnav-Ajay/agent-planner-executor) — reasoning separation

It explicitly defers to later repos:

* Failure-first analysis
* Observability UX
* Cross-system synthesis

---