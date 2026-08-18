# Software Requirements Specification (SRS)
## Dashboardku - Personal Task Management System

**Version:** 1.0
**Date:** August 18, 2026
**Document Status:** Draft
**Tech Stack:** Vanilla HTML + Tailwind CSS

---

## 1. Introduction

### 1.1 Purpose
This document specifies the software requirements for Dashboardku, a browser-based personal task management system with webhook-based deadline notifications. The system is designed to be self-hosted and run locally without external server dependencies.

### 1.2 Scope
Dashboardku provides:
- Task creation, management, and organization
- Webhook-based deadline notifications
- Browser-based UI following Meta's design system
- Local data persistence using localStorage
- Export/import functionality
- Responsive design for mobile, tablet, and desktop

### 1.3 Definitions, Acronyms, and Abbreviations
- **CRUD:** Create, Read, Update, Delete
- **DOM:** Document Object Model
- **PWA:** Progressive Web Application
- **WCAG:** Web Content Accessibility Guidelines
- **XSS:** Cross-Site Scripting
- **CSRF:** Cross-Site Request Forgery
- **CSP:** Content Security Policy

### 1.4 References
- PRD.md: Product Requirements Document
- DESIGN.md: Meta Design System Specification
- Tailwind CSS Documentation
- MDN Web Docs

---

## 2. Overall Description

### 2.1 Product Perspective
Dashboardku is a standalone browser-based application that:
- Runs entirely in the client's browser
- Uses no external APIs or services
- Stores all data locally in browser localStorage
- Can be served using any static file server (e.g., `python3 -m http.server`)
- Functions as a single-page application (SPA)

### 2.2 Product Functions
| Function | Description | Priority |
|----------|-------------|----------|
| Task Management | Create, read, update, delete tasks | Mandatory |
| Project Organization | Group tasks into projects | Mandatory |
| Webhook Notifications | Send deadline alerts via HTTP | Mandatory |
| Dashboard View | Overview of tasks and deadlines | Mandatory |
| Data Persistence | Save to localStorage | Mandatory |
| Export/Import | Backup and restore data | Optional |
| Task Templates | Reusable task patterns | Optional |
| Bulk Operations | Perform actions on multiple tasks | Optional |

### 2.3 User Characteristics
- **Primary Users:** Developers, privacy-conscious individuals, power users
- **Technical Proficiency:** Intermediate to advanced
- **Expected Environment:** Modern web browser, desktop or mobile
- **Usage Pattern:** Daily interaction, periodic webhook monitoring

### 2.4 Constraints
- **Storage:** Browser localStorage limitations (typically 5-10MB)
- **Network:** Webhook delivery depends on user's network connectivity
- **Browser:** Must support modern JavaScript (ES6+), localStorage, and CSS Grid
- **Execution:** Client-side only, no server-side processing
- **Security:** Cannot make HTTP requests to CORS-restricted endpoints without proper configuration

### 2.5 Assumptions and Dependencies
- **Assumptions:**
  - User has modern web browser with localStorage enabled
  - User's browser supports ES6+ JavaScript features
  - User has network connectivity for webhook delivery
  - User understands webhook concepts and can configure endpoints

- **Dependencies:**
  - Tailwind CSS (via CDN for development, build for production)
  - Modern browser with ES6+ support
  - Static file server for development

---

## 3. System Features

### 3.1 Task Management

#### 3.1.1 Functional Requirements

**FR-1.1: Create Task**
- The system SHALL allow users to create tasks with:
  - Title (string, 1-200 characters, required)
  - Description (string, 0-5000 characters, optional)
  - Due Date (datetime, optional)
  - Priority (enum: none, low, medium, high, optional)
  - Status (enum: todo, in_progress, completed, blocked, default: todo)
  - Project ID (UUID, optional)
  - Tags (array of strings, optional)
  - Created At (datetime, auto-generated)
  - Updated At (datetime, auto-generated)
- The system SHALL generate a unique UUID for each task
- The system SHALL validate title length before creation
- The system SHALL save the task to localStorage within 100ms of submission
- The system SHALL display the created task in the task list

**FR-1.2: Read Tasks**
- The system SHALL retrieve all tasks from localStorage on application load
- The system SHALL display tasks in the configured view (list, grid, timeline)
- The system SHALL support filtering tasks by:
  - Status
  - Project
  - Priority
  - Due date range
  - Tags
- The system SHALL support sorting tasks by:
  - Due date (ascending/descending)
  - Priority (high to low)
  - Created date
  - Updated date
- The system SHALL render task list within 2 seconds of loading

**FR-1.3: Update Task**
- The system SHALL allow users to update all task fields except UUID and Created At
- The system SHALL automatically update the Updated At timestamp
- The system SHALL validate all field changes before saving
- The system SHALL save changes to localStorage within 100ms
- The system SHALL provide undo functionality for task deletions (stored in session)
- The system SHALL maintain audit log of status changes

**FR-1.4: Delete Tasks**
- The system SHALL allow users to delete individual tasks
- The system SHALL allow users to bulk delete tasks
- The system SHALL require confirmation for bulk deletion
- The system SHALL remove tasks from localStorage within 100ms
- The system SHALL provide undo functionality for individual task deletions

