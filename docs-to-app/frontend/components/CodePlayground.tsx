'use client'

import { useState, useEffect } from 'react'
import Editor from '@monaco-editor/react'
import { Play, RotateCcw, BookOpen, Sparkles, Info } from 'lucide-react'

interface Props {
  examples: any[]
  concepts: string[]
}

export default function CodePlayground({ examples, concepts }: Props) {
  const [selectedExample, setSelectedExample] = useState(0)
  const [code, setCode] = useState('')
  const [output, setOutput] = useState('')
  const [isRunning, setIsRunning] = useState(false)

  useEffect(() => {
    if (examples.length > 0) {
      setCode(examples[0].code || '# No code available')
    }
  }, [examples])

  const runCode = async () => {
    setIsRunning(true)
    setOutput('Running code...\n')

    // Simulate code execution (in real app, this would call the backend)
    setTimeout(() => {
      setOutput(`Code executed successfully!\n\nExample output:\nHello from the playground!`)
      setIsRunning(false)
    }, 1000)
  }

  const resetCode = () => {
    if (examples.length > 0) {
      setCode(examples[selectedExample].code || '')
      setOutput('')
    }
  }

  const loadExample = (index: number) => {
    setSelectedExample(index)
    if (examples[index]) {
      setCode(examples[index].code || '')
      setOutput('')
    }
  }

  return (
    <div className="h-[800px] flex flex-col bg-gray-900 rounded-xl border border-gray-700 overflow-hidden">
      {/* Header */}
      <div className="bg-gray-800 border-b border-gray-700 p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-600 rounded-lg">
              <BookOpen className="w-5 h-5 text-white" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-white">Interactive Code Playground</h2>
              <p className="text-sm text-gray-400">
                Learn by doing - edit and run code examples
              </p>
            </div>
          </div>
          <div className="flex gap-2">
            <button
              onClick={resetCode}
              className="px-4 py-2 bg-gray-700 hover:bg-gray-600 text-white rounded-lg flex items-center gap-2 transition"
            >
              <RotateCcw className="w-4 h-4" />
              Reset
            </button>
            <button
              onClick={runCode}
              disabled={isRunning}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg flex items-center gap-2 transition disabled:opacity-50"
            >
              <Play className="w-4 h-4" />
              {isRunning ? 'Running...' : 'Run Code'}
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar - Examples */}
        <div className="w-64 bg-gray-800 border-r border-gray-700 overflow-y-auto">
          <div className="p-4">
            <h3 className="text-sm font-semibold text-gray-400 mb-3 flex items-center gap-2">
              <Sparkles className="w-4 h-4" />
              Examples
            </h3>
            <div className="space-y-2">
              {examples.length > 0 ? (
                examples.map((example, i) => (
                  <button
                    key={i}
                    onClick={() => loadExample(i)}
                    className={`
                      w-full text-left p-3 rounded-lg transition
                      ${selectedExample === i
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
                      }
                    `}
                  >
                    <p className="font-medium text-sm mb-1">
                      {example.title || `Example ${i + 1}`}
                    </p>
                    {example.language && (
                      <code className="text-xs opacity-75">
                        {example.language}
                      </code>
                    )}
                  </button>
                ))
              ) : (
                <div className="text-sm text-gray-500 p-3 bg-gray-700/50 rounded-lg">
                  <Info className="w-4 h-4 inline mr-2" />
                  No examples found in documentation
                </div>
              )}
            </div>

            {/* Concepts */}
            <h3 className="text-sm font-semibold text-gray-400 mb-3 mt-6 flex items-center gap-2">
              <BookOpen className="w-4 h-4" />
              Related Concepts
            </h3>
            <div className="flex flex-wrap gap-2">
              {concepts.slice(0, 8).map((concept, i) => (
                <span
                  key={i}
                  className="px-2 py-1 bg-gray-700 text-gray-300 text-xs rounded"
                >
                  {concept}
                </span>
              ))}
            </div>
          </div>
        </div>

        {/* Code Editor */}
        <div className="flex-1 flex flex-col">
          <div className="flex-1 border-b border-gray-700">
            <Editor
              height="100%"
              defaultLanguage="python"
              theme="vs-dark"
              value={code}
              onChange={(value) => setCode(value || '')}
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                lineNumbers: 'on',
                scrollBeyondLastLine: false,
                automaticLayout: true,
                tabSize: 2,
                wordWrap: 'on',
              }}
            />
          </div>

          {/* Output Panel */}
          <div className="h-48 bg-gray-800 border-t border-gray-700 flex flex-col">
            <div className="px-4 py-2 border-b border-gray-700">
              <h3 className="text-sm font-semibold text-gray-300">Output</h3>
            </div>
            <div className="flex-1 p-4 overflow-auto">
              <pre className="text-sm text-gray-100 font-mono whitespace-pre-wrap">
                {output || 'Run code to see output...'}
              </pre>
            </div>
          </div>
        </div>
      </div>

      {/* Info Bar */}
      {examples[selectedExample]?.explanation && (
        <div className="bg-blue-900/30 border-t border-blue-700/50 p-4">
          <div className="flex items-start gap-3">
            <Info className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" />
            <div>
              <p className="text-sm text-blue-100">
                <strong>About this example:</strong> {examples[selectedExample].explanation}
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
