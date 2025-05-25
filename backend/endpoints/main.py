"""
Host the FastAPI app.
"""

from datetime import datetime
from http import HTTPStatus
from typing import List, Optional
from uuid import UUID

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from pydantic import BaseModel, Field

from backend.services.changelog_service import ChangelogService

load_dotenv()


# Pydantic Models
class ChangelogBase(BaseModel):
    title: str
    version: str
    tags: Optional[List[str]] = []
    model: Optional[str] = "gpt-4"
    temperature: Optional[float] = 0.7


class ChangelogCreate(ChangelogBase):
    source: str = Field(..., description="Source of changelog: 'git' or 'manual'")
    repo_url: Optional[str] = None
    commit_range: Optional[str] = None
    content: Optional[str] = None


class ChangelogResponse(ChangelogBase):
    id: UUID
    user_id: UUID
    repository_id: Optional[UUID]
    content: str
    is_public: bool = False
    created_at: datetime
    updated_at: datetime


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


# Update the original app declaration with lifespan
app = FastAPI(
    title="ChangeLog-AI API",
    description="API for generating and managing AI-powered changelogs",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Changelog endpoints
@app.get("/api/changelogs", response_model=List[ChangelogResponse])
async def list_changelogs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    version: Optional[str] = None,
    tags: Optional[List[str]] = None,
):
    """List all changelogs with optional filtering and pagination."""
    # TODO: Implement database query with filters
    return []


@app.post(
    "/api/changelogs", response_model=ChangelogResponse, status_code=HTTPStatus.CREATED
)
async def create_changelog(changelog: ChangelogCreate):
    """Create a new changelog entry."""
    try:
        # TODO: Get user_id from auth context
        user_id = UUID("00000000-0000-0000-0000-000000000000")  # Placeholder
        
        result = await ChangelogService.create_changelog(
            source=changelog.source,
            repo_url=changelog.repo_url,
            commit_range=changelog.commit_range,
            content=changelog.content,
            version=changelog.version,
            title=changelog.title,
            tags=changelog.tags,
            model=changelog.model,
            temperature=changelog.temperature,
            user_id=user_id,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/changelogs/{changelog_id}", response_model=ChangelogResponse)
async def get_changelog(changelog_id: UUID):
    """Get a specific changelog by ID."""
    try:
        result = await ChangelogService.get_changelog(changelog_id)
        if not result:
            raise HTTPException(status_code=404, detail="Changelog not found")
        return result
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Database integration not implemented")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/changelogs/{changelog_id}", response_model=ChangelogResponse)
async def update_changelog(changelog_id: UUID, changelog: ChangelogCreate):
    """Update a specific changelog."""
    try:
        updates = changelog.dict(exclude_unset=True)
        result = await ChangelogService.update_changelog(changelog_id, updates)
        if not result:
            raise HTTPException(status_code=404, detail="Changelog not found")
        return result
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Database integration not implemented")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/changelogs/{changelog_id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_changelog(changelog_id: UUID):
    """Delete a specific changelog."""
    try:
        await ChangelogService.delete_changelog(changelog_id)
    except NotImplementedError:
        raise HTTPException(status_code=501, detail="Database integration not implemented")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Auth endpoints
@app.post("/api/auth/login", response_model=UserResponse)
async def login():
    """Login with GitHub OAuth."""
    # TODO: Implement GitHub OAuth login
    raise HTTPException(status_code=501, detail="Not implemented")


@app.post(
    "/api/auth/register", response_model=UserResponse, status_code=HTTPStatus.CREATED
)
async def register(user: UserCreate):
    """Register a new user."""
    # TODO: Implement user registration
    raise HTTPException(status_code=501, detail="Not implemented")


@app.get("/api/auth/me", response_model=UserResponse)
async def get_current_user():
    """Get current user information."""
    # TODO: Implement current user retrieval
    raise HTTPException(status_code=501, detail="Not implemented")
