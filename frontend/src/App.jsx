import { useEffect, useState } from 'react'
import { getDashboard, getRecent } from './services/api'
import LookupForm from './components/LookupForm'
import RecentTable from './components/RecentTable'

export default function App() {
  const [stats, setStats] = useState({ total: 0, high: 0, medium: 0, low: 0 })
  const [rows, setRows] = useState([])

  async function refresh() {
    const [s, r] = await Promise.all([getDashboard(), getRecent(20)])
    setStats(s)
    setRows(r)
  }

  useEffect(() => { refresh() }, [])

  return (
    <div style={{maxWidth:900, margin:'24px auto', padding:'0 16px'}}>
      <h1 style={{fontSize:24, fontWeight:700, marginBottom:6}}>CTI Dashboard </h1>
      

      <LookupForm onResult={() => refresh()} />

      <div style={{display:'flex', gap:12, margin:'12px 0'}}>
        <Card title="Total" value={stats.total} />
        <Card title="High" value={stats.high} />
        <Card title="Medium" value={stats.medium} />
        <Card title="Low" value={stats.low} />
      </div>

      <RecentTable rows={rows} />
    </div>
  )
}

function Card({ title, value }) {
  return (
    <div style={{flex:1, border:'1px solid #eee', borderRadius:12, padding:14, boxShadow:'0 2px 8px rgba(0,0,0,0.04)'}}>
      <div style={{fontSize:12, color:'#666'}}>{title}</div>
      <div style={{fontSize:22, fontWeight:700}}>{value}</div>
    </div>
  )
}
