"""
LLM interface using Groq — free API, fast inference, open-source models.
Get a free key at https://console.groq.com
"""

import logging
from typing import List, Dict
from groq import Groq
from config.settings import settings

logger = logging.getLogger(__name__)

# Best free models on Groq (as of 2025)
MODELS = {
    "fast":    "llama-3.1-8b-instant",    # very fast, good quality
    "quality": "llama-3.3-70b-versatile", # slower but smarter
    "default": "llama-3.1-8b-instant",
}

SYSTEM_PROMPT = """You are a helpful medical knowledge assistant.
Answer questions using ONLY the provided context documents.
If the answer isn't in the context, say "I don't have enough information in the knowledge base to answer that."
Always cite which document your answer comes from.
Keep answers clear and concise."""


class LLMClient:
    """
    Groq-backed LLM client for RAG answer generation.
    Free tier: ~14,400 requests/day, ~500k tokens/min.
    """

    def __init__(self, model: str = MODELS["default"]):
        if not settings.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY not set.\n"
                "1. Get a free key at https://console.groq.com\n"
                "2. Add  GROQ_API_KEY=your_key  to your .env file"
            )
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = model
        logger.info(f"LLM ready — model: {model} via Groq (free)")

    def generate(
        self,
        query: str,
        context_chunks: List[Dict],
        chat_history: List[Dict] | None = None,
    ) -> str:
        """
        Generate an answer grounded in the retrieved context chunks.

        Args:
            query:          The user's question.
            context_chunks: Retrieved chunks from the vector store.
            chat_history:   Previous turns [{role, content}, ...] for multi-turn memory.

        Returns:
            Generated answer string.
        """
        context = self._format_context(context_chunks)

        messages: List[Dict] = [{"role": "system", "content": SYSTEM_PROMPT}]

        # Inject previous turns (last 6 messages = 3 full Q&A rounds) so the
        # model can answer follow-up questions without losing context.
        if chat_history:
            for msg in chat_history[-6:]:
                messages.append({"role": msg["role"], "content": msg["content"]})

        messages.append({
            "role": "user",
            "content": f"Context documents:\n\n{context}\n\nQuestion: {query}",
        })

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,       # low temp = more factual for medical content
                max_tokens=1024,
            )
            answer = response.choices[0].message.content
            logger.info(f"Generated answer ({len(answer)} chars)")
            return answer
        except Exception as e:
            logger.error(f"Groq generation failed: {e}")
            return f"Error generating answer: {e}"

    def _format_context(self, chunks: List[Dict]) -> str:
        parts = []
        for i, chunk in enumerate(chunks, 1):
            parts.append(
                f"[Document {i} — {chunk.get('source', 'unknown')}]\n"
                f"{chunk.get('content', '')}"
            )
        return "\n\n".join(parts)
