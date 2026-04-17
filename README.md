# Mo-Wallet

A comprehensive **Personal Finance Management System** built with Django, designed to help users efficiently manage their finances with transaction tracking, budgeting, goal setting, and analytics.

## 🎯 Overview

Mo-Wallet is a full-featured financial management platform that provides users with complete control over their finances. Whether tracking daily expenses, managing multiple accounts, setting savings goals, or monitoring spending patterns through advanced analytics, Mo-Wallet delivers an intuitive and powerful experience.

### ✨ Key Features
- **Secure User Accounts**: Robust registration, authentication, and profile management
- **Multi-Account Management**: Create and manage multiple account types (Savings, Checking, Investment, Credit)
- **Transaction Tracking**: Comprehensive income, expense, and transfer recording with detailed categorization
- **Smart Budget Management**: Set spending limits, track progress, and receive alerts for budget overruns
- **Financial Goal Setting**: Define, monitor, and achieve personal financial goals
- **Advanced Analytics**: Generate detailed reports and visualize spending patterns over time
- **Payment Integration**: M-Pesa integration for mobile money transactions
- **User Notifications**: Smart alerts for transactions, budget updates, and achievements
- **SEO-Optimized**: Enterprise-grade SEO implementation for public pages
- **Vision UI Dashboard**: Modern, responsive interface for authenticated users
- **Mobile-Friendly**: Fully responsive design for desktop, tablet, and mobile devices

---

## 🛠️ Tech Stack

### Backend
- **Python 3.10+** — Main programming language  
- **Django 5.x** — Web framework
- **Django REST Framework** — API development
- **SQLite** (development) / **PostgreSQL** (recommended for production)
- **Gunicorn/uWSGI** — Production WSGI servers
- **Nginx** — Reverse proxy and static file server

### Frontend & UI
- **HTML5, CSS3** — Semantic markup and styling with CSS variables
- **Bootstrap 5.3.3** — Responsive UI framework
- **Font Awesome 6.4.0** — Icon library
- **JavaScript (ES6+)** — Client-side interactivity
- **Chart.js** — Analytics and dashboard visualization
- **jQuery** — DOM manipulation and AJAX
- **Vision UI** — Custom modern design system for authenticated dashboard

### Core Features & Tools
- **Django ORM** — Database abstraction layer
- **Django Admin (Jazzmin)** — Enhanced admin interface
- **Django Signals** — Event-driven architecture for automatic actions
- **Custom Template Tags** — Reusable template filters and logic
- **AJAX** — Real-time form interactions and updates
- **M-Pesa Integration** — Mobile money payment processing
- **Semantic HTML/SEO** — Enterprise-grade SEO optimization with meta tags, structured data, and Open Graph

### Design System
- **Color Palette**:
  - Primary: `#4318FF` (Purple)
  - Success: `#01B574` (Green)
  - Danger: `#E31A1A` (Red)
  - Warning: `#FFA500` (Orange)
  - Light: `#F7FAFC` (Light Gray)

### Development & DevOps
- **Docker** (optional) — Containerization support
- **Git** — Version control with semantic commits
- **Django Test Framework** — Comprehensive testing
- **Branching**: Strategy uses main, Astro-Dev, Wambui-Dev branches for team collaboration

---

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- SQLite (included with Python) or PostgreSQL for production
- Git (optional but recommended)
- Virtual environment manager (venv, virtualenv, or conda)

### Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Astro-cmd/Mo-wallet.git
   cd Mo-wallet
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # On Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # On macOS/Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (admin):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the application:**
   - Django App: `http://127.0.0.1:8000`
   - Admin Interface: `http://127.0.0.1:8000/admin`

---

## 🚀 Usage

### For End Users
1. **Sign Up**: Create a new account on the landing page
2. **Add Account**: Create financial accounts and set initial balances
3. **Record Transactions**: Add income, expenses, or transfers with categorization
4. **Set Budgets**: Create spending budgets and monitor category expenditures
5. **Track Goals**: Define financial goals and monitor progress
6. **View Analytics**: Access detailed reports and spending visualizations

### For Administrators
1. Access the admin panel: `/admin`
2. Manage users, transactions, budgets, goals, and notifications
3. View system analytics and user activity
4. Configure M-Pesa integration settings

---

## 📁 Project Structure

```
Mo-wallet/
│
├── Mowallet/                    # Django project settings
│   ├── settings.py              # Django configuration
│   ├── urls.py                  # Main URL routing
│   ├── wsgi.py                  # Production WSGI entry point
│   └── asgi.py                  # Async ASGI entry point
│
├── apps/                        # Django applications
│   ├── analytics/               # Financial analytics and reporting
│   ├── budget/                  # Budget management
│   ├── core/                    # Core functionality (dashboard, home)
│   ├── goals/                   # Financial goals tracking
│   ├── mpesa/                   # M-Pesa payment integration
│   ├── notifications/           # User notifications system
│   ├── testimonials/            # User testimonials
│   ├── transactions/            # Transaction management
│   ├── users/                   # User authentication and profiles
│   └── wallet/                  # Wallet/account management
│
├── static/                      # Static files (CSS, JS, images)
│   ├── css/
│   │   ├── vision-ui.css        # Main dashboard UI styles
│   │   ├── dashboard.css       
│   │   ├── budget.css
│   │   ├── goals.css
│   │   └── ...
│   ├── js/
│   │   ├── dashboard.js
│   │   ├── budget.js
│   │   ├── goals.js
│   │   └── ...
│   └── images/
│       └── mo-wallet.jpg        # Logo and branding
│
├── templates/                   # Django templates (HTML)
│   ├── base.html                # Main template (public pages)
│   ├── base_vision.html         # Dashboard template (authenticated)
│   ├── login_vision.html
│   ├── signup_vision.html
│   ├── dashboard_vision.html
│   ├── budgets_vision.html
│   ├── goals_vision.html
│   ├── wallet.html
│   ├── transactions.html
│   ├── analytics.html
│   └── ...
│
├── db.sqlite3                   # SQLite database (development)
├── manage.py                    # Django management command
├── requirements.txt             # Python dependencies
├── populate_db.py              # Database population script
├── README.md                    # This file
└── .gitignore                   # Git ignore rules
```

