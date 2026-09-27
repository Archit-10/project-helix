from app.schemas.prompt import Prompt
from app.schemas.search_result import SearchResult


class PromptBuilder:
    def build(
        self,
        query: str,
        results: list[SearchResult],
    ) -> Prompt:
        context_parts = []

        for index, result in enumerate(results, start=1):
            context_parts.append(f"[Source {index}]\n{result.content}")

        context = "\n\n".join(context_parts)

        system_prompt = (
            "You are an engineering knowledge assistant. "
            "Answer questions using only the provided context. "
            "If the answer cannot be found in the context, "
            "say that the information is not available. "
            "Do not invent or assume information."
        )

        user_prompt = f"Context:\n{context}\n\nQuestion:\n{query}"

        return Prompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )
