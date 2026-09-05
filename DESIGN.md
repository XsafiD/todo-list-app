## Overview

Dashboardku reads as a confident personal task management system with clean, data-dense layouts that prioritize actionable information over decorative flourish. The design voice is functionality-first: cards, lists, and controls dominate above-the-fold real estate, with white space and clear visual hierarchy carrying the rest. The system has a recognizable card-based pattern — white project cards with colored accent tags, paired with floating action buttons for quick task creation.

Inter UI (via Google Fonts) anchors the entire system, ranging from a 32px section header down to a 12px caption. The face's clean geometric forms contribute to the app's no-nonsense, productivity-focused character. Below 768px the system collapses cleanly: project grids stack to single columns, the task list becomes full-width, and action buttons transform into a bottom navigation bar.

**Key Characteristics:**
- Soft gray canvas ({colors.canvas}) carrying white cards with `{rounded.lg}` (8px) corner softening
- Single-tier primary button system: cobalt blue ({colors.primary}) pills for all CTAs
- Inter UI as the universal display + body face with consistent 400–700 weight progression
- Rounded buttons ({rounded.full}) and `{rounded.lg}`/`{rounded.xl}` cards as the dominant geometric signature
- Color-coded project tags for quick visual categorization
- Minimal chrome — the task list IS the surface treatment

## Colors

> Source pages: Dashboard (project grid), Task List view, Project Detail page. Token coverage was identical across all pages — the design system is genuinely unified.

### Brand & Accent
- **Primary Blue** ({colors.primary}): The main CTA color. Used on every "Create task", "Save", "Add project" button.
- **Primary Deep** ({colors.primary-deep}): Pressed-state and dark-surface variant of primary.
- **Primary Soft** ({colors.primary-soft}): Translucent background tint for active states (`{colors.primary-soft}` at 10% alpha).
- **Success Green** ({colors.success}): "Task completed", "Project archived" affirmations. Soft tint `{colors.success-soft}` (10% alpha) untuk background kolom Selesai.
- **Warning Amber** ({colors.warning}): "Deadline approaching", "Overdue" indicators. Soft tint `{colors.warning-soft}` (10% alpha) untuk background kolom Proses.
- **Critical Red** ({colors.critical}): "Missed deadline", "Delete" actions.

### Project Colors (Tags)
- **Project Blue** ({colors.project-blue}): Default project color
- **Project Purple** ({colors.project-purple}): Work category
- **Project Green** ({colors.project-green}): Personal category
- **Project Orange** ({colors.project-orange}): Urgent category
- **Project Pink** ({colors.project-pink}): Ideas category
- **Project Teal** ({colors.project-teal}): Learning category

### Surface
- **Canvas Gray** ({colors.canvas}): Page background.
- **Surface White** ({colors.surface}): Primary card surface and task list background.
- **Surface Soft** ({colors.surface-soft}): Subtle hover states and completed task backgrounds.
- **Hairline Gray** ({colors.hairline}): 1px input border and divider lines.
- **Hairline Soft** ({colors.hairline-soft}): Quieter divider used on cards, section breaks.

### Text
- **Ink Black** ({colors.ink-deep}): Primary headline and task titles.
- **Ink** ({colors.ink}): Standard body and secondary text.
- **Charcoal** ({colors.charcoal}): Tertiary text and form labels.
- **Slate** ({colors.slate}): Section-header copy and supporting microcopy.
- **Steel** ({colors.steel}): Quieter timestamp text and metadata.
- **Stone** ({colors.stone}): Disabled or de-emphasized labels.

> **Tuning WCAG AA (2026-08-27, audit Phase 3):** nilai `steel`/`stone` diredamkan agar teks 12–14px lolos kontras 4.5:1 di atas `surface`, `surface-soft`, dan `canvas`. Teks kecil di atas tint badge/flash memakai varian `{colors.*.ink}` (`success-ink`, `warning-ink`, `critical-ink`, `info-ink`) — varian DEFAULT tetap untuk ikon, fill, dan aksen.

### Semantic
- **Success** ({colors.success}): Task completed, project archived.
- **Warning** ({colors.warning}): Deadline within 24 hours.
- **Critical** ({colors.critical}): Overdue tasks, missed deadlines.
- **Info** ({colors.info}): Informational callouts.

## Typography

### Font Family
**Inter UI** is Dashboardku's typeface. Fallbacks: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif. The variable axes carry from 400 (body, caption) through 500 (subtitle, subheading) up to 700 (display, heading, button labels). The geometric forms and tight spacing create a modern, productive feel.

### Hierarchy

