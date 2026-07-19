from typing import Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

from config import settings


class LLM:
    def __init__(self):
        self.model = ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=settings.temperature,
        )

    def invoke(self, prompt: str) -> str:
        """
        Simple text prompt.
        """

        response = self.model.invoke(prompt)

        return response.content.strip()

    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        """
        Chat interface with system + user messages.
        """

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]

        response = self.model.invoke(messages)

        return response.content.strip()

    def review(
        self,
        system_prompt: str,
        review_prompt: str,
    ) -> str:
        """
        Wrapper used by reviewer.py
        """

        return self.chat(
            system_prompt,
            review_prompt,
        )


llm = LLM()


if __name__ == "__main__":
    print("=" * 60)
    print("RepoGuardian AI")
    print("=" * 60)

    answer = llm.invoke(
        "Explain what a pull request review is in one sentence."
    )

    print(answer)