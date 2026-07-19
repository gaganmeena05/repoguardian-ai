import argparse
import sys

from config import settings
from github_client import GitHubClient
from rag import RepositoryRAG
from reviewer import PullRequestReviewer


def parse_args():
    parser = argparse.ArgumentParser(
        prog="RepoGuardian AI",
        description="AI-powered Pull Request Reviewer",
    )

    parser.add_argument(
        "--pr",
        required=True,
        type=int,
        help="Pull Request Number",
    )

    parser.add_argument(
        "--repo-path",
        default=settings.repository_path,
        help="Local repository path",
    )

    parser.add_argument(
        "--index",
        action="store_true",
        help="Rebuild repository index before reviewing",
    )

    parser.add_argument(
        "--comment",
        action="store_true",
        help="Post review back to GitHub",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    print("=" * 60)
    print("RepoGuardian AI")
    print("=" * 60)

    github = GitHubClient()

    print(f"Repository : {github.get_repository_name()}")
    print(f"PR Number  : {args.pr}")

    rag = RepositoryRAG(args.repo_path)

    if args.index:
        print("\nBuilding repository index...")
        rag.rebuild()
        print("Repository indexed successfully.\n")
    else:
        rag.get_index()

    reviewer = PullRequestReviewer(args.repo_path)

    if args.comment:
        print("Reviewing PR and posting comment...\n")

        reviewer.review_and_comment(args.pr)

        print("\nReview posted successfully.")

    else:
        print("Reviewing PR...\n")

        review = reviewer.review(args.pr)

        print(review)

    print("\nDone.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)