| Token | Size | Weight | Line Height | Letter Spacing | Use |
|---|---|---|---|---|---|
| `{typography.display}` | 32px | 700 | 1.25 | 0 | Page title (Dashboard, Settings) |
| `{typography.heading-lg}` | 24px | 700 | 1.33 | 0 | Section headers (Projects, Tasks) |
| `{typography.heading-md}` | 20px | 500 | 1.40 | 0 | Card titles, project names |
| `{typography.heading-sm}` | 16px | 500 | 1.50 | 0 | Task titles, form labels |
| `{typography.subtitle-md}` | 14px | 500 | 1.43 | 0 | Section subheads |
| `{typography.body-md}` | 14px | 400 | 1.50 | 0 | Primary body text |
| `{typography.body-sm}` | 12px | 400 | 1.50 | 0 | Secondary body, helper text |
| `{typography.caption}` | 12px | 400 | 1.33 | 0 | Timestamps, metadata |
| `{typography.button}` | 14px | 500 | 1.43 | 0 | Button labels |

### Principles
- Consistent 14px base for body and button text creates tight visual rhythm
- 500 weight for subtitles creates hierarchy without shouting
- 700 weight reserved for display and primary headings only
- Letter spacing remains 0 for all scales — Inter is designed for standard spacing

## Layout

### Spacing System
- **Base unit**: 4px increment with 8px as the dominant primary step.
- **Tokens**: `{spacing.xxs}` (4px) · `{spacing.xs}` (8px) · `{spacing.sm}` (12px) · `{spacing.md}` (16px) · `{spacing.lg}` (20px) · `{spacing.xl}` (24px) · `{spacing.xxl}` (32px) · `{spacing.section}` (48px).
- **Section rhythm**: Dashboard sections separate at `{spacing.section}` (48px); task list items stack at `{spacing.md}` (16px).
- **Card internal padding**: Standard `{spacing.lg}` (20px); task cards use `{spacing.md}` (16px).

### Grid & Container
- Dashboard max-width sits around 1200px with 24px gutters.
- The project grid uses 3 columns on desktop, 2 on tablet, 1 on mobile.
- Task list uses single-column full-width layout.

### Whitespace Philosophy
Whitespace is task-density-first. The task list is information-dense with `{spacing.md}` rhythm between tasks. Project cards breathe with `{spacing.xl}` padding. Modal panels use `{spacing.xl}` to `{spacing.xxl}` internal padding for focus.

## Elevation & Depth

The system runs predominantly flat. Elevation is reserved for two interaction layers:

| Level | Treatment | Use |
|---|---|---|
| 0 (flat) | No shadow; `{rounded.lg}` rounding + `{colors.hairline}` border | Default cards, task items |
| 1 (hover) | `rgba(0, 0, 0, 0.08) 0px 2px 8px 0px` | Card hover states, dropdown menus |
| 2 (modal) | `rgba(0, 0, 0, 0.16) 0px 8px 32px 0px` | Modal panels, dialogs |

## Shapes

### Border Radius Scale

| Token | Value | Use |
|---|---|---|
| `{rounded.sm}` | 4px | Tags, small badges |
| `{rounded.md}` | 6px | Checkboxes, radio buttons |
| `{rounded.lg}` | 8px | Cards, inputs, buttons |
| `{rounded.xl}` | 12px | Modal panels |
| `{rounded.full}` | 9999px | Pills, tags, badges |

### Component Geometry
- Task items use `{rounded.lg}` (8px) corners
- Project cards use `{rounded.lg}` (8px) corners
- Color tags are `{rounded.full}` pills
- Buttons are `{rounded.full}` pills

## Components

> Per the productivity-first philosophy, hover states are documented but transitions are kept snappy (150ms).

### Buttons

**`button-primary`** — Blue pill primary CTA for all actions ("Create Task", "Save Project", "Add Reminder").
- Background `{colors.primary}`, text `{colors.surface}`, typography `{typography.button}`, padding `8px 16px`, rounded `{rounded.full}`.
- Hover state `button-primary-hover` brightens background.
- Pressed state `button-primary-pressed` deepens to `{colors.primary-deep}`.
- Disabled state `button-primary-disabled` uses `{colors.stone}` text.

**`button-secondary`** — Outlined ghost CTA for secondary actions ("Cancel", "Close").
- Background transparent, text `{colors.primary}`, border `1px solid {colors.primary}`, typography `{typography.button}`, padding `8px 16px`, rounded `{rounded.full}`.
- Hover fills with `{colors.primary-soft}`.

