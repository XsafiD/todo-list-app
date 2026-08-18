# Technical Architecture Documentation
## Dashboardku - Personal Task Management System

**Version:** 1.0
**Date:** August 18, 2026
**Tech Stack:** Vanilla HTML + Tailwind CSS + JavaScript ES6+

---

## 1. System Architecture Overview

### 1.1 Architecture Pattern
Dashboardku follows a **Model-View-Controller (MVC)** architecture adapted for client-side applications:

```
┌───────────────────────────────────────────────────────────────┐
│                        VIEW LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  Dashboard   │  │  Task List   │  │   Settings   │        │
│  │  Component   │  │  Component   │  │  Component   │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└───────────────────────────────────────────────────────────────┘
                              ↓ Events/Commands
┌───────────────────────────────────────────────────────────────┐
│                      CONTROLLER LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   Task       │  │  Project     │  │  Webhook     │        │
│  │ Controller   │  │ Controller   │  │ Controller   │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└───────────────────────────────────────────────────────────────┘
                              ↓ Data Operations
┌───────────────────────────────────────────────────────────────┐
│                        MODEL LAYER                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │    Task      │  │   Project    │  │   Webhook    │        │
│  │    Model     │  │    Model     │  │    Model     │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└───────────────────────────────────────────────────────────────┘
                              ↓ CRUD Operations
┌───────────────────────────────────────────────────────────────┐
│                      SERVICE LAYER                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  Storage     │  │ Validation   │  │ Notification │        │
│  │  Service    │  │   Service    │  │   Service    │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└───────────────────────────────────────────────────────────────┘
                              ↓ Persistent Storage
┌───────────────────────────────────────────────────────────────┐
│                    BROWSER STORAGE                             │
│         localStorage / sessionStorage                         │
└───────────────────────────────────────────────────────────────┘
```

### 1.2 Data Flow Architecture

```
User Interaction → Event Handler → Controller → Service → Model → Storage
                                                           ↓
Response ← UI Update ← Component ← Controller ← Service ← Model
```

**Example: Task Creation Flow**
1. User fills task form and clicks "Create Task"
2. Form submit event → `TaskController.handleCreateTask()`
3. Controller validates input → `ValidationService.validateTask()`
4. Controller creates model → `Task.create(validatedData)`
5. Model saves to storage → `StorageService.save()`
6. Controller updates UI → `TaskListComponent.render()`
7. Component emits success event → Show notification

---

## 2. Technology Stack Details

### 2.1 Frontend Technologies

#### 2.1.1 HTML Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboardku - Personal Task Management</title>

    <!-- Meta Design System Font -->
    <link rel="stylesheet" href="assets/fonts/optimistic-vf.css">

    <!-- Tailwind CSS (Development) -->
    <script src="https://cdn.tailwindcss.com"></script>

    <!-- Tailwind Config with Design Tokens -->
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        // Meta design system colors
                        primary: '#0064E0',
                        'primary-deep': '#0047B3',
                        canvas: '#FFFFFF',
                        'ink-button': '#0A1317',
                        // ... other design tokens
                    },
                    fontFamily: {
                        sans: ['Optimistic VF', 'Montserrat', 'sans-serif'],
                    },
                    borderRadius: {
                        'xxxl': '32px',
                        'feature': '40px',
                        'full': '100px',
                    }
                }
            }
        }
    </script>

    <!-- Custom Styles -->
    <link rel="stylesheet" href="css/main.css">
</head>
<body>
    <!-- Application Container -->
    <div id="app"></div>

    <!-- Application JavaScript -->
    <script type="module" src="js/app.js"></script>
</body>
</html>
```

#### 2.1.2 CSS Architecture (Tailwind + Custom)

**File Structure:**
```
css/
├── main.css           # Main entry point
├── components.css     # Component-specific styles
├── utilities.css      # Custom utility classes
└── design-tokens.css  # Design system token definitions
```

**main.css:**
```css
/* Design Token Imports */
@import 'design-tokens.css';

/* Tailwind Base */
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom Base Styles */
@layer base {
    body {
        @apply bg-canvas text-ink;
        font-feature-settings: 'ss01' on, 'ss02' on;
    }

    /* Heading OpenType Features */
    h1, h2, h3, h4, h5, h6 {
        font-feature-settings: 'ss01' on, 'ss02' on;
    }
}

/* Custom Component Styles */
@layer components {
    .btn-primary {
        @apply bg-ink-button text-on-ink-button;
        @apply px-[30px] py-[14px] rounded-full;
        @apply text-button font-bold;
    }

    .btn-buy-cta {
        @apply bg-primary text-on-primary;
        @apply px-[30px] py-[14px] rounded-full;
        @apply text-button font-bold;
    }

    .card-product-feature {
        @apply bg-canvas rounded-[32px] p-8;
        @apply border border-hairline-soft;
    }

    /* ... other component classes */
}
```

**design-tokens.css:**
```css
:root {
    /* Brand & Accent Colors */
    --color-primary: #0064E0;
    --color-primary-deep: #0047B3;
    --color-primary-soft: rgba(0, 100, 224, 0.15);

    /* Surface Colors */
    --color-canvas: #FFFFFF;
    --color-surface-soft: #F4F4F4;

    /* Text Colors */
    --color-ink-deep: #0A1317;
    --color-ink: #1C1E21;

    /* Typography */
    --font-family: 'Optimistic VF', sans-serif;
    --text-hero-display: 64px;

    /* Spacing */
    --spacing-section: 64px;
    --spacing-xxl: 32px;

    /* Border Radius */
    --rounded-full: 100px;
    --rounded-xxxl: 32px;
}
```

### 2.2 JavaScript Architecture

#### 2.2.1 Module Structure

```javascript
// app.js - Application Entry Point
import { UIController } from './controllers/uiController.js';
import { TaskController } from './controllers/taskController.js';
import { ProjectController } from './controllers/projectController.js';
import { WebhookController } from './controllers/webhookController.js';
import { StorageService } from './services/storageService.js';
import { NotificationService } from './services/notificationService.js';

class DashboardkuApp {
    constructor() {
        this.controllers = {
            ui: new UIController(),
            task: new TaskController(),
            project: new ProjectController(),
            webhook: new WebhookController()
        };

        this.services = {
            storage: new StorageService(),
            notification: new NotificationService()
        };
    }

    async init() {
        // Initialize services
        await this.services.storage.init();
        await this.services.notification.init();

        // Initialize controllers
        await this.controllers.ui.init();

        // Start notification service
        this.services.notification.start();

        console.log('Dashboardku initialized');
    }
}

