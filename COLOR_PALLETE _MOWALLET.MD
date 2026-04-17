# Mo Wallet Design System — Color Reference

This document defines the color system for **Mo Wallet**. It is intended for use by tools like Copilot to ensure consistent styling across the application.

---

## 🎨 Primary Colors

Core palette used across product UI, dashboards, and marketing.

| Name      | Value     | Usage |
|----------|----------|------|
| Primary  | #4318FF  | Main brand color, buttons, highlights |
| Secondary| #0F1535  | Backgrounds, headers, dark sections |
| Info     | #0075FF  | Informational elements, links |
| Success  | #01B574  | Success states, confirmations |
| Warning  | #FFB547  | Alerts, warnings |
| Error    | #E31A1A  | Errors, destructive actions |
| Light    | #E9ECEF  | Light backgrounds, containers |
| Dark     | #344767  | Text, dark UI elements |

---

## 🌈 Gradient Colors

Used for modern UI effects such as cards, buttons, backgrounds.

| Name       | Gradient Value |
|-----------|---------------|
| Primary   | #4318FF → #9F7AEA |
| Secondary | #627594 → #A8B8D8 |
| Info      | #0075FF → #21D4FD |
| Success   | #01B574 → #C9FBD5 |
| Warning   | #F53939 → #FBCF33 |
| Error     | #F53C2B → #F53C2B |
| Light     | #CED4DA → #EBEFF4 |
| Dark      | #141727 → #3A416F |

### Specialized Gradients

| Name     | Value |
|----------|------|
| CardDark | #CED4DA → #EBEFF4 |
| Card     | rgba(6,11,40,0.94) 19.41% → rgba(10,14,35,0.49) 76.65% |
| Bill     | rgba(24,29,60,0.94) 19.41% → rgba(10,14,35,0.49) 76.65% |
| Menu     | #05153F 28.26% → #072561 91.2% |
| Sidenav  | rgba(6,11,40,0.94) 19.41% → rgba(10,14,35,0.49) 76.65% |
| Logo     | #FFFFFF 70.67% → rgba(117,122,140,0) 108.55% |

---

## ⚪ Light Neutrals

Used for backgrounds, borders, and subtle UI separation.

| Shade | Value   |
|------|--------|
| 100  | #EDF2F7 |
| 200  | #E2E8F0 |
| 300  | #CBD5E0 |
| 400  | #A0AEC0 |
| 500  | #718096 |
| 600  | #4A5568 |
| 700  | #2D3748 |
| 800  | #1A202A |
| 900  | #171923 |

---

## ✅ Usage Guidelines

- Use **Primary** for main actions (CTA buttons, active states)
- Use **Secondary/Dark** for layout structure (sidebar, navbar)
- Use **Success / Warning / Error** strictly for system feedback
- Prefer **Gradients** for:
  - Cards
  - Hero sections
  - Financial highlights
- Use **Light Neutrals** for:
  - Backgrounds
  - Dividers
  - Disabled states

---

## 🧠 Copilot Notes

- Maintain consistent spacing and contrast ratios
- Avoid mixing too many gradients in one view
- Ensure accessibility (contrast with text)
- Prefer semantic usage (e.g., success = green, error = red)

---

## Example (CSS Variables)

```css
:root {
  --color-primary: #4318ff;
  --color-secondary: #0f1535;
  --color-info: #0075ff;
  --color-success: #01b574;
  --color-warning: #ffb547;
  --color-error: #e31a1a;
  --color-light: #e9ecef;
  --color-dark: #344767;
}