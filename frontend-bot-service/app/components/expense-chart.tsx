"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts"
import { TrendingUp, PieChartIcon } from "lucide-react"
import { api } from "@/lib/api"

const COLORS = [
  "#3B82F6",
  "#EF4444",
  "#10B981",
  "#F59E0B",
  "#8B5CF6",
  "#EC4899",
  "#06B6D4",
  "#84CC16",
  "#F97316",
  "#6366F1",
  "#14B8A6",
  "#F43F5E",
]

export function ExpenseChart() {
  const [categoryData, setCategoryData] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [chartType, setChartType] = useState<"bar" | "pie">("bar")

  useEffect(() => {
    const fetchCategoryData = async () => {
      try {
        setLoading(true)
        const data = await api.getCategorySummary(1)
        setCategoryData(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to fetch chart data")
      } finally {
        setLoading(false)
      }
    }

    fetchCategoryData()
  }, [])

  if (loading) {
    return (
      <Card className="bg-gradient-to-br from-white to-gray-50 border-0 shadow-xl">
        <CardHeader>
          <div className="h-6 w-48 bg-gray-300 rounded animate-pulse"></div>
        </CardHeader>
        <CardContent>
          <div className="h-80 w-full bg-gray-300 rounded animate-pulse"></div>
        </CardContent>
      </Card>
    )
  }

  if (error) {
    return (
      <Card className="bg-red-50 border-red-200">
        <CardHeader>
          <CardTitle className="text-red-600">Expense Analytics</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-red-600">Error loading chart: {error}</p>
        </CardContent>
      </Card>
    )
  }

  // Fix reduce parameter types
  const totalAmount = categoryData.reduce((sum: number, item: any) => sum + item.total, 0)

  return (
    <Card className="bg-gradient-to-br from-white to-gray-50 border-0 shadow-xl">
      <CardHeader>
        <CardTitle className="flex items-center justify-between text-xl">
          <div className="flex items-center gap-2">
            <TrendingUp className="h-6 w-6 text-indigo-600" />
            Expense Analytics
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setChartType("bar")}
              className={`px-3 py-1 rounded-md text-sm transition-colors ${
                chartType === "bar" ? "bg-indigo-600 text-white" : "bg-gray-200 text-gray-700 hover:bg-gray-300"
              }`}
            >
              Bar Chart
            </button>
            <button
              onClick={() => setChartType("pie")}
              className={`px-3 py-1 rounded-md text-sm transition-colors ${
                chartType === "pie" ? "bg-indigo-600 text-white" : "bg-gray-200 text-gray-700 hover:bg-gray-300"
              }`}
            >
              <PieChartIcon className="h-4 w-4 inline mr-1" />
              Pie Chart
            </button>
          </div>
        </CardTitle>
      </CardHeader>
      <CardContent>
        {categoryData.length === 0 ? (
          <div className="h-80 flex items-center justify-center text-gray-500">
            <div className="text-center">
              <TrendingUp className="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>No expense data available</p>
              <p className="text-sm">Add some expenses to see analytics</p>
            </div>
          </div>
        ) : (
          <div className="h-80">
            {chartType === "bar" ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={categoryData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                  <XAxis dataKey="category" stroke="#666" fontSize={12} angle={-45} textAnchor="end" height={80} />
                  <YAxis stroke="#666" fontSize={12} />
                  <Tooltip
                    formatter={(value: number) => [`$${value.toFixed(2)}`, "Amount"]}
                    labelStyle={{ color: "#333" }}
                    contentStyle={{
                      backgroundColor: "white",
                      border: "1px solid #ccc",
                      borderRadius: "8px",
                    }}
                  />
                  <Bar dataKey="total" fill="#3B82F6" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={categoryData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    // Fix Pie label types
                    label={({ category, total }: { category: string; total: number }) => `${category}: $${total.toFixed(0)}`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="total"
                  >
                    {categoryData.map((entry: any, index: number) => (
                      // Fix map parameter types
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    formatter={(value: number) => [
                      `$${value.toFixed(2)} (${((value / totalAmount) * 100).toFixed(1)}%)`,
                      "Amount",
                    ]}
                  />
                </PieChart>
              </ResponsiveContainer>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
