interface DataTableProps {
  data: Array<Record<string, any>>
  columns: string[]
}

export function DataTable({ data, columns }: DataTableProps) {
  if (!data || data.length === 0) {
    return (
      <div style={{ padding: '1rem', textAlign: 'center', color: '#666' }}>
        No data available
      </div>
    )
  }

  if (!columns || columns.length === 0) {
    return (
      <div style={{ padding: '1rem', textAlign: 'center', color: '#666' }}>
        No columns specified
      </div>
    )
  }

  return (
    <div className="data-table-container">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col}>{col}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, idx) => (
            <tr key={idx}>
              {columns.map((col) => (
                <td key={`${idx}-${col}`}>
                  {row[col] !== null && row[col] !== undefined
                    ? String(row[col])
                    : '-'}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