// Initialize application
const app = new DashboardkuApp();
app.init();
```

#### 2.2.2 Model Layer Implementation

```javascript
// models/Task.js
import { v4 as uuidv4 } from '../utils/uuid.js';
import { validateTask } from '../utils/validation.js';

export class Task {
    constructor(data = {}) {
        this.id = data.id || uuidv4();
        this.title = data.title || '';
        this.description = data.description || '';
        this.dueDate = data.dueDate || null;
        this.priority = data.priority || 'none';
        this.status = data.status || 'todo';
        this.projectId = data.projectId || null;
        this.tags = data.tags || [];
        this.webhookTriggers = data.webhookTriggers || [];
        this.createdAt = data.createdAt || new Date().toISOString();
        this.updatedAt = data.updatedAt || new Date().toISOString();
    }

    static create(data) {
        const validation = validateTask(data);
        if (!validation.valid) {
            throw new Error(validation.errors.join(', '));
        }
        return new Task(data);
    }

    update(data) {
        Object.assign(this, data);
        this.updatedAt = new Date().toISOString();
        return this.save();
    }

    async save() {
        const storageService = new StorageService();
        return await storageService.saveTask(this);
    }

    toJSON() {
        return {
            id: this.id,
            title: this.title,
            description: this.description,
            dueDate: this.dueDate,
            priority: this.priority,
            status: this.status,
            projectId: this.projectId,
            tags: this.tags,
            webhookTriggers: this.webhookTriggers,
            createdAt: this.createdAt,
            updatedAt: this.updatedAt
        };
    }

    static fromJSON(json) {
        return new Task(json);
    }
}
```

#### 2.2.3 Controller Layer Implementation

```javascript
// controllers/taskController.js
import { Task } from '../models/Task.js';
import { StorageService } from '../services/storageService.js';
import { ValidationService } from '../services/validationService.js';
import { emit, on } from '../utils/eventBus.js';

export class TaskController {
    constructor() {
        this.storageService = new StorageService();
        this.validationService = new ValidationService();
        this.tasks = [];
    }

    async init() {
        this.tasks = await this.storageService.getTasks();
        this.setupEventListeners();
    }

    setupEventListeners() {
        on('task:create', this.handleCreateTask.bind(this));
        on('task:update', this.handleUpdateTask.bind(this));
        on('task:delete', this.handleDeleteTask.bind(this));
    }

    async handleCreateTask(taskData) {
        try {
            // Validate input
            const validation = this.validationService.validateTask(taskData);
            if (!validation.valid) {
                emit('task:create:error', { errors: validation.errors });
                return;
            }

            // Create task model
            const task = Task.create(taskData);

            // Save to storage
            await this.storageService.saveTask(task);

            // Update local cache
            this.tasks.push(task);

            // Emit success event
            emit('task:created', { task });

            return task;
        } catch (error) {
            emit('task:create:error', { error: error.message });
            throw error;
        }
    }

    async handleUpdateTask(taskId, updates) {
        const task = this.tasks.find(t => t.id === taskId);
        if (!task) {
            throw new Error('Task not found');
        }

        const validation = this.validationService.validateTask(updates);
        if (!validation.valid) {
            emit('task:update:error', { errors: validation.errors });
            return;
        }

        Object.assign(task, updates);
        task.updatedAt = new Date().toISOString();

        await this.storageService.saveTask(task);
        emit('task:updated', { task });

        return task;
    }

    async handleDeleteTask(taskId) {
        const taskIndex = this.tasks.findIndex(t => t.id === taskId);
        if (taskIndex === -1) {
            throw new Error('Task not found');
        }

        const task = this.tasks[taskIndex];
        await this.storageService.deleteTask(taskId);

        this.tasks.splice(taskIndex, 1);
        emit('task:deleted', { taskId });

        return taskId;
    }

    getTasks(filter = {}) {
        let filtered = [...this.tasks];

        if (filter.status) {
            filtered = filtered.filter(t => t.status === filter.status);
        }

        if (filter.projectId) {
            filtered = filtered.filter(t => t.projectId === filter.projectId);
        }

        if (filter.priority) {
            filtered = filtered.filter(t => t.priority === filter.priority);
        }

        return filtered;
    }

    getTaskById(taskId) {
        return this.tasks.find(t => t.id === taskId);
    }
}
```

#### 2.2.4 Service Layer Implementation

```javascript
// services/storageService.js
export class StorageService {
    constructor() {
        this.storageKeys = {
            TASKS: 'dashboardku_tasks',
            PROJECTS: 'dashboardku_projects',
            WEBHOOKS: 'dashboardku_webhooks',
            SETTINGS: 'dashboardku_settings',
            NOTIFICATIONS: 'dashboardku_notifications',
            VERSION: 'dashboardku_version'
        };

        this.currentVersion = '1.0.0';
    }

    async init() {
        // Check if this is first run
        if (!localStorage.getItem(this.storageKeys.VERSION)) {
            await this.migrateToCurrentVersion();
        }

        // Validate data integrity
        await this.validateDataIntegrity();
    }

    async migrateToCurrentVersion() {
        console.log('Initializing Dashboardku storage');
        localStorage.setItem(this.storageKeys.VERSION, this.currentVersion);

        // Initialize empty data structures
        if (!localStorage.getItem(this.storageKeys.TASKS)) {
            localStorage.setItem(this.storageKeys.TASKS, JSON.stringify([]));
        }

        if (!localStorage.getItem(this.storageKeys.PROJECTS)) {
            localStorage.setItem(this.storageKeys.PROJECTS, JSON.stringify([]));
        }

        if (!localStorage.getItem(this.storageKeys.WEBHOOKS)) {
            localStorage.setItem(this.storageKeys.WEBHOOKS, JSON.stringify([]));
        }

        if (!localStorage.getItem(this.storageKeys.SETTINGS)) {
            localStorage.setItem(this.storageKeys.SETTINGS, JSON.stringify({
                theme: 'light',
                defaultView: 'list',
                notificationsEnabled: true
            }));
        }
    }

    async validateDataIntegrity() {
        try {
            const tasks = this.getTasks();
            const projects = this.getProjects();
            const webhooks = this.getWebhooks();

            // Validate JSON structure
            JSON.parse(tasks);
            JSON.parse(projects);
            JSON.parse(webhooks);

            return true;
        } catch (error) {
            console.error('Data integrity validation failed:', error);
            throw new Error('Corrupted data detected. Please restore from backup.');
        }
    }

    async getTasks() {
        const data = localStorage.getItem(this.storageKeys.TASKS);
        return data ? JSON.parse(data) : [];
    }

