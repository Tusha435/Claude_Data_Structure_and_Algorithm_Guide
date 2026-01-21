'use client'

import { useState } from 'react'
import { BookOpen, Code, ChevronRight, ArrowLeft, Sparkles } from 'lucide-react'
import ReactMarkdown from 'react-markdown'

interface Props {
  analysis: any
  onGenerateApp: () => void
  onBack: () => void
}

export default function AnalysisView({ analysis, onGenerateApp, onBack }: Props) {
  const [selectedSection, setSelectedSection] = useState(0)

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <button
            onClick={onBack}
            className="flex items-center gap-2 text-gray-400 hover:text-white mb-4 transition"
          >
            <ArrowLeft className="w-4 h-4" />
            Back to Upload
          </button>
          <h2 className="text-3xl font-bold text-white">{analysis.title}</h2>
          <p className="text-gray-300 mt-2">{analysis.summary}</p>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-3 gap-6 mb-8">
        {/* Concepts */}
        <div className="bg-gradient-to-br from-blue-900/50 to-blue-800/30 rounded-xl border border-blue-600/50 p-6">
          <div className="flex items-center gap-2 mb-4">
            <BookOpen className="w-5 h-5 text-blue-400" />
            <h3 className="font-semibold text-white">Key Concepts</h3>
          </div>
          <div className="flex flex-wrap gap-2">
            {analysis.concepts?.slice(0, 10).map((concept: string, i: number) => (
              <span
                key={i}
                className="px-3 py-1 bg-blue-700/50 text-blue-100 text-sm rounded-full"
              >
                {concept}
              </span>
            ))}
          </div>
          <p className="text-sm text-gray-400 mt-4">
            {analysis.concepts?.length || 0} concepts identified
          </p>
        </div>

        {/* Sections */}
        <div className="bg-gradient-to-br from-purple-900/50 to-purple-800/30 rounded-xl border border-purple-600/50 p-6">
          <div className="flex items-center gap-2 mb-4">
            <Code className="w-5 h-5 text-purple-400" />
            <h3 className="font-semibold text-white">Sections</h3>
          </div>
          <div className="space-y-2">
            {analysis.sections?.slice(0, 5).map((section: any, i: number) => (
              <div
                key={i}
                className="px-3 py-2 bg-purple-700/30 rounded-lg cursor-pointer hover:bg-purple-700/50 transition"
                onClick={() => setSelectedSection(i)}
              >
                <p className="text-purple-100 font-medium text-sm">{section.title}</p>
                <p className="text-xs text-purple-300 mt-1">
                  {section.difficulty || 'intermediate'}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Examples */}
        <div className="bg-gradient-to-br from-green-900/50 to-green-800/30 rounded-xl border border-green-600/50 p-6">
          <div className="flex items-center gap-2 mb-4">
            <Sparkles className="w-5 h-5 text-green-400" />
            <h3 className="font-semibold text-white">Code Examples</h3>
          </div>
          <div className="space-y-3">
            {analysis.examples?.slice(0, 3).map((example: any, i: number) => (
              <div key={i} className="px-3 py-2 bg-green-700/30 rounded-lg">
                <p className="text-green-100 font-medium text-sm">{example.title}</p>
                <code className="text-xs text-green-300 mt-1 block">
                  {example.language}
                </code>
              </div>
            ))}
          </div>
          <p className="text-sm text-gray-400 mt-4">
            {analysis.examples?.length || 0} examples found
          </p>
        </div>
      </div>

      {/* Section Detail */}
      {analysis.sections && analysis.sections[selectedSection] && (
        <div className="bg-gray-800/50 rounded-xl border border-gray-600 p-6 mb-8">
          <h3 className="text-2xl font-bold text-white mb-3">
            {analysis.sections[selectedSection].title}
          </h3>
          <div className="flex gap-2 mb-4">
            <span className="px-3 py-1 bg-blue-700/50 text-blue-100 text-sm rounded-full">
              {analysis.sections[selectedSection].difficulty}
            </span>
          </div>
          <div className="text-gray-300 mb-4">
            {analysis.sections[selectedSection].description}
          </div>
          {analysis.sections[selectedSection].key_points && (
            <div>
              <h4 className="font-semibold text-white mb-2">Key Points:</h4>
              <ul className="list-disc list-inside space-y-1 text-gray-300">
                {analysis.sections[selectedSection].key_points.map((point: string, i: number) => (
                  <li key={i}>{point}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Learning Path */}
      {analysis.learning_path && analysis.learning_path.length > 0 && (
        <div className="bg-gradient-to-r from-indigo-900/50 to-purple-900/50 rounded-xl border border-indigo-600/50 p-6 mb-8">
          <h3 className="text-xl font-bold text-white mb-4">Recommended Learning Path</h3>
          <div className="flex items-center gap-3 overflow-x-auto pb-2">
            {analysis.learning_path.map((step: string, i: number) => (
              <div key={i} className="flex items-center gap-3 flex-shrink-0">
                <div className="px-4 py-2 bg-indigo-700/50 rounded-lg text-indigo-100 whitespace-nowrap">
                  {i + 1}. {step}
                </div>
                {i < analysis.learning_path.length - 1 && (
                  <ChevronRight className="w-5 h-5 text-indigo-400" />
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Generate Button */}
      <div className="flex justify-center">
        <button
          onClick={onGenerateApp}
          className="px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold rounded-xl transition flex items-center gap-3 shadow-lg shadow-blue-900/50"
        >
          <Sparkles className="w-5 h-5" />
          Generate Interactive Learning App
          <ChevronRight className="w-5 h-5" />
        </button>
      </div>
    </div>
  )
}