**FR-1.5: Task Search**
- The system SHALL provide a search input field
- The system SHALL search task titles and descriptions
- The system SHALL highlight matching text in search results
- The system SHALL update search results within 300ms of input

#### 3.1.2 Non-Functional Requirements

**NFR-1.1 Performance**
- Task creation: < 100ms from submission to localStorage save
- Task retrieval: < 500ms for up to 10,000 tasks
- Task update: < 100ms from submission to localStorage save
- Search query: < 300ms response time for 10,000 tasks

**NFR-1.2 Data Integrity**
- All tasks MUST have unique UUIDs
- Task timestamps MUST use ISO 8601 format
- Task data MUST be validated before localStorage write
- Corrupted task data MUST be detected and logged

**NFR-1.3 Usability**
- Task creation form MUST be accessible via keyboard navigation
- Task list MUST support keyboard shortcuts (j/k for navigation, enter to edit)
- Filter controls MUST be visible and accessible on all screen sizes
- Task cards MUST clearly display due dates, priorities, and status

### 3.2 Project Management

#### 3.2.1 Functional Requirements

**FR-2.1: Create Project**
- The system SHALL allow users to create projects with:
  - Name (string, 1-100 characters, required)
  - Description (string, 0-500 characters, optional)
  - Color (hex color, optional)
  - Icon (string, optional)
  - Created At (datetime, auto-generated)
- The system SHALL generate a unique UUID for each project
- The system SHALL validate project name uniqueness
- The system SHALL save projects to a separate localStorage key

**FR-2.2: Organize Tasks into Projects**
- The system SHALL allow users to assign tasks to projects
- The system SHALL allow users to change task project assignment
- The system SHALL display tasks grouped by project
- The system SHALL support filtering tasks by project
- The system SHALL allow unassigned tasks (no project)

**FR-2.3: Delete Projects**
- The system SHALL allow users to delete projects
- The system SHALL prompt users to reassign or delete tasks in deleted projects
- The system SHALL prevent deletion of projects containing tasks without confirmation
- The system SHALL maintain project statistics (completion rate, etc.)

#### 3.2.2 Non-Functional Requirements

**NFR-2.1 Performance**
- Project creation: < 100ms
- Project retrieval: < 200ms
- Project statistics calculation: < 500ms for up to 100 projects

### 3.3 Webhook Notifications

#### 3.3.1 Functional Requirements

**FR-3.1: Webhook Configuration**
- The system SHALL allow users to configure webhooks with:
  - Name (string, 1-100 characters, required)
  - URL (string, valid HTTP/HTTPS URL, required)
  - HTTP Method (enum: GET, POST, PUT, PATCH, default: POST)
  - Headers (array of key-value pairs, optional)
  - Payload Template (JSON string, optional)
  - Enabled (boolean, default: true)
  - Created At (datetime, auto-generated)
- The system SHALL validate webhook URL format
- The system SHALL support placeholder variables in payload templates
- The system SHALL generate unique UUID for each webhook
- The system SHALL save webhooks to localStorage

**FR-3.2: Payload Templating**
- The system SHALL support the following template variables:
  - `{{task_id}}`: Task UUID
  - `{{title}}`: Task title
  - `{{description}}`: Task description
  - `{{due_date}}`: Task due date (ISO 8601)
  - `{{priority}}`: Task priority
  - `{{project}}`: Project name
  - `{{status}}`: Task status
  - `{{notification_type}}`: Trigger type (deadline, overdue, etc.)
  - `{{timestamp}}`: Current timestamp (ISO 8601)
- The system SHALL replace placeholders with actual values
- The system SHALL validate JSON payload format
- The system SHALL provide example payload templates

**FR-3.3: Notification Triggers**
- The system SHALL support the following triggers:
  - At deadline (exact due time)
  - Before deadline (configurable intervals)
  - When task becomes overdue
  - On status change (optional)
  - Daily digest (optional, configurable time)
- The system SHALL allow users to configure triggers per task
- The system SHALL allow users to set default triggers per project
- The system SHALL prevent duplicate notifications for same trigger

**FR-3.4: Notification Delivery**
- The system SHALL send HTTP requests to configured webhook URLs
- The system SHALL use the configured HTTP method
- The system SHALL include custom headers in requests
- The system SHALL send the rendered payload as the request body
- The system SHALL implement retry logic:
  - First retry: immediate
  - Second retry: 5 seconds after first failure
  - Third retry: 15 seconds after second failure
- The system SHALL log all delivery attempts
- The system SHALL display delivery status (success/failure)

**FR-3.5: Notification Scheduling**
- The system SHALL check for due tasks every 60 seconds
- The system SHALL process overdue tasks immediately
- The system SHALL queue notifications to prevent rate-limiting
- The system SHALL rate-limit requests to 1 request/second per endpoint
- The system SHALL persist notification queue in localStorage

**FR-3.6: Webhook Testing**
- The system SHALL provide a "Test Webhook" function
- The system SHALL send a test notification with sample data
- The system SHALL display test results (HTTP status code, response body)
- The system SHALL allow users to test webhooks before saving