**`button-ghost`** — Text-only tertiary CTA ("Edit", "Delete").
- Background transparent, text `{colors.ink}`, typography `{typography.body-sm}`, padding `4px 8px`, rounded `{rounded.lg}`.
- Hover background `{colors.surface-soft}`.

**`button-fab`** — Floating action button (mobile only).
- Background `{colors.primary}`, icon color white, 56×56px, rounded `{rounded.full}`, shadow `rgba(0, 0, 0, 0.16) 0px 8px 24px 0px`.

### Cards & Containers

**`card-project`** — White project card with title, task count, color tag.
- Background `{colors.surface}`, rounded `{rounded.lg}`, padding `{spacing.lg}`, border `1px solid {colors.hairline}`, shadow `0 2px 8px rgba(0,0,0,0.04)`.
- Hover: shadow `0 4px 16px rgba(0,0,0,0.08)`.

**`card-task`** — White task item with checkbox, title, metadata.
- Background `{colors.surface}`, rounded `{rounded.lg}`, padding `{spacing.md}`, border `1px solid {colors.hairline}`.
- Completed: background `{colors.surface-soft}`, text `{colors.stone}`.

**`card-modal`** — Modal panel for forms.
- Background `{colors.surface}`, rounded `{rounded.xl}`, padding `{spacing.xl}`, shadow `rgba(0, 0, 0, 0.16) 0px 8px 32px 0px`.

**`section-header`** — Section title with optional action button.
- Typography `{typography.heading-lg}`, padding `{spacing.xl} 0`, border-bottom `1px solid {colors.hairline-soft}`.

### Inputs & Forms

**`text-input`** — Standard form field (task title, project name).
- Background `{colors.surface}`, text `{colors.ink}`, border `1px solid {colors.hairline}`, rounded `{rounded.lg}`, padding `{spacing.md}`, height 40px.

**`text-input-focused`** — Activated state.
- Border switches to `2px solid {colors.primary}`, shadow `0 0 0 3px {colors.primary-soft}`.

**`text-input-error`** — Validation error state.
- Border switches to `1px solid {colors.critical}`; error label below in `{colors.critical}` `{typography.body-sm}`.

**`textarea`** — Multi-line input (task description).
- Same as `text-input` but min-height 80px, resize vertical.

**`select-input`** — Dropdown selector (priority, project).
- Same as `text-input` with chevron icon right.

**`checkbox`** — Task completion checkbox.
- 20×20px, `{rounded.md}`, border `2px solid {colors.hairline}`, background `{colors.surface}`.
- Checked: background `{colors.primary}`, border `{colors.primary}`, white checkmark.

**`date-input`** — Date/time picker for deadline.
- Same as `text-input` with calendar icon.

### Badges & Tags

**`tag-project`** — Color-coded project tag.
- Background varies by project color (see Project Colors), text white, typography `{typography.caption}`, rounded `{rounded.full}`, padding `4px 10px`.

**`badge-priority`** — Priority indicator (Low, Medium, High).
- Low: `{colors.stone}` background, `{colors.stone}` text.
- Medium: `{colors.warning}` background, `{colors.ink}` text.
- High: `{colors.critical}` background, white text.

**`badge-status`** — Status chip (Todo, In Progress, Done).
- Todo: `{colors.stone}` background.
- In Progress: `{colors.info}` background.
- Done: `{colors.success}` background.
- All: white text, typography `{typography.body-sm}`, rounded `{rounded.full}`, padding `4px 10px`.

**`badge-deadline`** — Deadline indicator.
- Upcoming: `{colors.info}` background.
- Today: `{colors.warning}` background.
- Overdue: `{colors.critical}` background.

### Task List

**`task-item`** — Individual task row.
- Layout: checkbox (left) + title + metadata (right: deadline, priority, project tag).
- Spacing: `{spacing.md}` between items.
- Height: 56px minimum.

**`task-item-completed`** — Completed task state.
- Background `{colors.surface-soft}`, text `{colors.stone}`, title strikethrough.

**`task-item-overdue`** — Overdue task state.
- Left border `4px solid {colors.critical}`.

### Task Table

**`table-task`** — Task list as table (project detail, section "Tugas").
- Container: `{colors.surface}`, rounded `{rounded.lg}`, border `1px solid {colors.hairline}`, horizontal scroll wrapper.
- Header: uppercase, `{typography.caption}` (12px, semibold), text `{colors.steel}`, bottom border `1px solid {colors.hairline}`.
- Columns: ✓ toggle | Judul (link) | Prioritas | Status | Deadline | Aksi.
- Row: min padding 12px, bottom border `1px solid {colors.hairline-soft}` (last row none), hover background `{colors.surface-soft}`.
- Mobile (<768px): kolom Prioritas & Status disembunyikan — cukup ✓, Judul, Deadline, Aksi.
- Row actions: "Arsipkan" hanya untuk task `done`.

