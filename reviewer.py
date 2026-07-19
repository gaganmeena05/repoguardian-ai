from github_client import GitHubClient
from rag import RepositoryRAG
from llm import llm
from prompts import (
    SYSTEM_PROMPT,
    PR_REVIEW_PROMPT,
)


class PullRequestReviewer:
    def __init__(self, repository_path: str = "."):
        self.github = GitHubClient()
        self.rag = RepositoryRAG(repository_path)

    def build_context(self, files):
        """
        Build RAG query from changed files.
        """

        filenames = "\n".join(
            file["filename"] for file in files
        )

        query = f"""
The following files were modified:

{filenames}

Provide the most relevant repository context,
related modules, business logic and architecture.
"""

        return self.rag.retrieve(query)

    def build_file_summary(self, files):
        """
        Convert changed files into markdown.
        """

        output = []

        for file in files:

            output.append(
                f"""
File: {file["filename"]}

Status: {file["status"]}

Additions: {file["additions"]}

Deletions: {file["deletions"]}

Patch:

{file["patch"]}
"""
            )

        return "\n\n".join(output)

    def review(self, pr_number: int):

        print(f"Reviewing PR #{pr_number}")

        title = self.github.get_pr_title(pr_number)

        description = self.github.get_pr_description(pr_number)

        files = self.github.get_changed_files(pr_number)

        repository_context = self.build_context(files)

        changed_files = self.build_file_summary(files)

        prompt = PR_REVIEW_PROMPT.format(
            repository=self.github.get_repository_name(),
            title=title,
            description=description,
            context=repository_context,
            files=changed_files,
        )

        review = llm.review(
            SYSTEM_PROMPT,
            prompt,
        )

        return review

    def review_and_comment(
        self,
        pr_number: int,
    ):
        """
        Review PR and post GitHub comment.
        """

        review = self.review(pr_number)

        self.github.post_review_comment(
            pr_number,
            review,
        )

        return review

    def summarize_pr(
        self,
        pr_number: int,
    ):
        """
        Return review without posting.
        """

        return self.review(pr_number)


if __name__ == "__main__":

    reviewer = PullRequestReviewer(".")

    result = reviewer.review(1)

    print(result)