#### 3.3.2 Non-Functional Requirements

**NFR-3.1 Performance**
- Webhook delivery: < 5 seconds per request (excluding retry delays)
- Notification check: < 1 second per minute
- Payload rendering: < 100ms

**NFR-3.2 Reliability**
- Webhook delivery success rate: ≥ 95% (excluding network failures)
- Notification scheduling accuracy: ± 60 seconds
- Retry logic MUST handle network failures gracefully
- Failed webhooks MUST be logged with error details

**NFR-3.3 Security**
- Webhook URLs MUST be stored encrypted in localStorage
- Payload templates MUST be validated to prevent injection attacks
- HTTP requests MUST enforce CORS policies
- Custom headers MUST NOT contain authentication tokens in plain text (warning to user)

### 3.4 User Interface

#### 3.4.1 Functional Requirements

**FR-4.1: Dashboard View**
- The system SHALL display a welcome section with user greeting
- The system SHALL display task statistics:
  - Total tasks
  - Tasks due today
  - Overdue tasks
  - Completed this week
- The system SHALL display quick-add task input
- The system SHALL display recently completed tasks
- The system SHALL display upcoming deadlines
- The system SHALL follow Meta design system patterns

**FR-4.2: Task List View**
- The system SHALL display tasks in a list or grid format
- The system SHALL show task title, description preview, due date, priority, status
- The system SHALL provide filter controls
- The system SHALL provide sort controls
- The system SHALL provide search input
- The system SHALL support pagination (50 tasks per page)
- The system SHALL allow inline task editing

**FR-4.3: Project View**
- The system SHALL display project statistics
- The system SHALL display project tasks
- The system SHALL display project completion timeline
- The system SHALL provide bulk action controls
- The system SHALL allow project settings modification

**FR-4.4: Settings View**
- The system SHALL provide webhook configuration interface
- The system SHALL provide data export functionality
- The system SHALL provide data import functionality
- The system SHALL provide application settings:
  - Theme selection (light/dark, if implemented)
  - Default view preference
  - Notification preferences
- The system SHALL display application version

**FR-4.5: Responsive Design**
- The system SHALL adapt layout for mobile (< 768px)
- The system SHALL adapt layout for tablet (768-1023px)
- The system SHALL adapt layout for desktop (≥ 1024px)
- The system SHALL collapse navigation to hamburger menu on mobile
- The system SHALL maintain touch target accessibility (min 44×44px)

#### 3.4.2 Non-Functional Requirements

**NFR-4.1 Accessibility**
- The system SHALL meet WCAG 2.1 AA standards
- The system SHALL support keyboard navigation
- The system SHALL provide ARIA labels for interactive elements
- The system SHALL maintain color contrast ratios (min 4.5:1)
- The system SHALL support screen readers

**NFR-4.2 Performance**
- Initial page load: < 2 seconds
- UI interactions: < 100ms response time
- Animation frame rate: ≥ 60 FPS
- Rendering: < 16ms per frame

**NFR-4.3 Design System Compliance**
- All components MUST follow DESIGN.md specifications
- Colors MUST use specified tokens
- Typography MUST follow hierarchy
- Spacing MUST use 4px/8px grid system
- Border radius MUST follow specified scale
- Components MUST follow defined patterns

### 3.5 Data Management

#### 3.5.1 Functional Requirements

**FR-5.1: Data Storage**
- The system SHALL store all data in localStorage
- The system SHALL use separate keys for:
  - Tasks: `dashboardku_tasks`
  - Projects: `dashboardku_projects`
  - Webhooks: `dashboardku_webhooks`
  - Settings: `dashboardku_settings`
  - Notifications: `dashboardku_notifications`
- The system SHALL implement data compression if storage exceeds 80% capacity
- The system SHALL validate data integrity on load

**FR-5.2: Data Export**
- The system SHALL export all data as JSON
- The system SHALL include all tasks, projects, webhooks, and settings
- The system SHALL format JSON with proper indentation
- The system SHALL provide filename with timestamp: `dashboardku_export_YYYY-MM-DD.json`
- The system SHALL validate JSON before export

**FR-5.3: Data Import**
- The system SHALL accept JSON files exported from Dashboardku
- The system SHALL validate JSON structure and data types
- The system SHALL warn users about data overwriting
- The system SHALL provide import preview
- The system SHALL merge or replace data based on user selection
- The system SHALL create backup before import

**FR-5.4: Data Backup**
- The system SHALL create automatic backups weekly
- The system SHALL maintain maximum 5 automatic backups
- The system SHALL store backups in separate localStorage keys
- The system SHALL allow manual backup creation
- The system SHALL allow backup restoration

**FR-5.5: Data Migration**
- The system SHALL support schema versioning
- The system SHALL migrate old data formats to current format
- The system SHALL log migration operations
- The system SHALL provide migration rollback if errors occur

#### 3.5.2 Non-Functional Requirements

**NFR-5.1 Data Integrity**
- All data writes MUST be atomic
- All data MUST be validated before storage
- Corrupted data MUST be detected and logged
- Data schema version MUST be stored and checked

