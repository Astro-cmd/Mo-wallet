export interface Transaction {
  id: number;
  description: string;
  amount: number;
  transaction_type: 'income' | 'expense';
  category: string;
  transaction_date: string;
}

export interface Budget {
  id: number;
  category: string;
  limit: number;
  amount_spent: number;
  remaining: number;
  percentage: number;
}

export interface Goal {
  id: number;
  goal_name: string;
  target_amount: number;
  current_savings: number;
  progress: number;
  deadline: string;
}

export interface DashboardData {
  total_income: number;
  total_expenses: number;
  income_trend: number;
  expense_trend: number;
  savings_rate: number;
  money_in_percentage: number;
  money_out_percentage: number;
  recent_transactions: Transaction[];
  budgets: Budget[];
  goals: Goal[];
  income_expense_labels: number[];
  income_data: number[];
  expense_data: number[];
}