    async saveTask(task) {
        const tasks = await this.getTasks();
        const index = tasks.findIndex(t => t.id === task.id);

        if (index >= 0) {
            tasks[index] = task;
        } else {
            tasks.push(task);
        }

        localStorage.setItem(this.storageKeys.TASKS, JSON.stringify(tasks));
        return task;
    }

    async deleteTask(taskId) {
        const tasks = await this.getTasks();
        const filtered = tasks.filter(t => t.id !== taskId);
        localStorage.setItem(this.storageKeys.TASKS, JSON.stringify(filtered));
    }

    async getProjects() {
        const data = localStorage.getItem(this.storageKeys.PROJECTS);
        return data ? JSON.parse(data) : [];
    }

    async saveProject(project) {
        const projects = await this.getProjects();
        const index = projects.findIndex(p => p.id === project.id);

        if (index >= 0) {
            projects[index] = project;
        } else {
            projects.push(project);
        }

        localStorage.setItem(this.storageKeys.PROJECTS, JSON.stringify(projects));
        return project;
    }

    async getWebhooks() {
        const data = localStorage.getItem(this.storageKeys.WEBHOOKS);
        return data ? JSON.parse(data) : [];
    }

    async saveWebhook(webhook) {
        const webhooks = await this.getWebhooks();
        const index = webhooks.findIndex(w => w.id === webhook.id);

        if (index >= 0) {
            webhooks[index] = webhook;
        } else {
            webhooks.push(webhook);
        }

        localStorage.setItem(this.storageKeys.WEBHOOKS, JSON.stringify(webhooks));
        return webhook;
    }

    async exportData() {
        return {
            version: this.currentVersion,
            exportDate: new Date().toISOString(),
            tasks: await this.getTasks(),
            projects: await this.getProjects(),
            webhooks: await this.getWebhooks(),
            settings: JSON.parse(localStorage.getItem(this.storageKeys.SETTINGS))
        };
    }

    async importData(data) {
        // Validate data structure
        if (!data.tasks || !data.projects || !data.webhooks) {
            throw new Error('Invalid data format');
        }

        // Create backup before import
        await this.createBackup();

        // Import data
        localStorage.setItem(this.storageKeys.TASKS, JSON.stringify(data.tasks));
        localStorage.setItem(this.storageKeys.PROJECTS, JSON.stringify(data.projects));
        localStorage.setItem(this.storageKeys.WEBHOOKS, JSON.stringify(data.webhooks));
        localStorage.setItem(this.storageKeys.SETTINGS, JSON.stringify(data.settings));

        return true;
    }

    async createBackup() {
        const backup = {
            timestamp: new Date().toISOString(),
            tasks: await this.getTasks(),
            projects: await this.getProjects(),
            webhooks: await this.getWebhooks(),
            settings: JSON.parse(localStorage.getItem(this.storageKeys.SETTINGS))
        };

        const backups = JSON.parse(localStorage.getItem('dashboardku_backups') || '[]');
        backups.push(backup);

        // Keep only last 5 backups
        if (backups.length > 5) {
            backups.shift();
        }

        localStorage.setItem('dashboardku_backups', JSON.stringify(backups));
    }

    getStorageUsage() {
        let total = 0;
        for (let key in localStorage) {
            if (localStorage.hasOwnProperty(key)) {
                total += localStorage[key].length + key.length;
            }
        }
        return total; // Return in bytes
    }
}
```

```javascript
// services/notificationService.js
import { StorageService } from './storageService.js';
import { WebhookService } from './webhookService.js';
import { emit } from '../utils/eventBus.js';

export class NotificationService {
    constructor() {
        this.storageService = new StorageService();
        this.webhookService = new WebhookService();
        this.checkInterval = null;
        this.isRunning = false;
    }

    async init() {
        console.log('Initializing notification service');
    }

    start() {
        if (this.isRunning) return;

        this.isRunning = true;
        this.checkInterval = setInterval(() => {
            this.checkNotifications();
        }, 60000); // Check every minute

        console.log('Notification service started');
    }

    stop() {
        if (this.checkInterval) {
            clearInterval(this.checkInterval);
            this.checkInterval = null;
        }
        this.isRunning = false;
        console.log('Notification service stopped');
    }

    async checkNotifications() {
        try {
            const tasks = await this.storageService.getTasks();
            const webhooks = await this.storageService.getWebhooks();
            const enabledWebhooks = webhooks.filter(w => w.enabled);

            if (enabledWebhooks.length === 0) return;

            const now = new Date();
            const notifications = [];

            for (const task of tasks) {
                if (!task.dueDate || task.status === 'completed') continue;

                const dueDate = new Date(task.dueDate);
                const taskWebhooks = task.webhookTriggers || [];

                for (const trigger of taskWebhooks) {
                    if (!trigger.enabled) continue;

                    const shouldNotify = this.shouldTriggerNotification(trigger, dueDate, now);

                    if (shouldNotify) {
                        notifications.push({
                            task,
                            trigger,
                            webhooks: enabledWebhooks
                        });
                    }
                }
            }

            // Send notifications
            for (const notification of notifications) {
                await this.sendNotification(notification);
            }

        } catch (error) {
            console.error('Error checking notifications:', error);
            emit('notification:error', { error: error.message });
        }
    }

    shouldTriggerNotification(trigger, dueDate, now) {
        const triggerTime = this.calculateTriggerTime(trigger, dueDate);
        const lastMinute = new Date(now.getTime() - 60000); // Last minute

        return triggerTime <= now && triggerTime > lastMinute;
    }

    calculateTriggerTime(trigger, dueDate) {
        switch (trigger.type) {
            case 'deadline':
                return dueDate;
            case 'before_deadline':
                return new Date(dueDate.getTime() - this.parseDuration(trigger.offset));
            case 'overdue':
                return new Date(dueDate.getTime() + 60000); // 1 minute after due
            default:
                return dueDate;
        }
    }

    parseDuration(duration) {
        // Parse duration strings like "1h", "30m", "1d"
        const match = duration.match(/(\d+)([hmd])/);
        if (!match) return 0;

        const value = parseInt(match[1]);
        const unit = match[2];

        switch (unit) {
            case 'm': return value * 60000;
            case 'h': return value * 3600000;
            case 'd': return value * 86400000;
            default: return 0;
        }
    }

    async sendNotification(notification) {
        const { task, trigger, webhooks } = notification;

        for (const webhook of webhooks) {
            try {
                const payload = this.buildPayload(task, trigger, webhook);
                await this.webhookService.sendWebhook(webhook, payload);

                emit('notification:sent', {
                    taskId: task.id,
                    webhookId: webhook.id,
                    triggerType: trigger.type
                });

            } catch (error) {
                console.error(`Failed to send notification to ${webhook.url}:`, error);
                emit('notification:failed', {
                    taskId: task.id,
                    webhookId: webhook.id,
                    error: error.message
                });
            }
        }
    }

