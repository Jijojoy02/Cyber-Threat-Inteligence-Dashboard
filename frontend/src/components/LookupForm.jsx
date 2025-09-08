import { useState } from 'react'
import { lookup } from '../services/api'

export default function LookupForm({ onResult }) {
  const [indicator, setIndicator] = useState('')
  const [loading, setLoading] = useState(false)
  const [err, setErr] = useState('')

  const submit = async (e) => {
    e.preventDefault()
    setErr('')
    if (!indicator.trim()) return
    setLoading(true)
    try {
      const res = await lookup(indicator.trim())
      onResult?.(res)
      setIndicator('')
    } catch (e) {
      setErr('Lookup failed. Check keys/rate limits.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={submit} style={{marginBottom:12}}>
      <input
        value={indicator}
        onChange={e=>setIndicator(e.target.value)}
        placeholder="Enter IP / domain / URL / hash"
        style={{padding:8, border:'1px solid #ccc', borderRadius:6, width:320, marginRight:8}}
      />
      <button
        disabled={loading}
        style={{padding:'8px 14px', borderRadius:6, border:'none', background:'#2563eb', color:'#fff'}}
      >
        {loading ? 'Checking...' : 'Lookup'}
      </button>
      {err && <div style={{color:'crimson', marginTop:6}}>{err}</div>}
    </form>
  )
}