---

## 🔧 App Structure Overview

### analytics
- **Purpose**: Financial analytics, reporting, and visualization
- **Key Models**: Custom analytics data models
- **Views**: AnalyticsView for generating charts and insights

### budget
- **Purpose**: Budget creation and tracking
- **Key Models**: Budget, budgetCategory models
- **Views**: Budget CRUD operations, progress tracking

### core
- **Purpose**: Core dashboard and user experience
- **Key Models**: Core configuration and settings
- **Views**: Dashboard, Home, Navigation views

### goals
- **Purpose**: Financial goal setting and monitoring
- **Key Models**: Goal, GoalContribution models
- **Views**: Goal CRUD, progress tracking, contribution management

### mpesa
- **Purpose**: M-Pesa payment integration
- **Key Models**: MpesaTransaction model
- **Views**: Payment processing, transaction callbacks

### notifications
- **Purpose**: User notifications and alerts
- **Key Models**: Notification model
- **Views**: Notification listing and management

### testimonials
- **Purpose**: User testimonials and reviews
- **Key Models**: Testimonial model
- **Views**: Testimonial display and management

### transactions
- **Purpose**: Transaction recording and management
- **Key Models**: Transaction model
- **Views**: Transaction CRUD, reporting

### users
- **Purpose**: User authentication and profile management
- **Key Models**: User (extended Django User model)
- **Views**: Registration, login, profile management

### wallet
- **Purpose**: Wallet/account management
- **Key Models**: Wallet, Account models
- **Views**: Wallet management, transfers

---

## 🔄 User Flow Diagram

```
┌─────────────────┐
│   Landing Page  │
│  (Home, About,  │
│   Features)     │
└────────┬────────┘
         │
    ┌────▼───────┐
    │  Sign Up/  │
    │   Login    │
    └────┬───────┘
         │
    ┌────▼──────────────────────┐
    │   Dashboard (Core)         │
    └────┬─────────────────────┬─┘
         │                     │
    ┌────▼─┐            ┌──────▼────┐
    │      │            │   View    │
    │ View │◄──────────►│ Analytics │
    │      │            │           │
    └────┬─┘            └──────┬────┘
         │                     │
    ┌────▼────┐         ┌──────▼─────┐
    │          │         │            │
    │  Wallet  │◄───────►│ Budget &   │
    │          │         │   Goals    │
    └────┬─────┘         └──────┬─────┘
         │                      │
         └──────────┬───────────┘
                    │
            ┌───────▼────────┐
            │ Notifications  │
            └────────────────┘
```

---

## 👥 Team & Contributors

| Name | Role | GitHub |
|------|------|--------|
| Astro (Moses M.) | Full Stack Developer | [@Astro-cmd](https://github.com/Astro-cmd) |
| Lucy Wambui | Full Stack Developer | [@wambuiw](https://github.com/wambuiw) |

---

## 🤝 Contributing

We welcome contributions to Mo-Wallet! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Commit** your changes with semantic commit messages:
   ```bash
   git commit -m "feat(module): description of changes"
   ```
4. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
5. **Create** a Pull Request with a clear description

### Branching Strategy
- **main** — Production-ready code
- **Astro-Dev** — Development branch for Astro
- **Wambui-Dev** — Development branch for Wambui

---

## 📋 Implementation Checklist

- [x] User authentication and profile management
- [x] Multi-account wallet system
- [x] Transaction tracking (income/expenses/transfers)
- [x] Budget management and tracking
- [x] Financial goal setting and monitoring
- [x] Analytics and reporting dashboard
- [x] M-Pesa payment integration
- [x] User notifications system
- [x] Vision UI modern dashboard design
- [x] SEO optimization for public pages
- [x] Mobile-responsive design
- [ ] Advanced machine learning predictions (future)
- [ ] Mobile app (future)
- [ ] Enhanced reporting export (future)

---

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## 📞 Contact & Support

For questions, issues, or support, please contact:

- **Email**: mmuichuhia@gmail.com
- **GitHub**: [@Astro-cmd](https://github.com/Astro-cmd)
- **Issues**: [GitHub Issues](https://github.com/Astro-cmd/Mo-wallet/issues)

---

## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap team for responsive UI components
- Chart.js for beautiful data visualization
- All contributors and testers

---

**Last Updated**: April 2026
**Version**: 1.0.0
