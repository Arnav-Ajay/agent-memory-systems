# planner/planner.py
from decision.decide import decide_retrieval
from planner.plan_schema import Plan, PlanStep

class Planner:
    def generate_plan(self, question: str, *, k: int = 4, wm=None, memory_signal=None) -> Plan:
        decision = decide_retrieval(question)

        force_retrieval = bool(memory_signal and memory_signal.get("force_retrieval"))

        if force_retrieval:
            if wm is not None:
                wm.thoughts.append("Planner forcing retrieval due to retrieval policy")

            step = PlanStep(
                step_id=1,
                action="retrieve",
                args={"question": question, "k": k},
                rationale="forced by retrieval policy based on episodic history",
            )

            return Plan(objective=question, steps=[step])

        if wm is not None:
            wm.thoughts.append(
                f"Planner deciding retrieval for goal: {question}"
            )

        if decision.requires_external_evidence:
            step = PlanStep(
                step_id=1,
                action="retrieve",
                args={"question": question, "k": k},
                rationale=decision.decision_rationale,
            )
        else:
            step = PlanStep(
                step_id=1,
                action="noop",
                args={},
                rationale=decision.decision_rationale,
            )

        return Plan(
            objective=question,
            steps=[step],
        )
