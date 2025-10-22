import { Table, BarChart3, List } from 'lucide-react'

export default function ResultsPanel({ data, type }) {
  if (!data) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="text-center py-12">
          <BarChart3 className="w-12 h-12 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-500">Results will appear here when you ask questions</p>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 px-6 py-4">
        <div className="flex items-center gap-3">
          <Table className="w-5 h-5 text-white" />
          <h2 className="text-lg font-semibold text-white">Query Results</h2>
        </div>
      </div>

      {/* Content */}
      <div className="p-6">
        {type === 'table' && (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  {data.headers?.map((header, idx) => (
                    <th
                      key={idx}
                      className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                    >
                      {header}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {data.rows?.map((row, idx) => (
                  <tr key={idx} className="hover:bg-gray-50">
                    {Object.values(row).map((cell, cellIdx) => (
                      <td key={cellIdx} className="px-4 py-3 text-sm text-gray-900">
                        {typeof cell === 'number' && cell.toString().includes('.')
                          ? `$${cell.toFixed(2)}`
                          : cell}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {type === 'list' && (
          <div className="space-y-3">
            {data.items?.map((item, idx) => (
              <div key={idx} className="flex items-start gap-3 p-3 bg-gray-50 rounded-lg">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                  <span className="text-sm font-semibold text-blue-600">{idx + 1}</span>
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">{item.description}</p>
                  <div className="flex items-center gap-4 mt-1">
                    <span className="text-lg font-semibold text-blue-600">
                      ${parseFloat(item.amount).toFixed(2)}
                    </span>
                    {item.category && (
                      <span className="text-xs px-2 py-1 bg-purple-100 text-purple-700 rounded-full">
                        {item.category}
                      </span>
                    )}
                    {item.date && (
                      <span className="text-xs text-gray-500">{item.date}</span>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {type === 'insights' && (
          <div className="prose max-w-none">
            <div className="space-y-4">
              {data.sections?.map((section, idx) => (
                <div key={idx} className="border-l-4 border-blue-500 pl-4 py-2">
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{section.title}</h3>
                  <p className="text-gray-700">{section.content}</p>
                  {section.items && (
                    <ul className="mt-2 space-y-1">
                      {section.items.map((item, itemIdx) => (
                        <li key={itemIdx} className="text-sm text-gray-600">
                          • {item}
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {type === 'text' && (
          <div className="prose max-w-none">
            <p className="text-gray-700 whitespace-pre-wrap">{data.text}</p>
          </div>
        )}
      </div>
    </div>
  )
}
