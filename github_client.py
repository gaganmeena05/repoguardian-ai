from typing import List, Dict

from github import Github
from github.PullRequest import PullRequest

from config import settings


class GitHubClient:
    def __init__(self):
        self.github = Github(settings.github_token)

        self.repo = self.github.get_repo(
            f"{settings.github_owner}/{settings.github_repo}"
        )

    # --------------------------------------------------
    # Pull Requests
    # --------------------------------------------------

    def get_pull_request(self, pr_number: int) -> PullRequest:
        return self.repo.get_pull(pr_number)

    def get_pr_title(self, pr_number: int) -> str:
        return self.get_pull_request(pr_number).title

    def get_pr_description(self, pr_number: int) -> str:
        body = self.get_pull_request(pr_number).body
        return body or ""

    # --------------------------------------------------
    # Files
    # --------------------------------------------------

    def get_changed_files(self, pr_number: int) -> List[Dict]:
        pr = self.get_pull_request(pr_number)

        files = []

        for file in pr.get_files():
            files.append(
                {
                    "filename": file.filename,
                    "status": file.status,
                    "additions": file.additions,
                    "deletions": file.deletions,
                    "changes": file.changes,
                    "patch": file.patch or "",
                }
            )

        return files

    def get_file_content(self, path: str) -> str:
        try:
            content = self.repo.get_contents(path)

            return content.decoded_content.decode("utf-8")

        except Exception:
            return ""

    # --------------------------------------------------
    # Repository
    # --------------------------------------------------

    def list_repository_files(self, path: str = "") -> List[str]:
        files = []

        contents = self.repo.get_contents(path)

        while contents:

            content = contents.pop(0)

            if content.type == "dir":
                contents.extend(self.repo.get_contents(content.path))
            else:
                files.append(content.path)

        return files

    # --------------------------------------------------
    # Reviews
    # --------------------------------------------------

    def post_review_comment(
        self,
        pr_number: int,
        comment: str,
    ):
        pr = self.get_pull_request(pr_number)

        pr.create_issue_comment(comment)

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    def get_repository_name(self):
        return self.repo.full_name

    def get_default_branch(self):
        return self.repo.default_branch