**NFR-5.2 Storage Management**
- The system SHALL monitor localStorage capacity
- The system SHALL warn users at 80% capacity
- The system SHALL implement data compression at 90% capacity
- The system SHALL provide cleanup recommendations

---

## 4. System Architecture

### 4.1 Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │   Dashboard │  │  Task List  │  │   Settings  │   │
│  │     View    │  │    View     │  │    View     │   │
│  └─────────────┘  └─────────────┘  └─────────────┘   │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                   Application Layer                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │  Task Manager│  │Project Mgr  │  │Webhook Mgr  │   │
│  │  Controller  │  │ Controller   │  │  Controller │   │
│  └─────────────┘  └─────────────┘  └─────────────┘   │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                      Data Layer                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │LocalStorage  │  │  Data Model │  │ Validation  │   │
│  │  Adapter    │  │  Schema      │  │  Service    │   │
│  └─────────────┘  └─────────────┘  └─────────────┘   │
└─────────────────────────────────────────────────────────┘
                           ↓
┌─────────────────────────────────────────────────────────┐
│                   Browser Storage                        │
│              (localStorage / sessionStorage)              │
└─────────────────────────────────────────────────────────┘
```

### 4.2 Technology Stack

#### 4.2.1 Frontend
- **HTML5**: Semantic markup
- **Vanilla JavaScript (ES6+)**: No frameworks or libraries
- **Tailwind CSS**: Utility-first CSS framework
  - Development: CDN version
  - Production: Built CSS file
- **Font**: Optimistic VF (Meta's variable font) with fallbacks

#### 4.2.2 Development Tools
- **Static File Server**: Python's built-in HTTP server
  ```bash
  python3 -m http.server 8080
  ```
- **Browser DevTools**: For debugging and profiling
- **Code Editor**: Any text editor with HTML/CSS/JS support

#### 4.2.3 Browser APIs Used
- **localStorage**: Data persistence
- **sessionStorage**: Temporary data (undo, drafts)
- **Fetch API**: Webhook HTTP requests
- **Request/Response APIs**: Advanced webhook configuration
- **Intersection Observer**: Lazy loading (if needed)
- **Broadcast Channel**: Cross-tab communication (optional)

### 4.3 Data Model

#### 4.3.1 Task Schema
```json
{
  "id": "uuid-v4",
  "title": "string (1-200 chars)",
  "description": "string (0-5000 chars)",
  "due_date": "ISO 8601 datetime",
  "priority": "none|low|medium|high",
  "status": "todo|in_progress|completed|blocked",
  "project_id": "uuid|null",
  "tags": ["string"],
  "webhook_triggers": [
    {
      "type": "deadline|overdue|before_deadline|status_change",
      "offset": "duration (e.g., -1h, -1d)",
      "enabled": true
    }
  ],
  "created_at": "ISO 8601 datetime",
  "updated_at": "ISO 8601 datetime"
}
```

#### 4.3.2 Project Schema
```json
{
  "id": "uuid-v4",
  "name": "string (1-100 chars)",
  "description": "string (0-500 chars)",
  "color": "hex color",
  "icon": "string",
  "default_webhook_triggers": [],
  "created_at": "ISO 8601 datetime"
}
```

#### 4.3.3 Webhook Schema
```json
{
  "id": "uuid-v4",
  "name": "string (1-100 chars)",
  "url": "HTTP/HTTPS URL",
  "method": "GET|POST|PUT|PATCH",
  "headers": [
    {
      "key": "string",
      "value": "string"
    }
  ],
  "payload_template": "JSON string with {{placeholders}}",
  "enabled": true,
  "created_at": "ISO 8601 datetime"
}
```

#### 4.3.4 Notification Schema
```json
{
  "id": "uuid-v4",
  "task_id": "uuid",
  "webhook_id": "uuid",
  "trigger_type": "deadline|overdue|before_deadline|status_change",
  "status": "pending|sent|failed",
  "attempts": 0,
  "last_attempt": "ISO 8601 datetime",
  "error_message": "string|null",
  "created_at": "ISO 8601 datetime"
}
```

### 4.4 Component Architecture

```
src/
├── index.html                 # Main HTML entry point
├── css/
│   ├── main.css              # Main stylesheet (Tailwind + custom)
│   └── components.css        # Component-specific styles
├── js/
│   ├── app.js                # Application initialization
│   ├── controllers/
│   │   ├── taskController.js     # Task CRUD operations
│   │   ├── projectController.js  # Project management
│   │   ├── webhookController.js  # Webhook configuration & delivery
│   │   └── uiController.js        # UI state management
│   ├── models/
│   │   ├── Task.js               # Task data model
│   │   ├── Project.js            # Project data model
│   │   ├── Webhook.js            # Webhook data model
│   │   └── Notification.js       # Notification data model
│   ├── services/
│   │   ├── storageService.js     # localStorage wrapper
│   │   ├── validationService.js  # Data validation
│   │   ├── notificationService.js # Notification scheduling
│   │   └── webhookService.js     # HTTP webhook delivery
│   ├── utils/
│   │   ├── uuid.js               # UUID generation
│   │   ├── dateUtils.js          # Date formatting
│   │   ├── templateEngine.js     # Payload template rendering
│   │   └── constants.js          # App constants
│   └── components/
│       ├── taskList.js           # Task list component
│       ├── taskCard.js           # Task card component
│       ├── projectList.js        # Project list component
│       ├── webhookConfig.js      # Webhook configuration UI
│       └── dashboard.js           # Dashboard view
└── assets/
    ├── fonts/                   # Optimistic VF font files
    └── icons/                   # SVG icons
