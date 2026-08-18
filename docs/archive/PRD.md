# Product Requirements Document (PRD)
## Dashboardku - Personal Task Management System

**Version:** 1.0
**Date:** August 18, 2026
**Product Owner:** [User]
**Status:** Draft

---

## 1. Executive Summary

### 1.1 Product Vision
Dashboardku is a personal task management system designed to overcome the limitations of existing todo applications like Todoist. The application provides a customizable workflow with webhook-based deadline notifications, similar to Uptime Kuma's notification system, enabling users to receive alerts through any service that supports HTTP webhooks.

### 1.2 Problem Statement
Current todo list applications (specifically Todoist) have several limitations:
- Premium features required for reminder functionality
- Inflexible workflow customization
- Limited notification options (locked to specific integrations)
- No support for custom webhook-based notifications
- Restricted ability to integrate with personal monitoring systems

### 1.3 Solution
A self-hosted, browser-based task management application that:
- Provides unlimited task creation and organization
- Supports webhook notifications for deadline reminders
- Allows complete workflow customization
- Integrates with existing monitoring tools (like Uptime Kuma)
- Runs locally without external dependencies
- Uses Meta's proven commerce design system for familiar UX

### 1.4 Target Audience
- Developers who want programmatic access to task notifications
- Privacy-conscious users who prefer self-hosted solutions
- Users with complex notification workflows
- Teams already using webhook-based monitoring systems

---

## 2. Core Features

### 2.1 Task Management (MVP)

#### 2.1.1 Task Creation
**User Story:** As a user, I want to create tasks with titles, descriptions, and deadlines so that I can track my work effectively.

**Functional Requirements:**
- Create tasks with the following fields:
  - Title (required, max 200 characters)
  - Description (optional, rich text support)
  - Due date/time (optional, datetime picker)
  - Priority level (optional: none, low, medium, high)
  - Tags/labels (optional, multiple)
  - Status (default: "todo")
- Support task creation via web UI
- Tasks auto-save to browser localStorage

**UI Specifications:**
- Use `button-primary` (black pill) for "Create Task" CTA
- Input fields follow `text-input` component from design system
- Priority selector uses `radio-option` pattern
- Form layout follows 2-column split: left column (58%) for content, right rail (42%) for settings

#### 2.1.2 Task Organization
**User Story:** As a user, I want to organize tasks into projects so that I can manage different aspects of my life separately.

**Functional Requirements:**
- Create unlimited projects/folders
- Assign tasks to projects (optional)
- Filter tasks by project
- Reorder projects via drag-and-drop

**UI Specifications:**
- Projects displayed as `card-icon-feature` tiles
- Active project uses `radio-option-selected` styling (`{colors.primary}` border)
- Maximum 6 projects visible above fold

#### 2.1.3 Task Status Management
**User Story:** As a user, I want to change task status so that I can track progress.

**Functional Requirements:**
- Status options: "todo", "in_progress", "completed", "blocked"
- Bulk status updates
- Visual status indicators on task cards
- Status change history (audit log)

**UI Specifications:**
- Status badges use `badge-success` (completed), `badge-attention` (in_progress), `badge-critical` (blocked)
- No badge for "todo" status
- Status selector appears as `button-pill-tab` row above task list

### 2.2 Webhook Notifications (Core Differentiator)

#### 2.2.1 Webhook Configuration
**User Story:** As a user, I want to configure webhook endpoints so that I receive deadline notifications through my preferred services.

**Functional Requirements:**
- Add unlimited webhook URLs
- Configure HTTP method (POST, GET, PUT, PATCH)
- Set custom headers (e.g., Authorization tokens)
- Define custom payload template (JSON support)
- Test webhook endpoint
- Enable/disable individual webhooks
- Set retry logic (3 attempts with exponential backoff)

**UI Specifications:**
- Webhook configuration page uses `card-checkout-summary` layout
- Webhook list displayed as `product-thumbnail` cards
- "Add Webhook" CTA uses `button-buy-cta` (cobalt primary)
- Test webhook button uses `button-secondary` ghost outline

