import { Suspense } from "react"
import { DashboardHeader } from "./components/dashboard-header"
import { ExpenseOverview } from "./components/expense-overview"
import { ExpenseChart } from "./components/expense-chart"
import { RecentExpenses } from "./components/recent-expenses"
import { AddExpenseForm } from "./components/add-expense-form"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
      <DashboardHeader />

      <main className="container mx-auto px-4 py-8 space-y-8">
        {/* Overview Cards */}
        <Suspense fallback={<ExpenseOverviewSkeleton />}>
          <ExpenseOverview />
        </Suspense>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Chart Section */}
          <div className="lg:col-span-2">
            <Suspense fallback={<ChartSkeleton />}>
              <ExpenseChart />
            </Suspense>
          </div>

          {/* Add Expense Form */}
          <div>
            <AddExpenseForm />
          </div>
        </div>

        {/* Recent Expenses */}
        <Suspense fallback={<RecentExpensesSkeleton />}>
          <RecentExpenses />
        </Suspense>
      </main>
    </div>
  )
}

function ExpenseOverviewSkeleton() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {Array.from({ length: 4 }).map((_, i) => (
        <Card key={i} className="bg-gradient-to-br from-gray-100 to-gray-200 animate-pulse">
          <CardHeader className="pb-2">
            <Skeleton className="h-4 w-24" />
          </CardHeader>
          <CardContent>
            <Skeleton className="h-8 w-20 mb-2" />
            <Skeleton className="h-3 w-16" />
          </CardContent>
        </Card>
      ))}
    </div>
  )
}

function ChartSkeleton() {
  return (
    <Card className="bg-gradient-to-br from-gray-100 to-gray-200 animate-pulse">
      <CardHeader>
        <Skeleton className="h-6 w-48" />
      </CardHeader>
      <CardContent>
        <Skeleton className="h-80 w-full" />
      </CardContent>
    </Card>
  )
}

function RecentExpensesSkeleton() {
  return (
    <Card className="bg-gradient-to-br from-gray-100 to-gray-200 animate-pulse">
      <CardHeader>
        <Skeleton className="h-6 w-32" />
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {Array.from({ length: 5 }).map((_, i) => (
            <div key={i} className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <Skeleton className="h-10 w-10 rounded-full" />
                <div>
                  <Skeleton className="h-4 w-24 mb-1" />
                  <Skeleton className="h-3 w-16" />
                </div>
              </div>
              <Skeleton className="h-4 w-16" />
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
