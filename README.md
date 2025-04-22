# Mo-wallet
Its a personal finance management system that uses django for backend

# Personal Finance Management System

## Overview
The **Personal Finance Management System** is a powerful tool designed to help users manage their finances efficiently. With features like transaction tracking, budget management, and goal setting, it provides a comprehensive solution for personal financial planning.

## Features
- **User Accounts**: Secure registration and authentication for personalized experiences.
- **Account Management**: Create and manage multiple account types (Savings, Checking, Investment, Credit).
- **Transaction Tracking**: Record income, expenses, and transfers with detailed categorization.
- **Budget Management**: Set spending limits and track progress in various categories.
- **Goal Setting**: Define financial goals and monitor progress towards achieving them.
- **Reports and Insights**: Generate reports to analyze spending and saving patterns.

## Tech Stack

**Backend:**
- Python 3.10+
- Django 5.x
- Django REST Framework (for APIs)
- Celery + Redis (for background tasks)
- PostgreSQL (recommended for production)
- Gunicorn or uWSGI (production WSGI server)
- Nginx (reverse proxy/static file server)

**Frontend:**
- HTML5, CSS3 (custom styles, CSS variables)
- JavaScript (ES6+)
- Chart.js (for analytics and dashboard charts)
- Bootstrap 5 or Tailwind CSS (optional, for rapid UI development)
- FontAwesome (for icons)

**Templates:**
- Django Templates
- (Optional) React or Vue.js for SPA

**Other:**
- Docker (for containerization)
- Git (version control)
- pytest or Django’s test framework (testing)
- Sentry (error monitoring)
- Black/flake8/isort (code formatting/linting)
- Pre-commit hooks (code quality)

---

## Installation
### Prerequisites
- Python 3.8 or higher
- MySQL Server
- Git (optional but recommended)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/personal-finance-management.git
   cd personal-finance-management
   ```
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your database:
   - Update `settings.py` with your MySQL credentials.
   - Run migrations:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```
6. Access the application in your browser at `http://127.0.0.1:8000/`.

## Usage
1. **Sign Up**: Create a new account.
2. **Add Accounts**: Define financial accounts and set initial balances.
3. **Record Transactions**: Add income, expenses, or transfers with relevant details.
4. **Set Budgets**: Create budgets for various categories and monitor progress.
5. **Define Goals**: Set financial goals and track your journey towards achieving them.
6. **Generate Reports**: View insights and detailed analytics on your financial activities.

---

## Project Structure (Recommended)

```
Mo-wallet/
│
├── Mowallet/                # Django project settings
│
├── apps/                    # All Django apps here for clarity
│   ├── analytics/
│   ├── budget/
│   ├── core/
│   ├── goals/
│   ├── mpesa/
│   ├── notifications/
│   ├── testimonials/
│   ├── transactions/
│   ├── users/
│   └── wallet/
│
├── static/                  # Global static files
│   ├── css/
│   ├── js/
│   └── images/
│
├── templates/               # Global templates
│   ├── base.html
│   ├── dashboard.html
│   ├── analytics.html
│   ├── budgets.html
│   ├── goals.html
│   ├── home.html
│   ├── login.html
│   ├── signup.html
│   ├── transactions.html
│   └── ...
│
├── requirements.txt
├── manage.py
└── README.md
```

- Move all apps into an `apps/` directory for clarity.
- Each app should have its own `templates/<app_name>/` and `static/<app_name>/` folders for modularity.
- Use Django’s `STATICFILES_DIRS` and `TEMPLATES` settings to include these paths.

---

## App Structure Overview

### analytics
- **Models:** (see analytics/models.py)
- **Views:** analytics/views.py

### budget
- **Models:** (see budget/models.py)
- **Views:** budget/views.py

### core
- **Models:** (see core/models.py)
- **Views:** core/views.py

### goals
- **Models:** (see goals/models.py)
- **Views:** goals/views.py

### mpesa
- **Models:** (see mpesa/models.py)
- **Views:** mpesa/views.py

### notifications
- **Models:** (see notifications/models.py)
- **Views:** notifications/views.py

### testimonials
- **Models:** (see testimonials/models.py)
- **Views:** testimonials/views.py

### transactions
- **Models:** (see transactions/models.py)
- **Views:** transactions/views.py

### users
- **Models:** (see users/models.py)
- **Views:** users/views.py

### wallet
- **Models:** (see wallet/models.py)
- **Views:** wallet/views.py

---

## Project Flow Diagram

**User Flow (Simplified):**

```
[Login/Signup]
      |
      v
   [Dashboard] <-----------------------------+
      |                                      |
      v                                      |
[Transactions] <-> [Wallets] <-> [Mpesa]     |
      |                                      |
      v                                      |
   [Budgets] <-> [Analytics] <-> [Goals]     |
      |                                      |
      v                                      |
 [Notifications] <---------------------------+
```

