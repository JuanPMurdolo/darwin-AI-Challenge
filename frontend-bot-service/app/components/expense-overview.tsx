"use client"

import { api } from "@/lib/api"
import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card"
import { TrendingUp, TrendingDown, DollarSign, CreditCard, Target, Activity } from "lucide-react"

export function ExpenseOverview() {
  const [overview, setOverview] = useState<any | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchOverview = async () => {
      try {
        setLoading(true)
        const data = await api.getExpenseOverview(1)
        setOverview(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch overview")
      } finally {
        setLoading(false)
      }
    }
    fetchOverview()
  }, [])

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {Array.from({ length: 4 }).map((_, i) => (
          <Card key={i} className="bg-gradient-to-br from-gray-100 to-gray-200 animate-pulse">
            <CardHeader className="pb-2">
              <div className="h-4 w-24 bg-gray-300 rounded"></div>
            </CardHeader>
            <CardContent>
              <div className="h-8 w-20 bg-gray-300 rounded mb-2"></div>
              <div className="h-3 w-16 bg-gray-300 rounded"></div>
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  if (error) {
    return (
      <Card className="bg-red-50 border-red-200">
        <CardContent className="p-6">
          <p className="text-red-600">Error loading overview: {error}</p>
        </CardContent>
      </Card>
    )
  }

  if (!overview) return null

  const cards = [
    {
      title: "Total Expenses",
      value: `$${(overview.total_expenses ?? 0).toFixed(2)}`,
      change: "+12.5%",
      trend: "up" as const,
      icon: DollarSign,
      gradient: "from-emerald-500 to-teal-600",
    },
    {
      title: "Expense Count",
      value: (overview.expense_count ?? 0).toString(),
      change: "+3 this week",
      trend: "up" as const,
      icon: CreditCard,
      gradient: "from-blue-500 to-indigo-600",
    },
    {
      title: "Average Amount",
      value: `$${(overview.average_expense ?? 0).toFixed(2)}`,
      change: "-2.1%",
      trend: "down" as const,
      icon: Target,
      gradient: "from-purple-500 to-pink-600",
    },
    {
      title: "Monthly Budget",
      value: "$2,500",
      change: `${((overview.total_expenses ?? 0) / 2500 * 100).toFixed(1)}% used`,
      trend: (overview.total_expenses ?? 0) > 2000 ? "down" : ("up" as const),
      icon: Activity,
      gradient: "from-orange-500 to-red-600",
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {cards.map((card, index) => {
        const Icon = card.icon
        const TrendIcon = card.trend === "up" ? TrendingUp : TrendingDown

        return (
          <Card
            key={index}
            className="bg-gradient-to-br from-white to-gray-50 border-0 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
          >
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600 flex items-center justify-between">
                {card.title}
                <div className={`bg-gradient-to-r ${card.gradient} p-2 rounded-lg`}>
                  <Icon className="h-4 w-4 text-white" />
                </div>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-gray-900 mb-1">{card.value}</div>
              <div className={`text-xs flex items-center ${card.trend === "up" ? "text-green-600" : "text-red-600"}`}>
                <TrendIcon className="h-3 w-3 mr-1" />
                {card.change}
              </div>
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}
