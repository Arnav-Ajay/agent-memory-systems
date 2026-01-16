# planner/planner.py
from decision.decide import decide_retrieval
from planner.plan_schema import Plan, PlanStep


class Planner:
    def generate_plan(self, question: str, *, k: int = 4) -> Plan:
        decision = decide_retrieval(question)

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
