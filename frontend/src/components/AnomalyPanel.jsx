function AnomalyPanel({ anomalies }) {
  if (anomalies.length === 0) {
    return <p>No anomalies detected</p>
  }

  return (
    <div>
      {anomalies.map((anomaly, index) => (
        <div key={index}>
          <p>{anomaly.column}</p>
          <p>{anomaly.count}</p>
        </div>
      ))}
    </div>
  )
}

export default AnomalyPanel