**`table-task-archived`** — Archived task table (project detail, section "Arsip", collapsed `<details>`).
- Columns: Judul (link, strikethrough `{colors.stone}`) | Selesai | Diarsipkan | Aksi.
- Mobile (<768px): kolom Selesai disembunyikan.
- Row actions: "Buka Kembali" (unarchive) + "Hapus" (via modal konfirmasi dinamis).
- Summary header: judul section + counter badge (`{colors.surface-soft}`, `{rounded.full}`) + chevron yang berputar saat terbuka.

### Navigation

**`top-nav`** — Sticky header with logo, search, user menu.
- Background `{colors.surface}`, height 64px, bottom border `1px solid {colors.hairline}`.
- Logo left (text "Dashboardku" in `{typography.heading-md}`).
- Search center (search input `{rounded.full}`).
- User menu right (avatar + dropdown).

**`bottom-nav-mobile`** — Mobile bottom navigation.
- Background `{colors.surface}`, height 56px, top border `1px solid {colors.hairline}`.
- 4 items: Dashboard, Projects, Tasks, Settings.
- Active item: `{colors.primary}` icon + text.

**`sidebar`** — Desktop side navigation.
- Background `{colors.surface}`, width 240px, right border `1px solid {colors.hairline}`.
- Nav items: Dashboard, Projects, Tasks, Tugas Kanban, Calendar, Settings.
- Active: `{colors.primary-soft}` background + `{colors.primary}` text.

### Signature Components

**`dashboard-grid`** — 3-column project grid on homepage.
- Gap: `{spacing.lg}` (20px).
- Each card: `card-project`.

**`task-list-view`** — Full task list with filters.
- Top: Filters (project, status, priority).
- List: `task-item` stack.
- Bottom: Pagination.

**`kanban-board`** — Board 3 kolom per status (Todo, Proses, Selesai) — drag & drop untuk ubah status.
- Grid 3 kolom desktop (`{spacing.md}` gap), stack 1 kolom mobile.
- Kolom: rounded `{rounded.lg}`, border `1px solid` senada + tint background per status — Todo abu soft (`{colors.hairline}` 40% alpha), Proses `{colors.warning-soft}`, Selesai `{colors.success-soft}`.
- Header: dot aksen 8px + label `{typography.subtitle-md}` + counter pill (`{colors.surface}` bg; teks `{colors.slate}` / `{colors.warning-ink}` / `{colors.success-ink}` per kolom), divider warna senada kolom.
- Saat drag aktif: board dapat class `is-dragging` → area kartu tiap kolom diberi outline 1px dashed sebagai cue drop target.
- Kartu di-drop ke kolom lain → POST status via AJAX → toast; gagal → revert posisi.
- Reorder dalam kolom sama tidak dipersist (tanpa field urutan).

**`kanban-card`** — Kartu task di board, varian kompak `card-task`.
- Background `{colors.surface}`, rounded `{rounded.lg}`, padding `{spacing.md}`, border `1px solid {colors.hairline}`; overdue: left border `4px solid {colors.critical}`.
- Isi: judul (2-line clamp, link ke detail), `badge-priority`, `tag-project`, `badge-deadline`.
- Done: judul `{colors.stone}` + strikethrough (`is-done`).
- Hover: lift `translateY(-2px)` + elevasi level 1; Drag: cursor grab; ghost saat drag = opacity 0.4 + border dashed; kartu terangkat = elevasi level 1; fallback keyboard/touch = tombol "Pindah" ‹ › di footer kartu.

**`project-detail`** — Project overview with stats + task list.
- Header: Project name, color tag, stats (total/active/completed).
- Body: Task list filtered by project.
- Actions: Edit project, archive project.

**`reminder-config`** — Reminder configuration card.
- Reminder type selector (Day H, Relative, Absolute).
- Relative inputs: number + unit (minutes/hours/days).
- Preview: Shows when reminder will trigger.

**`webhook-config`** — Webhook settings panel.
- Input: Endpoint URL, custom headers.
- Template: Message template with variable placeholders.
- Test: Send test notification button.

**`notification-log`** — Notification history list.
- Columns: Time, Task, Status, Response.
- Status badges: Sent (green), Failed (red), Pending (gray).

### Feedback