    buildPayload(task, trigger, webhook) {
        const template = webhook.payloadTemplate || this.getDefaultPayloadTemplate();

        const variables = {
            task_id: task.id,
            title: task.title,
            description: task.description,
            due_date: task.dueDate,
            priority: task.priority,
            project: this.getProjectName(task.projectId),
            status: task.status,
            notification_type: trigger.type,
            timestamp: new Date().toISOString()
        };

        return this.renderTemplate(template, variables);
    }

    renderTemplate(template, variables) {
        let rendered = template;

        for (const [key, value] of Object.entries(variables)) {
            const placeholder = `{{${key}}}`;
            rendered = rendered.replace(new RegExp(placeholder, 'g'), value);
        }

        return rendered;
    }

    getDefaultPayloadTemplate() {
        return JSON.stringify({
            task_id: '{{task_id}}',
            title: '{{title}}',
            description: '{{description}}',
            due_date: '{{due_date}}',
            priority: '{{priority}}',
            status: '{{status}}',
            notification_type: '{{notification_type}}',
            timestamp: '{{timestamp}}'
        }, null, 2);
    }

    async getProjectName(projectId) {
        if (!projectId) return null;

        const projects = await this.storageService.getProjects();
        const project = projects.find(p => p.id === projectId);
        return project ? project.name : null;
    }
}
```

```javascript
// services/webhookService.js
export class WebhookService {
    constructor() {
        this.requestQueue = [];
        this.isProcessing = false;
        this.rateLimitDelay = 1000; // 1 second between requests
    }

    async sendWebhook(webhook, payload) {
        // Add to queue
        this.requestQueue.push({ webhook, payload });

        // Process queue if not already processing
        if (!this.isProcessing) {
            await this.processQueue();
        }
    }

    async processQueue() {
        this.isProcessing = true;

        while (this.requestQueue.length > 0) {
            const request = this.requestQueue.shift();
            await this.sendRequest(request.webhook, request.payload);

            // Rate limiting delay
            if (this.requestQueue.length > 0) {
                await this.delay(this.rateLimitDelay);
            }
        }

        this.isProcessing = false;
    }

    async sendRequest(webhook, payload) {
        const maxRetries = 3;
        const retryDelays = [0, 5000, 15000]; // Immediate, 5s, 15s

        for (let attempt = 0; attempt < maxRetries; attempt++) {
            try {
                const response = await fetch(webhook.url, {
                    method: webhook.method || 'POST',
                    headers: this.buildHeaders(webhook.headers),
                    body: this.buildBody(webhook.method, payload)
                });

                if (response.ok) {
                    return { success: true, status: response.status };
                } else {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }

            } catch (error) {
                console.error(`Webhook attempt ${attempt + 1} failed:`, error);

                if (attempt < maxRetries - 1) {
                    await this.delay(retryDelays[attempt + 1]);
                } else {
                    throw error;
                }
            }
        }
    }

    buildHeaders(headers) {
        const defaultHeaders = {
            'Content-Type': 'application/json'
        };

        const customHeaders = {};
        if (headers) {
            for (const header of headers) {
                customHeaders[header.key] = header.value;
            }
        }

        return { ...defaultHeaders, ...customHeaders };
    }

    buildBody(method, payload) {
        if (method === 'GET') {
            return undefined;
        }
        return JSON.stringify(payload);
    }

    async testWebhook(webhook) {
        const testPayload = {
            test: true,
            timestamp: new Date().toISOString(),
            message: 'This is a test notification from Dashboardku'
        };

        try {
            const result = await this.sendRequest(webhook, testPayload);
            return {
                success: true,
                ...result
            };
        } catch (error) {
            return {
                success: false,
                error: error.message
            };
        }
    }

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}
```

#### 2.2.5 Utility Functions

```javascript
// utils/uuid.js
export function uuid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

// utils/validation.js
export function validateTask(data) {
    const errors = [];

    if (!data.title || typeof data.title !== 'string') {
        errors.push('Title is required');
    } else if (data.title.length < 1 || data.title.length > 200) {
        errors.push('Title must be between 1 and 200 characters');
    }

    if (data.description && data.description.length > 5000) {
        errors.push('Description cannot exceed 5000 characters');
    }

    if (data.dueDate && isNaN(new Date(data.dueDate))) {
        errors.push('Invalid due date');
    }

    if (data.priority && !['none', 'low', 'medium', 'high'].includes(data.priority)) {
        errors.push('Invalid priority value');
    }

    if (data.status && !['todo', 'in_progress', 'completed', 'blocked'].includes(data.status)) {
        errors.push('Invalid status value');
    }

    return {
        valid: errors.length === 0,
        errors
    };
}

// utils/eventBus.js
const listeners = {};

export function emit(eventName, data) {
    if (listeners[eventName]) {
        listeners[eventName].forEach(callback => callback(data));
    }
}

export function on(eventName, callback) {
    if (!listeners[eventName]) {
        listeners[eventName] = [];
    }
    listeners[eventName].push(callback);
}

export function off(eventName, callback) {
    if (listeners[eventName]) {
        listeners[eventName] = listeners[eventName].filter(cb => cb !== callback);
    }
}

// utils/dateUtils.js
export function formatDate(date, format = 'ISO') {
    const d = new Date(date);

    switch (format) {
        case 'ISO':
            return d.toISOString();
        case 'readable':
            return d.toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        case 'short':
            return d.toLocaleDateString('en-US', {
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            });
        default:
            return d.toISOString();
    }
}

export function isOverdue(date) {
    return new Date(date) < new Date();
}

export function getTimeRemaining(date) {
    const now = new Date();
    const due = new Date(date);
    const diff = due - now;

    if (diff <= 0) return { overdue: true };

    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));

    return { days, hours, minutes, overdue: false };
}
```

---

## 3. Component Implementation Guide

### 3.1 UI Component Structure

```javascript
// components/dashboard.js
import { emit } from '../utils/eventBus.js';

export class DashboardComponent {
    constructor(container) {
        this.container = container;
        this.data = {
            totalTasks: 0,
            tasksDueToday: 0,
            overdueTasks: 0,
            completedThisWeek: 0
        };
    }

