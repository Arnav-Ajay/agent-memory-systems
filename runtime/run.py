# runtime/run.py
from planner import Planner
from executor import Executor
from response.generate import Generator
from utils.logging_utils import write_trace
from memory import MemoryRouter

from dataclasses import asdict


class Runtime:
    def _serialize_plan(self, plan):
        return asdict(plan)

    def run(self, question: str, *, k: int = 4):
        mem = MemoryRouter()
        
        # First step: prove persistence exists and is auditable.
        last_user_question = mem.read_semantic("last_user_question")
        recent_episodes = mem.read_recent_episodic(n=10)

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

        mem.write_semantic("last_user_question", question)
        mem.write_semantic("last_answer_preview", answer[:200])

        mem.write_episodic({
            "ts_utc": __import__("time").time(),
            "question": question,
            "plan_actions": [s.action for s in plan.steps],
            "used_retrieval": any(s["action"] == "retrieve" for s in execution_trace),
            "last_user_question_before_run": last_user_question,
            "recent_episode_count_before_run": len(recent_episodes),
        })

        write_trace({
            "question": question,
            "plan": self._serialize_plan(plan),
            "execution": execution_trace,
            "final_answer": answer,
            "memory": {
                "semantic_reads": {"last_user_question": last_user_question},
                "episodic_reads": {"recent_episodes_n": len(recent_episodes)},
                "semantic_writes": ["last_user_question", "last_answer_preview"],
                "episodic_write": "append",
            },
        })

        return answer