```

---

## 5. External Interface Requirements

### 5.1 User Interfaces

#### 5.1.1 Dashboard Interface
- **Purpose**: Provide overview of tasks and system status
- **Layout**: Hero section with stats, task list, quick-add input
- **Components**:
  - Welcome hero with personalized greeting
  - Task statistics (4-up icon feature row)
  - Recent tasks list
  - Quick-add task input
  - Upcoming deadlines timeline
- **Design Pattern**: `hero-band-marketing` + `feature-icon-row` + `card-product-feature`

#### 5.1.2 Task List Interface
- **Purpose**: Display and manage tasks
- **Layout**: Filter/sort controls, search, pagination, task cards
- **Components**:
  - Search input (`search-pill`)
  - Filter pill tabs (`button-pill-tab`)
  - Sort dropdown
  - Task cards (`card-product-feature`)
  - Pagination controls
  - Bulk action buttons
- **Design Pattern**: `button-pill-tab` row + `card-product-feature` list

#### 5.1.3 Webhook Configuration Interface
- **Purpose**: Configure webhook endpoints and test delivery
- **Layout**: Webhook list, add/edit form, test controls
- **Components**:
  - Webhook list (`product-thumbnail` cards)
  - Add webhook button (`button-buy-cta`)
  - Configuration form
  - Test webhook button (`button-secondary`)
  - Delivery history (`tech-specs-table`)
- **Design Pattern**: `card-checkout-summary` + `product-thumbnail` + `text-input`

### 5.2 Hardware Interfaces
- **Keyboard**: Full keyboard navigation support
- **Mouse**: Click interactions, drag-and-drop (optional)
- **Touch**: Touch targets ≥ 44×44px, swipe gestures (optional)
- **Screen Reader**: ARIA labels, semantic HTML

### 5.3 Software Interfaces

#### 5.3.1 localStorage Interface
```javascript
// Storage keys
const STORAGE_KEYS = {
  TASKS: 'dashboardku_tasks',
  PROJECTS: 'dashboardku_projects',
  WEBHOOKS: 'dashboardku_webhooks',
  SETTINGS: 'dashboardku_settings',
  NOTIFICATIONS: 'dashboardku_notifications',
  VERSION: 'dashboardku_version'
};
```

#### 5.3.2 Webhook HTTP Interface
```javascript
// Webhook request format
{
  method: 'POST',  // GET, POST, PUT, PATCH
  url: 'https://example.com/webhook',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer token'  // optional
  },
  body: {
    // Rendered payload template
  }
}