    async render() {
        this.container.innerHTML = `
            <section class="hero-band-marketing">
                <div class="max-w-7xl mx-auto px-8 py-16">
                    <h1 class="text-hero-display font-medium">
                        Welcome back!
                    </h1>
                    <p class="text-subtitle-md mt-4">
                        Here's your task overview for today
                    </p>
                </div>
            </section>

            <section class="max-w-7xl mx-auto px-8 py-8">
                <div class="feature-icon-row grid grid-cols-4 gap-6">
                    ${this.renderStatCards()}
                </div>
            </section>

            <section class="max-w-7xl mx-auto px-8 py-8">
                <h2 class="text-heading-lg mb-6">Quick Add Task</h2>
                <form id="quick-add-form" class="mb-8">
                    <div class="flex gap-4">
                        <input
                            type="text"
                            id="quick-add-input"
                            placeholder="What needs to be done?"
                            class="search-pill flex-1 px-4 py-3 rounded-full"
                        >
                        <button type="submit" class="btn-primary">
                            Add Task
                        </button>
                    </div>
                </form>

                <h2 class="text-heading-lg mb-6">Upcoming Deadlines</h2>
                <div id="upcoming-tasks" class="space-y-4">
                    ${this.renderUpcomingTasks()}
                </div>
            </section>
        `;

        this.attachEventListeners();
    }

    renderStatCards() {
        const stats = [
            {
                label: 'Total Tasks',
                value: this.data.totalTasks,
                icon: '📋'
            },
            {
                label: 'Due Today',
                value: this.data.tasksDueToday,
                icon: '📅'
            },
            {
                label: 'Overdue',
                value: this.data.overdueTasks,
                icon: '⚠️'
            },
            {
                label: 'Completed This Week',
                value: this.data.completedThisWeek,
                icon: '✅'
            }
        ];

        return stats.map(stat => `
            <div class="card-icon-feature">
                <div class="text-4xl mb-4">${stat.icon}</div>
                <h3 class="text-subtitle-lg font-bold mb-2">${stat.label}</h3>
                <p class="text-heading-sm font-medium">${stat.value}</p>
            </div>
        `).join('');
    }

    renderUpcomingTasks() {
        // Render upcoming tasks here
        return '<p>Loading upcoming tasks...</p>';
    }

    attachEventListeners() {
        const form = document.getElementById('quick-add-form');
        const input = document.getElementById('quick-add-input');

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const title = input.value.trim();

            if (title) {
                emit('task:create', {
                    title,
                    status: 'todo'
                });
                input.value = '';
            }
        });
    }

    updateData(newData) {
        this.data = { ...this.data, ...newData };
        this.render();
    }
}
```

### 3.2 Task List Component

```javascript
// components/taskList.js
export class TaskListComponent {
    constructor(container) {
        this.container = container;
        this.tasks = [];
        this.filters = {
            status: null,
            project: null,
            priority: null
        };
        this.sortBy = 'due_date';
        this.sortOrder = 'asc';
    }

    render() {
        this.container.innerHTML = `
            <div class="task-list-view">
                <div class="mb-8">
                    <div class="flex gap-4 mb-4">
                        <input
                            type="text"
                            id="task-search"
                            placeholder="Search tasks..."
                            class="search-pill flex-1 px-4 py-3 rounded-full"
                        >
                    </div>

                    <div class="flex gap-2 mb-4" id="filter-pills">
                        ${this.renderFilterPills()}
                    </div>

                    <div class="flex gap-4">
                        <select id="sort-select" class="text-input px-4 py-2 rounded-lg">
                            <option value="due_date">Sort by Due Date</option>
                            <option value="priority">Sort by Priority</option>
                            <option value="created_at">Sort by Created Date</option>
                        </select>
                    </div>
                </div>

                <div id="task-list" class="space-y-4">
                    ${this.renderTasks()}
                </div>

                ${this.renderPagination()}
            </div>
        `;

        this.attachEventListeners();
    }

    renderFilterPills() {
        const statuses = ['All', 'todo', 'in_progress', 'completed', 'blocked'];

        return statuses.map(status => `
            <button
                class="button-pill-tab ${this.filters.status === status ? 'button-pill-tab-active' : ''}"
                data-status="${status === 'All' ? null : status}"
            >
                ${status.charAt(0).toUpperCase() + status.slice(1).replace('_', ' ')}
            </button>
        `).join('');
    }

    renderTasks() {
        if (this.tasks.length === 0) {
            return `
                <div class="text-center py-12">
                    <p class="text-slate">No tasks found. Create your first task to get started!</p>
                </div>
            `;
        }

        return this.tasks.map(task => this.renderTaskCard(task)).join('');
    }

