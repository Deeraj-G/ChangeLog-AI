"""
Host the FastAPI app.
"""
from typing import List, Optional
from uuid import UUID

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware

from backend.models.models import (
    ChangelogBase,
    ChangelogResponse,
    UserCreate,
    UserResponse,
)
from backend.services.changelog_service import ChangelogService


load_dotenv()


app = FastAPI(
    title="ChangeLog-AI API",
    description="API for generating and managing AI-powered changelogs",
    version="1.0.0",
)


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
    "/api/changelogs", response_model=ChangelogResponse, status_code=status.HTTP_201_CREATED
)
async def create_changelog(changelog: ChangelogBase):
    """Create a new changelog entry from git history."""
    try:
        # TODO: Get user_id from auth context
        user_id = UUID("00000000-0000-0000-0000-000000000000")  # Placeholder

        result = await ChangelogService.create_changelog(
            repo_url=changelog.repo_url,
            commit_range=changelog.commit_range,
            user_id=user_id,
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid request")
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/api/changelogs/{changelog_id}", response_model=ChangelogResponse)
async def get_changelog(changelog_id: UUID):
    """Get a specific changelog by ID."""
    try:
        result = await ChangelogService.get_changelog(changelog_id)
        if not result:
            raise HTTPException(status_code=404, detail="Changelog not found")
        return result
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail="Database integration not implemented") from exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.put("/api/changelogs/{changelog_id}", response_model=ChangelogResponse)
async def update_changelog(changelog_id: UUID, changelog: ChangelogBase):
    """Update a specific changelog."""
    try:
        updates = changelog.dict(exclude_unset=True)
        result = await ChangelogService.update_changelog(changelog_id, updates)
        if not result:
            raise HTTPException(status_code=404, detail="Changelog not found")
        return result
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail="Database integration not implemented") from exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.delete("/api/changelogs/{changelog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_changelog(changelog_id: UUID):
    """Delete a specific changelog."""
    try:
        await ChangelogService.delete_changelog(changelog_id)
    except NotImplementedError as exc:
        raise HTTPException(status_code=501, detail="Database integration not implemented") from exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


# Auth endpoints
@app.post("/api/auth/login", response_model=UserResponse)
async def login():
    """Login with GitHub OAuth."""
    # TODO: Implement GitHub OAuth login
    raise HTTPException(status_code=501, detail="Not implemented")


@app.post(
    "/api/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
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