// Expected response
{
  status: 200,  // 2xx = success, 4xx/5xx = failure
  // Response body ignored
}
```

### 5.4 Communication Interfaces

#### 5.4.1 Webhook Delivery Protocol
1. **Scheduling**: Background timer checks every 60 seconds
2. **Queue Processing**: Process notifications in FIFO order
3. **Rate Limiting**: Max 1 request/second per endpoint
4. **Retry Logic**: Immediate, +5s, +15s delays
5. **Status Update**: Log success/failure to localStorage

#### 5.4.2 Cross-Tab Communication (Optional)
```javascript
// Broadcast Channel for multi-tab sync
const channel = new BroadcastChannel('dashboardku_sync');
channel.postMessage({ type: 'TASK_UPDATED', data: task });
```

---

## 6. Non-Functional Requirements

### 6.1 Performance Requirements

| Metric | Requirement | Measurement |
|--------|-------------|-------------|
| Initial Page Load | < 2 seconds | Navigation Timing API |
| Time to Interactive | < 3 seconds | Navigation Timing API |
| Task Creation | < 100ms | localStorage write timing |
| Task Retrieval | < 500ms (10k tasks) | localStorage read timing |
| Search Query | < 300ms (10k tasks) | Search execution timing |
| Webhook Delivery | < 5 seconds | Fetch API timing |
| UI Interaction | < 100ms | Event handler timing |
| Animation Frame Rate | ≥ 60 FPS | RequestAnimationFrame |

### 6.2 Security Requirements

#### 6.2.1 Data Protection
- All webhook URLs stored encrypted (Base64 + XOR cipher)
- No sensitive data logged to console
- No data transmitted to external services (except configured webhooks)
- localStorage data accessible only to same-origin pages

#### 6.2.2 Input Validation
- All user inputs validated before storage
- Task titles: 1-200 characters, no HTML tags
- URLs: Valid HTTP/HTTPS format
- JSON payloads: Valid JSON structure
- No XSS vulnerabilities in rendered content

#### 6.2.3 CORS and CSP
- Webhook requests respect browser CORS policies
- Content-Security-Policy header:
  ```
  default-src 'self';
  script-src 'self' 'unsafe-inline';
  style-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com;
  font-src 'self';
  connect-src *;  // Allow webhook requests
  ```
- X-Frame-Options: DENY
- X-Content-Type-Options: nosniff

### 6.3 Reliability Requirements

| Metric | Requirement | Description |
|--------|-------------|-------------|
| Data Persistence | 100% | All saves to localStorage must succeed |
| Webhook Success Rate | ≥ 95% | Excluding network failures |
| Retry Logic | 3 attempts | Immediate, +5s, +15s delays |
| Notification Accuracy | ± 60s | Check interval |
| Zero Data Loss | Required | Validate all writes |

### 6.4 Availability Requirements
- **Uptime**: N/A (client-side only, no server)
- **Recovery**: Auto-recover from localStorage corruption
- **Backup**: Automatic weekly backups
- **Graceful Degradation**: Function without localStorage (read-only mode)

### 6.5 Maintainability Requirements
- **Code Structure**: Modular, component-based
- **Documentation**: Inline comments, function documentation
- **Naming**: Clear, descriptive variable and function names
- **Error Handling**: Comprehensive try-catch blocks
- **Logging**: Error logs to console (development only)

### 6.6 Compatibility Requirements

#### 6.6.1 Browser Support
| Browser | Minimum Version | Notes |
|---------|----------------|-------|
| Chrome | 90+ | Full support |
| Firefox | 88+ | Full support |
| Safari | 14+ | Full support |
| Edge | 90+ | Full support |
| Mobile Safari | 14+ | Full support |
| Chrome Mobile | 90+ | Full support |

#### 6.6.2 Device Support
- **Desktop**: 1024px+ width
- **Tablet**: 768-1023px width
- **Mobile**: < 768px width
- **Touch**: Minimum 44×44px touch targets

### 6.7 Usability Requirements

#### 6.7.1 Accessibility (WCAG 2.1 AA)
- Color contrast: Minimum 4.5:1 for normal text, 3:1 for large text
- Keyboard navigation: All functions accessible via keyboard
- Screen reader: ARIA labels for all interactive elements
- Focus indicators: Visible focus on all interactive elements
- Error identification: Clear error messages and suggestions

#### 6.7.2 User Experience
- Learnability: First-time users can create task within 2 minutes
- Efficiency: Power users can perform common tasks < 5 seconds
- Memorability: Retain users after 7 days (target 60%)
- Errors: Clear error messages with recovery suggestions
- Satisfaction: Intuitive interface following familiar design patterns

---

## 7. Design System Requirements

### 7.1 Color Tokens

All colors MUST reference DESIGN.md tokens:

```css
:root {
  /* Brand & Accent */
  --color-primary: #0064E0;          /* Cobalt */
  --color-primary-deep: #0047B3;    /* Deep Cobalt */
  --color-primary-soft: rgba(0, 100, 224, 0.15);
  --color-fb-blue: #1877F2;
  --color-meta-link: #0081F2;
  --color-oculus-purple: #1D2B5F;

  /* Surface */
  --color-canvas: #FFFFFF;
  --color-surface-soft: #F4F4F4;
  --color-hairline: #DADDE1;
  --color-hairline-soft: #E4E6EB;

  /* Text */
  --color-ink-deep: #0A1317;
  --color-ink: #1C1E21;
  --color-charcoal: #434343;
  --color-slate: #65676B;
  --color-steel: #8A8D91;
  --color-stone: #BCC1C6;

  /* Semantic */
  --color-success: #31A24C;
  --color-attention: #FF8800;
  --color-warning: #FFDC00;
  --color-critical: #DC3545;
  --color-critical-strong: #B02A37;

  /* Buttons */
  --color-ink-button: #0A1317;
  --color-on-ink-button: #FFFFFF;
  --color-on-primary: #FFFFFF;
  --color-disabled-text: #BCC1C6;
}
```

### 7.2 Typography Tokens

All typography MUST reference DESIGN.md tokens:

```css
:root {
  --font-family: 'Optimistic VF', 'Montserrat', 'Helvetica', 'Arial', sans-serif;
  --font-mono: 'SF Mono', 'Monaco', 'Cascadia Code', 'Roboto Mono', monospace;

  /* Font Sizes */
  --text-hero-display: 64px;
  --text-display-lg: 48px;
  --text-heading-lg: 36px;
  --text-heading-md: 28px;
  --text-heading-sm: 24px;
  --text-subtitle-lg: 18px;
  --text-subtitle-md: 18px;
  --text-body-md: 16px;
  --text-body-sm: 14px;
  --text-caption: 12px;
  --text-button: 14px;

  /* Font Weights */
  --font-light: 300;
  --font-regular: 400;
  --font-medium: 500;
  --font-bold: 700;

  /* Line Heights */
  --leading-hero: 1.16;
  --leading-display: 1.17;
  --leading-heading: 1.28;
  --leading-body: 1.50;
  --leading-caption: 1.33;

  /* Letter Spacing */
  --tracking-body: -0.16px;
  --tracking-body-sm: -0.14px;
}
```

### 7.3 Spacing Tokens

All spacing MUST use 4px/8px grid:

```css
:root {
  --spacing-xxs: 4px;
  --spacing-xs: 8px;
  --spacing-sm: 10px;
  --spacing-md: 12px;
  --spacing-base: 16px;
  --spacing-lg: 20px;
  --spacing-xl: 24px;
  --spacing-xxl: 32px;
  --spacing-xxxl: 40px;
  --spacing-section-sm: 48px;
  --spacing-section: 64px;
  --spacing-section-lg: 80px;
  --spacing-hero: 120px;
}
```

### 7.4 Border Radius Tokens

All border radius MUST reference DESIGN.md scale:

```css
:root {
  --rounded-xs: 2px;
  --rounded-sm: 4px;
  --rounded-md: 6px;
  --rounded-lg: 8px;
  --rounded-xl: 16px;
  --rounded-xxl: 24px;
  --rounded-xxxl: 32px;
  --rounded-feature: 40px;
  --rounded-full: 100px;
  --rounded-circle: 50%;
}
```

### 7.5 Component Patterns

All components MUST follow DESIGN.md patterns:

```javascript
// Button Components
const BUTTON_STYLES = {
  primary: {
    background: 'var(--color-ink-button)',
    color: 'var(--color-on-ink-button)',
    padding: '14px 30px',
    borderRadius: 'var(--rounded-full)',
    fontSize: 'var(--text-button)',
    fontWeight: 'var(--font-bold)'
  },
  buyCta: {
    background: 'var(--color-primary)',
    color: 'var(--color-on-primary)',
    padding: '14px 30px',
    borderRadius: 'var(--rounded-full)',
    fontSize: 'var(--text-button)',
    fontWeight: 'var(--font-bold)'
  },
  secondary: {
    background: 'transparent',
    color: 'var(--color-ink-deep)',
    border: '2px solid var(--color-ink-deep)',
    padding: '12px 28px',
    borderRadius: 'var(--rounded-full)',
    fontSize: 'var(--text-button)',
    fontWeight: 'var(--font-bold)'
  }
};

