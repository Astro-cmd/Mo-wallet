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

## Technologies Used
- **Backend**: Python (Django Framework)
- **Database**: MySQL
- **Frontend**: (Optional, depending on implementation) HTML, CSS, JavaScript

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

## Project Structure
- `accounts/`: Handles user account-related functionalities.
- `budgets/`: Manages budget creation and tracking.
- `goals/`: Supports goal setting and monitoring.
- `transactions/`: Handles transaction recording and categorization.
- `templates/`: Contains HTML templates for frontend views.
- `static/`: Stores static assets like CSS, JavaScript, and images.

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
