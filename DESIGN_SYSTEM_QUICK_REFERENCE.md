# Mo-Wallet UI/UX Design System - Quick Reference

## Color Palette Quick Reference

### Primary Colors
```
Deep Purple (Primary)
RGB: 91, 33, 182 | HEX: #5B21B6 | HSL: 260°, 79%, 43%
├─ Light: #8B5CF6
├─ Dark: #3C0F7B
└─ Darkest: #1F0A47

Emerald (Success)
RGB: 16, 185, 129 | HEX: #10B981 | HSL: 160°, 84%, 39%

Amber (Warning)
RGB: 245, 158, 11 | HEX: #F59E0B | HSL: 45°, 96%, 50%

Red (Danger)
RGB: 239, 68, 68 | HEX: #EF4444 | HSL: 0°, 84%, 60%
```

### Neutral Colors
```
Dark Gray: #1F2937
Medium Gray: #6B7280
Light Gray: #F3F4F6
White: #FFFFFF
Black: #000000 (use sparingly)
```

---

## Visual Component Library

### 1. Card Component
```
┌─────────────────────────────────┐
│ ■ Title                    [×]  │ (Header with icon, title, action)
├─────────────────────────────────┤
│                                 │
│  Content area                   │
│  - Flexible layout              │
│  - Custom content               │
│                                 │
├─────────────────────────────────┤
│ [Button] [Button] [Action]      │ (Optional footer with actions)
└─────────────────────────────────┘

Styles:
- Background: White (#FFFFFF)
- Border: 1px solid #F3F4F6
- Border-radius: 0.75rem
- Padding: 1.5rem
- Shadow: 0 2px 4px rgba(0,0,0,0.1)
- Hover Shadow: 0 4px 8px rgba(0,0,0,0.1)
- Transition: 300ms ease-in-out
```

### 2. Button Variants
```
Primary Button:
┌──────────────────────┐
│ Action Label         │  Background: #5B21B6, White text
└──────────────────────┘  Hover: #4C1D95, Translate-y: -2px

Secondary Button:
┌──────────────────────┐
│ Action Label         │  Border: 1px, Light background
└──────────────────────┘  Text: Dark gray, Hover: bg-gray-200

Danger Button:
┌──────────────────────┐
│ Delete Action        │  Background: #EF4444, White text
└──────────────────────┘  Hover: #DC2626

Disabled Button:
┌──────────────────────┐
│ Action (disabled)    │  Opacity: 50%, Cursor: not-allowed
└──────────────────────┘
```

### 3. Stat Card Component
```
┌─ [Primary] (Left border, 4px)
│ Income
│ KES 50,000
│ ↑ 12% vs last month
│                    [$]
└─────────────────────────────────
```

### 4. Progress Bar Variants
```
Success (Green):
████████░░░░░░░░░░ 60%
.progress-bar { background: #10B981; }

Warning (Amber):
████████████░░░░░░ 75%
.progress-bar { background: #F59E0B; }

Danger (Red):
████████████████░░ 90%
.progress-bar { background: #EF4444; }
```

### 5. Badge System
```
Success Badge:     [✓ Completed]       bg-green-100, text-green-700
Warning Badge:     [⚠ Attention]       bg-amber-100, text-amber-700
Danger Badge:      [✕ Critical]        bg-red-100, text-red-700
Info Badge:        [! Information]     bg-blue-100, text-blue-700
```

### 6. Form Components
```
Label
┌──────────────────────────────┐
│ Input field * (required)     │  Border: 1px solid #D1D5DB
│                              │  Padding: 0.5rem 1rem
└──────────────────────────────┘  Focus: Border #5B21B6, Ring
Helper text or error message

Select/Dropdown:
┌────────────────────────────┐
│ Select an option         ▼ │
└────────────────────────────┘

Toggle:
   [●····] OFF  [····●] ON

Checkbox:
☐ Unchecked
☑ Checked
```

---

## Typography Scale

```
Display (H1):     40px | 2.5rem | Bold 700
Heading 1 (H2):   32px | 2rem   | Bold 700
Heading 2 (H3):   24px | 1.5rem | Semibold 600
Heading 3 (H4):   20px | 1.25rem| Semibold 600
Body Large:       18px | 1.125rem| Regular 400
Body (default):   16px | 1rem   | Regular 400
Body Small:       14px | 0.875rem| Regular 400
Caption:          12px | 0.75rem | Regular 400
Monospace:        14px | 0.875rem| Regular 400

Font Family: 'Inter', 'Segoe UI', Tahoma, Geneva, sans-serif
Line Height:
  - Headings: 1.2
  - Body: 1.5
  - Captions: 1.4
```