    renderTaskCard(task) {
        const priorityBadge = this.renderPriorityBadge(task.priority);
        const statusBadge = this.renderStatusBadge(task.status);
        const dueDate = task.dueDate ? this.formatDueDate(task.dueDate) : 'No due date';

        return `
            <div class="card-product-feature task-card" data-task-id="${task.id}">
                <div class="flex items-start gap-4">
                    <input
                        type="checkbox"
                        class="mt-1"
                        ${task.status === 'completed' ? 'checked' : ''}
                        data-task-id="${task.id}"
                    >

                    <div class="flex-1">
                        <div class="flex items-center gap-2 mb-2">
                            <h3 class="text-heading-sm font-medium">${task.title}</h3>
                            ${priorityBadge}
                            ${statusBadge}
                        </div>

                        ${task.description ? `
                            <p class="text-body-sm text-slate mb-3">
                                ${task.description.substring(0, 150)}${task.description.length > 150 ? '...' : ''}
                            </p>
                        ` : ''}

                        <div class="flex items-center gap-4 text-body-sm text-steel">
                            <span>📅 ${dueDate}</span>
                            ${task.projectId ? `<span>📁 Project</span>` : ''}
                            ${task.tags.length > 0 ? `
                                <span class="flex gap-1">
                                    ${task.tags.map(tag => `<span class="badge-promo-yellow">${tag}</span>`).join('')}
                                </span>
                            ` : ''}
                        </div>
                    </div>

                    <div class="flex gap-2">
                        <button class="button-icon-circular" data-action="edit" data-task-id="${task.id}">
                            ✏️
                        </button>
                        <button class="button-icon-circular" data-action="delete" data-task-id="${task.id}">
                            🗑️
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    renderPriorityBadge(priority) {
        if (priority === 'none') return '';

        const colors = {
            low: 'bg-success text-on-primary',
            medium: 'bg-attention text-canvas',
            high: 'bg-critical text-canvas'
        };

        return `<span class="badge-${priority} ${colors[priority]}">${priority}</span>`;
    }

    renderStatusBadge(status) {
        const colors = {
            todo: '',
            in_progress: 'bg-attention text-canvas',
            completed: 'bg-success text-canvas',
            blocked: 'bg-critical text-canvas'
        };

        if (!colors[status]) return '';

        const label = status.replace('_', ' ');
        return `<span class="badge-${status} ${colors[status]}">${label}</span>`;
    }

    formatDueDate(dueDate) {
        const date = new Date(dueDate);
        const now = new Date();
        const diff = date - now;

        if (diff < 0) return `Overdue by ${Math.floor(Math.abs(diff) / (1000 * 60 * 60 * 24))} days`;
        if (diff < 86400000) return `Due today`;
        if (diff < 172800000) return `Due tomorrow`;

        return `Due ${date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}`;
    }

    renderPagination() {
        if (this.tasks.length <= 50) return '';

        return `
            <div class="flex justify-center mt-8">
                <div class="flex gap-2">
                    <button class="button-secondary" id="prev-page">Previous</button>
                    <span class="flex items-center px-4">Page 1 of 2</span>
                    <button class="button-secondary" id="next-page">Next</button>
                </div>
            </div>
        `;
    }

    attachEventListeners() {
        // Search functionality
        const searchInput = document.getElementById('task-search');
        searchInput.addEventListener('input', (e) => {
            this.handleSearch(e.target.value);
        });

        // Filter pills
        const filterPills = document.querySelectorAll('#filter-pills button');
        filterPills.forEach(pill => {
            pill.addEventListener('click', (e) => {
                const status = e.target.dataset.status;
                this.handleFilterChange(status);
            });
        });

        // Sort select
        const sortSelect = document.getElementById('sort-select');
        sortSelect.addEventListener('change', (e) => {
            this.handleSortChange(e.target.value);
        });

        // Task card actions
        this.container.addEventListener('click', (e) => {
            const taskId = e.target.dataset.taskId;
            const action = e.target.dataset.action;

            if (action === 'edit') {
                this.handleEditTask(taskId);
            } else if (action === 'delete') {
                this.handleDeleteTask(taskId);
            } else if (e.target.type === 'checkbox') {
                this.handleToggleComplete(taskId, e.target.checked);
            }
        });
    }

    handleSearch(query) {
        // Emit search event to controller
        const event = new CustomEvent('task:search', { detail: { query } });
        document.dispatchEvent(event);
    }

    handleFilterChange(status) {
        this.filters.status = status;
        this.render();

        const event = new CustomEvent('task:filter', { detail: { filters: this.filters } });
        document.dispatchEvent(event);
    }

    handleSortChange(sortBy) {
        this.sortBy = sortBy;
        this.render();

        const event = new CustomEvent('task:sort', { detail: { sortBy, order: this.sortOrder } });
        document.dispatchEvent(event);
    }

    handleEditTask(taskId) {
        const event = new CustomEvent('task:edit', { detail: { taskId } });
        document.dispatchEvent(event);
    }

    handleDeleteTask(taskId) {
        if (confirm('Are you sure you want to delete this task?')) {
            const event = new CustomEvent('task:delete', { detail: { taskId } });
            document.dispatchEvent(event);
        }
    }

    handleToggleComplete(taskId, completed) {
        const status = completed ? 'completed' : 'todo';
        const event = new CustomEvent('task:update', {
            detail: { taskId, updates: { status } }
        });
        document.dispatchEvent(event);
    }

    updateTasks(tasks) {
        this.tasks = tasks;
        this.render();
    }
}
```

---

## 4. Development Workflow

### 4.1 Local Development Setup

```bash
# 1. Navigate to project directory
cd Dashboardku

# 2. Create initial file structure
mkdir -p src/{css,js/{controllers,models,services,utils,components},assets/{fonts,icons}}

# 3. Start development server
python3 -m http.server 8080

# 4. Open browser
open http://localhost:8080
```

### 4.2 File Structure

```
Dashboardku/
├── index.html              # Main HTML entry point
├── PRD.md                  # Product Requirements Document
├── SRS.md                  # Software Requirements Specification
├── DESIGN.md               # Design System Reference
├── TECHNICAL_ARCHITECTURE.md
├── README.md               # Project documentation
│
├── src/
│   ├── css/
│   │   ├── main.css               # Main entry point
│   │   ├── components.css         # Component styles
│   │   ├── utilities.css          # Custom utilities
│   │   └── design-tokens.css      # Design system tokens
│   │
│   ├── js/
│   │   ├── app.js                 # Application initialization
│   │   ├── controllers/
│   │   │   ├── taskController.js
│   │   │   ├── projectController.js
│   │   │   ├── webhookController.js
│   │   │   └── uiController.js
│   │   ├── models/
│   │   │   ├── Task.js
│   │   │   ├── Project.js
│   │   │   ├── Webhook.js
│   │   │   └── Notification.js
│   │   ├── services/
│   │   │   ├── storageService.js
│   │   │   ├── validationService.js
│   │   │   ├── notificationService.js
│   │   │   └── webhookService.js
│   │   ├── utils/
│   │   │   ├── uuid.js
│   │   │   ├── eventBus.js
│   │   │   ├── validation.js
│   │   │   └── dateUtils.js
│   │   └── components/
│   │       ├── dashboard.js
│   │       ├── taskList.js
│   │       ├── taskForm.js
│   │       └── webhookConfig.js
│   │
│   └── assets/
│       ├── fonts/
│       │   └── optimistic-vf/     # Optimistic VF font files
│       └── icons/
│           └── *.svg              # SVG icons
│
└── tests/                       # Test files
    ├── unit/
    ├── integration/
    └── e2e/
```

### 4.3 Build Process

```bash
# Development (using Tailwind CDN)
# No build process required, just serve static files

# Production Build
# 1. Install Tailwind CLI
npm install -D tailwindcss

# 2. Build CSS
npx tailwindcss -i ./src/css/main.css -o ./dist/main.css --minify

# 3. Copy files to dist
cp -r index.html dist/
cp -r src/assets dist/

# 4. Serve production build
python3 -m http.server 80 --directory dist
```

---

## 5. Testing Strategy

### 5.1 Unit Testing

```javascript
// tests/unit/task.test.js
import { Task } from '../../src/js/models/Task.js';
import { validateTask } from '../../src/js/utils/validation.js';

describe('Task Model', () => {
    test('should create task with valid data', () => {
        const taskData = {
            title: 'Test Task',
            description: 'Test description',
            priority: 'high',
            status: 'todo'
        };

        const task = Task.create(taskData);

        expect(task.id).toBeDefined();
        expect(task.title).toBe('Test Task');
        expect(task.priority).toBe('high');
        expect(task.status).toBe('todo');
    });

    test('should reject task with empty title', () => {
        expect(() => {
            Task.create({ title: '' });
        }).toThrow('Title is required');
    });

    test('should reject task with title too long', () => {
        expect(() => {
            Task.create({ title: 'a'.repeat(201) });
        }).toThrow('Title must be between 1 and 200 characters');
    });

    test('should update task and modify updatedAt', () => {
        const task = Task.create({ title: 'Original' });
        const originalUpdatedAt = task.updatedAt;

        task.update({ title: 'Updated' });

        expect(task.title).toBe('Updated');
        expect(task.updatedAt).not.toBe(originalUpdatedAt);
    });
});
```

### 5.2 Integration Testing

```javascript
// tests/integration/taskWorkflow.test.js
import { TaskController } from '../../src/js/controllers/taskController.js';
import { StorageService } from '../../src/js/services/storageService.js';
import { NotificationService } from '../../src/js/services/notificationService.js';

describe('Task Workflow Integration', () => {
    let taskController;
    let storageService;
    let notificationService;

    beforeEach(async () => {
        storageService = new StorageService();
        await storageService.init();

        notificationService = new NotificationService();

        taskController = new TaskController(storageService, notificationService);
        await taskController.init();
    });

    test('should create task and persist to storage', async () => {
        const taskData = {
            title: 'Integration Test Task',
            description: 'Testing task creation workflow',
            priority: 'medium'
        };

        const task = await taskController.createTask(taskData);

        expect(task.id).toBeDefined();

        const stored = await storageService.getTaskById(task.id);
        expect(stored).toEqual(task);
    });

    test('should create task with webhook and send notification', async () => {
        const webhook = await storageService.saveWebhook({
            name: 'Test Webhook',
            url: 'https://example.com/webhook',
            method: 'POST',
            enabled: true
        });

        const taskData = {
            title: 'Task with Webhook',
            dueDate: new Date(Date.now() + 60000).toISOString(),
            webhookTriggers: [{
                type: 'deadline',
                enabled: true
            }]
        };

        const task = await taskController.createTask(taskData);

        // Wait for notification processing
        await new Promise(resolve => setTimeout(resolve, 2000));

        const notifications = await storageService.getNotificationsByTaskId(task.id);
        expect(notifications.length).toBeGreaterThan(0);
    });
});
```

### 5.3 End-to-End Testing

```javascript
// tests/e2e/userFlow.test.js
describe('User Task Creation Flow', () => {
    beforeEach(() => {
        cy.visit('/');
    });

    test('first-time user creates first task', () => {
        // Welcome screen should be visible
        cy.get('h1').should('contain', 'Welcome to Dashboardku');

        // Click "Get Started"
        cy.contains('Get Started').click();

        // Create project step
        cy.get('#project-name').type('My First Project');
        cy.contains('Continue').click();

        // Skip webhook step
        cy.contains('Skip for now').click();

        // Create task step
        cy.get('#task-title').type('My First Task');
        cy.get('#task-description').type('This is my first task in Dashboardku');
        cy.contains('Create Task').click();

        // Verify task was created
        cy.get('.task-card').should('contain', 'My First Task');
        cy.get('.badge-success').should('contain', 'Task created');
    });

    test('experienced user creates task with webhook', () => {
        // Navigate to task creation
        cy.get('[data-testid="add-task-button"]').click();

        // Fill task form
        cy.get('#task-title').type('Webhook Test Task');
        cy.get('#task-due-date').type('2026-12-31T23:59');
        cy.get('#task-priority').select('high');

        // Configure webhook trigger
        cy.get('[data-testid="add-webhook-trigger"]').click();
        cy.get('[data-testid="trigger-type"]').select('deadline');
        cy.get('[data-testid="trigger-offset"]').type('-1h');

        // Create task
        cy.contains('Create Task').click();

        // Verify task created with webhook
        cy.get('.task-card').should('contain', 'Webhook Test Task');
        cy.get('.badge-high').should('contain', 'high');
        cy.get('.webhook-indicator').should('be.visible');
    });
});
```

---

## 6. Performance Optimization

### 6.1 Optimization Strategies

#### 6.1.1 Lazy Loading
```javascript
// Lazy load components
const loadComponent = async (componentName) => {
    const module = await import(`./components/${componentName}.js`);
    return module.default;
};

// Example usage
document.addEventListener('click', async (e) => {
    if (e.target.matches('[data-component="taskForm"]')) {
        const TaskForm = await loadComponent('taskForm');
        const form = new TaskForm(e.target);
        form.render();
    }
});
```

#### 6.1.2 Virtual Scrolling
```javascript
// Implement virtual scrolling for large task lists
class VirtualScroller {
    constructor(container, itemHeight, renderItem) {
        this.container = container;
        this.itemHeight = itemHeight;
        this.renderItem = renderItem;
        this.visibleItems = Math.ceil(container.clientHeight / itemHeight);
        this.scrollTop = 0;
    }

    render(items) {
        const startIdx = Math.floor(this.scrollTop / this.itemHeight);
        const endIdx = startIdx + this.visibleItems + 1;
        const visibleItems = items.slice(startIdx, endIdx);

        this.container.innerHTML = `
            <div style="height: ${items.length * this.itemHeight}px">
                <div style="transform: translateY(${startIdx * this.itemHeight}px)">
                    ${visibleItems.map(this.renderItem).join('')}
                </div>
            </div>
        `;
    }
}
```

#### 6.1.3 Debouncing Search
```javascript
// Debounce search input
const debounce = (func, wait) => {
    let timeout;
    return (...args) => {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
};

// Usage in search component
searchInput.addEventListener('input', debounce((e) => {
    this.handleSearch(e.target.value);
}, 300));
```

### 6.2 Monitoring

```javascript
// Performance monitoring
class PerformanceMonitor {
    constructor() {
        this.metrics = {};
    }

    startMeasure(operation) {
        this.metrics[operation] = performance.now();
    }

    endMeasure(operation) {
        const duration = performance.now() - this.metrics[operation];
        console.log(`${operation} took ${duration.toFixed(2)}ms`);

        // Log to analytics service in production
        if (typeof gtag !== 'undefined') {
            gtag('event', 'timing_complete', {
                name: operation,
                value: Math.round(duration)
            });
        }

        return duration;
    }

    measureStorageUsage() {
        let total = 0;
        for (let key in localStorage) {
            if (localStorage.hasOwnProperty(key)) {
                total += localStorage[key].length + key.length;
            }
        }

        const percentage = (total / (5 * 1024 * 1024)) * 100;
        console.log(`Storage usage: ${percentage.toFixed(2)}%`);

        return percentage;
    }
}

// Usage
const monitor = new PerformanceMonitor();
monitor.startMeasure('task_creation');
// ... perform operation
monitor.endMeasure('task_creation');
```

---

## 7. Security Considerations

### 7.1 Data Protection

```javascript
// Encrypt sensitive data in localStorage
class EncryptionService {
    constructor() {
        this.key = this.generateKey();
    }

    generateKey() {
        // Simple XOR encryption (not for production use)
        return 'dashboardku-secret-key';
    }

    encrypt(text) {
        let encrypted = '';
        for (let i = 0; i < text.length; i++) {
            encrypted += String.fromCharCode(
                text.charCodeAt(i) ^ this.key.charCodeAt(i % this.key.length)
            );
        }
        return btoa(encrypted);
    }

    decrypt(encoded) {
        const text = atob(encoded);
        let decrypted = '';
        for (let i = 0; i < text.length; i++) {
            decrypted += String.fromCharCode(
                text.charCodeAt(i) ^ this.key.charCodeAt(i % this.key.length)
            );
        }
        return decrypted;
    }
}

// Usage for webhook URLs
const encryptionService = new EncryptionService();
webhook.url = encryptionService.encrypt(webhook.url);
```

### 7.2 Input Sanitization

```javascript
// Sanitize user input to prevent XSS
const sanitizeInput = (input) => {
    const div = document.createElement('div');
    div.textContent = input;
    return div.innerHTML;
};

// Sanitize HTML (if needed)
const sanitizeHTML = (html) => {
    const temp = document.createElement('div');
    temp.textContent = html;
    return temp.innerHTML;
};

// Usage in task creation
const task = {
    title: sanitizeInput(userInput.title),
    description: sanitizeHTML(userInput.description)
};
```

### 7.3 Content Security Policy

```html
<meta http-equiv="Content-Security-Policy" content="
    default-src 'self';
    script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com;
    style-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com;
    font-src 'self';
    connect-src *;
    img-src 'self' data:;
">
```

---

## 8. Deployment Guide

### 8.1 Development Deployment

```bash
# Start development server
python3 -m http.server 8080

# Access at http://localhost:8080
```

### 8.2 Production Deployment

```bash
# Build for production
npm run build

# Build script in package.json
{
  "scripts": {
    "build": "tailwindcss -i ./src/css/main.css -o ./dist/main.css --minify && cp -r index.html src/assets dist/",
    "dev": "python3 -m http.server 8080",
    "start": "python3 -m http.server 80 --directory dist"
  }
}

# Run production server
npm start
```

### 8.3 Static File Hosting

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name dashboardku.example.com;
    root /var/www/dashboardku/dist;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Add security headers
    add_header X-Frame-Options "DENY";
    add_header X-Content-Type-Options "nosniff";
    add_header X-XSS-Protection "1; mode=block";
}
```

**Netlify Deployment:**
```toml
# netlify.toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
```

---

## 9. Maintenance & Updates

### 9.1 Version Management

```javascript
// services/versionService.js
export class VersionService {
    constructor() {
        this.currentVersion = '1.0.0';
        this.migrations = {
            '0.9.0': this.migrateFrom090.bind(this),
            '1.0.0': this.migrateFrom100.bind(this)
        };
    }

