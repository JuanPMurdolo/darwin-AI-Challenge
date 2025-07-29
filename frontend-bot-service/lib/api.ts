const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001"

export interface Expense {
  id: number
  user_id: string
  amount: number
  description: string
  category: string
  date: string
  created_at: string
}

export interface ExpenseCreate {
  amount: number
  description: string
  category: string
  date?: string
  user_id: string
  telegram_id: string
  text?: string
}

export interface ExpenseOverview {
  total_expenses: number
  monthly_expenses: number
  expense_count: number
  average_expense: number
}

export interface CategorySummary {
  category: string
  total: number
  count: number
}

class ApiError extends Error {
  constructor(
    public status: number,
    message: string,
  ) {
    super(message)
    this.name = "ApiError"
  }
}

async function apiRequest<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`

  try {
    const response = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    })

    if (!response.ok) {
      const errorText = await response.text()
      throw new ApiError(response.status, errorText || `HTTP ${response.status}`)
    }

    return await response.json()
  } catch (error) {
    if (error instanceof ApiError) {
      throw error
    }
    throw new ApiError(0, `Network error: ${error instanceof Error ? error.message : "Unknown error"}`)
  }
}

export const api = {
  // Expenses
  async getExpenses(userId = 1): Promise<Expense[]> {
    return apiRequest<Expense[]>(`/api/expenses/user/${userId}`)
  },

  async createExpense(expense: ExpenseCreate, userId = "1"): Promise<Expense> {
    return apiRequest<Expense>("/api/expenses/", {
      method: "POST",
      body: JSON.stringify({ ...expense, user_id: userId }),
    })
  },

  async deleteExpense(expenseId: number): Promise<void> {
    return apiRequest<void>(`/api/expenses/${expenseId}`, {
      method: "DELETE",
    })
  },

  // Analytics
  async getExpenseOverview(userId = 1): Promise<ExpenseOverview> {
    return apiRequest<ExpenseOverview>(`/api/analytics/overview/${userId}`)
  },

  async getCategorySummary(userId = 1): Promise<CategorySummary[]> {
    return apiRequest<CategorySummary[]>(`/api/analytics/category-summary/${userId}`)
  },

  async getMonthlyTrends(userId = 1): Promise<any[]> {
    return apiRequest<any[]>(`/api/analytics/monthly-trends/${userId}`)
  },

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    return apiRequest<{ status: string }>("/health")
  },
}
