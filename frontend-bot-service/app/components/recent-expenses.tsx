"use client"

import { useEffect, useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { MoreHorizontal, Edit, Trash2, Eye, Clock } from "lucide-react"
import { formatDistanceToNow } from "date-fns"

interface Expense {
  id: number
  description: string
  amount: number
  category: string
  added_at: string
}

const mockExpenses: Expense[] = [
  {
    id: 1,
    description: "Grocery shopping",
    amount: 85.5,
    category: "Food",
    added_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 2,
    description: "Gas station",
    amount: 45.0,
    category: "Transportation",
    added_at: new Date(Date.now() - 5 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 3,
    description: "Netflix subscription",
    amount: 15.99,
    category: "Entertainment",
    added_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 4,
    description: "Coffee shop",
    amount: 4.5,
    category: "Food",
    added_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
  },
  {
    id: 5,
    description: "Electric bill",
    amount: 120.0,
    category: "Utilities",
    added_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
  },
]

const categoryStyles: Record<string, { icon: string; bg: string; text: string; border: string }> = {
  Food: { icon: "🍕", bg: "bg-orange-100", text: "text-orange-800", border: "border-orange-200" },
  Transportation: { icon: "🚗", bg: "bg-blue-100", text: "text-blue-800", border: "border-blue-200" },
  Entertainment: { icon: "🎬", bg: "bg-purple-100", text: "text-purple-800", border: "border-purple-200" },
  Utilities: { icon: "⚡", bg: "bg-yellow-100", text: "text-yellow-800", border: "border-yellow-200" },
  Housing: { icon: "🏠", bg: "bg-red-100", text: "text-red-800", border: "border-red-200" },
  Other: { icon: "📦", bg: "bg-gray-100", text: "text-gray-800", border: "border-gray-200" },
}

export function RecentExpenses() {
  const [expenses, setExpenses] = useState<Expense[]>([])

  useEffect(() => {
    // Mock data - replace with actual API call
    setExpenses(mockExpenses)
  }, [])

  const handleDelete = async (id: number) => {
    try {
      // Mock delete - replace with actual API call
      setExpenses(expenses.filter((expense) => expense.id !== id))
    } catch (error) {
      console.error("Failed to delete expense:", error)
    }
  }

  return (
    <Card className="bg-gradient-to-br from-white to-gray-50 border-0 shadow-xl">
      <CardHeader className="bg-gradient-to-r from-emerald-500 to-teal-600 text-white rounded-t-lg">
        <CardTitle className="flex items-center gap-2 text-xl">
          <div className="bg-white/20 p-2 rounded-lg">
            <Clock className="h-6 w-6" />
          </div>
          Recent Expenses
          <Badge variant="secondary" className="bg-white/20 text-white border-white/30 ml-auto">
            {expenses.length} items
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <Table>
          <TableHeader>
            <TableRow className="bg-gray-50/50">
              <TableHead className="font-semibold text-gray-700">Description</TableHead>
              <TableHead className="font-semibold text-gray-700">Category</TableHead>
              <TableHead className="font-semibold text-gray-700">Amount</TableHead>
              <TableHead className="font-semibold text-gray-700">Date</TableHead>
              <TableHead className="w-[50px]"></TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {expenses.map((expense, index) => (
              <TableRow key={expense.id} className="hover:bg-gray-50/50 transition-colors">
                <TableCell className="font-medium text-gray-900">
                  <div className="flex items-center gap-3">
                    <div className="w-2 h-8 bg-gradient-to-b from-indigo-500 to-purple-600 rounded-full"></div>
                    {expense.description}
                  </div>
                </TableCell>
                <TableCell>
                  <Badge
                    variant="secondary"
                    className={`${categoryStyles[expense.category]?.bg || categoryStyles.Other.bg} ${categoryStyles[expense.category]?.text || categoryStyles.Other.text} ${categoryStyles[expense.category]?.border || categoryStyles.Other.border} border font-medium`}
                  >
                    <span className="mr-1 text-sm">
                      {categoryStyles[expense.category]?.icon || categoryStyles.Other.icon}
                    </span>
                    {expense.category}
                  </Badge>
                </TableCell>
                <TableCell className="font-mono font-bold text-lg">
                  <span className="bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
                    ${expense.amount.toFixed(2)}
                  </span>
                </TableCell>
                <TableCell className="text-gray-500 flex items-center gap-1">
                  <Clock className="h-3 w-3" />
                  {formatDistanceToNow(new Date(expense.added_at), { addSuffix: true })}
                </TableCell>
                <TableCell>
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button variant="ghost" className="h-8 w-8 p-0 hover:bg-gray-100">
                        <MoreHorizontal className="h-4 w-4" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end" className="w-40">
                      <DropdownMenuItem className="text-blue-600">
                        <Eye className="mr-2 h-4 w-4" />
                        View
                      </DropdownMenuItem>
                      <DropdownMenuItem className="text-amber-600">
                        <Edit className="mr-2 h-4 w-4" />
                        Edit
                      </DropdownMenuItem>
                      <DropdownMenuItem className="text-red-600" onClick={() => handleDelete(expense.id)}>
                        <Trash2 className="mr-2 h-4 w-4" />
                        Delete
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </CardContent>
    </Card>
  )
}
