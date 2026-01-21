'use client'

import { useState } from 'react'
import { ArrowLeft, Loader2, Play, BookOpen, Layout } from 'lucide-react'
import CodePlayground from './CodePlayground'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface Props {
  analysis: any
  onBack: () => void
}

type AppType = 'playground' | 'tutorial' | 'demo'

export default function AppGenerator({ analysis, onBack }: Props) {
  const [selectedType, setSelectedType] = useState<AppType>('playground')
  const [generating, setGenerating] = useState(false)
  const [generatedApp, setGeneratedApp] = useState<any>(null)
  const [error, setError] = useState('')

  const appTypes = [
    {
      id: 'playground' as AppType,
      name: 'Interactive Playground',
      description: 'Code editor with live execution',
      icon: Play,
      color: 'from-blue-600 to-cyan-600'
    },
    {
      id: 'tutorial' as AppType,
      name: 'Step-by-Step Tutorial',
      description: 'Guided learning experience',
      icon: BookOpen,
      color: 'from-purple-600 to-pink-600'
    },
    {
      id: 'demo' as AppType,
      name: 'Demo Application',
      description: 'Working demonstration',
      icon: Layout,
      color: 'from-green-600 to-emerald-600'
    }
  ]

  const handleGenerate = async () => {
    setError('')
    setGenerating(true)

    try {
      const response = await axios.post(`${API_URL}/api/generate/app`, {
        analysis_id: 'temp-id',
        app_type: selectedType,
        features: ['code_execution', 'syntax_highlighting', 'examples']
      })

      setGeneratedApp(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Generation failed')
    } finally {
      setGenerating(false)
    }
  }

  if (generatedApp) {
    return (
      <div>
        <button
          onClick={() => setGeneratedApp(null)}
          className="flex items-center gap-2 text-gray-400 hover:text-white mb-6 transition"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Options
        </button>

        {selectedType === 'playground' && (
          <CodePlayground
            examples={analysis.examples || []}
            concepts={analysis.concepts || []}
          />
        )}

        {selectedType === 'tutorial' && (
          <div className="bg-gray-800/50 rounded-xl border border-gray-600 p-8">
            <h3 className="text-2xl font-bold text-white mb-4">
              Interactive Tutorial
            </h3>
            <div className="text-gray-300">
              Tutorial interface would be rendered here with step-by-step content
              from the analysis.
            </div>
          </div>
        )}

        {selectedType === 'demo' && (
          <div className="bg-gray-800/50 rounded-xl border border-gray-600 p-8">
            <h3 className="text-2xl font-bold text-white mb-4">
              Demo Application
            </h3>
            <div className="text-gray-300">
              Demo application would be rendered here based on the documentation.
            </div>
          </div>
        )}
      </div>
    )
  }

  return (
    <div>
      <button
        onClick={onBack}
        className="flex items-center gap-2 text-gray-400 hover:text-white mb-6 transition"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Analysis
      </button>

      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-white mb-3">
          Choose Your Learning Experience
        </h2>
        <p className="text-gray-300">
          Select how you'd like to interact with this documentation
        </p>
      </div>

      {/* App Type Selection */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {appTypes.map((type) => {
          const Icon = type.icon
          const isSelected = selectedType === type.id

          return (
            <button
              key={type.id}
              onClick={() => setSelectedType(type.id)}
              className={`
                p-6 rounded-xl border-2 transition text-left
                ${isSelected
                  ? 'border-blue-500 bg-blue-900/30'
                  : 'border-gray-600 bg-gray-800/30 hover:border-gray-500'
                }
              `}
            >
              <div className={`
                w-12 h-12 rounded-lg bg-gradient-to-br ${type.color}
                flex items-center justify-center mb-4
              `}>
                <Icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-xl font-bold text-white mb-2">{type.name}</h3>
              <p className="text-gray-400">{type.description}</p>

              {isSelected && (
                <div className="mt-4 px-3 py-1 bg-blue-600 text-white text-sm rounded-full inline-block">
                  Selected
                </div>
              )}
            </button>
          )
        })}
      </div>

      {/* Features Preview */}
      <div className="bg-gray-800/50 rounded-xl border border-gray-600 p-6 mb-8">
        <h3 className="text-lg font-semibold text-white mb-4">
          Your app will include:
        </h3>
        <div className="grid grid-cols-2 gap-4">
          <div className="flex items-start gap-3">
            <div className="w-2 h-2 bg-green-500 rounded-full mt-2" />
            <div>
              <p className="text-white font-medium">Interactive Examples</p>
              <p className="text-sm text-gray-400">Based on {analysis.examples?.length || 0} code examples</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-2 h-2 bg-green-500 rounded-full mt-2" />
            <div>
              <p className="text-white font-medium">Visual Diagrams</p>
              <p className="text-sm text-gray-400">Auto-generated from concepts</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-2 h-2 bg-green-500 rounded-full mt-2" />
            <div>
              <p className="text-white font-medium">Guided Learning</p>
              <p className="text-sm text-gray-400">Following {analysis.concepts?.length || 0} key concepts</p>
            </div>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-2 h-2 bg-green-500 rounded-full mt-2" />
            <div>
              <p className="text-white font-medium">Live Code Execution</p>
              <p className="text-sm text-gray-400">Run and test examples in real-time</p>
            </div>
          </div>
        </div>
      </div>

      {error && (
        <div className="mb-6 p-4 bg-red-900/50 border border-red-500 rounded-lg text-red-200">
          {error}
        </div>
      )}

      {/* Generate Button */}
      <div className="flex justify-center">
        <button
          onClick={handleGenerate}
          disabled={generating}
          className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 disabled:from-gray-600 disabled:to-gray-600 text-white font-bold rounded-xl transition flex items-center gap-3 shadow-lg"
        >
          {generating ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Generating Your App...
            </>
          ) : (
            <>
              <Play className="w-5 h-5" />
              Generate {appTypes.find(t => t.id === selectedType)?.name}
            </>
          )}
        </button>
      </div>
    </div>
  )
}
