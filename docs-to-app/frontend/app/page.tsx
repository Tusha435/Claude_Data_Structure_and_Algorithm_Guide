'use client'

import { useState } from 'react'
import { Upload, Link as LinkIcon, FileText, Sparkles } from 'lucide-react'
import DocumentUploader from '@/components/DocumentUploader'
import AnalysisView from '@/components/AnalysisView'
import AppGenerator from '@/components/AppGenerator'

export default function Home() {
  const [step, setStep] = useState<'upload' | 'analyze' | 'generate'>('upload')
  const [analysis, setAnalysis] = useState<any>(null)

  const handleAnalysisComplete = (analysisData: any) => {
    setAnalysis(analysisData)
    setStep('analyze')
  }

  const handleGenerateApp = () => {
    setStep('generate')
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-gray-700 bg-black/20 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-600 rounded-lg">
              <Sparkles className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">Docs-to-App</h1>
              <p className="text-sm text-gray-300">GenAI Documentation Platform</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Progress Steps */}
        <div className="mb-12">
          <div className="flex items-center justify-center gap-4">
            {/* Step 1 */}
            <div className="flex items-center gap-3">
              <div className={`
                w-10 h-10 rounded-full flex items-center justify-center font-semibold
                ${step === 'upload' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}
              `}>
                1
              </div>
              <span className={`font-medium ${step === 'upload' ? 'text-white' : 'text-gray-400'}`}>
                Upload Docs
              </span>
            </div>

            <div className="w-16 h-0.5 bg-gray-700" />

            {/* Step 2 */}
            <div className="flex items-center gap-3">
              <div className={`
                w-10 h-10 rounded-full flex items-center justify-center font-semibold
                ${step === 'analyze' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}
              `}>
                2
              </div>
              <span className={`font-medium ${step === 'analyze' ? 'text-white' : 'text-gray-400'}`}>
                Analyze
              </span>
            </div>

            <div className="w-16 h-0.5 bg-gray-700" />

            {/* Step 3 */}
            <div className="flex items-center gap-3">
              <div className={`
                w-10 h-10 rounded-full flex items-center justify-center font-semibold
                ${step === 'generate' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-300'}
              `}>
                3
              </div>
              <span className={`font-medium ${step === 'generate' ? 'text-white' : 'text-gray-400'}`}>
                Generate
              </span>
            </div>
          </div>
        </div>

        {/* Content Area */}
        <div className="bg-white/5 backdrop-blur-sm rounded-2xl border border-gray-700 p-8 min-h-[500px]">
          {step === 'upload' && (
            <DocumentUploader onAnalysisComplete={handleAnalysisComplete} />
          )}

          {step === 'analyze' && analysis && (
            <AnalysisView
              analysis={analysis}
              onGenerateApp={handleGenerateApp}
              onBack={() => setStep('upload')}
            />
          )}

          {step === 'generate' && analysis && (
            <AppGenerator
              analysis={analysis}
              onBack={() => setStep('analyze')}
            />
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="border-t border-gray-700 bg-black/20 backdrop-blur-sm mt-20">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="text-center text-gray-400 text-sm">
            <p>Transform documentation into interactive learning experiences with GenAI</p>
            <p className="mt-2">Built with FastAPI, Next.js, and Claude</p>
          </div>
        </div>
      </footer>
    </main>
  )
}
