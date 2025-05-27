from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ChangelogBase(BaseModel):
    repo_url: str = Field(..., description="URL of the git repository")
    commit_range: int = Field(
        ..., description="Number of commits to include in the changelog"
    )


class ChangelogResponse(ChangelogBase):
    content: str
    # id: UUID
    # user_id: UUID
    # created_at: datetime
    # updated_at: datetime


class UserBase(BaseModel):
    github_username: str


class UserCreate(UserBase):
    github_id: str
    github_access_token: str


class UserResponse(UserBase):
    id: UUID
    api_key: str
    created_at: datetime
    updated_at: datetime