**`toast`** — Notifikasi singkat untuk aksi cepat tanpa reload (mis. toggle complete via AJAX).
- Posisi: fixed kanan-bawah; di mobile ditumpuk di atas bottom nav (`bottom-20`), di desktop `bottom-6`.
- Max lebar `288px` (max-w-xs), stack vertikal gap `{spacing.xs}`.
- Styling sama dengan flash alert: border + tint background + varian `*-ink` untuk teks, ikon Font Awesome per tipe (success/error/info).
- Container `role="status"` + `aria-live="polite"` agar screen reader mengumumkan.
- Auto-dismiss 4 detik + tombol tutup; animasi masuk `toast-in` 150ms ease-out.

### Keyboard Shortcuts

Shortcut global (aktif saat login, diabaikan saat fokus di input/textarea/select atau dengan modifier Ctrl/Meta/Alt):

| Key | Aksi |
|---|---|
| `n` | Buat tugas baru (navigasi ke form create) |
| `/` | Fokus ke filter pertama di halaman Tugas |
| `Escape` | Tutup modal (sudah berlaku sejak Phase 1) |

## Do's and Don'ts

### Do
- Use `{rounded.full}` for all buttons, tags, and pills.
- Apply `{rounded.lg}` to all cards and inputs.
- Use color tags consistently for project identification.
- Show task metadata (deadline, priority, project) compactly.
- Keep spacing tight — this is a productivity tool, not a marketing site.
- Use consistent 14px base for body text.

### Don't
- Don't use shadows heavier than level 1 — keep it flat.
- Don't use more than 3 colors for project tags — stick to the defined palette.
- Don't add decorative flourishes — the task list IS the design.
- Don't sacrifice density for whitespace — tasks should be scannable.
- Don't use heavy borders — 1px is maximum.

## Responsive Behavior

### Breakpoints
| Name | Width | Key Changes |
|---|---|---|
| Mobile | < 640px | Single column. Project grid 1 column. Bottom nav appears. Fab button for create. |
| Tablet | 640 – 1023px | 2-column project grid. Side nav appears. Task list 2 columns optional. |
| Desktop | ≥ 1024px | 3-column project grid. Full side nav. Task list full-width. |

### Touch Targets
- Buttons render at 40px minimum height.
- Checkboxes are 20×20px with 4px hit padding.
- Task items are 56px minimum height.

### Collapsing Strategy
- **Project grid**: 3 columns → 2 columns → 1 column.
- **Task list**: Remains single-column but expands width.
- **Navigation**: Side nav → top nav → bottom nav (mobile).
- **Modals**: Full-screen on mobile, centered panel on desktop.

## Interactive States

### Transitions
- All transitions: 150ms ease-out.
- Hover states: brightness or shadow only.
- Focus states: ring + shadow.

### Micro-interactions
- Checkbox: Scale(1.1) on press.
- Button: Scale(0.98) on press.
- Card: TranslateY(-2px) on hover.

### Loading States
- Skeleton loaders: Pulse animation on gray blocks.
- Button loading: Spinner replaces text.
- List loading: Skeleton cards in place of items.

## Accessibility

### Color Contrast
- All text meets WCAG AA (4.5:1 minimum).
- Primary buttons: AAA (7:1).
- Input borders: 3:1 minimum for non-text.

### Keyboard Navigation
- Tab order follows visual flow.
- Focus visible on all interactive elements.
- Escape closes modals/dropdowns.
- Modal: fokus pindah ke dalam panel saat dibuka, ter-trap di dalamnya (siklus Tab), dan kembali ke elemen pemicu saat ditutup.

### Screen Reader
- Task items use `<button>` for checkboxes.
- ARIA labels on all icons.
- Live regions for notification updates.

## Animation Guide

1. Keep animations snappy — 150ms is standard.
2. Use transform for performance (no left/top).
3. Minimal easing — ease-out is preferred.
4. No decorative animations — all motion supports function.
5. Loading states use subtle pulse (1.5s duration).

## Known Gaps

- Dark mode tokens not yet defined — **diputuskan ditunda (2026-08-27, Phase 3)**; didefinisikan saat ada kebutuhan nyata.
- Calendar view component not specified — **diputuskan ditunda (2026-08-27, Phase 3)**; list + filter deadline dinilai cukup untuk sekarang.
- Drag-and-drop: **sudah dispesifikasikan** untuk `kanban-board` (lihat §Components → Signature Components) — implementasi SortableJS di `static/js/kanban.js`; reorder intra-kolom belum dipersist (menunggu kebutuhan field urutan).
- Keyboard shortcuts: **sudah dispesifikasikan** (lihat §Components → Keyboard Shortcuts) — implementasi di `static/js/shortcuts.js`.

---

**Created:** 2026-08-18
**Version:** 1.0 - Design System Specification
**Inspired by:** Meta Commerce Design System format
