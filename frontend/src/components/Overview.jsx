import { DollarSign, ShoppingCart, TrendingUp, RefreshCw } from 'lucide-react'

export default function Overview({ overview, loading, onRefresh }) {
  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          <div className="h-8 bg-gray-200 rounded"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Total Spending Card */}
      <div className="bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl shadow-lg p-6 text-white">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-sm font-medium opacity-90">This Month</h3>
          <button
            onClick={onRefresh}
            className="p-1 hover:bg-white/20 rounded-lg transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
        <div className="flex items-baseline gap-2">
          <DollarSign className="w-8 h-8" />
          <span className="text-4xl font-bold">
            {overview?.total?.toFixed(2) || '0.00'}
          </span>
        </div>
        <div className="mt-4 flex items-center gap-2 text-sm opacity-90">
          <ShoppingCart className="w-4 h-4" />
          <span>{overview?.count || 0} transactions</span>
        </div>
      </div>

      {/* Categories Card */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-center gap-2 mb-4">
          <TrendingUp className="w-5 h-5 text-gray-600" />
          <h3 className="font-semibold text-gray-900">Top Categories</h3>
        </div>
        
        {overview?.top_categories?.length > 0 ? (
          <div className="space-y-3">
            {overview.top_categories.map((cat, idx) => (
              <div key={idx} className="space-y-1">
                <div className="flex items-center justify-between text-sm">
                  <span className="font-medium text-gray-700">{cat.category}</span>
                  <span className="font-semibold text-gray-900">
                    ${cat.total.toFixed(2)}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-blue-500 to-purple-600 rounded-full"
                      style={{
                        width: `${(cat.total / overview.total) * 100}%`
                      }}
                    />
                  </div>
                  <span className="text-xs text-gray-500">{cat.count}</span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-gray-500">No expenses yet</p>
        )}
      </div>

      {/* Quick Tips */}
      <div className="bg-blue-50 rounded-xl border border-blue-100 p-4">
        <h4 className="font-semibold text-blue-900 text-sm mb-2">💡 Quick Tips</h4>
        <ul className="text-xs text-blue-800 space-y-1">
          <li>• Ask in plain English</li>
          <li>• Request category breakdowns</li>
          <li>• View top expenses</li>
          <li>• Add expenses naturally</li>
        </ul>
      </div>
    </div>
  )
}
