import { useState, useEffect } from 'react'
import { DollarSign, TrendingUp, MessageSquare, RefreshCw, Download } from 'lucide-react'
import Chat from './components/Chat'
import Overview from './components/Overview'
import ResultsPanel from './components/ResultsPanel'
import './App.css'

function App() {
  const [overview, setOverview] = useState(null)
  const [loading, setLoading] = useState(true)
  const [resultsData, setResultsData] = useState(null)
  const [resultsType, setResultsType] = useState(null)

  const fetchOverview = async () => {
    try {
      const response = await fetch('http://localhost:8000/overview')
      const data = await response.json()
      setOverview(data)
    } catch (error) {
      console.error('Error fetching overview:', error)
    } finally {
      setLoading(false)
    }
  }

  const syncSplitwise = async () => {
    try {
      await fetch('http://localhost:8000/sync-splitwise', { method: 'POST' })
      fetchOverview()
      alert('✅ Synced successfully!')
    } catch (error) {
      alert('❌ Error syncing: ' + error.message)
    }
  }

  useEffect(() => {
    fetchOverview()
  }, [])

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <DollarSign className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-semibold text-gray-900">Expense Tracker</h1>
                <p className="text-sm text-gray-500">AI-powered expense management</p>
              </div>
            </div>
            <button
              onClick={syncSplitwise}
              className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors"
            >
              <Download className="w-4 h-4" />
              Sync Splitwise
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Overview & Stats */}
          <div className="lg:col-span-1 space-y-6">
            <Overview overview={overview} loading={loading} onRefresh={fetchOverview} />
          </div>

          {/* Middle Column - Chat */}
          <div className="lg:col-span-2 space-y-6">
            <Chat 
              onExpenseAdded={fetchOverview} 
              onResultsUpdate={(data, type) => {
                setResultsData(data)
                setResultsType(type)
              }}
            />
            <ResultsPanel data={resultsData} type={resultsType} />
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