**Payload Template Variables:**
```
{
  "task_id": "{{task_id}}",
  "title": "{{title}}",
  "description": "{{description}}",
  "due_date": "{{due_date}}",
  "priority": "{{priority}}",
  "project": "{{project}}",
  "status": "{{status}}",
  "notification_type": "{{notification_type}}",
  "timestamp": "{{timestamp}}"
}
```

#### 2.2.2 Notification Triggers
**User Story:** As a user, I want to specify when notifications should be sent so that I'm reminded at the right time.

**Functional Requirements:**
- Triggers:
  - At deadline (exact due time)
  - Before deadline (configurable: 5min, 15min, 1hour, 1day, 1week)
  - When task becomes overdue
  - On status change (optional)
  - Daily digest (optional)
- Multiple triggers per task
- Per-project trigger defaults

**UI Specifications:**
- Trigger selector uses `button-pill-tab` pattern
- Active triggers use `button-pill-tab-active` (dark fill)
- Time interval selector uses `radio-option` cards

#### 2.2.3 Notification Delivery
**User Story:** As a user, I want my notifications to be delivered reliably so that I never miss a deadline.

**Functional Requirements:**
- Send webhook notifications at scheduled times
- Retry failed webhooks (3 attempts: immediate, 5min, 15min)
- Log delivery status (success/failure)
- Display notification history
- Support rate limiting (max 1 request/second per endpoint)

**UI Specifications:**
- Delivery status shown in `tech-specs-table` format
- Success: `{colors.success}`, Failure: `{colors.critical}`
- Notification history uses `faq-accordion` pattern

### 2.3 User Interface

#### 2.3.1 Dashboard (Homepage)
**User Story:** As a user, I want a dashboard showing my tasks so that I can see what needs to be done at a glance.

**Functional Requirements:**
- Display all tasks across projects
- Show overdue tasks prominently
- Display task count by status
- Quick-add task input
- Today's deadline summary

**UI Specifications:**
- Follow `hero-band-marketing` pattern with personalized greeting
- Task summary stats in `feature-icon-row` (4-up grid):
  - Tasks due today
  - Overdue tasks
  - In progress
  - Completed this week
- Task list uses `card-product-feature` pattern
- Quick-add input uses `search-pill` styling

#### 2.3.2 Task List View
**Functional Requirements:**
- Sortable columns (due date, priority, status, project)
- Filter by status, project, priority
- Search by title/description
- Pagination (50 tasks/page)
- Inline task editing

**UI Specifications:**
- Sort controls as `button-pill-tab` row
- Search input uses `search-pill` pattern
- Task cards use `card-product-feature` styling
- Active filters shown as `badge-promo-yellow`

#### 2.3.3 Project Detail View
**Functional Requirements:**
- Project-specific task list
- Project statistics (completion rate, average overdue time)
- Project deadline timeline
- Bulk actions (archive, complete, delete)

**UI Specifications:**
- Project header uses `display-lg` typography
- Stats in `feature-icon-row` pattern
- Task timeline visual using `card-promo-strip` style

### 2.4 Data Management

#### 2.4.1 Data Storage
**Functional Requirements:**
- All data stored in browser localStorage
- Export data as JSON
- Import data from JSON
- Automatic backups (weekly)
- Data validation on import

**UI Specifications:**
- Export/Import in "Settings" section
- "Export Data" button uses `button-secondary`
- "Import Data" button uses `button-ghost`
- Success/error messages use `badge-success` / `badge-critical`

#### 2.4.2 Task Templates
**Functional Requirements:**
- Create task templates with predefined fields
- Save common task patterns
- Quick-create from template
- Template categories

**UI Specifications:**
- Template selector as `color-sku-picker-row`
- Template cards use `product-thumbnail` pattern
- "Use Template" CTA uses `button-buy-cta`

---

## 3. User Experience Flows

### 3.1 Onboarding Flow

