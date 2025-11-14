import { useState, useEffect } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp } from 'lucide-react';

export default function Trends() {
  const [trendsData, setTrendsData] = useState([]);
  const [period, setPeriod] = useState('month');
  const [chartType, setChartType] = useState('line');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchTrends();
  }, [period]);

  const fetchTrends = async () => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/trends?period=${period}`);
      const data = await response.json();
      setTrendsData(data.data || []);
    } catch (error) {
      console.error('Error fetching trends:', error);
    } finally {
      setLoading(false);
    }
  };

  // Calculate comparison with previous period
  const getComparison = () => {
    if (trendsData.length === 0) return null;

    const midpoint = Math.floor(trendsData.length / 2);
    const firstHalf = trendsData.slice(0, midpoint);
    const secondHalf = trendsData.slice(midpoint);

    const firstTotal = firstHalf.reduce((sum, item) => sum + item.amount, 0);
    const secondTotal = secondHalf.reduce((sum, item) => sum + item.amount, 0);

    const change = secondTotal - firstTotal;
    const percentChange = firstTotal > 0 ? ((change / firstTotal) * 100).toFixed(1) : 0;

    return {
      firstTotal,
      secondTotal,
      change,
      percentChange,
      isIncrease: change > 0
    };
  };

  const comparison = getComparison();

  return (
    <div className="bg-white rounded-2xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          <TrendingUp className="w-6 h-6 text-purple-600" />
          <h2 className="text-2xl font-bold text-gray-800">Spending Trends</h2>
        </div>
        
        <div className="flex gap-2">
          {/* Period selector */}
          <select
            value={period}
            onChange={(e) => setPeriod(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option value="week">Last 7 Days</option>
            <option value="month">Last 2 Months</option>
            <option value="year">Last 12 Months</option>
          </select>

          {/* Chart type selector */}
          <select
            value={chartType}
            onChange={(e) => setChartType(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
          >
            <option value="line">Line Chart</option>
            <option value="bar">Bar Chart</option>
          </select>
        </div>
      </div>

      {/* Comparison stats */}
      {comparison && (
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="bg-gradient-to-br from-purple-50 to-blue-50 p-4 rounded-xl">
            <p className="text-sm text-gray-600 mb-1">Previous Period</p>
            <p className="text-2xl font-bold text-gray-800">${comparison.firstTotal.toFixed(2)}</p>
          </div>
          <div className="bg-gradient-to-br from-blue-50 to-purple-50 p-4 rounded-xl">
            <p className="text-sm text-gray-600 mb-1">Current Period</p>
            <p className="text-2xl font-bold text-gray-800">${comparison.secondTotal.toFixed(2)}</p>
          </div>
          <div className={`bg-gradient-to-br ${comparison.isIncrease ? 'from-red-50 to-orange-50' : 'from-green-50 to-emerald-50'} p-4 rounded-xl`}>
            <p className="text-sm text-gray-600 mb-1">Change</p>
            <p className={`text-2xl font-bold ${comparison.isIncrease ? 'text-red-600' : 'text-green-600'}`}>
              {comparison.isIncrease ? '↑' : '↓'} {Math.abs(comparison.percentChange)}%
            </p>
          </div>
        </div>
      )}

      {/* Chart */}
      <div className="h-80">
        {loading ? (
          <div className="flex items-center justify-center h-full">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
          </div>
        ) : trendsData.length === 0 ? (
          <div className="flex items-center justify-center h-full text-gray-500">
            No data available for this period
          </div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            {chartType === 'line' ? (
              <LineChart data={trendsData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis 
                  dataKey="date" 
                  stroke="#6b7280"
                  tick={{ fontSize: 12 }}
                />
                <YAxis 
                  stroke="#6b7280"
                  tick={{ fontSize: 12 }}
                  tickFormatter={(value) => `$${value}`}
                />
                <Tooltip 
                  formatter={(value) => [`$${value.toFixed(2)}`, 'Amount']}
                  contentStyle={{ 
                    backgroundColor: 'rgba(255, 255, 255, 0.95)', 
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px'
                  }}
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="amount" 
                  stroke="#7c3aed" 
                  strokeWidth={3}
                  dot={{ fill: '#7c3aed', r: 4 }}
                  activeDot={{ r: 6 }}
                  name="Spending"
                />
              </LineChart>
            ) : (
              <BarChart data={trendsData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis 
                  dataKey="date" 
                  stroke="#6b7280"
                  tick={{ fontSize: 12 }}
                />
                <YAxis 
                  stroke="#6b7280"
                  tick={{ fontSize: 12 }}
                  tickFormatter={(value) => `$${value}`}
                />
                <Tooltip 
                  formatter={(value) => [`$${value.toFixed(2)}`, 'Amount']}
                  contentStyle={{ 
                    backgroundColor: 'rgba(255, 255, 255, 0.95)', 
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px'
                  }}
                />
                <Legend />
                <Bar 
                  dataKey="amount" 
                  fill="url(#colorGradient)"
                  radius={[8, 8, 0, 0]}
                  name="Spending"
                />
                <defs>
                  <linearGradient id="colorGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#7c3aed" stopOpacity={0.8}/>
                    <stop offset="100%" stopColor="#3b82f6" stopOpacity={0.8}/>
                  </linearGradient>
                </defs>
              </BarChart>
            )}
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}