**Component Diagram:**

```
+-------------------+
|    Users App      |
+-------------------+
         |
         v
+-------------------+      +-------------------+
|  Transactions     |<---->|     Wallet        |
+-------------------+      +-------------------+
         |                        |
         v                        v
+-------------------+      +-------------------+
|     Budgets       |<---->|     Analytics     |
+-------------------+      +-------------------+
         |                        |
         v                        v
+-------------------+      +-------------------+
|      Goals        |      |   Notifications   |
+-------------------+      +-------------------+
```

---

## Views and Templates

### Views to be Made (per app):

**core**
- HomeView (home.html)
- AboutView (about.html)

**users**
- LoginView (login.html)
- SignupView (signup.html)
- LogoutView (no template, redirect)
- ProfileView (profile.html)
- PasswordResetView (password_reset.html)

**dashboard**
- DashboardView (dashboard.html)

**transactions**
- TransactionListView (transactions.html)
- TransactionCreateView (transaction_form.html)
- TransactionDetailView (transaction_detail.html)
- TransactionUpdateView (transaction_form.html)
- TransactionDeleteView (transaction_confirm_delete.html)

**wallet**
- WalletListView (wallets.html)
- WalletDetailView (wallet_detail.html)
- WalletCreateView (wallet_form.html)
- WalletTransferView (wallet_transfer.html)

**budget**
- BudgetListView (budgets.html)
- BudgetCreateView (budget_form.html)
- BudgetDetailView (budget_detail.html)
- BudgetUpdateView (budget_form.html)

**goals**
- GoalListView (goals.html)
- GoalCreateView (goal_form.html)
- GoalDetailView (goal_detail.html)
- GoalUpdateView (goal_form.html)

**analytics**
- AnalyticsView (analytics.html)
- API endpoints for charts/forecasts (JSON)

**mpesa**
- MpesaPaymentView (mpesa_form.html)
- MpesaCallbackView (no template)
- MpesaTestView (mpesa_test.html)

**notifications**
- NotificationListView (notifications.html)

**testimonials**
- TestimonialListView (testimonials.html)
- TestimonialCreateView (testimonial_form.html)

---

### Templates to be Made

- base.html (global)
- home.html
- about.html
- login.html
- signup.html
- profile.html
- password_reset.html
- dashboard.html
- transactions.html
- transaction_form.html
- transaction_detail.html
- transaction_confirm_delete.html
- wallets.html
- wallet_detail.html
- wallet_form.html
- wallet_transfer.html
- budgets.html
- budget_form.html
- budget_detail.html
- goals.html
- goal_form.html
- goal_detail.html
- analytics.html
- mpesa_form.html
- mpesa_test.html
- notifications.html
- testimonials.html
- testimonial_form.html

---

## Development Flow for Each App

For every new feature or model in an app, follow this order:

1. **Model**: Define or update your model in `models.py`.
2. **Form**: (If needed) Create a form in `forms.py` for user input/validation.
3. **View**: Add a view in `views.py` to handle the logic (class-based or function-based).
4. **Template**: Create a template in the app's template folder (e.g., `templates/app_name/feature.html`).
5. **URL**: Register the view in your app’s `urls.py` and include it in the project’s main `urls.py` if needed.
6. **Admin**: (Optional) Register your model in `admin.py` for admin interface access.
7. **Tests**: Add or update tests in `tests.py` to cover your new feature.

---

## Recommended App Hierarchy (Implementation Order)

1. **users** — User registration, login, authentication, profile management
2. **core** — Home page, dashboard, global/static content
3. **wallet** — Wallet/account creation and management
4. **transactions** — Add/view/manage transactions (income/expenses/transfers)
5. **budget** — Set and track budgets
6. **goals** — Set and monitor savings/financial goals
7. **analytics** — Analytics, charts, and insights
8. **mpesa** — Mobile money/payment integration
9. **notifications** — User notifications, reminders, alerts
10. **testimonials** — (Optional) User testimonials

---

Follow this hierarchy to build a solid foundation, starting with user management and core navigation, then progressing to financial features and analytics.

---

## Additional Suggestions

- Use Django’s class-based views for CRUD operations.
- Use Django REST Framework for API endpoints (especially for analytics and charts).
- Add tests for all critical views and models.
- Use environment variables for sensitive settings.
- Add pagination for lists (transactions, notifications, etc).
- Use Django signals for notifications and analytics triggers.
- Modularize static and template files per app for easier maintenance.

---

## Contributors

- Lucy Wambui — Full Stack Developer ([GitHub](https://github.com/wambuiw))
- Avin Katami — Full Stack Developer

---

## Contributing
1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature description"
   ```
4. Push your branch and open a pull request:
   ```bash
   git push origin feature-name
   ```

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact
For questions or support, contact:
- **Name**: Astro
- **Email**: mmuichuhia@gmail.com