    async migrate() {
        const storedVersion = localStorage.getItem('dashboardku_version') || '0.0.0';

        if (storedVersion === this.currentVersion) {
            return; // Already up to date
        }

        // Run migrations in order
        for (const [version, migration] of Object.entries(this.migrations)) {
            if (this.shouldRunMigration(storedVersion, version)) {
                console.log(`Running migration to ${version}`);
                await migration();
            }
        }

        localStorage.setItem('dashboardku_version', this.currentVersion);
        console.log(`Migrated to ${this.currentVersion}`);
    }

    shouldRunMigration(currentVersion, migrationVersion) {
        const current = this.parseVersion(currentVersion);
        const migration = this.parseVersion(migrationVersion);

        return migration.major > current.major ||
               (migration.major === current.major && migration.minor > current.minor);
    }

    parseVersion(version) {
        const [major, minor, patch] = version.split('.').map(Number);
        return { major, minor, patch };
    }

    async migrateFrom090() {
        // Migration logic for version 0.9.0
        const tasks = JSON.parse(localStorage.getItem('dashboardku_tasks') || '[]');

        // Update task structure
        const migrated = tasks.map(task => ({
            ...task,
            webhookTriggers: task.webhookTriggers || []
        }));

        localStorage.setItem('dashboardku_tasks', JSON.stringify(migrated));
    }

