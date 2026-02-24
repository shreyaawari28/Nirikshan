function InsightsFeed({ insights }) {
  return (
    <ul>
      {insights.map((insight, index) => (
        <li key={index}>{insight}</li>
      ))}
    </ul>
  )
}

export default InsightsFeed