// Card Components
const CARD_STYLES = {
  productFeature: {
    background: 'var(--color-canvas)',
    borderRadius: 'var(--rounded-xxxl)',
    padding: 'var(--spacing-xxl)',
    border: '1px solid var(--color-hairline-soft)'
  },
  iconFeature: {
    background: 'var(--color-canvas)',
    borderRadius: 'var(--rounded-xl)',
    padding: 'var(--spacing-xl)',
    border: '1px solid var(--color-hairline-soft)'
  },
  checkoutSummary: {
    background: 'var(--color-canvas)',
    borderRadius: 'var(--rounded-xl)',
    padding: 'var(--spacing-xl)',
    border: '1px solid var(--color-hairline-soft)',
    boxShadow: 'rgba(20, 22, 26, 0.3) 0px 1px 4px 0px'
  }
};
```

---

## 8. Verification & Validation

### 8.1 Verification Methods

#### 8.1.1 Code Review
- All code reviewed against requirements
- Design system compliance verified
- Security audit performed
- Performance testing conducted

#### 8.1.2 Automated Testing
```javascript
// Example test structure
describe('Task Management', () => {
  test('should create task with valid data', () => {
    const task = new Task({
      title: 'Test Task',
      description: 'Test description'
    });
    expect(task.id).toBeDefined();
    expect(task.title).toBe('Test Task');
  });

  test('should reject task with invalid title', () => {
    expect(() => {
      new Task({ title: '' });  // Empty title
    }).toThrow('Title is required');
  });

  test('should save to localStorage within 100ms', async () => {
    const start = performance.now();
    await taskService.createTask(validTaskData);
    const duration = performance.now() - start;
    expect(duration).toBeLessThan(100);
  });
});
```

#### 8.1.3 Manual Testing Checklist
- [ ] Task creation with all field combinations
- [ ] Task editing and deletion
- [ ] Project creation and management
- [ ] Webhook configuration and testing
- [ ] Notification delivery (manual time manipulation)
- [ ] Data export/import
- [ ] Responsive design on all breakpoints
- [ ] Keyboard navigation
- [ ] Screen reader compatibility
- [ ] Cross-browser compatibility

### 8.2 Validation Methods

#### 8.2.1 User Acceptance Testing
- **Scenario 1**: First-time user creates first task within 2 minutes
- **Scenario 2**: Power user creates task with webhook notification in < 5 minutes
- **Scenario 3**: User successfully receives webhook notification
- **Scenario 4**: User exports and imports data without errors
- **Scenario 5**: User navigates entire application using keyboard only

#### 8.2.2 Performance Validation
```javascript
// Performance measurement examples
console.time('Task Creation');
await taskService.createTask(validTaskData);
console.timeEnd('Task Creation');  // Should be < 100ms