**First-time user experience:**
1. **Welcome Screen** (`hero-band-marketing`)
   - Headline: "Welcome to Dashboardku"
   - Subtitle: "Your personal task management system"
   - Dual CTA: "Get Started" (`button-primary`), "View Demo" (`button-secondary`)

2. **Quick Setup** (3-step wizard)
   - Step 1: Create first project
   - Step 2: Configure first webhook (optional, skip available)
   - Step 3: Create first task

3. **Dashboard Entry**
   - Display created task
   - Show notification configuration tip
   - Offer video tutorial (optional)

### 3.2 Task Creation Flow

1. Click "Add Task" button (`button-buy-cta`)
2. Task creation modal opens (center screen, 600px max-width)
3. Fill required fields (title highlighted)
4. Optionally add: description, due date, priority, tags
5. Select notification triggers (expandable `faq-accordion` section)
6. Click "Create Task" (`button-primary`)
7. Task appears in list with animation
8. Success confirmation: `badge-success` "Task created"

### 3.3 Webhook Configuration Flow

1. Navigate to Settings → Webhooks
2. Click "Add Webhook" (`button-buy-cta`)
3. Enter webhook URL
4. Select HTTP method (`radio-option` cards: GET, POST, PUT, PATCH)
5. Add custom headers (key-value pairs, `text-input` fields)
6. Configure payload template (JSON editor with syntax highlighting)
7. Click "Test Webhook" (`button-secondary`)
8. View test results in `tech-specs-table` format
9. Click "Save Webhook" (`button-primary`)
10. Webhook appears in webhook list (`product-thumbnail` cards)

### 3.4 Notification Delivery Flow

**When deadline is reached:**
1. Background process checks due tasks (every minute)
2. For each due task:
   - Retrieve active webhooks
   - Build payload with template variables
   - Send POST request to each webhook
   - Log result (success/failure)
   - Retry on failure (exponential backoff)
3. Update notification history UI
4. Display `badge-promo-yellow` "Notification sent" in task card

---

## 4. Non-Functional Requirements

### 4.1 Performance
- Initial page load: < 2 seconds
- Task creation: < 100ms
- Notification delivery: < 5 seconds per webhook
- Support 10,000 tasks without degradation
- Webhook delivery rate: max 100 requests/minute

### 4.2 Security
- All data stored locally (no server transmission)
- Webhook URLs encrypted in localStorage
- XSS protection on all user inputs
- CSRF tokens for form submissions
- Input validation on all fields
- Secure headers (CSP, X-Frame-Options)

### 4.3 Compatibility
- Browsers: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- Responsive: Mobile, Tablet, Desktop
- Accessibility: WCAG 2.1 AA
- Screen reader support

### 4.4 Reliability
- Data persistence: localStorage
- Auto-save every 30 seconds
- Recovery mode for corrupted data
- Webhook retry logic with exponential backoff
- Graceful degradation if localStorage unavailable

### 4.5 Maintainability
- Code structure: Modular vanilla JavaScript
- Component-based architecture
- Clear separation of concerns
- Comprehensive inline documentation
- Version tracking for data schema

---

## 5. Design System Compliance

All UI components MUST follow the Meta design system defined in DESIGN.md:

### 5.1 Color Usage Rules
- `{colors.primary}` (cobalt): ONLY for webhook CTAs and notification-related actions
- `{colors.ink-button}` (black): Marketing surface CTAs ("Create Task", "Add Project")
- `{colors.success}`: Task completed, webhook success
- `{colors.critical}`: Overdue tasks, webhook failures, errors
- `{colors.warning}`: Promotional banners, limited-time offers
- `{colors.canvas}`: Page background
- `{colors.hairline-soft}`: Card borders

### 5.2 Typography Rules
- Hero: `{typography.hero-display}` (64px) for welcome screen
- Section headers: `{typography.heading-lg}` (36px)
- Card titles: `{typography.heading-sm}` (24px)
- Body: `{typography.body-md}` (16px)
- Buttons: `{typography.button-md}` (14px)
- Captions: `{typography.caption}` (12px)
- Headings MUST use `ss01, ss02` stylistic sets
- Negative letter-spacing on body roles (-0.14px to -0.16px)

