"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { TrendingUp, TrendingDown, Calendar, Wallet, CreditCard, Receipt } from "lucide-react"

interface ExpenseStats {
  totalExpenses: number
  monthlyExpenses: number
  averageExpense: number
  expenseCount: number
}

export function ExpenseOverview() {
  const [stats, setStats] = useState<ExpenseStats>({
    totalExpenses: 0,
    monthlyExpenses: 0,
    averageExpense: 0,
    expenseCount: 0,
  })

  useEffect(() => {
    // Mock data - replace with actual API call
    setStats({
      totalExpenses: 2847.5,
      monthlyExpenses: 1234.75,
      averageExpense: 89.32,
      expenseCount: 32,
    })
  }, [])

  const cards = [
    {
      title: "Total Expenses",
      value: `$${stats.totalExpenses.toFixed(2)}`,
      icon: Wallet,
      change: "+12.5%",
      changeType: "increase" as const,
      gradient: "from-purple-500 to-pink-500",
      bgColor: "bg-gradient-to-br from-purple-50 to-pink-50",
      iconBg: "bg-gradient-to-br from-purple-500 to-pink-500",
    },
    {
      title: "This Month",
      value: `$${stats.monthlyExpenses.toFixed(2)}`,
      icon: Calendar,
      change: "+8.2%",
      changeType: "increase" as const,
      gradient: "from-blue-500 to-cyan-500",
      bgColor: "bg-gradient-to-br from-blue-50 to-cyan-50",
      iconBg: "bg-gradient-to-br from-blue-500 to-cyan-500",
    },
    {
      title: "Average Expense",
      value: `$${stats.averageExpense.toFixed(2)}`,
      icon: CreditCard,
      change: "-2.1%",
      changeType: "decrease" as const,
      gradient: "from-emerald-500 to-teal-500",
      bgColor: "bg-gradient-to-br from-emerald-50 to-teal-50",
      iconBg: "bg-gradient-to-br from-emerald-500 to-teal-500",
    },
    {
      title: "Total Transactions",
      value: stats.expenseCount.toString(),
      icon: Receipt,
      change: "+15.3%",
      changeType: "increase" as const,
      gradient: "from-orange-500 to-red-500",
      bgColor: "bg-gradient-to-br from-orange-50 to-red-50",
      iconBg: "bg-gradient-to-br from-orange-500 to-red-500",
    },
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {cards.map((card, index) => (
        <Card
          key={index}
          className={`${card.bgColor} border-0 shadow-lg hover:shadow-xl transition-all duration-300 hover:scale-105`}
        >
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-semibold text-gray-700">{card.title}</CardTitle>
            <div className={`p-2 rounded-lg ${card.iconBg} shadow-lg`}>
              <card.icon className="h-5 w-5 text-white" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-gray-900 mb-2">{card.value}</div>
            <div className="flex items-center justify-between">
              <p
                className={`text-sm font-medium flex items-center ${
                  card.changeType === "increase" ? "text-green-600" : "text-red-600"
                }`}
              >
                {card.changeType === "increase" ? (
                  <TrendingUp className="h-4 w-4 mr-1" />
                ) : (
                  <TrendingDown className="h-4 w-4 mr-1" />
                )}
                {card.change}
              </p>
              <span className="text-xs text-gray-500">vs last month</span>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