---

## Spacing Scale (8px base unit)

```
xs:   4px  (0.25rem)
sm:   8px  (0.5rem)
md:   16px (1rem)    ← Base unit
lg:   24px (1.5rem)
xl:   32px (2rem)
2xl:  48px (3rem)
3xl:  64px (4rem)

Usage:
Padding:     Use consistent spacing (sm, md, lg)
Margins:     Use vertical rhythm (md, lg, xl)
Gaps:        Component spacing (sm, md, lg)
```

---

## Shadow Elevation System

```
Elevation 0 (Flat):
box-shadow: none;

Elevation 1 (Subtle):
box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
← Card, badge, small components

Elevation 2 (Base):
box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
← Default cards, standard elements

Elevation 3 (Medium):
box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
← Card hover, elevated content

Elevation 4 (High):
box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
← Modal, important content

Elevation 5 (Maximum):
box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25);
← Full-screen overlays, dialogs
```

---

## Border Radius Scale

```
xs: 0.25rem (4px)   ← Badges, small components
sm: 0.375rem (6px)  ← Form inputs
md: 0.75rem (12px)  ← Cards, buttons (default)
lg: 1rem (16px)     ← Large cards, modals
xl: 1.5rem (24px)   ← Extra large components
full: 9999px        ← Pills, circles
```

---

## Animation & Transition Speeds

```
Fast:       150ms ease-in-out  ← Hover effects, quick changes
Normal:     300ms ease-in-out  ← Default transitions
Slow:       500ms ease-in-out  ← Page transitions, important changes

Easing Functions:
ease-in:        Ease in
ease-out:       Ease out
ease-in-out:    Ease in and out
linear:         Linear
cubic-bezier(): Custom

Common Animations:
Slide:    transform: translateY/X
Fade:     opacity: 0 → 1
Scale:    transform: scale()
Rotate:   transform: rotate()
```

---

## Responsive Breakpoints

```
Mobile (< 640px):
├─ Single column layouts
├─ Stack vertically
├─ Full-width components
└─ Large touch targets (44x44px min)

Tablet (640px - 1024px):
├─ 2-column layouts
├─ Mixed layouts
├─ Readable width
└─ Balanced spacing

Desktop (> 1024px):
├─ Multi-column layouts
├─ Sidebar navigation
├─ Optimal reading width (~70-80 chars)
└─ Advanced layouts

Grid Columns by breakpoint:
Mobile:   1 column
Tablet:   2 columns
Desktop:  3-4 columns
```

---

## Common Component Specs

### Stat Card
```
Height: Auto (min 120px)
Width: Responsive (1/1 mobile, 1/2 tablet, 1/4 desktop)
Padding: 1.5rem
Border-left: 4px (status color)
Icon: 2rem (32px)
Title: 14px, #6B7280, uppercase, medium weight
Value: 28px, #1F2937, bold
Trend: 14px, color-coded
```

### Budget Card
```
Height: Auto (min 200px)
Width: 300px (300-400px responsive)
Padding: 1.5rem
Category: 20px, semibold
Amount: 18px, medium
Progress bar: 8px height, rounded
Status indicator: Color badge
Actions: Icon buttons (36x36px)
Hover: Lift 5px (transform: translateY(-5px))
```

### Transaction Row
```
Height: 64px
Padding: 1rem
Category icon: 32px (rounded)
Amount: 16px, color-coded
Date: 14px, gray
Actions: Icon buttons (visible on hover)
Hover: Light background (bg-gray-50)
Chevron: Clickable for details
```

---

## States & Interactions

### Button States
```
Normal:   Default styling
Hover:   Shadow increase + slight translate
Active:   Color deepened + slight scale down
Focus:    2px outline ring (3px offset)
Loading:  Spinner + disabled appearance
Disabled: 50% opacity + no hover effects
```

### Form Input States
```
Default:    1px border #D1D5DB, white background
Hover:      Border #9CA3AF
Focus:      Border #5B21B6 + ring
Filled:     Border #6B7280
Error:      Border #EF4444 + error message
Success:    Border #10B981 + check icon
Disabled:   bg-gray-100, gray text, no interaction
```

