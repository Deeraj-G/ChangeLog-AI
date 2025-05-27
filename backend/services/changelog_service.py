"""
Service layer for changelog generation and management.
"""

import os
import subprocess
from datetime import datetime
from typing import Dict, List
from uuid import UUID

import requests
from fastapi import HTTPException, status
from loguru import logger
import aiohttp

from .openai_client import OpenAIClientManager


class ChangelogService:
    def __init__(self, db_session):  # Add database session
        self.github_api_url = "https://api.github.com"
        self.db = db_session

    @staticmethod
    async def _validate_repository(repo_url: str) -> bool:
        """Validate if the repository exists and is accessible."""
        try:
            # Try to get repository info without cloning
            response = requests.head(repo_url)
            if response.status_code == 404:
                raise ValueError("Repository not found")
            if response.status_code == 403:
                raise ValueError("Repository is private or access is restricted")
            return True
        except requests.RequestException as e:
            raise ValueError(f"Error accessing repository: {str(e)}")


    @staticmethod
    async def _get_git_commits(repo_url: str, commit_range: int) -> List[Dict]:
        """Fetch commits from a git repository."""
        try:
            # Clone the repository if it doesn't exist
            repo_name = repo_url.split("/")[-1].replace(".git", "")
            if not os.path.exists(f"/tmp/{repo_name}"):
                subprocess.run(
                    ["git", "clone", repo_url, f"/tmp/{repo_name}"],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

            # Change to the repository directory
            os.chdir(f"/tmp/{repo_name}")

            # Format: commit hash, author, date, and commit message
            format_string = "%H%n%an%n%ad%n%s%n%b%n----------"
            result = subprocess.run(
                ["git", "log", f"-{commit_range}", f"--pretty=format:{format_string}"],
                check=True,
                stdout=subprocess.PIPE,
                text=True,
            )
            commits_raw = result.stdout.split("----------")[:-1]

            # Parse the raw commit data
            commits = []
            for commit_raw in commits_raw:
                lines = commit_raw.strip().split("\n")
                if len(lines) >= 4:
                    commit = {
                        "hash": lines[0],
                        "author": lines[1],
                        "date": lines[2],
                        "subject": lines[3],
                        "body": "\n".join(lines[4:]) if len(lines) > 4 else "",
                    }
                    commits.append(commit)

            return commits
        except subprocess.CalledProcessError as e:
            logger.error(f"Error fetching git commits: {e}")
            raise RuntimeError(f"Failed to fetch git commits: {str(e)}")

    @staticmethod
    def _preprocess_commits(commits: List[Dict], max_commits: int = 50) -> List[Dict]:
        """Preprocess and filter commits for better changelog generation."""
        if len(commits) > max_commits:
            # Score commits by message length and keywords
            scored_commits = []
            for commit in commits:
                score = len(commit["subject"] + commit["body"])

                # Boost score for important keywords
                keywords = [
                    "add",
                    "added",
                    "adding",
                    "refactor",
                    "refactored",
                    "refactoring",
                    "refactored",
                    "feature",
                    "featured",
                    "improve",
                    "improved",
                    "fixed",
                    "implement",
                    "implemented",
                    "update",
                    "updated",
                    "updates",
                    "support",
                    "supported",
                    "refactor",
                    "refactored",
                    "merge",
                    "merged",
                    "merging",
                ]
                lowered = (commit["subject"] + commit["body"]).lower()

                for keyword in keywords:
                    if keyword in lowered:
                        score += 10

                # Reduce score for trivial changes
                trivial = [
                    "patch",
                    "minor",
                    "typo",
                    "typos",
                    "whitespace",
                    "comment",
                    "comments",
                    "commented",
                    "formatting",
                    "format",
                    "spacing",
                    "lint"
                    "linting",
                ]
                for word in trivial:
                    if word in lowered:
                        score -= 15

                scored_commits.append((score, commit))

            # Sort by score and take top max_commits
            scored_commits.sort(reverse=True)
            return [commit for _, commit in scored_commits[:max_commits]]

        return commits

    @staticmethod
    async def _generate_changelog(
        commits: List[Dict], model: str = "gpt-4o-mini", temperature: float = 0.5
    ) -> str:
        """Generate a changelog using the OpenAI API."""
        commit_details = "\n\n".join(
            [
                f"Commit: {commit['hash']}\n"
                f"Author: {commit['author']}\n"
                f"Date: {commit['date']}\n"
                f"Subject: {commit['subject']}\n"
                f"Body: {commit['body']}"
                for commit in commits
            ]
        )

        system_prompt = "You are an expert analyst specializing in analyzing software changes and creating clear, user-focused changelogs. You excel at identifying patterns across commits, grouping related changes, and communicating technical updates in business-friendly language. Your changelogs are well-structured, emphasize user impact, and maintain professional tone."
        prompt = f"""
        ### INSTRUCTIONS ###
        Create a professional changelog based on the git commits below. Your task is to analyze these commits and produce a well-organized, user-friendly changelog that follows the style of leading tech companies like Stripe and Vercel.

        ### KEY POINTS ###
        - Include month/year heading and descriptive section headings
        - Translate technical details into user benefits
        - Use clear categories and consistent formatting
        - Consolidate similar/small across multiple commits; skip trivial changes
        - Some commits may be minor (typo fixes, small adjustments) and should be aggregated

        ### RESPONSE FORMAT ###
        - Clean Markdown without emojis
        - ## for category headings (New Features, Improvements, Bug Fixes, etc.)
        - Bullet points with **bold** feature names
        - Brief descriptions focused on user value
        - Include step-by-step guides for major features
        - IMPORTANT: Provide ONLY raw markdown with no commentary or code blocks.
        - Start directly with "# Month Year" heading.
        
        ### COMMIT DETAILS ###
        {commit_details}
        """
        try:
            # Get the client instance from the manager
            client = OpenAIClientManager.get_client()
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=4096,
                temperature=temperature,
            )
            result = response.choices[0].message
            if result.content:
                return result.content
            else:
                raise RuntimeError("Unexpected API response format")

        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling OpenAI API: {e}")
            if hasattr(e, "response") and e.response:
                logger.error(f"Response status code: {e.response.status_code}")
                logger.error(f"Response body: {e.response.text}")
            raise RuntimeError(f"Failed to generate changelog: {str(e)}")

    async def _get_user_github_token(self, user_id: UUID) -> str:
        """Get the user's GitHub token from our database."""
        user = await self.db.get_user(user_id)
        if not user or not user.github_access_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="GitHub authentication required"
            )
        return user.github_access_token

    async def _get_commits_from_api(self, repo_url: str, commit_range: int, user_id: UUID) -> List[Dict]:
        """Fetch the last N commits using GitHub API."""
        try:
            # Convert repo URL to API format
            # e.g., https://github.com/username/repo.git -> username/repo
            repo_path = "/".join(repo_url.split("/")[-2:]).replace(".git", "")
            
            # Get the user's GitHub token from our database
            github_token = await self._get_user_github_token(user_id)
            
            async with aiohttp.ClientSession() as session:
                headers = {"Authorization": f"token {github_token}"}
                # Use the commits endpoint with per_page parameter
                url = f"{self.github_api_url}/repos/{repo_path}/commits?per_page={commit_range}"
                
                async with session.get(url, headers=headers) as response:
                    if response.status == 401:
                        raise HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="GitHub authentication expired"
                        )
                    if response.status == 404:
                        raise ValueError("Repository not found")
                    if response.status == 403:
                        raise ValueError("Repository access denied")
                    if response.status != 200:
                        raise ValueError(f"GitHub API error: {response.status}")
                    
                    commits = await response.json()
                    return commits

        except aiohttp.ClientError as e:
            raise ValueError(f"Error accessing GitHub API: {str(e)}")


    async def create_changelog(
        self,
        repo_url: str,
        commit_range: int,
        user_id: UUID,
    ) -> Dict:
        """Create a new changelog entry using GitHub API."""
        try:
            # # Validate the repository
            await ChangelogService._validate_repository(repo_url)
            # # Get git commits
            commits = await ChangelogService._get_git_commits(repo_url, commit_range)
            # commits = await self._get_commits_from_api(repo_url, commit_range, user_id)
            # Preprocess commits
            commits = ChangelogService._preprocess_commits(
                commits, max_commits=commit_range
            )
            # Generate changelog
            content = await ChangelogService._generate_changelog(commits)
            
            # TODO: Store in database
            changelog = {
                "id": UUID("00000000-0000-0000-0000-000000000000"),  # Placeholder
                "user_id": user_id,
                "content": content,
                "repo_url": repo_url,
                "commit_range": commit_range,
                "created_at": datetime.now(),
                "updated_at": datetime.now(),
            }
            return changelog

        except ValueError as e:
            # Handle validation errors
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
            logger.error(f"Error creating changelog: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create changelog: {str(e)}"
            )

    @staticmethod
    async def get_changelog(changelog_id: UUID) -> Dict:
        """Get a specific changelog by ID."""
        # TODO: Implement database retrieval
        raise NotImplementedError("Database integration not implemented")

    @staticmethod
    async def update_changelog(changelog_id: UUID, updates: Dict) -> Dict:
        """Update a specific changelog."""
        # TODO: Implement database update
        raise NotImplementedError("Database integration not implemented")

    @staticmethod
    async def delete_changelog(changelog_id: UUID) -> None:
        """Delete a specific changelog."""
        # TODO: Implement database deletion
        raise NotImplementedError("Database integration not implemented")
