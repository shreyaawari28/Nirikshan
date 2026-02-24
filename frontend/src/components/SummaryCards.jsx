function SummaryCards({ summary }) {
  return (
    <div className="summary-row">
      {summary.map((item, index) => (
        <div key={index} className="summary-card">
          <h3>{item.title}</h3>
          <p>{item.value}</p>
        </div>
      ))}
    </div>
  )
}

export default SummaryCards
