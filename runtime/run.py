# runtime/run.py
from planner.planner import Planner
from executor.executor import Executor
from response.generate import Generator
from utils.logging_utils import write_trace
from dataclasses import asdict


class Runtime:
    def _serialize_plan(self, plan):
        return asdict(plan)

    def run(self, question: str, *, k: int = 4):

        planner = Planner()
        plan = planner.generate_plan(question, k=k)

        executor = Executor()
        execution_trace = executor.execute(plan)
        # NOTE: If multiple retrieve steps exist, the last one wins by design.

        retrieved_context = ""
        for step in execution_trace:
            if step["action"] != "retrieve":
                continue

            tool_result = step.get("tool_result", {})
            all_chunks = tool_result.get("chunks", [])

            retrieved_context = "\n\n".join(
                f"[{c.get('chunk_id', '?')}] {c.get('text', '')}"
                for c in all_chunks[:k]
            )


        answer = Generator().generate_answer(question, retrieved_context)

        write_trace({
            "question": question,
            "plan": self._serialize_plan(plan),
            "execution": execution_trace,
            "final_answer": answer,
        })

        return answer
