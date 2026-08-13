"""Context manager for sliding window turn history pruning and conversation compression."""

from typing import List, Dict, Any
from app.core.logging import get_logger

logger = get_logger(__name__)


class ContextManager:
    """Manages LLM context window size, pruning trivial turns, and generating turn summaries."""

    DEFAULT_MAX_TURNS = 10

    @classmethod
    def prune_trivial_turns(cls, history: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Filter out trivial filler turns or duplicate empty speech detections."""
        pruned = []
        for turn in history:
            content = turn.get("content", "").strip()
            # Ignore empty or filler-only turns
            if not content or content in ["...", "um", "uh", "cough"]:
                continue
            pruned.append(turn)
        return pruned

    @classmethod
    def get_compressed_history(
        cls,
        history: List[Dict[str, str]],
        max_turns: int = DEFAULT_MAX_TURNS,
    ) -> List[Dict[str, str]]:
        """Apply sliding window compression keeping recent `max_turns` and summarizing older turns."""
        cleaned = cls.prune_trivial_turns(history)

        if len(cleaned) <= max_turns:
            return cleaned

        # Split into archived turns and recent window
        archived_turns = cleaned[:-max_turns]
        recent_turns = cleaned[-max_turns:]

        # Create quick summary of archived turns
        archived_topics = []
        for t in archived_turns:
            role = "Customer" if t.get("role") == "user" else "Agent"
            snippet = t.get("content", "")[:50]
            archived_topics.append(f"{role}: {snippet}")

        summary_text = (
            f"[Prior Conversation Summary: Caller discussed "
            + "; ".join(archived_topics[:4])
            + f" across {len(archived_turns)} earlier turns.]"
        )

        logger.info(
            "Compressed conversation history",
            total_turns=len(cleaned),
            archived_count=len(archived_turns),
            recent_count=len(recent_turns),
        )

        return [{"role": "system", "content": summary_text}] + recent_turns


context_manager = ContextManager()