### 5.3 Component Patterns
- Primary buttons: `{rounded.full}` (pill-shaped), ALWAYS
- Cards: `{rounded.xxxl}` for task cards, `{rounded.xl}` for icon features
- Inputs: `text-input` with `{rounded.lg}`
- Badges: `{rounded.full}` with appropriate color
- Section spacing: `{spacing.section}` (64px)
- Card padding: `{spacing.xxl}` (32px)

### 5.4 Layout Rules
- Max-width: 1280px for main content
- 2-column splits: 58%/42% (task content/settings)
- Feature grids: 3-up or 4-up with 24px gap
- Sticky rails: 42% width, max 380px
- Hero sections: 50-70% viewport height for imagery/branding

---

## 6. Success Metrics

### 6.1 User Engagement
- 7-day retention rate: Target 60%
- Average tasks created per user: Target 10+/week
- Webhook configuration rate: Target 40% of users
- Daily active users: Target 70% of weekly users

### 6.2 Feature Usage
- Task completion rate: Target 50%
- Webhook delivery success rate: Target 95%
- Feature usage distribution:
  - Task creation: 100%
  - Project organization: 60%
  - Webhook notifications: 40%
  - Templates: 20%

### 6.3 Technical Performance
- Page load time: < 2 seconds (95th percentile)
- Task creation latency: < 100ms (95th percentile)
- Webhook delivery latency: < 5 seconds (95th percentile)
- Zero data loss incidents

---

## 7. Roadmap

### Phase 1: MVP (Weeks 1-4)
- Core task management (CRUD)
- Project organization
- Basic dashboard
- localStorage persistence

### Phase 2: Webhooks (Weeks 5-6)
- Webhook configuration UI
- Notification scheduling
- Payload templating
- Delivery tracking

### Phase 3: Polish (Weeks 7-8)
- UI refinements per design system
- Responsive design optimization
- Accessibility improvements
- Performance optimization

### Phase 4: Advanced Features (Weeks 9+)
- Task templates
- Bulk operations
- Advanced filtering
- Data export/import

---

## 8. Risks & Mitigations

### 8.1 Technical Risks

**Risk:** LocalStorage limitations (5-10MB)
- **Mitigation:** Implement data compression, archive old tasks, provide export/import

**Risk:** Webhook delivery failures
- **Mitigation:** Retry logic, detailed logging, user notification of failures

**Risk:** Browser compatibility issues
- **Mitigation:** Progressive enhancement, polyfills, browser testing

### 8.2 Product Risks

**Risk:** User finds onboarding complex
- **Mitigation:** Simplify initial setup, provide video tutorial, offer "skip" options

**Risk:** Webhook configuration too technical
- **Mitigation:** Provide templates, presets for common services (Slack, Discord, etc.)

**Risk:** Limited functionality compared to Todoist
- **Mitigation:** Focus on webhook differentiation, emphasize privacy/self-hosting

---

## 9. Open Questions

1. **Multi-device sync:** Should we implement cross-device sync via a backend service, or keep purely local?
2. **Mobile app:** Should we prioritize PWA or native mobile app?
3. **Collaboration:** Should we add sharing/collaboration features in future iterations?
4. **Integrations:** Should we build preset integrations for common services (Slack, Discord, Telegram)?
5. **Recurring tasks:** Should we implement recurring task patterns?

---

## 10. Appendix

### 10.1 Terminology
- **Task:** A single to-do item with title, description, deadline, status
- **Project:** A collection of related tasks
- **Webhook:** An HTTP endpoint that receives notifications
- **Payload:** The JSON data sent to a webhook endpoint
- **Trigger:** An event that initiates a webhook notification

### 10.2 References
- DESIGN.md: Meta design system specification
- Uptime Kuma: Webhook notification inspiration
- Todoist: Current competitive analysis

---

**Document History:**
- v1.0 (2026-08-18): Initial PRD creation