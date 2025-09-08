export default function RecentTable({ rows = [] }) {
  return (
    <div className="mt-4">
      <h3 style={{fontWeight:'600'}}>Recent</h3>
      <table style={{width:'100%', borderCollapse:'collapse'}}>
        <thead>
          <tr>
            <th style={{textAlign:'left', borderBottom:'1px solid #ddd'}}>Indicator</th>
            <th style={{textAlign:'left', borderBottom:'1px solid #ddd'}}>Type</th>
            <th style={{textAlign:'left', borderBottom:'1px solid #ddd'}}>VT</th>
            <th style={{textAlign:'left', borderBottom:'1px solid #ddd'}}>Abuse</th>
            <th style={{textAlign:'left', borderBottom:'1px solid #ddd'}}>Severity</th>
            <th style={{textAlign:'left', borderBottom:'1px solid #ddd'}}>When</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.id}>
              <td style={{padding:'6px 4px'}}>{r.indicator}</td>
              <td>{r.type}</td>
              <td>{r.vt_positives}/{r.vt_total}</td>
              <td>{r.abuse_score}</td>
              <td>{r.severity}</td>
              <td>{r.created_at}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