    async migrateFrom100() {
        // Migration logic for version 1.0.0
        // (Placeholder for future migrations)
    }
}
```

### 9.2 Error Handling

```javascript
// utils/errorHandler.js
export class ErrorHandler {
    static handle(error, context = '') {
        console.error(`Error in ${context}:`, error);

        // Log to error tracking service (if available)
        if (typeof Sentry !== 'undefined') {
            Sentry.captureException(error, { context });
        }

        // Show user-friendly message
        this.showUserMessage(error);
    }

    static showUserMessage(error) {
        const messages = {
            'Storage quota exceeded': 'Storage is almost full. Please export and archive old tasks.',
            'Network error': 'Unable to connect. Please check your internet connection.',
            'Invalid data': 'There was an error processing your data. Please try again.',
            'default': 'An unexpected error occurred. Please refresh the page.'
        };

        const message = messages[error.message] || messages.default;

        // Show notification
        const notification = document.createElement('div');
        notification.className = 'notification badge-critical';
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => notification.remove(), 5000);
    }
}

// Usage
try {
    await taskService.createTask(taskData);
} catch (error) {
    ErrorHandler.handle(error, 'Task Creation');
}
```

---

## 10. Conclusion

This technical architecture provides a comprehensive blueprint for building Dashboardku as a client-side, browser-based task management system. The modular architecture ensures maintainability, while the service layer provides a clean separation of concerns.

### Key Benefits:
- **Zero Server Dependencies**: Runs entirely in the browser
- **Privacy-Focused**: All data stored locally
- **Performant**: Optimized for speed with lazy loading and virtual scrolling
- **Secure**: Input validation, encryption, and CSP headers
- **Maintainable**: Modular architecture with clear separation of concerns
- **Scalable**: Can handle 10,000+ tasks without performance degradation

### Next Steps:
1. Set up development environment
2. Implement core models (Task, Project, Webhook)
3. Build service layer (Storage, Validation, Notification)
4. Create UI components following design system
5. Implement webhook delivery system
6. Add comprehensive testing
7. Optimize performance and security
8. Deploy to production

---

**Document Status:** Complete
**Last Updated:** August 18, 2026
**Version:** 1.0