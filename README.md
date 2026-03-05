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

## Relationship to Other Repositories

This repository builds directly on:

* [`agent-tool-retriever`](https://github.com/Arnav-Ajay/agent-tool-retriever) — retrieval as an explicit decision
* [`agent-planner-executor`](https://github.com/Arnav-Ajay/agent-planner-executor) — planning vs execution separation

---

## Architectural Transition (What Comes Next)

At this point, the agent system has:

* explicit control over **whether to retrieve**
* explicit separation of **planning vs execution**
* explicit mechanisms for **state persistence and forgetting**

What remains unresolved is **output itself**.

Specifically:

> Given retrieved evidence and persisted state,
> **should the agent generate an answer at all?**

That question is **intentionally not addressed here**.

It is the focus of the next system layer:

* **[`llm-generation-control`](https://github.com/Arnav-Ajay/llm-generation-control)** —
  where generation is treated as a **policy-governed decision**, not a default behavior.

Only after memory exists *and* is governable does it make sense to ask whether speaking is justified.

---

### Final note

This repository proves **memory can exist without being helpful**.

The next repository asks a harder question:

> Even if memory and evidence exist — should the system respond?

---