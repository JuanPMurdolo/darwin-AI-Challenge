"use client"
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs"
import { TrendingUp, PieChartIcon } from "lucide-react"

const monthlyData = [
  { month: "Jan", amount: 1200 },
  { month: "Feb", amount: 1100 },
  { month: "Mar", amount: 1400 },
  { month: "Apr", amount: 1300 },
  { month: "May", amount: 1600 },
  { month: "Jun", amount: 1234 },
]

const categoryData = [
  { name: "Food", value: 450, color: "#FF6B6B", icon: "🍕" },
  { name: "Transportation", value: 320, color: "#4ECDC4", icon: "🚗" },
  { name: "Entertainment", value: 280, color: "#45B7D1", icon: "🎬" },
  { name: "Utilities", value: 184, color: "#FFA07A", icon: "⚡" },
  { name: "Other", value: 150, color: "#98D8C8", icon: "📦" },
]

const RADIAN = Math.PI / 180
const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent, name }: any) => {
  const radius = innerRadius + (outerRadius - innerRadius) * 0.5
  const x = cx + radius * Math.cos(-midAngle * RADIAN)
  const y = cy + radius * Math.sin(-midAngle * RADIAN)

  return (
    <text
      x={x}
      y={y}
      fill="white"
      textAnchor={x > cx ? "start" : "end"}
      dominantBaseline="central"
      className="font-bold text-sm"
    >
      {`${(percent * 100).toFixed(0)}%`}
    </text>
  )
}

export function ExpenseChart() {
  return (
    <Card className="bg-gradient-to-br from-white to-gray-50 border-0 shadow-xl">
      <CardHeader className="bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-t-lg">
        <CardTitle className="flex items-center gap-2 text-xl">
          <div className="bg-white/20 p-2 rounded-lg">
            <TrendingUp className="h-6 w-6" />
          </div>
          Expense Analytics
          <div className="ml-auto bg-white/20 px-3 py-1 rounded-full text-sm">📊 Interactive</div>
        </CardTitle>
      </CardHeader>
      <CardContent className="p-6">
        <Tabs defaultValue="monthly" className="w-full">
          <TabsList className="grid w-full grid-cols-2 bg-gray-100 p-1 rounded-lg">
            <TabsTrigger
              value="monthly"
              className="flex items-center gap-2 data-[state=active]:bg-gradient-to-r data-[state=active]:from-blue-500 data-[state=active]:to-purple-600 data-[state=active]:text-white"
            >
              <TrendingUp className="h-4 w-4" />
              Monthly Trend
            </TabsTrigger>
            <TabsTrigger
              value="category"
              className="flex items-center gap-2 data-[state=active]:bg-gradient-to-r data-[state=active]:from-blue-500 data-[state=active]:to-purple-600 data-[state=active]:text-white"
            >
              <PieChartIcon className="h-4 w-4" />
              By Category
            </TabsTrigger>
          </TabsList>

          <TabsContent value="monthly" className="mt-6">
            <div className="bg-gradient-to-br from-blue-50 to-purple-50 rounded-lg p-4">
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={monthlyData}>
                  <defs>
                    <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#8884d8" stopOpacity={0.8} />
                      <stop offset="95%" stopColor="#8884d8" stopOpacity={0.3} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e0e7ff" />
                  <XAxis dataKey="month" tick={{ fill: "#6b7280", fontSize: 12 }} axisLine={{ stroke: "#d1d5db" }} />
                  <YAxis tick={{ fill: "#6b7280", fontSize: 12 }} axisLine={{ stroke: "#d1d5db" }} />
                  <Tooltip
                    formatter={(value) => [`$${value}`, "Amount"]}
                    contentStyle={{
                      backgroundColor: "#1f2937",
                      border: "none",
                      borderRadius: "8px",
                      color: "white",
                    }}
                  />
                  <Bar dataKey="amount" fill="url(#colorGradient)" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </TabsContent>

          <TabsContent value="category" className="mt-6">
            <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg p-4">
              <div className="flex flex-col lg:flex-row items-center gap-6">
                <div className="flex-1">
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={categoryData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={renderCustomizedLabel}
                        outerRadius={100}
                        fill="#8884d8"
                        dataKey="value"
                        stroke="#fff"
                        strokeWidth={3}
                      >
                        {categoryData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip
                        formatter={(value) => [`$${value}`, "Amount"]}
                        contentStyle={{
                          backgroundColor: "#1f2937",
                          border: "none",
                          borderRadius: "8px",
                          color: "white",
                        }}
                      />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
                <div className="space-y-3">
                  {categoryData.map((entry, index) => (
                    <div key={index} className="flex items-center gap-3 bg-white rounded-lg p-3 shadow-sm">
                      <div className="w-4 h-4 rounded-full" style={{ backgroundColor: entry.color }}></div>
                      <span className="text-2xl">{entry.icon}</span>
                      <div>
                        <div className="font-semibold text-gray-800">{entry.name}</div>
                        <div className="text-sm text-gray-600">${entry.value}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}
