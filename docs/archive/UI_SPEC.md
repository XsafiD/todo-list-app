# UI Specification
## Dashboardku - Personal Task Management System

**Version:** 1.0
**Date:** August 18, 2026
**Design System:** Meta Commerce Design System (per DESIGN.md)
**Status:** Draft

---

## Table of Contents

1. [Design System Overview](#1-design-system-overview)
2. [Layout & Grid System](#2-layout--grid-system)
3. [Typography System](#3-typography-system)
4. [Color System](#4-color-system)
5. [Spacing System](#5-spacing-system)
6. [Component Specifications](#6-component-specifications)
7. [Screen Specifications](#7-screen-specifications)
8. [Responsive Specifications](#8-responsive-specifications)
9. [Interactive States](#9-interactive-states)
10. [Iconography](#10-iconography)
11. [Animation & Transitions](#11-animation--transitions)
12. [Accessibility Specifications](#12-accessibility-specifications)

---

## 1. Design System Overview

### 1.1 Design Philosophy
Dashboardku follows Meta's commerce design system philosophy:
- **Photography-first**: Large visual elements dominate above-the-fold
- **Dual-CTA pattern**: Primary black pill + secondary ghost outline
- **Typography hierarchy**: Optimistic VF with consistent weight steps
- **Pill-shaped everything**: Buttons, tabs, badges always use full rounding
- **Flat elevation**: Shadows reserved for sticky panels and overlays
- **White canvas base**: Clean, minimal background with strategic accent usage

### 1.2 Core Design Principles
1. **Cobalt Scarcity**: `{colors.primary}` (cobalt) ONLY for webhook CTAs
2. **Black CTA Marketing**: `{colors.ink-button}` for marketing surface buttons
3. **Full Rounding**: `{rounded.full}` (100px) on all buttons and pills
4. **Large Card Rounding**: `{rounded.xxxl}` (32px) for photographic/content cards
5. **Consistent Spacing**: 4px/8px grid system throughout
6. **Typography Rhythm**: 3-tier visual hierarchy (display → heading-md 300 → body 400)

---

## 2. Layout & Grid System

### 2.1 Container & Max-Widths

| Container Type | Max-Width | Usage | Padding |
|----------------|-----------|-------|---------|
| Marketing Container | 1280px | Homepage, dashboard | 32px |
| Content Container | 1080px | Task list, project view | 32px |
| Narrow Container | 720px | Settings, forms | 32px |
| Full-Width Container | 100% | Hero sections, promos | 32px |

### 2.2 Grid System

#### 2.2.1 Base Grid
- **Base Unit**: 4px
- **Primary Step**: 8px
- **Grid Type**: Flexible 12-column grid

#### 2.2.2 Column Spans
```css
/* Tailwind Grid Classes */
.grid-12 {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 24px;  /* {spacing.xl} */
}

.col-span-12 { grid-column: span 12; }
.col-span-8  { grid-column: span 8; }
.col-span-6  { grid-column: span 6; }
.col-span-4  { grid-column: span 4; }
.col-span-3  { grid-column: span 3; }
```

#### 2.2.3 Common Layouts

**3-Up Feature Grid (Homepage Stats)**
```css
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);  /* 4 columns */
  gap: 24px;  /* {spacing.xl} */
  padding: 0 32px;
}
```

**2-Up Task List (Tablet)**
```css
.task-grid-tablet {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}
```

**2-Column Split (Task Form)**
```css
.task-form-layout {
  display: grid;
  grid-template-columns: 58% 42%;  /* Content | Settings */
  gap: 32px;  /* {spacing.xxl} */
}
```

### 2.4 Section Spacing

| Section Type | Top Padding | Bottom Padding |
|--------------|-------------|----------------|
| Hero Section | `{spacing.hero}` (120px) | `{spacing.section}` (64px) |
| Marketing Section | `{spacing.section-lg}` (80px) | `{spacing.section-lg}` (80px) |
| Content Section | `{spacing.section}` (64px) | `{spacing.section}` (64px) |
| Compact Section | `{spacing.section-sm}` (48px) | `{spacing.section-sm}` (48px) |
| Card Stack | `{spacing.xxl}` (32px) | `{spacing.xxl}` (32px) |

---

## 3. Typography System

### 3.1 Font Family
```css
font-family: 'Optimistic VF', 'Montserrat', 'Helvetica', 'Arial', sans-serif;
```

### 3.2 Typography Scale

| Token | Size | Weight | Line Height | Letter Spacing | OpenType | Usage |
|-------|------|--------|-------------|----------------|-----------|-------|
| `hero-display` | 64px | 500 | 1.16 | 0 | ss01, ss02 | Welcome screen hero |
| `display-lg` | 48px | 500 | 1.17 | 0 | ss01, ss02 | Section openers |
| `heading-lg` | 36px | 500 | 1.28 | 0 | ss01, ss02 | Subsection headlines |
| `heading-md` | 28px | 300 | 1.21 | 0 | ss01, ss02 | Editorial subheads |
| `heading-sm` | 24px | 500 | 1.25 | 0 | ss01, ss02 | Card titles, feature headers |
| `subtitle-lg` | 18px | 700 | 1.44 | 0 | — | Bold callouts, FAQ titles |
| `subtitle-md` | 18px | 400 | 1.44 | 0 | — | Body lead, subtitles |
| `body-md` | 16px | 400 | 1.50 | -0.16px | — | Primary body text |
| `body-md-bold` | 16px | 700 | 1.50 | -0.16px | — | Body emphasis, links |
| `body-sm` | 14px | 400 | 1.43 | -0.14px | — | Secondary body, helper text |
| `body-sm-bold` | 14px | 700 | 1.43 | -0.14px | — | Pill tabs, footer headings |
| `caption-bold` | 12px | 700 | 1.33 | 0 | — | Badge labels, timestamps |
| `caption` | 12px | 400 | 1.33 | 0 | — | Footer fine print, legal |
| `button-md` | 14px | 700 | 1.43 | -0.14px | — | Button labels |

### 3.3 Typography Hierarchy Examples

**Hero Section:**
```html
<h1 class="text-hero-display font-medium">
  Welcome to Dashboardku
</h1>
<p class="text-subtitle-md mt-6">
  Your personal task management system
</p>
```

**Section Header:**
```html
<h2 class="text-heading-lg">
  Task Management
</h2>
<p class="text-body-md text-slate mt-4">
  Create, organize, and track your tasks with powerful webhook notifications
</p>
```

**Card Title:**
```html
<h3 class="text-heading-sm">
  Task Statistics
</h3>
```

### 3.4 Text Color Usage

| Token | Color | Usage |
|-------|-------|-------|
| `ink-deep` | #0A1317 | Primary headlines, body text |
| `ink` | #1C1E21 | Standard body text |
| `charcoal` | #434343 | Tertiary body text |
| `slate` | #65676B | Section headers, microcopy |
| `steel` | #8A8D91 | Quieter captions, footer links |
| `stone` | #BCC1C6 | Disabled labels, de-emphasized |

---

## 4. Color System

### 4.1 Brand & Accent Colors

```css
/* Primary (Cobalt) - ONLY for webhook CTAs */
--color-primary: #0064E0;
--color-primary-deep: #0047B3;
--color-primary-soft: rgba(0, 100, 224, 0.15);

/* Marketing CTAs */
--color-ink-button: #0A1317;
--color-on-ink-button: #FFFFFF;

/* Accent Colors */
--color-fb-blue: #1877F2;      /* Form controls */
--color-meta-link: #0081F2;    /* Legacy navigation */
--color-oculus-purple: #1D2B5F; /* VR accents */
```

### 4.2 Surface Colors

```css
--color-canvas: #FFFFFF;           /* Page background */
--color-surface-soft: #F4F4F4;     /* Thumbnails, cards */
--color-hairline: #DADDE1;          /* Input borders */
--color-hairline-soft: #E4E6EB;    /* Card borders */
```

### 4.3 Semantic Colors

```css
/* Success */
--color-success: #31A24C;

/* Attention/Warning */
--color-attention: #FF8800;
--color-warning: #FFDC00;

/* Critical */
--color-critical: #DC3545;
--color-critical-strong: #B02A37;
```

### 4.4 Color Usage Rules

#### 4.4.1 Button Colors
- **Marketing Primary**: `{colors.ink-button}` (black) → Only on marketing surfaces
- **Commerce Primary**: `{colors.primary}` (cobalt) → Only for webhook CTAs
- **Secondary**: Transparent with `{colors.ink-deep}` border
- **Ghost**: Transparent with faint border

#### 4.4.2 Status Badge Colors
- **Success**: `{colors.success}` - Completed, verified, in stock
- **Attention**: `{colors.attention}` - In progress, almost gone
- **Warning**: `{colors.warning}` - Limited time, promotional
- **Critical**: `{colors.critical}` - Overdue, blocked, errors

#### 4.4.3 Text Colors
- **Primary**: `{colors.ink-deep}` - Headlines, body text
- **Secondary**: `{colors.ink}` - Standard body
- **Tertiary**: `{colors.charcoal}` - Supporting text
- **Muted**: `{colors.slate}` - Section headers
- **Quiet**: `{colors.steel}` - Captions
- **Disabled**: `{colors.stone}` - Disabled labels

---

## 5. Spacing System

### 5.1 Spacing Scale

```css
/* Base: 4px with 8px as primary step */
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
```

### 5.2 Spacing Usage Guide

| Use Case | Spacing | Example |
|----------|---------|---------|
| Icon + text | 8px | Button icons, badge labels |
| List items | 12px | Form field groups |
| Related elements | 16px | Input label + input |
| Card internal | 24px | Icon feature cards |
| Card internal | 32px | Product feature cards |
| Section separation | 64px | Content sections |
| Marketing sections | 80px | Landing page sections |
| Hero spacing | 120px | Above/below hero content |

### 5.3 Common Spacing Patterns

**Card Padding:**
```css
/* Standard card */
.card-product-feature {
  padding: var(--spacing-xxl);  /* 32px */
}

/* Compact card */
.card-icon-feature {
  padding: var(--spacing-xl);  /* 24px */
}

/* Promo card */
.card-promo-strip {
  padding: var(--spacing-section);  /* 64px */
}
```

**Form Spacing:**
```css
.form-group {
  margin-bottom: var(--spacing-base);  /* 16px */
}

.form-section {
  margin-bottom: var(--spacing-xl);  /* 24px */
}
```

---

## 6. Component Specifications

### 6.1 Buttons

#### 6.1.1 Button-Primary (Marketing CTA)
**Usage:** Marketing surface CTAs ("Shop", "Create Task", "Get Started")

```css
.btn-primary {
  background: var(--color-ink-button);
  color: var(--color-on-ink-button);
  font: var(--font-bold) 14px/1.43;
  padding: 14px 30px;
  border-radius: var(--rounded-full);
  border: none;
  letter-spacing: -0.14px;
  cursor: pointer;
  transition: all 150ms ease-out;
}

.btn-primary:hover {
  opacity: 0.9;
}

.btn-primary:active {
  background: var(--color-charcoal);
}

.btn-primary:disabled {
  background: var(--color-stone);
  cursor: not-allowed;
  opacity: 0.5;
}
```

**HTML:**
```html
<button class="btn-primary">
  Create Task
</button>
```

**Dimensions:**
- Height: 48px (14px text + 17px top/bottom padding)
- Min-width: 120px
- Border radius: 100px (full pill)

#### 6.1.2 Button-Buy-CTA (Commerce/Webhook CTA)
**Usage:** Webhook configuration CTAs ONLY ("Add Webhook", "Save Webhook")

```css
.btn-buy-cta {
  background: var(--color-primary);
  color: var(--color-on-primary);
  font: var(--font-bold) 14px/1.43;
  padding: 14px 30px;
  border-radius: var(--rounded-full);
  border: none;
  letter-spacing: -0.14px;
  cursor: pointer;
  transition: all 150ms ease-out;
}

.btn-buy-cta:hover {
  background: var(--color-primary-deep);
}

.btn-buy-cta:active {
  opacity: 0.8;
}
```

**Usage Rule:** This variant ONLY appears in webhook configuration and notification-related contexts.

#### 6.1.3 Button-Secondary (Ghost Outline)
**Usage:** Secondary CTAs paired with primary ("Cancel", "Learn More")

```css
.btn-secondary {
  background: transparent;
  color: var(--color-ink-deep);
  font: var(--font-bold) 14px/1.43;
  padding: 12px 28px;
  border: 2px solid var(--color-ink-deep);
  border-radius: var(--rounded-full);
  letter-spacing: -0.14px;
  cursor: pointer;
  transition: all 150ms ease-out;
}

.btn-secondary:hover {
  background: var(--color-surface-soft);
}

.btn-secondary:active {
  background: var(--color-hairline);
}
```

#### 6.1.4 Button-Ghost
**Usage:** Tertiary CTAs ("Skip", "Maybe later")

```css
.btn-ghost {
  background: transparent;
  color: var(--color-ink-deep);
  font: var(--font-bold) 14px/1.43;
  padding: 10px 22px;
  border: 2px solid rgba(10, 19, 23, 0.12);
  border-radius: var(--rounded-full);
  letter-spacing: -0.14px;
  cursor: pointer;
  transition: all 150ms ease-out;
}

.btn-ghost:hover {
  border-color: var(--color-ink-deep);
  background: var(--color-surface-soft);
}
```

#### 6.1.5 Button-Pill-Tab
**Usage:** Category navigation, filter controls

```css
.btn-pill-tab {
  background: var(--color-canvas);
  color: var(--color-ink);
  font: var(--font-bold) 14px/1.43;
  padding: 8px 16px;
  border: 1px solid var(--color-hairline);
  border-radius: var(--rounded-full);
  letter-spacing: -0.14px;
  cursor: pointer;
  transition: all 150ms ease-out;
}

.btn-pill-tab:hover {
  background: var(--color-surface-soft);
}

.btn-pill-tab-active {
  background: var(--color-ink-deep);
  color: var(--color-canvas);
  border-color: var(--color-ink-deep);
}
```

**HTML:**
```html
<div class="filter-tabs">
  <button class="btn-pill-tab">All</button>
  <button class="btn-pill-tab-active">Active</button>
  <button class="btn-pill-tab">Completed</button>
</div>
```

#### 6.1.6 Button-Icon-Circular
**Usage:** Utility buttons (carousel arrows, share, edit, delete)

```css
.btn-icon-circular {
  width: 40px;
  height: 40px;
  background: var(--color-canvas);
  border-radius: var(--rounded-circle);
  border: 1px solid var(--color-hairline-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 150ms ease-out;
}

.btn-icon-circular:hover {
  background: var(--color-surface-soft);
  border-color: var(--color-hairline);
}

/* Mobile: bump to 44px for WCAG AAA */
@media (max-width: 767px) {
  .btn-icon-circular {
    width: 44px;
    height: 44px;
  }
}
```

### 6.2 Cards & Containers

#### 6.2.1 Card-Product-Feature
**Usage:** Task cards, feature showcase cards

```css
.card-product-feature {
  background: var(--color-canvas);
  border-radius: var(--rounded-xxxl);  /* 32px */
  padding: var(--spacing-xxl);  /* 32px */
  border: 1px solid var(--color-hairline-soft);
  box-shadow: none;
  transition: all 150ms ease-out;
}

.card-product-feature:hover {
  box-shadow: rgba(0, 0, 0, 0.2) 1px 1px 0px 0px;
}
```

**HTML Structure:**
```html
<div class="card-product-feature">
  <div class="card-content">
    <!-- Card content here -->
  </div>
</div>
```

**Internal Spacing:**
- Padding: 32px all around
- Content gap: 16px (between heading and body)
- Button spacing: 24px (from content)

#### 6.2.2 Card-Icon-Feature
**Usage:** Stat cards, benefit tiles, small feature cards

```css
.card-icon-feature {
  background: var(--color-canvas);
  border-radius: var(--rounded-xl);  /* 16px */
  padding: var(--spacing-xl);  /* 24px */
  border: 1px solid var(--color-hairline-soft);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card-icon-feature .icon {
  font-size: 32px;
  line-height: 1;
}

.card-icon-feature .title {
  font: var(--font-bold) 18px/1.44;
  color: var(--color-ink-deep);
}

.card-icon-feature .value {
  font: var(--font-medium) 24px/1.25;
  color: var(--color-ink-deep);
}
```

**HTML:**
```html
<div class="card-icon-feature">
  <div class="icon">📋</div>
  <h3 class="title">Total Tasks</h3>
  <p class="value">42</p>
</div>
```

#### 6.2.3 Card-Checkout-Summary
**Usage:** Sticky sidebar panels (task form settings, purchase summary)

```css
.card-checkout-summary {
  background: var(--color-canvas);
  border-radius: var(--rounded-xl);  /* 16px */
  padding: var(--spacing-xl);  /* 24px */
  border: 1px solid var(--color-hairline-soft);
  box-shadow: rgba(20, 22, 26, 0.3) 0px 1px 4px 0px;
  position: sticky;
  top: 32px;
  max-height: calc(100vh - 64px);
  overflow-y: auto;
}
```

**Usage Context:** Only for sticky right-rail panels (42% width, max 380px).

#### 6.2.4 Card-Promo-Strip
**Usage:** Full-width promotional banners, feature callouts

```css
.card-promo-strip {
  background: var(--color-ink-deep);
  color: var(--color-canvas);
  border-radius: var(--rounded-xxxl);  /* 32px */
  padding: var(--spacing-section);  /* 64px */
  margin: var(--spacing-section) 0;
}

.card-promo-strip.yellow {
  background: var(--color-warning);
  color: var(--color-ink-deep);
}
```

#### 6.2.5 Product-Thumbnail
**Usage:** Product/task variant images, project thumbnails

```css
.product-thumbnail {
  background: var(--color-surface-soft);
  border-radius: var(--rounded-xl);  /* 16px */
  padding: var(--spacing-base);  /* 16px */
  aspect-ratio: 1 / 1;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid transparent;
  transition: all 150ms ease-out;
  cursor: pointer;
}

.product-thumbnail:hover,
.product-thumbnail.selected {
  border-color: var(--color-ink-deep);
  background: var(--color-canvas);
}

.product-thumbnail img {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
```

### 6.3 Inputs & Forms

#### 6.3.1 Text-Input
**Usage:** Standard form fields (title, description, URLs)

```css
.text-input {
  background: var(--color-canvas);
  color: var(--color-ink);
  font: var(--font-regular) 16px/1.50;
  padding: var(--spacing-md);  /* 12px */
  height: 44px;
  border: 1px solid var(--color-hairline);
  border-radius: var(--rounded-lg);  /* 8px */
  letter-spacing: -0.16px;
  transition: all 150ms ease-out;
}

.text-input::placeholder {
  color: var(--color-stone);
}

.text-input:hover {
  border-color: var(--color-ink);
}

.text-input:focus {
  outline: none;
  border-color: var(--color-fb-blue);
  border-width: 2px;
  padding: 11px;  /* Adjust for 2px border */
}

.text-input-error {
  border-color: var(--color-critical-strong);
}

.text-input-error + .error-message {
  display: block;
}

.error-message {
  display: none;
  font: var(--font-regular) 14px/1.43;
  color: var(--color-critical-strong);
  margin-top: 8px;
}
```

**HTML:**
```html
<div class="form-group">
  <label for="task-title" class="form-label">Task Title</label>
  <input
    type="text"
    id="task-title"
    class="text-input"
    placeholder="What needs to be done?"
    maxlength="200"
  >
</div>
```

#### 6.3.2 Search-Pill
**Usage:** Search field, quick-add input

```css
.search-pill {
  background: var(--color-surface-soft);
  color: var(--color-steel);
  font: var(--font-regular) 14px/1.43;
  padding: 10px 16px;
  height: 40px;
  border: none;
  border-radius: var(--rounded-full);
  letter-spacing: -0.14px;
}

.search-pill:focus {
  outline: none;
  background: var(--color-canvas);
  color: var(--color-ink);
}

.search-pill::placeholder {
  color: var(--color-steel);
}
```

#### 6.3.3 Radio-Option
**Usage:** Configurator options (priority, status, project selection)

```css
.radio-option {
  background: var(--color-canvas);
  border-radius: var(--rounded-lg);  /* 8px */
  padding: var(--spacing-lg);  /* 20px */
  border: 1px solid rgba(10, 19, 23, 0.12);
  cursor: pointer;
  transition: all 150ms ease-out;
  display: flex;
  align-items: center;
  gap: 12px;
}

.radio-option:hover {
  border-color: var(--color-hairline);
  background: var(--color-surface-soft);
}

.radio-option-selected {
  border: 2px solid #0143b5;  /* Deep cobalt */
  background: var(--color-primary-soft);
}

.radio-option input[type="radio"] {
  appearance: none;
  width: 20px;
  height: 20px;
  border: 2px solid var(--color-hairline);
  border-radius: var(--rounded-circle);
  position: relative;
  cursor: pointer;
}

.radio-option-selected input[type="radio"] {
  border-color: #0143b5;
}

.radio-option-selected input[type="radio"]::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 10px;
  height: 10px;
  background: #0143b5;
  border-radius: var(--rounded-circle);
}
```

**HTML:**
```html
<div class="radio-options-grid">
  <label class="radio-option">
    <input type="radio" name="priority" value="low">
    <span>Low Priority</span>
  </label>
  <label class="radio-option-selected">
    <input type="radio" name="priority" value="medium" checked>
    <span>Medium Priority</span>
  </label>
  <label class="radio-option">
    <input type="radio" name="priority" value="high">
    <span>High Priority</span>
  </label>
</div>
```

#### 6.3.4 Color-Swatch-Circle
**Usage:** Color pickers, priority indicators

```css
.color-swatch-circle {
  width: 32px;
  height: 32px;
  border-radius: var(--rounded-circle);
  border: 2px solid var(--color-canvas);
  cursor: pointer;
  position: relative;
  transition: all 150ms ease-out;
}

.color-swatch-circle:hover {
  transform: scale(1.1);
}

.color-swatch-circle.selected {
  box-shadow: 0 0 0 2px var(--color-canvas),
              0 0 0 4px #0143b5;  /* Selection ring */
}
```

### 6.4 Badges & Status Indicators

#### 6.4.1 Badge-Promo-Yellow
**Usage:** Limited time offers, promotional tags

```css
.badge-promo-yellow {
  background: var(--color-warning);
  color: var(--color-ink-deep);
  font: var(--font-bold) 12px/1.33;
  padding: 4px 10px;
  border-radius: var(--rounded-full);
  display: inline-block;
  letter-spacing: 0;
}
```

#### 6.4.2 Badge-Attention
**Usage:** In progress, almost gone, selling fast

```css
.badge-attention {
  background: var(--color-attention);
  color: var(--color-canvas);
  font: var(--font-bold) 12px/1.33;
  padding: 4px 10px;
  border-radius: var(--rounded-full);
  display: inline-block;
  letter-spacing: 0;
}
```

#### 6.4.3 Badge-Success
**Usage:** Completed, verified, in stock

```css
.badge-success {
  background: var(--color-success);
  color: var(--color-canvas);
  font: var(--font-bold) 12px/1.33;
  padding: 4px 10px;
  border-radius: var(--rounded-full);
  display: inline-block;
  letter-spacing: 0;
}
```

#### 6.4.4 Badge-Critical
**Usage:** Overdue, blocked, errors, out of stock

```css
.badge-critical {
  background: var(--color-critical);
  color: var(--color-canvas);
  font: var(--font-bold) 12px/1.33;
  padding: 4px 10px;
  border-radius: var(--rounded-full);
  display: inline-block;
  letter-spacing: 0;
}
```

### 6.5 Navigation Components

#### 6.5.1 Top Navigation (Desktop)
**Usage:** Main site navigation

```css
.top-nav {
  background: var(--color-canvas);
  height: 64px;
  border-bottom: 1px solid var(--color-hairline-soft);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.top-nav .logo {
  height: 14px;
  width: 61px;
}

.top-nav .nav-center {
  display: flex;
  gap: 8px;
  align-items: center;
}

.top-nav .nav-right {
  display: flex;
  gap: 16px;
  align-items: center;
}
```

**HTML:**
```html
<nav class="top-nav">
  <div class="nav-left">
    <!-- Logo -->
  </div>
  <div class="nav-center">
    <!-- Pill tab navigation -->
  </div>
  <div class="nav-right">
    <!-- Search, account, cart -->
  </div>
</nav>
```

#### 6.5.2 Top Navigation (Mobile)
**Usage:** Mobile navigation with hamburger menu

```css
@media (max-width: 767px) {
  .top-nav .nav-center {
    display: none;  /* Hidden by default */
  }

  .mobile-nav-toggle {
    display: flex;
  }
}
```

#### 6.5.3 Promo Banner
**Usage:** Full-width promotional strip above navigation

```css
.promo-banner {
  background: var(--color-ink-deep);
  color: var(--color-canvas);
  font: var(--font-bold) 14px/1.43;
  padding: var(--spacing-md) var(--spacing-xl);  /* 12px 24px */
  text-align: center;
  position: sticky;
  top: 0;
  z-index: 101;
}

.promo-banner.yellow {
  background: var(--color-warning);
  color: var(--color-ink-deep);
}

.promo-banner a {
  color: inherit;
  text-decoration: underline;
  margin-left: 8px;
}
```

### 6.6 Data Display Components

#### 6.6.1 Tech-Specs-Table
**Usage:** Task details, webhook delivery history, specifications

```css
.tech-specs-table {
  width: 100%;
  border-collapse: collapse;
}

.tech-specs-table tbody tr {
  border-bottom: 1px solid var(--color-hairline-soft);
}

.tech-specs-table tbody tr:last-child {
  border-bottom: none;
}

.tech-specs-table td {
  padding: var(--spacing-base) var(--spacing-xl);  /* 16px 24px */
  vertical-align: top;
}

.tech-specs-table .label {
  font: var(--font-bold) 14px/1.43;
  color: var(--color-ink);
  width: 40%;
}

.tech-specs-table .value {
  font: var(--font-regular) 14px/1.43;
  color: var(--color-charcoal);
  width: 60%;
}

.tech-specs-table .section-header {
  font: var(--font-medium) 24px/1.25;
  color: var(--color-ink-deep);
  padding: var(--spacing-xl) var(--spacing-xl) var(--spacing-base);
}
```

#### 6.6.2 FAQ-Accordion
**Usage:** FAQ sections, expandable content

```css
.faq-accordion-item {
  border-bottom: 1px solid var(--color-hairline-soft);
}

.faq-accordion-question {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-xl) 0;  /* 24px */
  cursor: pointer;
}

.faq-accordion-question .title {
  font: var(--font-bold) 18px/1.44;
  color: var(--color-ink-deep);
}

.faq-accordion-question .icon {
  color: var(--color-steel);
  font-size: 20px;
  transition: transform 150ms ease-out;
}

.faq-accordion-item.expanded .faq-accordion-question .icon {
  transform: rotate(180deg);
}

.faq-accordion-answer {
  display: none;
  padding: 0 var(--spacing-xl) var(--spacing-xl);
  font: var(--font-regular) 16px/1.50;
  color: var(--color-ink);
}

.faq-accordion-item.expanded .faq-accordion-answer {
  display: block;
}
```

---

## 7. Screen Specifications

### 7.1 Dashboard Screen

**Purpose:** Overview of tasks and quick actions

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│                    Hero Band (120px top padding)         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Welcome back!                                    │  │
│  │  Here's your task overview for today              │  │
│  │  [Get Started] [Learn More]                       │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              Feature Icon Row (4 columns, 24px gap)       │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐        │
│  │ 📋      │ │ 📅      │ │ ⚠️      │ │ ✅      │        │
│  │ Total   │ │ Due     │ │ Overdue │ │ Compl.  │        │
│  │ 42      │ │ 5       │ │ 2       │ │ 12      │        │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                   Quick Add Section                        │
│  ┌───────────────────────────────────────────────────┐  │
│  │  🔍 What needs to be done?        [Add Task]      │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                  Upcoming Deadlines                       │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Task Card 1                                       │  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Task Card 2                                       │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

**Components:**
1. **Hero Band Marketing**
   - Typography: `{typography.hero-display}` (64px)
   - Subtitle: `{typography.subtitle-md}` (18px)
   - Padding: `{spacing.hero}` (120px) top, `{spacing.section}` (64px) bottom
   - CTA: `button-primary` + `button-secondary` pair

2. **Feature Icon Row**
   - Grid: 4 columns, 24px gap
   - Component: `card-icon-feature`
   - Icon size: 32px
   - Value typography: `{typography.heading-sm}` (24px)

3. **Quick Add Section**
   - Input: `search-pill` (40px height)
   - Button: `button-primary`

4. **Upcoming Tasks**
   - List of `card-product-feature` components
   - Vertical spacing: 24px gap

### 7.2 Task List Screen

**Purpose:** View and manage all tasks

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│                   Filter & Sort Controls                   │
│  ┌───────────────────────────────────────────────────┐  │
│  │  [All] [Active] [Completed] [Blocked]              │  │
│  │  🔍 Search...                          [Sort by ▼]  │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                      Task List                             │
│  ┌───────────────────────────────────────────────────┐  │
│  │  [✓] Task Title 1               [High] [Active]    │  │
│  │      Description preview...                       │  │
│  │      📅 Due today  🏷️ tag1 tag2              [✏️][🗑️]│  │
│  └───────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────┐  │
│  │  [ ] Task Title 2               [Medium] [Todo]   │  │
│  │      📅 Due tomorrow                           [✏️][🗑️]│  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    Pagination Controls                     │
│  ┌───────────────────────────────────────────────────┐  │
│  │  [Previous]        Page 1 of 3              [Next]  │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

**Components:**
1. **Filter Pills**
   - Component: `button-pill-tab` row
   - Active state: `button-pill-tab-active`
   - Gap: 8px

2. **Search Input**
   - Component: `search-pill`
   - Full width available

3. **Sort Dropdown**
   - Component: `text-input` with select styling

4. **Task Cards**
   - Component: `card-product-feature`
   - Checkbox: 20px
   - Title: `{typography.heading-sm}` (24px)
   - Badges: Priority + Status
   - Metadata: `{typography.body-sm}` (14px)

5. **Pagination**
   - Buttons: `button-secondary`
   - Current page: No button, text display

### 7.3 Task Creation/Edit Screen

**Purpose:** Create or edit tasks with webhook configuration

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│                   2-Column Split (58% | 42%)              │
│  ┌─────────────────────┐ ┌──────────────────────┐      │
│  │   Task Details      │ │   Settings            │      │
│  │  (Left 58%)         │ │   (Right 42%)         │      │
│  │                     │ │                      │      │
│  │  ┌───────────────┐ │ │  ┌────────────────┐  │      │
│  │  │ Title *       │ │ │  │ Priority        │  │      │
│  │  │ [___________] │ │ │  │ [ ] None        │  │      │
│  │  └───────────────┘ │ │  │ [x] Low         │  │      │
│  │                     │ │  │ [ ] Medium      │  │      │
│  │  ┌───────────────┐ │ │  │ [ ] High        │  │      │
│  │  │ Description   │ │ │  └────────────────┘  │      │
│  │  │ [___________] │ │ │                     │      │
│  │  │ [___________] │ │ │  ┌────────────────┐  │      │
│  │  └───────────────┘ │ │  │ Status          │  │      │
│  │                     │ │  │ [ ] Todo        │  │      │
│  │  ┌───────────────┐ │ │  │ [x] In Progress │  │      │
│  │  │ Due Date      │ │ │  │ [ ] Completed   │  │      │
│  │  │ [_______]     │ │  │ [ ] Blocked      │  │      │
│  │  └───────────────┘ │ │  └────────────────┘  │      │
│  │                     │ │                     │      │
│  │  ┌───────────────┐ │ │  ┌────────────────┐  │      │
│  │  │ Webhook Trig. │ │ │  │ [Add Webhook]  │  │      │
│  │  │ [+ Add]       │ │ │  └────────────────┘  │      │
│  │  └───────────────┘ │ │                     │      │
│  │                     │ │  ┌────────────────┐  │      │
│  │  [Cancel]          │ │  │ Webhooks:       │  │      │
│  │  [Create Task]     │ │  │ • Slack         │  │      │
│  │                     │ │  │ • Discord      │  │      │
│  └─────────────────────┘ └──────────────────────┘      │
└─────────────────────────────────────────────────────────┘
```

**Components:**
1. **Left Column (Task Details)**
   - Form fields: `text-input` (44px height)
   - Labels: `{typography.body-sm-bold}` (14px)
   - Description: Textarea, 100px height

2. **Right Column (Settings)**
   - Component: `card-checkout-summary`
   - Sticky positioning: top 32px
   - Max width: 380px

3. **Radio Options**
   - Component: `radio-option`
   - Selected: `radio-option-selected`
   - Vertical gap: 8px

4. **Webhook Configuration**
   - Button: `button-buy-cta` (cobalt)
   - List: Checkbox list with webhook names

5. **Action Buttons**
   - Primary: `button-primary` (Create/Save)
   - Secondary: `button-secondary` (Cancel)

### 7.4 Webhook Configuration Screen

**Purpose:** Configure and test webhook endpoints

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│                   Webhook Management                       │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Webhooks                            [+ Add Webhook] │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    Webhook List                             │
│  ┌───────────────────────────────────────────────────┐  │
│  │  ┌─────────────────┐ ┌─────────────────┐          │  │
│  │  │ Slack Webhook   │ │ Discord         │          │  │
│  │  │ ✓ Enabled       │ │ ✓ Enabled       │          │  │
│  │  │ [Test] [Edit]   │ │ [Test] [Edit]   │          │  │
│  │  └─────────────────┘ └─────────────────┘          │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                 Webhook Configuration Form                 │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Name *                                            │  │
│  │  [Slack Webhook__________________]                 │  │
│  │                                                     │  │
│  │  URL *                                              │  │
│  │  [https://hooks.slack.com/______________]         │  │
│  │                                                     │  │
│  │  HTTP Method                                       │  │
│  │  [x] POST  [ ] GET  [ ] PUT  [ ] PATCH            │  │
│  │                                                     │  │
│  │  Headers (optional)                                │  │
│  │  [+ Add Header]                                    │  │
│  │  ┌─────────────────────────────────────────┐     │  │
│  │  │ Content-Type  │ application/json        │ [X] │     │  │
│  │  └─────────────────────────────────────────┘     │  │
│  │                                                     │  │
│  │  Payload Template (JSON)                           │  │
│  │  ┌─────────────────────────────────────────┐     │  │
│  │  │ {                                        │     │  │
│  │  │   "text": "Task {{title}} is due!"      │     │  │
│  │  │ }                                        │     │  │
│  │  └─────────────────────────────────────────┘     │  │
│  │                                                     │  │
│  │  [Test Webhook]  [Cancel]  [Save Webhook]         │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

**Components:**
1. **Webhook List**
   - Component: `product-thumbnail` cards
   - Grid: 2 or 3 columns
   - Gap: 24px

2. **Configuration Form**
   - Component: `card-checkout-summary`
   - Text inputs: `text-input`
   - Radio buttons: `radio-option` for HTTP method
   - Code editor: JSON template input
   - Buttons: `button-secondary` (Test), `button-primary` (Save)

3. **Test Result Display**
   - Component: `tech-specs-table`
   - Status code, response body, error messages

### 7.5 Project Management Screen

**Purpose:** Create and manage projects

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│                   Project Overview                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Projects                            [+ New Project]│
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    Project List                             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────┐  │
│  │  Work           │ │  Personal       │ │  Health  │  │
│  │  12 tasks       │ │  8 tasks        │ │  5 tasks│  │
│  │  75% complete   │ │  50% complete   │ │  60%    │  │
│  │  [Manage]       │ │  [Manage]       │ │ [Manage]│  │
│  └─────────────────┘ └─────────────────┘ └─────────┘  │
└─────────────────────────────────────────────────────────┘
```

**Components:**
1. **Project Cards**
   - Component: `card-icon-feature`
   - Icon: Project icon or emoji
   - Stats: Task count, completion percentage

2. **Create Project Modal**
   - Form: Title, description, color picker
   - Buttons: `button-primary` (Create), `button-secondary` (Cancel)

### 7.6 Settings Screen

**Purpose:** Application settings and data management

**Layout:**
```
┌─────────────────────────────────────────────────────────┐
│                       Settings                           │
│  ┌───────────────────────────────────────────────────┐  │
│  │  General                                            │  │
│  │  ┌─────────────────────────────────────────┐      │  │
│  │  │ Theme                      [Light ▼]    │      │  │
│  │  │ Default View               [List ▼]     │      │  │
│  │  │ Notifications              [x] Enabled   │      │  │
│  │  └─────────────────────────────────────────┘      │  │
│  └───────────────────────────────────────────────────┘  │
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Data Management                                    │  │
│  │  ┌─────────────────────────────────────────┐      │  │
│  │  │ [Export Data]  [Import Data]            │      │  │
│  │  │ Last backup: 2 hours ago                 │      │  │
│  │  └─────────────────────────────────────────┘      │  │
│  └───────────────────────────────────────────────────┘  │
│                                                          │
│  ┌───────────────────────────────────────────────────┐  │
│  │  About                                              │  │
│  │  Version 1.0.0                                     │  │
│  │  © 2026 Dashboardku                                 │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

---

## 8. Responsive Specifications

### 8.1 Breakpoints

| Breakpoint | Width | Key Changes |
|------------|-------|-------------|
| Mobile Small | < 480px | Hero 24px, single column, stacked layout |
| Mobile Large | 480-767px | Hero 36px, 2-up features, stacked task form |
| Tablet | 768-1023px | Hero 48px, 2/3-up features, side-by-side form |
| Desktop | 1024-1359px | Full features, 58/42 split, full nav |
| Wide Desktop | ≥ 1360px | Same as desktop with wider gutters |

### 8.2 Component Responsive Behavior

#### 8.2.1 Hero Typography
```css
/* Mobile */
@media (max-width: 767px) {
  .hero-title {
    font-size: 36px;  /* {typography.heading-lg} */
  }
}

/* Tablet */
@media (min-width: 768px) {
  .hero-title {
    font-size: 48px;  /* {typography.display-lg} */
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .hero-title {
    font-size: 64px;  /* {typography.hero-display} */
  }
}
```

#### 8.2.2 Feature Grid
```css
/* Mobile: 1 column */
@media (max-width: 767px) {
  .feature-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}

/* Tablet: 2 columns */
@media (min-width: 768px) {
  .feature-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
}

/* Desktop: 4 columns */
@media (min-width: 1024px) {
  .feature-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 24px;
  }
}
```

#### 8.2.3 Task Form Layout
```css
/* Mobile: Stacked */
@media (max-width: 767px) {
  .task-form {
    grid-template-columns: 1fr;
  }

  .task-form .settings-panel {
    order: -1;  /* Settings above content on mobile */
    position: static;
  }
}

/* Desktop: 58/42 split */
@media (min-width: 768px) {
  .task-form {
    grid-template-columns: 58% 42%;
    gap: 32px;
  }

  .task-form .settings-panel {
    position: sticky;
    top: 32px;
  }
}
```

#### 8.2.4 Navigation
```css
/* Mobile: Hamburger menu */
@media (max-width: 767px) {
  .top-nav .nav-center {
    display: none;
  }

  .mobile-nav-toggle {
    display: flex;
  }
}

/* Desktop: Full navigation */
@media (min-width: 768px) {
  .top-nav .nav-center {
    display: flex;
  }

  .mobile-nav-toggle {
    display: none;
  }
}
```

### 8.3 Mobile Optimizations

#### 8.3.1 Touch Targets
```css
/* Minimum 44×44px for all interactive elements */
@media (max-width: 767px) {
  .btn-icon-circular {
    width: 44px;
    height: 44px;
  }

  .color-swatch-circle {
    width: 44px;
    height: 44px;
  }

  /* Add 12px clear hit zone around small elements */
  .small-touch-target {
    padding: 12px;
  }
}
```

#### 8.3.2 Mobile Form Adjustments
```css
@media (max-width: 767px) {
  .text-input,
  .search-pill {
    height: 48px;  /* Increased from 44px */
    font-size: 16px;  /* Prevent iOS zoom */
  }

  .form-group {
    margin-bottom: 20px;  /* Increased spacing */
  }
}
```

---

## 9. Interactive States

### 9.1 Button States

#### 9.1.1 Default State
```css
.btn-primary {
  background: var(--color-ink-button);
  opacity: 1;
}
```

#### 9.1.2 Hover State
```css
.btn-primary:hover {
  opacity: 0.9;
  cursor: pointer;
}
```

#### 9.1.3 Active/Pressed State
```css
.btn-primary:active {
  background: var(--color-charcoal);
  transform: scale(0.98);
}
```

#### 9.1.4 Disabled State
```css
.btn-primary:disabled {
  background: var(--color-stone);
  opacity: 0.5;
  cursor: not-allowed;
}
```

#### 9.1.5 Loading State
```css
.btn-primary.loading {
  position: relative;
  color: transparent;
}

.btn-primary.loading::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: translate(-50%, -50%) rotate(360deg); }
}
```

### 9.2 Input States

#### 9.2.1 Default State
```css
.text-input {
  border: 1px solid var(--color-hairline);
  background: var(--color-canvas);
}
```

#### 9.2.2 Focus State
```css
.text-input:focus {
  outline: none;
  border: 2px solid var(--color-fb-blue);
  padding: 11px;  /* Adjust for 2px border */
}
```

#### 9.2.3 Error State
```css
.text-input-error {
  border: 1px solid var(--color-critical-strong);
  animation: shake 0.3s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  75% { transform: translateX(4px); }
}
```

#### 9.2.4 Disabled State
```css
.text-input:disabled {
  background: var(--color-surface-soft);
  color: var(--color-stone);
  cursor: not-allowed;
}
```

### 9.3 Card States

#### 9.3.1 Default State
```css
.card-product-feature {
  border: 1px solid var(--color-hairline-soft);
  box-shadow: none;
}
```

#### 9.3.2 Hover State
```css
.card-product-feature:hover {
  box-shadow: rgba(0, 0, 0, 0.2) 1px 1px 0px 0px;
  transform: translateY(-1px);
}
```

#### 9.3.3 Active/Selected State
```css
.card-product-feature.selected {
  border: 2px solid var(--color-primary);
  background: var(--color-primary-soft);
}
```

### 9.4 Selection States

#### 9.4.1 Checkbox/Radio States
```css
/* Unchecked */
input[type="checkbox"] {
  appearance: none;
  width: 20px;
  height: 20px;
  border: 2px solid var(--color-hairline);
  border-radius: var(--rounded-xs);
}

/* Checked */
input[type="checkbox"]:checked {
  background: var(--color-fb-blue);
  border-color: var(--color-fb-blue);
}

input[type="checkbox"]:checked::after {
  content: '✓';
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 14px;
  height: 100%;
}

/* Indeterminate */
input[type="checkbox"]:indeterminate {
  background: var(--color-fb-blue);
  border-color: var(--color-fb-blue);
}
```

---

## 10. Iconography

### 10.1 Icon System

**Icon Source:** Custom SVG icons or emoji for MVP

**Icon Sizes:**
```css
.icon-xs { width: 12px; height: 12px; }
.icon-sm { width: 16px; height: 16px; }
.icon-md { width: 20px; height: 20px; }
.icon-lg { width: 24px; height: 24px; }
.icon-xl { width: 32px; height: 32px; }
.icon-2x { width: 40px; height: 40px; }
```

### 10.2 Icon Usage Guidelines

#### 10.2.1 Functional Icons
```css
/* Edit, delete, share buttons */
.btn-icon-circular .icon {
  font-size: 18px;
  line-height: 1;
}
```

#### 10.2.2 Decorative Icons
```css
/* Feature cards, stats */
.card-icon-feature .icon {
  font-size: 32px;
  line-height: 1;
}
```

#### 10.2.3 Status Icons
```css
/* Badges, status indicators */
.badge-icon {
  font-size: 12px;
  margin-right: 4px;
}
```

### 10.3 Common Icons

| Purpose | Icon | Size |
|---------|------|------|
| Task | 📋 | 32px |
| Calendar/Due Date | 📅 | 16px |
| Priority | ⚡ | 16px |
| Project | 📁 | 16px |
| Settings | ⚙️ | 20px |
| Edit | ✏️ | 18px |
| Delete | 🗑️ | 18px |
| Check/Complete | ✅ | 16px |
| Warning | ⚠️ | 32px |
| Overdue | 🔴 | 16px |
| Webhook | 🔗 | 16px |
| Notification | 🔔 | 16px |
| Search | 🔍 | 16px |
| Menu | ☰ | 24px |
| Close | × | 24px |

---

## 11. Animation & Transitions

### 11.1 Transition Timing

```css
/* Fast transitions (hover, focus) */
.transition-fast {
  transition: all 150ms ease-out;
}

/* Standard transitions (expand/collapse) */
.transition-standard {
  transition: all 250ms ease-in-out;
}

/* Slow transitions (page transitions) */
.transition-slow {
  transition: all 350ms ease-in-out;
}
```

### 11.2 Common Animations

#### 11.2.1 Fade In
```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in {
  animation: fadeIn 300ms ease-out;
}
```

#### 11.2.2 Slide In
```css
@keyframes slideIn {
  from {
    transform: translateX(-100%);
  }
  to {
    transform: translateX(0);
  }
}

.slide-in {
  animation: slideIn 250ms ease-out;
}
```

#### 11.2.3 Scale In
```css
@keyframes scaleIn {
  from {
    transform: scale(0.9);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.scale-in {
  animation: scaleIn 200ms ease-out;
}
```

#### 11.2.4 Spinner
```css
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.spinner {
  animation: spin 0.6s linear infinite;
}
```

### 11.3 Animation Usage Guidelines

1. **Button Interactions**: 150ms ease-out
2. **Expand/Collapse**: 300ms ease-in-out
3. **Page Transitions**: 350ms ease-in-out
4. **Loading States**: 600ms linear (spinner)
5. **Success Feedback**: 200ms ease-out (scale in)
6. **Error Feedback**: 300ms ease-in-out (shake)

---

## 12. Accessibility Specifications

### 12.1 WCAG 2.1 AA Compliance

#### 12.1.1 Color Contrast
```css
/* Minimum contrast ratios */
.text-on-primary {      /* 4.5:1 */
  color: var(--color-on-primary);
  background: var(--color-primary);
}

.text-on-canvas {       /* 4.5:1 */
  color: var(--color-ink-deep);
  background: var(--color-canvas);
}

.text-large-on-primary {  /* 3:1 for large text ≥18px */
  font-size: 18px;
  color: var(--color-on-primary);
  background: var(--color-primary);
}
```

#### 12.1.2 Focus Indicators
```css
/* Visible focus on all interactive elements */
:focus-visible {
  outline: 2px solid var(--color-fb-blue);
  outline-offset: 2px;
}

/* Remove default focus, replace with custom */
button:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--color-fb-blue);
}
```

#### 12.1.3 Touch Targets
```css
/* Minimum 44×44px for mobile */
@media (max-width: 767px) {
  .touch-target {
    min-width: 44px;
    min-height: 44px;
  }
}
```

### 12.2 Screen Reader Support

#### 12.2.1 ARIA Labels
```html
<!-- Icon buttons -->
<button class="btn-icon-circular" aria-label="Edit task">
  ✏️
</button>

<!-- Status indicators -->
<span class="badge-success" role="status" aria-live="polite">
  Completed
</span>

<!-- Form fields -->
<label for="task-title">Task Title</label>
<input
  type="text"
  id="task-title"
  aria-required="true"
  aria-invalid="false"
  aria-describedby="title-help"
>
<span id="title-help" class="helper-text">
  Enter a descriptive title for your task
</span>
```

#### 12.2.2 Live Regions
```html
<!-- Dynamic content updates -->
<div aria-live="polite" aria-atomic="true" class="notification">
  Task created successfully
</div>

<!-- Status updates -->
<span aria-live="polite" class="status-indicator">
  Saving...
</span>
```

#### 12.2.3 Navigation Landmarks
```html
<nav aria-label="Main navigation">
  <!-- Navigation content -->
</nav>

<main aria-label="Main content">
  <!-- Page content -->
</main>

<aside aria-label="Task settings">
  <!-- Sidebar content -->
</aside>
```

### 12.3 Keyboard Navigation

#### 12.3.1 Tab Order
```html
<!-- Logical tab order -->
<div class="task-card">
  <button aria-label="Mark as complete">✓</button>
  <h3>Task Title</h3>
  <button aria-label="Edit task">✏️</button>
  <button aria-label="Delete task">🗑️</button>
</div>
```

#### 12.3.2 Keyboard Shortcuts
```javascript
// Global shortcuts
const shortcuts = {
  'Alt+N': 'focus-new-task',
  'Alt+F': 'focus-search',
  'Alt+T': 'focus-task-list',
  'Escape': 'close-modal',
  'Enter': 'submit-form'
};

// Task list navigation
const taskListShortcuts = {
  'j': 'next-task',
  'k': 'previous-task',
  'x': 'toggle-complete',
  'e': 'edit-task',
  'd': 'delete-task'
};
```

### 12.4 Error Handling

#### 12.4.1 Error Messages
```html
<!-- Inline error messages -->
<div class="form-group">
  <label for="task-title">Task Title</label>
  <input
    type="text"
    id="task-title"
    aria-invalid="true"
    aria-describedby="title-error"
  >
  <span id="title-error" class="error-message" role="alert">
    Title is required and must be between 1 and 200 characters
  </span>
</div>
```

#### 12.4.2 Validation Feedback
```css
/* Visual feedback */
.text-input-error {
  border: 1px solid var(--color-critical-strong);
  animation: shake 300ms ease-in-out;
}

/* Screen reader feedback */
.error-message {
  display: block;
  color: var(--color-critical-strong);
  font: var(--font-regular) 14px/1.43;
}
```

---

## 13. Component Library Reference

### 13.1 Button Variants

| Variant | Class | Usage | Border |
|---------|-------|-------|--------|
| Primary | `.btn-primary` | Marketing CTAs | None |
| Buy CTA | `.btn-buy-cta` | Webhook CTAs | None |
| Secondary | `.btn-secondary` | Secondary actions | 2px solid |
| Ghost | `.btn-ghost` | Tertiary actions | 2px faint |
| Pill Tab | `.btn-pill-tab` | Navigation/filters | 1px |
| Icon Circular | `.btn-icon-circular` | Utility buttons | 1px |

### 13.2 Card Variants

| Variant | Class | Rounding | Padding | Shadow |
|---------|-------|----------|---------|--------|
| Product Feature | `.card-product-feature` | 32px | 32px | None |
| Icon Feature | `.card-icon-feature` | 16px | 24px | None |
| Checkout Summary | `.card-checkout-summary` | 16px | 24px | Subtle |
| Promo Strip | `.card-promo-strip` | 32px | 64px | None |
| Product Thumbnail | `.product-thumbnail` | 16px | 16px | None |

### 13.3 Badge Variants

| Variant | Class | Background | Text |
|---------|-------|------------|------|
| Promo Yellow | `.badge-promo-yellow` | Warning | Ink-deep |
| Success | `.badge-success` | Success | Canvas |
| Attention | `.badge-attention` | Attention | Canvas |
| Critical | `.badge-critical` | Critical | Canvas |

### 13.4 Input Variants

| Variant | Class | Height | Border | Focus |
|---------|-------|--------|--------|-------|
| Text Input | `.text-input` | 44px | 1px | 2px blue |
| Search Pill | `.search-pill` | 40px | None | Background |
| Radio Option | `.radio-option` | Auto | 1px | 2px blue |

---

## 14. Implementation Notes

### 14.1 Tailwind CSS Configuration

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        // Brand colors
        primary: '#0064E0',
        'primary-deep': '#0047B3',
        'primary-soft': 'rgba(0, 100, 224, 0.15)',

        // Marketing colors
        'ink-button': '#0A1317',
        'on-ink-button': '#FFFFFF',

        // Surface colors
        canvas: '#FFFFFF',
        'surface-soft': '#F4F4F4',
        hairline: '#DADDE1',
        'hairline-soft': '#E4E6EB',

        // Text colors
        'ink-deep': '#0A1317',
        ink: '#1C1E21',
        charcoal: '#434343',
        slate: '#65676B',
        steel: '#8A8D91',
        stone: '#BCC1C6',

        // Semantic colors
        success: '#31A24C',
        attention: '#FF8800',
        warning: '#FFDC00',
        critical: '#DC3545',
        'critical-strong': '#B02A37',
      },

      fontFamily: {
        sans: ['Optimistic VF', 'Montserrat', 'sans-serif'],
      },

      fontSize: {
        'hero-display': ['64px', { lineHeight: '1.16', letterSpacing: '0' }],
        'display-lg': ['48px', { lineHeight: '1.17', letterSpacing: '0' }],
        'heading-lg': ['36px', { lineHeight: '1.28', letterSpacing: '0' }],
        'heading-md': ['28px', { lineHeight: '1.21', letterSpacing: '0', fontWeight: '300' }],
        'heading-sm': ['24px', { lineHeight: '1.25', letterSpacing: '0' }],
        'subtitle-lg': ['18px', { lineHeight: '1.44', letterSpacing: '0', fontWeight: '700' }],
        'subtitle-md': ['18px', { lineHeight: '1.44', letterSpacing: '0', fontWeight: '400' }],
        'body-md': ['16px', { lineHeight: '1.50', letterSpacing: '-0.16px' }],
        'body-md-bold': ['16px', { lineHeight: '1.50', letterSpacing: '-0.16px', fontWeight: '700' }],
        'body-sm': ['14px', { lineHeight: '1.43', letterSpacing: '-0.14px' }],
        'body-sm-bold': ['14px', { lineHeight: '1.43', letterSpacing: '-0.14px', fontWeight: '700' }],
        'caption-bold': ['12px', { lineHeight: '1.33', letterSpacing: '0', fontWeight: '700' }],
        'caption': ['12px', { lineHeight: '1.33', letterSpacing: '0' }],
        'button-md': ['14px', { lineHeight: '1.43', letterSpacing: '-0.14px', fontWeight: '700' }],
      },

      spacing: {
        'xxs': '4px',
        'xs': '8px',
        'sm': '10px',
        'md': '12px',
        'base': '16px',
        'lg': '20px',
        'xl': '24px',
        'xxl': '32px',
        'xxxl': '40px',
        'section-sm': '48px',
        'section': '64px',
        'section-lg': '80px',
        'hero': '120px',
      },

      borderRadius: {
        'xxs': '2px',
        'sm': '4px',
        'md': '6px',
        'lg': '8px',
        'xl': '16px',
        'xxl': '24px',
        'xxxl': '32px',
        'feature': '40px',
        'full': '100px',
      },
    },
  },
  plugins: [
    // Add custom utilities if needed
  ],
};
```

### 14.2 Custom CSS Utilities

```css
/* src/css/utilities.css */

/* OpenType features for headings */
.font-ss01-ss02 {
  font-feature-settings: 'ss01' on, 'ss02' on;
}

/* Custom shadows */
.shadow-subtle {
  box-shadow: rgba(0, 0, 0, 0.2) 1px 1px 0px 0px;
}

.shadow-sticky {
  box-shadow: rgba(20, 22, 26, 0.3) 0px 1px 4px 0px;
}

/* Custom transitions */
.transition-fast {
  transition: all 150ms ease-out;
}

.transition-standard {
  transition: all 250ms ease-in-out;
}

/* Focus styles */
.focus-ring:focus-visible {
  outline: 2px solid #1877F2;
  outline-offset: 2px;
}

/* Loading states */
.loading-spinner {
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Animations */
.fade-in {
  animation: fadeIn 300ms ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.shake {
  animation: shake 300ms ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  75% { transform: translateX(4px); }
}
```

---

## 15. Design Tokens Reference

### 15.1 Complete Token List

```css
:root {
  /* === BRAND COLORS === */
  --color-primary: #0064E0;
  --color-primary-deep: #0047B3;
  --color-primary-soft: rgba(0, 100, 224, 0.15);
  --color-fb-blue: #1877F2;
  --color-meta-link: #0081F2;
  --color-oculus-purple: #1D2B5F;

  /* === BUTTON COLORS === */
  --color-ink-button: #0A1317;
  --color-on-ink-button: #FFFFFF;
  --color-on-primary: #FFFFFF;
  --color-disabled-text: #BCC1C6;

  /* === SURFACE COLORS === */
  --color-canvas: #FFFFFF;
  --color-surface-soft: #F4F4F4;
  --color-hairline: #DADDE1;
  --color-hairline-soft: #E4E6EB;

  /* === TEXT COLORS === */
  --color-ink-deep: #0A1317;
  --color-ink: #1C1E21;
  --color-charcoal: #434343;
  --color-slate: #65676B;
  --color-steel: #8A8D91;
  --color-stone: #BCC1C6;

  /* === SEMANTIC COLORS === */
  --color-success: #31A24C;
  --color-attention: #FF8800;
  --color-warning: #FFDC00;
  --color-critical: #DC3545;
  --color-critical-strong: #B02A37;

  /* === TYPOGRAPHY === */
  --font-family: 'Optimistic VF', 'Montserrat', sans-serif;
  --font-light: 300;
  --font-regular: 400;
  --font-medium: 500;
  --font-bold: 700;

  /* === SPACING === */
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

  /* === BORDER RADIUS === */
  --rounded-xxs: 2px;
  --rounded-sm: 4px;
  --rounded-md: 6px;
  --rounded-lg: 8px;
  --rounded-xl: 16px;
  --rounded-xxl: 24px;
  --rounded-xxxl: 32px;
  --rounded-feature: 40px;
  --rounded-full: 100px;
  --rounded-circle: 50%;

  /* === SHADOWS === */
  --shadow-subtle: rgba(0, 0, 0, 0.2) 1px 1px 0px 0px;
  --shadow-sticky: rgba(20, 22, 26, 0.3) 0px 1px 4px 0px;

  /* === TRANSITIONS === */
  --transition-fast: 150ms ease-out;
  --transition-standard: 250ms ease-in-out;
  --transition-slow: 350ms ease-in-out;
}
```

---

## 16. Design Checklist

### 16.1 Pre-Implementation Checklist

- [ ] All colors use design tokens (no hardcoded values)
- [ ] All typography uses design tokens with proper weights
- [ ] All spacing uses 4px/8px grid system
- [ ] All buttons use `{rounded.full}` (100px)
- [ ] All cards use appropriate rounding (`{rounded.xxxl}` or `{rounded.xl}`)
- [ ] `{colors.primary}` (cobalt) ONLY used for webhook CTAs
- [ ] Marketing CTAs use `{colors.ink-button}` (black)
- [ ] All headings use `ss01, ss02` stylistic sets
- [ ] All interactive elements have proper focus states
- [ ] All color contrasts meet WCAG 2.1 AA standards
- [ ] Touch targets are minimum 44×44px on mobile
- [ ] All animations use appropriate timing functions
- [ ] All forms have proper labels and error messages
- [ ] All icons have proper aria-labels
- [ ] Navigation follows logical tab order

### 16.2 Component Verification Checklist

For each component:
- [ ] Spacing follows 4px/8px grid
- [ ] Border radius matches specification
- [ ] Colors use design tokens
- [ ] Typography uses correct token
- [ ] Interactive states defined
- [ ] Responsive behavior specified
- [ ] Accessibility attributes included
- [ ] Animation timing specified

---

## 17. Appendix

### 17.1 Design System Alignment

This UI specification aligns with Meta's commerce design system as defined in DESIGN.md. All components, colors, typography, and spacing follow the established patterns with these adaptations:

1. **Cobalt Usage**: Extended for webhook CTAs (primary use case)
2. **Component Extensions**: Added task-specific components
3. **Badge System**: Adapted for task statuses
4. **Icon System**: Simplified for MVP (emoji/icons)
5. **Animation Patterns**: Consistent with Meta's motion principles

### 17.2 Browser Compatibility

| Browser | Minimum Version | Notes |
|---------|-----------------|-------|
| Chrome | 90+ | Full support |
| Firefox | 88+ | Full support |
| Safari | 14+ | Full support |
| Edge | 90+ | Full support |
| Mobile Safari | 14+ | Full support |
| Chrome Mobile | 90+ | Full support |

### 17.3 Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Initial Page Load | < 2s | Navigation Timing |
| Time to Interactive | < 3s | Navigation Timing |
| First Contentful Paint | < 1s | Navigation Timing |
| Interaction Readiness | < 100ms | Event Timing |

---

**Document Status:** Complete
**Version:** 1.0
**Last Updated:** August 18, 2026
**Maintained By:** Design Team

---

## Quick Reference

### Common Component Patterns

```html
<!-- Primary Button -->
<button class="btn-primary">Create Task</button>

<!-- Secondary Button -->
<button class="btn-secondary">Cancel</button>

<!-- Webhook CTA Button -->
<button class="btn-buy-cta">Add Webhook</button>

<!-- Product Feature Card -->
<div class="card-product-feature">
  <h3>Task Title</h3>
  <p>Task description</p>
  <button class="btn-primary">Action</button>
</div>

<!-- Icon Feature Card -->
<div class="card-icon-feature">
  <div class="icon">📋</div>
  <h3>Total Tasks</h3>
  <p>42</p>
</div>

<!-- Text Input -->
<input type="text" class="text-input" placeholder="Enter text...">

<!-- Search Pill -->
<input type="text" class="search-pill" placeholder="Search...">

<!-- Badge -->
<span class="badge-success">Completed</span>

<!-- Pill Tab -->
<button class="btn-pill-tab">All Tasks</button>
<button class="btn-pill-tab-active">Active</button>

<!-- Icon Button -->
<button class="btn-icon-circular" aria-label="Edit">✏️</button>
```