console.time('Task Retrieval (10k tasks)');
await taskService.getTasks();
console.timeEnd('Task Retrieval (10k tasks)');  // Should be < 500ms
```

#### 8.2.3 Design System Validation
- **Color Usage**: Verify `{colors.primary}` only used for webhook CTAs
- **Typography**: Verify all headings use `ss01, ss02` stylistic sets
- **Components**: Verify all buttons use `{rounded.full}`
- **Spacing**: Verify all spacing uses 4px/8px grid
- **Accessibility**: Verify WCAG 2.1 AA compliance

---

## 9. Documentation Requirements

### 9.1 User Documentation
- **Getting Started Guide**: Step-by-step first-time setup
- **Feature Guide**: Detailed explanation of all features
- **Webhook Configuration Guide**: How to configure webhook endpoints
- **FAQ**: Common questions and issues
- **Troubleshooting**: Common problems and solutions

### 9.2 Developer Documentation
- **Architecture Overview**: System architecture and component structure
- **API Documentation**: JavaScript module documentation
- **Data Schema**: Detailed data model documentation
- **Design System Guide**: How to use design tokens and components
- **Testing Guide**: How to run and write tests

### 9.3 Code Documentation
- **Inline Comments**: Complex logic explanations
- **Function Documentation**: JSDoc comments for all public functions
- **Module Documentation**: README in each major module
- **Changelog**: Version history and changes

---

## 10. Deployment & Operations

### 10.1 Development Environment

#### 10.1.1 Setup
```bash
# Clone repository
git clone <repository-url>
cd Dashboardku

# Start development server
python3 -m http.server 8080

# Open browser to http://localhost:8080
```

#### 10.1.2 Development Tools
- **Browser**: Chrome DevTools for debugging
- **Editor**: VS Code or similar
- **Version Control**: Git
- **File Server**: Python's built-in HTTP server

### 10.2 Production Deployment

#### 10.2.1 Build Process
```bash
# Install dependencies (if any)
npm install

# Build Tailwind CSS
npx tailwindcss -i ./css/main.css -o ./dist/main.css --minify

# Copy files to production directory
cp -r index.html css dist/ assets/ /path/to/production/

# Serve with any static file server
python3 -m http.server 80 --directory /path/to/production/
```

#### 10.2.2 Production Checklist
- [ ] All console logs removed or disabled
- [ ] Tailwind CSS built and minified
- [ ] JavaScript minified (if using build tools)
- [ ] All assets optimized (images compressed)
- [ ] Security headers configured
- [ ] Accessibility tested
- [ ] Cross-browser tested
- [ ] Performance tested

### 10.3 Operations

#### 10.3.1 Monitoring
- **Error Logging**: Console errors (development)
- **Performance Monitoring**: Page load times, interaction latency
- **User Feedback**: Bug reports, feature requests

#### 10.3.2 Backup & Recovery
- **Automatic Backups**: Weekly localStorage backups
- **Manual Backups**: User-triggered data export
- **Recovery**: Import from backup JSON file
- **Data Migration**: Schema version updates handled automatically

#### 10.3.3 Updates
- **Version Management**: Semantic versioning (MAJOR.MINOR.PATCH)
- **Data Migration**: Automatic on version change
- **Release Notes**: Document all changes
- **Rollback**: Ability to revert to previous version

---

## 11. Risks & Mitigations

### 11.1 Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| localStorage quota exceeded | High | Medium | Implement compression, archiving, cleanup recommendations |
| Webhook CORS failures | Medium | High | Provide CORS proxy documentation, test endpoint functionality |
| Browser compatibility | Medium | Low | Progressive enhancement, polyfills, browser testing |
| Data corruption | High | Low | Validation, backups, recovery mode |
| Performance degradation | Medium | Medium | Lazy loading, pagination, performance monitoring |

### 11.2 Product Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| User finds webhooks too technical | Medium | High | Provide templates, presets, examples |
| Feature parity with Todoist | Low | Medium | Focus on webhook differentiation |
| Limited functionality perception | Medium | Medium | Emphasize privacy, self-hosting benefits |
| Onboarding complexity | Medium | Low | Simplify initial setup, provide tutorial |

### 11.3 Security Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| XSS attacks | High | Low | Input validation, output escaping, CSP |
| CSRF attacks | Medium | Low | CSRF tokens, same-origin checks |
| Data leakage | Medium | Low | No external data transmission, encrypted storage |
| Webhook credential exposure | High | Medium | Warning messages, optional storage, examples |

---

## 12. Appendices

### Appendix A: Glossary

- **CRUD**: Create, Read, Update, Delete operations
- **DOM**: Document Object Model
- **localStorage**: Browser API for persistent data storage
- **UUID**: Universally Unique Identifier
- **Webhook**: HTTP callback that delivers notifications
- **Payload Template**: JSON string with placeholder variables

### Appendix B: Reference Documents

- **PRD.md**: Product Requirements Document
- **DESIGN.md**: Meta Design System Specification
- **Tailwind CSS Documentation**: https://tailwindcss.com/docs
- **MDN Web Docs**: https://developer.mozilla.org/

### Appendix C: Change Log

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-08-18 | Initial SRS creation | System |

---

**Document Status:** Draft
**Next Review Date:** Upon PRD approval
**Approval Required From:** Product Owner, Technical Lead