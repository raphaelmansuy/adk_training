import { Line, Bar, Scatter } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
)

interface ChartData {
  chart_type: string
  data: {
    labels: string[]
    values: number[]
  }
  options: {
    x_label: string
    y_label: string
    title: string
  }
}

interface ChartRendererProps {
  chartData: ChartData
}

export function ChartRenderer({ chartData }: ChartRendererProps) {
  const data = {
    labels: chartData.data.labels,
    datasets: [
      {
        label: chartData.options.y_label,
        data: chartData.data.values,
        backgroundColor: 'rgba(102, 126, 234, 0.5)',
        borderColor: 'rgba(102, 126, 234, 1)',
        borderWidth: 2,
        tension: 0.4, // Smooth line curves
      },
    ],
  }

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: true,
        text: chartData.options.title,
        font: {
          size: 16,
          weight: 'bold' as const,
        },
      },
      tooltip: {
        enabled: true,
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        titleFont: {
          size: 14,
        },
        bodyFont: {
          size: 13,
        },
        padding: 12,
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: chartData.options.x_label,
          font: {
            size: 14,
            weight: 'bold' as const,
          },
        },
        grid: {
          display: false,
        },
      },
      y: {
        title: {
          display: true,
          text: chartData.options.y_label,
          font: {
            size: 14,
            weight: 'bold' as const,
          },
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.1)',
        },
      },
    },
  }

  // Render appropriate chart type
  const renderChart = () => {
    switch (chartData.chart_type) {
      case 'line':
        return <Line data={data} options={options} />
      case 'bar':
        return <Bar data={data} options={options} />
      case 'scatter':
        return <Scatter data={data} options={options} />
      default:
        return (
          <div style={{ padding: '1rem', color: '#d32f2f' }}>
            ❌ Unsupported chart type: {chartData.chart_type}
          </div>
        )
    }
  }

  return (
    <div className="chart-container" style={{ height: '400px' }}>
      {renderChart()}
    </div>
  )
}
