## Technical Stack
- **Backend**: Python (FastAPI) - Reusing existing Python code
- **Database**: SQLite (for MVP) / PostgreSQL (if needed)
- **AI**: OpenAI (gpt-4o-mini) - For changelog generation

## Phase 1: Backend Development (Week 1)
1. **API Development**
   - Create FastAPI application structure
   - Port existing CLI logic into API endpoints
   - RESTful endpoints structure:
     ```
     /api/changelogs
     ├── GET    /api/changelogs          # List all changelogs (with filtering & pagination)
     ├── POST   /api/changelogs          # Create new changelog (git generation or manual)
     ├── GET    /api/changelogs/{id}     # Get specific changelog
     ├── PUT    /api/changelogs/{id}     # Update specific changelog
     └── DELETE /api/changelogs/{id}     # Delete specific changelog
     ```
   - Additional endpoints:
     ```
     /api/auth
     ├── POST   /api/auth/login          # User login
     ├── POST   /api/auth/register       # User registration
     └── GET    /api/auth/me             # Get current user info
     ```
   - Request/Response models:
     ```python
     # Changelog creation (POST /api/changelogs)
     {
         "source": "git" | "manual",
         "repo_url": str,        # if source is "git"
         "commit_range": str,    # if source is "git"
         "version": str,
         "content": str,         # if source is "manual"
         "title": str,
         "tags": List[str],      # optional
         "model": str,           # optional, defaults to "gpt-4"
         "temperature": float    # optional, defaults to 0.7
     }
     ```
   - Features:
     - Pagination for list endpoint
     - Filtering by version, date, tags
     - Sorting options
     - Rate limiting
     - Request validation
     - Error handling

2. **Database Integration**
   - Design schema for storing changelogs
   - Tables needed:
     ```
     users
     ├── id (PK, UUID)
     ├── github_id (unique)      # GitHub user ID
     ├── github_username        # GitHub username
     ├── github_access_token    # OAuth token for GitHub API
     ├── api_key (unique)       # For programmatic access
     ├── created_at
     └── updated_at

     repositories
     ├── id (PK, UUID)`
     ├── user_id (FK -> users.id)
     ├── github_repo_id        # GitHub repository ID
     ├── name
     ├── full_name            # e.g., "username/repo"
     ├── last_sync
     ├── created_at
     └── updated_at

     changelogs
     ├── id (PK, UUID)
     ├── user_id (FK -> users.id)
     ├── repository_id (FK -> repositories.id, nullable)
     ├── title
     ├── content
     ├── version
     ├── tags (JSON array)
     ├── is_public (boolean)
     ├── created_at
     └── updated_at
     ```

   - Authentication Flow:
     - User authenticates via GitHub OAuth
     - We store their GitHub access token
     - Use the token to:
       1. Verify user identity
       2. Access repository data
       3. Generate changelogs
     - API key is optional for programmatic access

3. **Security & Authentication**
   - Implement GitHub OAuth authentication
     - Secure token storage and refresh flow
     - Proper scopes for repository access
     - Token encryption at rest
   - Add rate limiting
     - Per-user rate limits for API calls
     - Per-repository rate limits for changelog generation
     - IP-based rate limiting for public endpoints
   - Secure storage of sensitive data
     - Encrypt GitHub access tokens
     - Secure storage of OpenAI API keys
     - Environment variable management
   - Security headers and CORS
     - Proper CORS configuration for frontend
     - Security headers (HSTS, CSP, etc.)
     - XSS protection
   - Audit logging
     - Track authentication attempts
     - Log changelog generation requests
     - Monitor rate limit hits

4. **AI Integration**
   - OpenAI API Integration
     - Implement GPT-4 for changelog generation
     - Optimize prompts for changelog style
     - Handle API rate limits and costs
     - Implement fallback to GPT-3.5 if needed
   - Prompt Engineering
     - Design system prompts for consistent output
     - Create templates for different changelog styles
     - Implement context management for commit history
   - Cost Management
     - Token usage tracking
     - Cost estimation before generation
     - Usage limits per user