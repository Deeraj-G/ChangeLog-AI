# ChangeLog-AI Project Plan

## Project Overview
Transform the existing CLI-based AI changelog generator into a full-stack application with:
1. A developer-facing web interface for generating changelogs
2. A public-facing website to display the changelogs
3. Reuse of existing AI-powered changelog generation logic

## Technical Stack
- **Backend**: Python (FastAPI) - Reusing existing Python code
- **Frontend**: React + TypeScript
- **Database**: SQLite (for MVP) / PostgreSQL (if needed)
- **AI**: OpenAI (GPT-4) - For changelog generation
- **Deployment**: Docker + GitHub Actions

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

## Phase 2: Frontend Development (Week 1-2)
1. **Developer Interface**
   - Create React application
   - Key features:
     - Repository connection form
     - Changelog generation interface
     - Preview and edit capabilities
     - Version management
     - API key management

2. **Public Changelog Website**
   - Clean, minimal design inspired by Stripe/Twilio
   - Features:
     - Chronological changelog display
     - Version filtering
     - Search functionality
     - RSS feed support

3. **UI/UX Design**
   - Modern, developer-focused design
   - Responsive layout
   - Dark/light mode
   - Clear typography and spacing

## Phase 3: Integration & Testing (Week 2)
1. **Integration**
   - Connect frontend with backend APIs
   - Implement error handling
   - Add loading states and feedback

2. **Testing**
   - Unit tests for backend
   - Integration tests
   - Frontend component testing
   - End-to-end testing

3. **Documentation**
   - API documentation
   - Setup instructions
   - Usage guide
   - Contributing guidelines

## Phase 4: Deployment & Polish (Week 3)
1. **Deployment**
   - Docker containerization
   - CI/CD pipeline setup
   - Production environment configuration

2. **Final Polish**
   - Performance optimization
   - SEO optimization
   - Analytics integration
   - Error monitoring

## Technical Decisions & Rationale
1. **FastAPI over Flask**
   - Modern, async support
   - Better performance
   - Automatic API documentation
   - Type hints support

2. **React + TypeScript**
   - Type safety
   - Better developer experience
   - Component reusability
   - Strong ecosystem

3. **SQLite for MVP**
   - Simple setup
   - No additional infrastructure needed
   - Easy to migrate to PostgreSQL later

4. **Docker**
   - Consistent development environment
   - Easy deployment
   - Scalability

## Success Criteria
1. **Developer Experience**
   - Easy setup process
   - Clear documentation
   - Intuitive interface
   - Fast changelog generation

2. **End User Experience**
   - Clean, readable changelog display
   - Easy navigation
   - Mobile responsive
   - Fast loading times

3. **Technical Quality**
   - Well-tested code
   - Secure implementation
   - Scalable architecture
   - Maintainable codebase

## Timeline
- Week 1: Backend development and initial frontend setup
- Week 2: Frontend development and integration
- Week 3: Testing, deployment, and polish

## Next Steps
1. Set up project structure
2. Initialize backend with FastAPI
3. Create basic frontend scaffold
4. Begin porting CLI logic to API endpoints
