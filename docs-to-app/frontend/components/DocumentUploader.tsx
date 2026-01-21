'use client'

import { useState } from 'react'
import { Upload, Link as LinkIcon, FileText, Loader2 } from 'lucide-react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Props {
  onAnalysisComplete: (analysis: any) => void
}

export default function DocumentUploader({ onAnalysisComplete }: Props) {
  const [activeTab, setActiveTab] = useState<'url' | 'text' | 'file'>('text')
  const [url, setUrl] = useState('')
  const [text, setText] = useState('')
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async () => {
    setError('')
    setLoading(true)

    try {
      let response

      if (activeTab === 'url') {
        response = await axios.post(`${API_URL}/api/parse/url`, {
          url,
          doc_type: 'readme'
        })
      } else if (activeTab === 'text') {
        if (!text.trim()) {
          throw new Error('Please enter some documentation text')
        }
        response = await axios.post(`${API_URL}/api/parse/text`, {
          content: text,
          doc_type: 'readme',
          title: 'Documentation'
        })
      } else {
        if (!file) {
          throw new Error('Please select a file')
        }
        const formData = new FormData()
        formData.append('file', file)
        response = await axios.post(`${API_URL}/api/parse/file`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
      }

      onAnalysisComplete(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Analysis failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-white mb-3">
          Upload Your Documentation
        </h2>
        <p className="text-gray-300">
          Paste a URL, upload a file, or enter text to transform into an interactive learning app
        </p>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6">
        <button
          onClick={() => setActiveTab('text')}
          className={`flex-1 py-3 px-4 rounded-lg font-medium transition flex items-center justify-center gap-2 ${
            activeTab === 'text'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-700/50 text-gray-300 hover:bg-gray-700'
          }`}
        >
          <FileText className="w-5 h-5" />
          Paste Text
        </button>
        <button
          onClick={() => setActiveTab('url')}
          className={`flex-1 py-3 px-4 rounded-lg font-medium transition flex items-center justify-center gap-2 ${
            activeTab === 'url'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-700/50 text-gray-300 hover:bg-gray-700'
          }`}
        >
          <LinkIcon className="w-5 h-5" />
          From URL
        </button>
        <button
          onClick={() => setActiveTab('file')}
          className={`flex-1 py-3 px-4 rounded-lg font-medium transition flex items-center justify-center gap-2 ${
            activeTab === 'file'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-700/50 text-gray-300 hover:bg-gray-700'
          }`}
        >
          <Upload className="w-5 h-5" />
          Upload File
        </button>
      </div>

      {/* Content */}
      <div className="bg-gray-800/50 rounded-xl border border-gray-600 p-6">
        {activeTab === 'url' && (
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Documentation URL
            </label>
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://github.com/user/repo/blob/main/README.md"
              className="w-full px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p className="mt-2 text-sm text-gray-400">
              Supports GitHub README URLs, raw documentation, and more
            </p>
          </div>
        )}

        {activeTab === 'text' && (
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Documentation Content
            </label>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Paste your README, API docs, or any documentation here..."
              rows={12}
              className="w-full px-4 py-3 bg-gray-900 border border-gray-600 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
            />
            <p className="mt-2 text-sm text-gray-400">
              Supports Markdown, plain text, and RST formats
            </p>
          </div>
        )}

        {activeTab === 'file' && (
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Upload Documentation File
            </label>
            <div className="border-2 border-dashed border-gray-600 rounded-lg p-8 text-center hover:border-blue-500 transition cursor-pointer">
              <input
                type="file"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                accept=".md,.txt,.rst"
                className="hidden"
                id="file-upload"
              />
              <label htmlFor="file-upload" className="cursor-pointer">
                <Upload className="w-12 h-12 text-gray-400 mx-auto mb-3" />
                {file ? (
                  <p className="text-white font-medium">{file.name}</p>
                ) : (
                  <>
                    <p className="text-gray-300 font-medium mb-1">
                      Click to upload or drag and drop
                    </p>
                    <p className="text-sm text-gray-400">
                      .md, .txt, or .rst files
                    </p>
                  </>
                )}
              </label>
            </div>
          </div>
        )}

        {error && (
          <div className="mt-4 p-4 bg-red-900/50 border border-red-500 rounded-lg text-red-200">
            {error}
          </div>
        )}

        <button
          onClick={handleSubmit}
          disabled={loading}
          className="w-full mt-6 py-4 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 text-white font-semibold rounded-lg transition flex items-center justify-center gap-2"
        >
          {loading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Analyzing Documentation...
            </>
          ) : (
            <>
              <FileText className="w-5 h-5" />
              Analyze Documentation
            </>
          )}
        </button>
      </div>

      {/* Example hint */}
      {activeTab === 'text' && !text && (
        <div className="mt-6 p-4 bg-blue-900/30 border border-blue-600/50 rounded-lg">
          <p className="text-sm text-blue-200">
            <strong>Tip:</strong> Try pasting the Data Structures & Algorithms README from this repository,
            or any technical documentation you want to learn from!
          </p>
        </div>
      )}
    </div>
  )
}
