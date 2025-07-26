"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card"
import { Badge } from "./ui/badge"
import { Avatar, AvatarFallback } from "./ui/avatar"
import { Clock, DollarSign } from "lucide-react"
import { apiClient, type Expense } from "@/lib/api"

const categoryIcons: Record<string, string> = {
  Housing: "🏠",
  Transportation: "🚗",
  Food: "🍕",
  Utilities: "⚡",
  Insurance: "🛡️",
  "Medical/Healthcare": "🏥",
  Savings: "💰",
  Debt: "💳",
  Education: "📚",
  Entertainment: "🎬",
  Other: "📦",
}

const categoryColors: Record<string, string> = {
  Housing: "bg-blue-100 text-blue-800",
  Transportation: "bg-green-100 text-green-800",
  Food: "bg-orange-100 text-orange-800",
  Utilities: "bg-yellow-100 text-yellow-800",
  Insurance: "bg-purple-100 text-purple-800",
  "Medical/Healthcare": "bg-red-100 text-red-800",
  Savings: "bg-emerald-100 text-emerald-800",
  Debt: "bg-gray-100 text-gray-800",
  Education: "bg-indigo-100 text-indigo-800",
  Entertainment: "bg-pink-100 text-pink-800",
  Other: "bg-slate-100 text-slate-800",
}

export function RecentExpenses() {
  const [expenses, setExpenses] = useState<Expense[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchExpenses = async () => {
      try {
        setLoading(true)
        // Using mock user ID - in real app, get from auth context
        const data = await apiClient.getExpenses(1)
        // Sort by date and take the 5 most recent
        const sortedExpenses = data
          .sort((a, b) => new Date(b.added_at).getTime() - new Date(a.added_at).getTime())
          .slice(0, 5)
        setExpenses(sortedExpenses)
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch expenses")
      } finally {
        setLoading(false)
      }
    }

    fetchExpenses()
  }, [])

  if (loading) {
    return (
      <Card className="bg-gradient-to-br from-white to-gray-50 border-0 shadow-xl">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-xl">
            <Clock className="h-6 w-6 text-indigo-600" />
            Recent Expenses
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="flex items-center justify-between animate-pulse">
                <div className="flex items-center space-x-4">
                  <div className="h-10 w-10 bg-gray-300 rounded-full"></div>
                  <div>
                    <div className="h-4 w-24 bg-gray-300 rounded mb-1"></div>
                    <div className="h-3 w-16 bg-gray-300 rounded"></div>
                  </div>
                </div>
                <div className="h-4 w-16 bg-gray-300 rounded"></div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    )
  }

  if (error) {
    return (
      <Card className="bg-red-50 border-red-200">
        <CardHeader>
          <CardTitle className="text-red-600">Recent Expenses</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-red-600">Error loading expenses: {error}</p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="bg-gradient-to-br from-white to-gray-50 border-0 shadow-xl">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-xl">
          <Clock className="h-6 w-6 text-indigo-600" />
          Recent Expenses
          <Badge variant="secondary" className="ml-auto">
            {expenses.length} items
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent>
        {expenses.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <DollarSign className="h-12 w-12 mx-auto mb-4 opacity-50" />
            <p>No expenses found</p>
            <p className="text-sm">Add your first expense to get started!</p>
          </div>
        ) : (
          <div className="space-y-4">
            {expenses.map((expense) => {
              const categoryIcon = categoryIcons[expense.category] || "📦"
              const categoryColor = categoryColors[expense.category] || "bg-gray-100 text-gray-800"
              const date = new Date(expense.added_at).toLocaleDateString()

              return (
                <div
                  key={expense.id}
                  className="flex items-center justify-between p-3 rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center space-x-4">
                    <Avatar className="h-10 w-10">
                      <AvatarFallback className="text-lg">{categoryIcon}</AvatarFallback>
                    </Avatar>
                    <div>
                      <p className="font-medium text-gray-900">{expense.description}</p>
                      <div className="flex items-center gap-2 mt-1">
                        <Badge className={`text-xs ${categoryColor}`}>{expense.category}</Badge>
                        <span className="text-xs text-gray-500">{date}</span>
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold text-gray-900">${expense.amount.toFixed(2)}</p>
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
