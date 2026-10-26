from app.schemas.prompt import Prompt
from app.schemas.search_result import SearchResult


class PromptBuilder:
    """Builds grounded prompts from retrieved knowledge chunks."""

    def build(
        self,
        query: str,
        results: list[SearchResult],
    ) -> Prompt:
        context_parts = []

        for index, result in enumerate(results, start=1):
            context_parts.append(
                f"[Source {index}: {result.metadata.file_name}]\n{result.content}"
            )

        context = "\n\n".join(context_parts)

        system_prompt = (
            "You are an engineering knowledge assistant. "
            "Answer the user's question using only the provided context. "
            "Treat the context as the source of truth. "
            "Do not invent facts, procedures, requirements, or technical details. "
            "For process or procedure questions, identify and explain all "
            "relevant steps explicitly supported by the context, in a logical "
            "order. Do not skip important steps merely to shorten the answer. "
            "Use numbered lists for multi-step procedures and concise bullets "
            "for supporting details. "
            "Combine information from multiple sources only when relevant, "
            "and do not introduce unrelated details. "
            "If the context provides only part of an answer, explain the "
            "supported part and clearly state what is not specified. "
            "If the answer cannot be found in the context, say so."
        )

        user_prompt = (
            f"Retrieved context:\n{context}\n\n"
            f"Question:\n{query}\n\n"
            "Provide a clear, accurate answer grounded in the retrieved context."
        )

        return Prompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )
