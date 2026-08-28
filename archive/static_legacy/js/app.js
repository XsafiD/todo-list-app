// Dashboardku - Alpine.js Components
document.addEventListener('alpine:init', () => {

    // Main App Data
    Alpine.data('dashboardApp', () => ({
        projects: [
            { id: 1, name: 'Work', color: 'project-purple', taskCount: 5, activeCount: 3 },
            { id: 2, name: 'Personal', color: 'project-green', taskCount: 8, activeCount: 2 },
            { id: 3, name: 'Ideas', color: 'project-pink', taskCount: 3, activeCount: 3 },
            { id: 4, name: 'Learning', color: 'project-teal', taskCount: 6, activeCount: 4 },
            { id: 5, name: 'Urgent', color: 'project-orange', taskCount: 2, activeCount: 2 },
            { id: 6, name: 'Inbox', color: 'project-blue', taskCount: 12, activeCount: 8 },
        ],
        tasks: [
            { id: 1, title: 'Review project requirements', project: 'Work', priority: 'high', status: 'todo', deadline: '2024-08-20T10:00', completed: false, overdue: false },
            { id: 2, title: 'Update design system documentation', project: 'Work', priority: 'medium', status: 'in_progress', deadline: '2024-08-19T14:00', completed: false, overdue: true },
            { id: 3, title: 'Plan weekend trip', project: 'Personal', priority: 'low', status: 'todo', deadline: '2024-08-25T18:00', completed: false, overdue: false },
            { id: 4, title: 'Read 30 pages of book', project: 'Personal', priority: 'medium', status: 'done', deadline: '2024-08-18T22:00', completed: true, overdue: false },
            { id: 5, title: 'Research new frameworks', project: 'Learning', priority: 'medium', status: 'todo', deadline: '2024-08-21T12:00', completed: false, overdue: false },
            { id: 6, title: 'Build MVP prototype', project: 'Ideas', priority: 'high', status: 'in_progress', deadline: '2024-08-19T16:00', completed: false, overdue: true },
        ],
        newProjectModal: false,
        newTaskModal: false,
        editProject: null,
        newProjectName: '',
        newProjectColor: 'project-blue',
        newTaskTitle: '',
        newTaskProject: 'Inbox',
        newTaskPriority: 'medium',
        newTaskDeadline: '',
        filterProject: 'all',
        filterStatus: 'all',
        searchQuery: '',

        // Computed: Filtered tasks
        get filteredTasks() {
            return this.tasks.filter(task => {
                const matchesProject = this.filterProject === 'all' || task.project === this.filterProject;
                const matchesStatus = this.filterStatus === 'all' || task.status === this.filterStatus;
                const matchesSearch = task.title.toLowerCase().includes(this.searchQuery.toLowerCase());
                return matchesProject && matchesStatus && matchesSearch;
            });
        },

        // Computed: Task statistics
        get stats() {
            const total = this.tasks.length;
            const completed = this.tasks.filter(t => t.completed).length;
            const active = total - completed;
            const overdue = this.tasks.filter(t => t.overdue && !t.completed).length;
            return { total, completed, active, overdue };
        },

        // Format deadline
        formatDeadline(deadlineStr) {
            if (!deadlineStr) return '';
            const date = new Date(deadlineStr);
            const now = new Date();
            const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
            const taskDate = new Date(date.getFullYear(), date.getMonth(), date.getDate());

            const diffTime = taskDate - today;
            const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

            if (diffDays === 0) {
                return `Today ${date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}`;
            } else if (diffDays === 1) {
                return 'Tomorrow';
            } else if (diffDays === -1) {
                return 'Yesterday';
            } else if (diffDays < -1) {
                return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            } else {
                return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
            }
        },

        // Check if task is due today
        isDueToday(deadlineStr) {
            if (!deadlineStr) return false;
            const date = new Date(deadlineStr);
            const now = new Date();
            return date.toDateString() === now.toDateString();
        },

        // Check if task is overdue
        isOverdue(deadlineStr, completed) {
            if (!deadlineStr || completed) return false;
            return new Date(deadlineStr) < new Date();
        },

        // Toggle task completion
        toggleTask(taskId) {
            const task = this.tasks.find(t => t.id === taskId);
            if (task) {
                task.completed = !task.completed;
                task.status = task.completed ? 'done' : 'todo';
                this.showToast(task.completed ? 'Task completed!' : 'Task reopened', 'success');
            }
        },

        // Create new project
        createProject() {
            if (!this.newProjectName.trim()) return;

            const project = {
                id: Date.now(),
                name: this.newProjectName,
                color: this.newProjectColor,
                taskCount: 0,
                activeCount: 0
            };

            this.projects.push(project);
            this.newProjectName = '';
            this.newProjectModal = false;
            this.showToast('Project created!', 'success');
        },

        // Create new task
        createTask() {
            if (!this.newTaskTitle.trim()) return;

            const task = {
                id: Date.now(),
                title: this.newTaskTitle,
                project: this.newTaskProject,
                priority: this.newTaskPriority,
                status: 'todo',
                deadline: this.newTaskDeadline,
                completed: false,
                overdue: this.isOverdue(this.newTaskDeadline, false)
            };

            this.tasks.unshift(task);
            this.newTaskTitle = '';
            this.newTaskProject = 'Inbox';
            this.newTaskPriority = 'medium';
            this.newTaskDeadline = '';
            this.newTaskModal = false;
            this.showToast('Task created!', 'success');
        },

        // Delete task
        deleteTask(taskId) {
            this.tasks = this.tasks.filter(t => t.id !== taskId);
            this.showToast('Task deleted', 'info');
        },

        // Archive project
        archiveProject(projectId) {
            this.projects = this.projects.filter(p => p.id !== projectId);
            this.showToast('Project archived', 'info');
        },

        // Show toast notification
        showToast(message, type = 'info') {
            const toast = document.createElement('div');
            toast.className = `toast ${type}`;
            toast.textContent = message;
            toast.setAttribute('x-data', '{ show: true }');
            document.body.appendChild(toast);

            setTimeout(() => {
                toast.style.animation = 'toast-out 200ms ease-out';
                setTimeout(() => toast.remove(), 200);
            }, 3000);
        },

        // Get priority badge class
        getPriorityBadgeClass(priority) {
            switch (priority) {
                case 'low': return 'badge-priority-low';
                case 'medium': return 'badge-priority-medium';
                case 'high': return 'badge-priority-high';
                default: return 'badge-priority-low';
            }
        },

        // Get status badge class
        getStatusBadgeClass(status) {
            switch (status) {
                case 'todo': return 'bg-gray-200 text-gray-700';
                case 'in_progress': return 'bg-blue-100 text-blue-700';
                case 'done': return 'bg-green-100 text-green-700';
                default: return 'bg-gray-200 text-gray-700';
            }
        },

        // Initialize - update overdue status on load
        init() {
            this.tasks.forEach(task => {
                if (this.isOverdue(task.deadline, task.completed)) {
                    task.overdue = true;
                }
            });
        }
    }));

    // Modal Component
    Alpine.data('modal', (open = false) => ({
        open,

        toggle() {
            this.open = !this.open;
            if (this.open) {
                document.body.style.overflow = 'hidden';
            } else {
                document.body.style.overflow = '';
            }
        },

        close() {
            this.open = false;
            document.body.style.overflow = '';
        }
    }));

    // Dropdown Component
    Alpine.data('dropdown', () => ({
        open: false,

        toggle() {
            this.open = !this.open;
        },

        close() {
            this.open = false;
        },

        init() {
            document.addEventListener('click', (e) => {
                if (!this.$el.contains(e.target)) {
                    this.close();
                }
            });
        }
    }));
});
