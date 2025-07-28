"use client"

import type React from "react"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card"
import { Button } from "../components/ui/button"
import { Input } from "../components/ui/input"
import { Label } from "../components/ui/label"
import { Textarea } from "../components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select"
import { Plus, Loader2, Sparkles, DollarSign, Tag, MessageSquare } from "lucide-react"
import { useToast } from "@/hooks/use-toast"
import { api } from "@/lib/api"

const categories = [
	{ name: "Housing", icon: "🏠", color: "from-blue-500 to-blue-600" },
	{ name: "Transportation", icon: "🚗", color: "from-green-500 to-green-600" },
	{ name: "Food", icon: "🍕", color: "from-orange-500 to-orange-600" },
	{ name: "Utilities", icon: "⚡", color: "from-yellow-500 to-yellow-600" },
	{ name: "Insurance", icon: "🛡️", color: "from-purple-500 to-purple-600" },
	{ name: "Medical/Healthcare", icon: "🏥", color: "from-red-500 to-red-600" },
	{ name: "Savings", icon: "💰", color: "from-emerald-500 to-emerald-600" },
	{ name: "Debt", icon: "💳", color: "from-gray-500 to-gray-600" },
	{ name: "Education", icon: "📚", color: "from-indigo-500 to-indigo-600" },
	{ name: "Entertainment", icon: "🎬", color: "from-pink-500 to-pink-600" },
	{ name: "Other", icon: "📦", color: "from-slate-500 to-slate-600" },
]

export function AddExpenseForm() {
	const [isLoading, setIsLoading] = useState(false)
	const [formData, setFormData] = useState({
		description: "",
		amount: "",
		category: "",
		text: "",
	})
	const { toast } = useToast()

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault()
		setIsLoading(true)

		try {
			await api.createExpense({
				description: formData.description,
				amount: Number.parseFloat(formData.amount),
				category: formData.category,
				user_id: "1",
				telegram_id: "123456789",
				text: formData.text,
			})
			toast({
				title: "🎉 Success!",
				description: "Expense added successfully.",
			})
			setFormData({ description: "", amount: "", category: "", text: "" })
		} catch (error) {
			toast({
				title: "❌ Error",
				description: error instanceof Error ? error.message : "Failed to add expense",
				variant: "destructive",
			})
		} finally {
			setIsLoading(false)
		}
	}

	return (
		<Card className="bg-gradient-to-br from-white to-gray-50 border-0 shadow-xl">
			<CardHeader className="bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-t-lg">
				<CardTitle className="flex items-center gap-2 text-xl">
					<div className="bg-white/20 p-2 rounded-lg">
						<Plus className="h-6 w-6" />
					</div>
					Add New Expense
					<Sparkles className="h-5 w-5 ml-auto animate-pulse" />
				</CardTitle>
			</CardHeader>
			<CardContent className="p-6">
				<form onSubmit={handleSubmit} className="space-y-6">
					<div className="space-y-2">
						<Label htmlFor="description" className="flex items-center gap-2 text-sm font-semibold text-gray-700">
							<Tag className="h-4 w-4" />
							Description
						</Label>
						<Input
							id="description"
							placeholder="e.g., Lunch at restaurant"
							value={formData.description}
							onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFormData({ ...formData, description: e.target.value })}
							className="border-2 border-gray-200 focus:border-indigo-500 transition-colors"
							required
						/>
					</div>

					<div className="space-y-2">
						<Label htmlFor="amount" className="flex items-center gap-2 text-sm font-semibold text-gray-700">
							<DollarSign className="h-4 w-4" />
							Amount ($)
						</Label>
						<Input
							id="amount"
							type="number"
							step="0.01"
							placeholder="0.00"
							value={formData.amount}
							onChange={(e: React.ChangeEvent<HTMLInputElement>) => setFormData({ ...formData, amount: e.target.value })}
							className="border-2 border-gray-200 focus:border-indigo-500 transition-colors font-mono text-lg"
							required
						/>
					</div>

					<div className="space-y-2">
						<Label htmlFor="category" className="flex items-center gap-2 text-sm font-semibold text-gray-700">
							<Tag className="h-4 w-4" />
							Category
						</Label>
						<Select
							value={formData.category}
							onValueChange={(value: string) => setFormData({ ...formData, category: value })}
							required
						>
							<SelectTrigger className="border-2 border-gray-200 focus:border-indigo-500">
								<SelectValue placeholder="Select a category" />
							</SelectTrigger>
							<SelectContent>
								{categories.map((category) => (
									<SelectItem key={category.name} value={category.name} className="flex items-center gap-2">
										<span className="text-lg">{category.icon}</span>
										{category.name}
									</SelectItem>
								))}
							</SelectContent>
						</Select>
					</div>

					<div className="space-y-2">
						<Label htmlFor="text" className="flex items-center gap-2 text-sm font-semibold text-gray-700">
							<MessageSquare className="h-4 w-4" />
							Natural Language (Optional)
							<span className="bg-gradient-to-r from-purple-500 to-pink-500 text-white text-xs px-2 py-1 rounded-full">
								AI ✨
							</span>
						</Label>
						<Textarea
							id="text"
							placeholder="e.g., Pizza 20 dollars"
							value={formData.text}
							onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) => setFormData({ ...formData, text: e.target.value })}
							rows={3}
							className="border-2 border-gray-200 focus:border-indigo-500 transition-colors"
						/>
						<p className="text-xs text-gray-500 flex items-center gap-1">
							<Sparkles className="h-3 w-3" />
							Use natural language for AI categorization
						</p>
					</div>

					<Button
						type="submit"
						className="w-full bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white font-semibold py-3 rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
						disabled={isLoading}
					>
						{isLoading ? (
							<>
								<Loader2 className="mr-2 h-5 w-5 animate-spin" />
								Adding Magic...
							</>
						) : (
							<>
								<Plus className="mr-2 h-5 w-5" />
								Add Expense ✨
							</>
						)}
					</Button>
				</form>
			</CardContent>
		</Card>
	)
}
