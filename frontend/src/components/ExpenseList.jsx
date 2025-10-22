import { useState, useEffect } from 'react'
import { Receipt } from 'lucide-react'
import axios from 'axios'

export default function ExpenseList() {
  const [expenses, setExpenses] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchExpenses()
  }, [])

  const fetchExpenses = async () => {
    try {
      const response = await axios.get('http://localhost:8000/expenses?limit=10')
      setExpenses(response.data)
    } catch (error) {
      console.error('Error fetching expenses:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="animate-pulse space-y-3">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-16 bg-gray-200 rounded"></div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      <div className="px-6 py-4 border-b border-gray-200">
        <div className="flex items-center gap-2">
          <Receipt className="w-5 h-5 text-gray-600" />
          <h2 className="text-lg font-semibold text-gray-900">Recent Expenses</h2>
        </div>
      </div>
      
      <div className="divide-y divide-gray-100">
        {expenses.length > 0 ? (
          expenses.map((expense) => (
            <div key={expense.id} className="px-6 py-4 hover:bg-gray-50 transition-colors">
              <div className="flex items-center justify-between">
                <div className="flex-1">
                  <p className="font-medium text-gray-900">{expense.description}</p>
                  <div className="flex items-center gap-2 mt-1">
                    <span className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded">
                      {expense.category}
                    </span>
                    <span className="text-xs text-gray-500">{expense.date}</span>
                    {expense.source === 'splitwise' && (
                      <span className="text-xs px-2 py-1 bg-purple-100 text-purple-700 rounded">
                        Splitwise
                      </span>
                    )}
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-lg font-semibold text-gray-900">
                    ${parseFloat(expense.amount).toFixed(2)}
                  </p>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="px-6 py-12 text-center text-gray-500">
            <Receipt className="w-12 h-12 text-gray-300 mx-auto mb-2" />
            <p>No expenses yet</p>
          </div>
        )}
      </div>
    </div>
  )
}
