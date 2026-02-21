"use client"
import ReactMarkdown from "react-markdown"
import { useState } from "react"

export default function Home() {
  const [url, setUrl] = useState("")
  const [report, setReport] = useState("")
  const [loading, setLoading] = useState(false)

  const generateReport = async () => {
    setLoading(true)

    const res = await fetch("https://papersummarizer-vpnu.onrender.com/generate-report", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ pdf_url: url })
    })

    const data = await res.json()
    setReport(data.report)
    setLoading(false)
  }

  return (
    <main className="min-h-screen p-10 bg-[#7B1E3A]">
      <div className="max-w-3xl mx-auto space-y-6 text-white">
        <h1 className="text-3xl font-bold">
          arXiv Paper → Pedagogy Report
        </h1>

        <input
          type="text"
          placeholder="Paste arXiv PDF URL"
          className="w-full p-3 border rounded"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />

        <button
          onClick={generateReport}
          className="px-6 py-3 bg-black text-white rounded"
        >
          {loading ? "Generating..." : "Generate Report"}
        </button>

 {report && (
  <div className="bg-white text-black p-6 rounded-xl shadow-lg max-h-[60vh] overflow-y-auto">
    <div className="prose max-w-none">
      <ReactMarkdown>
        {report}
      </ReactMarkdown>
    </div>
  </div>
)}


      </div>
    </main>
  )
}