### Loading States
```
Skeleton:   Light gray pulse animation
Spinner:    CSS spinner or icon animation
Progress:   Indeterminate progress bar
Message:    "Loading..." text with animation
```

---

## Dark Mode Color Adjustments

```
Primary Text:     #F3F4F6 (light)
Secondary Text:   #D1D5DB (medium-light)
Card Background:  #1F2937 (dark gray)
Page Background:  #111827 (darker gray)

Primary Color:    #8B5CF6 (lighter purple)
Success:          #34D399 (lighter green)
Warning:          #FBBF24 (lighter amber)
Danger:           #F87171 (lighter red)
```

---

## Accessibility Checklist

```
Color Contrast:
├─ Text on background: 4.5:1 (normal text)
├─ Large text (18px+): 3:1
├─ Graphics/borders: 3:1
└─ Not conveyed by color alone

Interactive Elements:
├─ Touch targets: 44x44px minimum
├─ Focus indicators: Visible and obvious
├─ Keyboard navigation: All features accessible
└─ Tab order: Logical and intuitive

Images & Media:
├─ Alt text for meaningful images
├─ Video captions
├─ Audio transcripts
└─ SVG: Proper titles/descriptions

Forms:
├─ Labels associated with inputs
├─ Error messages clear & helpful
├─ Required fields indicated
└─ Instructions provided

Text:
├─ Minimum 16px font size
├─ 1.5+ line height
├─ Adequate contrast
└─ No justified alignment only
```

---

## File Structure for Design System

```
styles/
├── variables.css          (CSS custom properties)
├── base.css              (Global styles, reset)
├── typography.css        (Font system)
├── spacing.css           (Spacing utilities)
├── colors.css            (Color palette)
└── animations.css        (Transitions, animations)

components/
├── buttons.css
├── cards.css
├── forms.css
├── badges.css
├── progress.css
├── navigation.css
└── modals.css

utilities/
├── flex.css
├── grid.css
├── text.css
├── sizing.css
├── positioning.css
└── responsive.css

templates/
├── components/
│   ├── button.html
│   ├── card.html
│   ├── stat_card.html
│   ├── form_input.html
│   └── progress_indicator.html
└── layouts/
    ├── base.html
    ├── dashboard.html
    └── full_width.html
```

---

## Implementation Checklist

### Week 1-2 (Design System Foundation)
- [ ] Create CSS custom properties file
- [ ] Define color palette
- [ ] Set up typography scale
- [ ] Create spacing utilities
- [ ] Document all tokens

### Week 3-4 (Component Library)
- [ ] Build button component
- [ ] Build card component
- [ ] Build form components
- [ ] Build progress indicators
- [ ] Build badge system

### Week 5-6 (Page Redesigns)
- [ ] Redesign dashboard
- [ ] Redesign budgets page
- [ ] Redesign transactions page
- [ ] Test responsive behavior
- [ ] Gather feedback

### Week 7-8 (Polish & Optimize)
- [ ] Add animations
- [ ] Implement dark mode
- [ ] Optimize images
- [ ] Performance testing
- [ ] Accessibility audit

---

## Performance Budgets

```
Page Load: < 3 seconds
TTI: < 3.5 seconds
LCP: < 2.5 seconds
FID: < 100ms
CLS: < 0.1

Asset Budgets:
CSS: < 50KB (minified)
JavaScript: < 200KB (minified)
Images: < 500KB total
Fonts: < 100KB

API Response:
Dashboard: < 500ms
Page transitions: < 200ms
```

---

## Brand Voice & Tone

```
Friendly: Use conversational language
Clear: Avoid jargon, be direct
Helpful: Provide guidance and suggestions
Encouraging: Celebrate achievements
Professional: Maintain credibility
Empowering: Give users control

Examples:
✗ "Error 402: Failed to process transaction"
✓ "We couldn't complete that transaction. Try again or contact support."

✗ "Insufficient funds"
✓ "You're short by KES 500. Add funds to continue."

✗ "Goal creation successful"
✓ "Great! Your goal is all set. Let's reach it together! 🎯"
```

---

This quick reference provides all essential design system specifications for consistent implementation across Mo-wallet's frontend.

