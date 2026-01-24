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

### Inputs

* Task sequences spanning multiple runs
* Optional static documents (unchanged from earlier system iterations)

### Outputs

* Agent plans and actions
* Explicit memory reads
* Explicit memory writes
* Artifacts showing when and why state was accessed

### Invariant

> If state is persisted or retrieved, that interaction must be explicitly logged and auditable.

---

## Memory Is a First-Class Mechanism (Not a Capability)

Memory is treated as a **constrained subsystem**, not an emergent behavior.

This repository makes **no claim** that memory is beneficial.
It only establishes the **conditions under which memory exists at all**.

Memory is defined by:

* explicit interfaces
* explicit routing
* explicit persistence rules

---

## Memory Taxonomy (Implementation Scope)

This repository implements **three distinct memory mechanisms**, each with different guarantees.

---

### 1. Working Context (Session-Local)

**Stores**

* Current goal
* Planner thoughts
* Execution flags

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

* Past questions
* Plan actions taken
* Whether retrieval occurred
* Execution metadata

**Properties**

* Time-indexed
* Append-only
* Subject to decay rules
* Read explicitly, never implicitly

**Purpose**

* Preserve a trace of prior events **without asserting relevance or correctness**

---

### 3. Semantic Memory (Persisted, Curated)

**Stores**

* Abstracted state (e.g. last question, answer preview)

**Properties**

* Written only through gating rules
* Overwritten deliberately
* Retrieved only via explicit read

**Purpose**

* Represent long-lived state **without claiming long-term correctness**

---

## Architectural Overview

```
User Task
   ↓
Runtime
   ├── Working State (execution-local)
   │     ├── Planner
   │     └── Executor
   │
   └── Memory Router (persisted state)
         ├── Episodic Store
         └── Semantic Store
```

**Non-negotiable rule**

Planner and Executor cannot access persisted memory directly.
All cross-session state interaction occurs exclusively through the Memory Router.

---

## Policy Layer (Explicitly Controllable)

This repository introduces **policy-governed memory behavior**.

Policies implemented:

* **Retrieval policy** — may force retrieval based on episodic history
* **Write filter** — gates what is allowed into semantic memory
* **Forgetting policy** — decays episodic memory over time

### Policy Mode Toggle

All policies can be **enabled or disabled at runtime**:

```python
runtime.run(question, enforce_policies=True)
runtime.run(question, enforce_policies=False)
```

This enables **direct comparison** between:

* Memory present but unconstrained
* Memory present and policy-constrained

No other system components change.

---

## Observed Behaviors (From Artifacts)

Across repeated runs, the following behaviors are **directly observable**:

1. **State persistence exists**

   * Prior questions and answers appear in subsequent runs
   * Persistence is explicit and logged

2. **Policy enforcement changes behavior**

   * With policies enabled, retrieval can be forced even for conceptual questions
   * With policies disabled, planner decisions rely solely on parametric judgment

3. **Memory does not imply usefulness**

   * Persisted state does not guarantee relevance
   * Forced retrieval can introduce unrelated context

These are **observations**, not claims of improvement.

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
│   │   └── events.jsonl
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
* Forced retrieval polluting reasoning
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
* Policy enforcement measurably alters agent behavior

---

## What This Repository Does NOT Establish

* That memory improves correctness
* That memory improves planning quality
* That memory improves agent performance
* That more memory is beneficial

Those questions are explicitly deferred.

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
* Explicit policy-on vs policy-off behavioral differences

No scoring, optimization, or quality claims are made.

---

## Relationship to Other Repositories

This repository builds directly on:

* [`agent-tool-retriever`](https://github.com/Arnav-Ajay/agent-tool-retriever) — tool-using decisions
* [`agent-planner-executor`](https://github.com/Arnav-Ajay/agent-planner-executor) — reasoning separation

It explicitly defers to later repositories for:

* Failure-first synthesis
* Observability UX
* Cross-system conclusions

---

### Final note (implicit but true)

This repository proves **memory can exist without being helpful**.

That is the point.

---

## 🔚 Architectural Closure

This repository completes the agent mechanics layer mentioned in [`agent-systems-core`](https://github.com/Arnav-Ajay/agent-systems-core).

At this point, the system has:

* explicit control over whether to retrieve
* explicit separation of planning vs execution
* explicit mechanisms for state persistence and forgetting

No additional agent capability can be meaningfully evaluated without failure analysis.

The remaining work is not to add features, but to understand:

* how these systems fail under pressure
* where observability breaks down
* which abstractions mislead builders

Those questions are addressed in subsequent repositories focused on failure modes, tracing, and system-level synthesis.