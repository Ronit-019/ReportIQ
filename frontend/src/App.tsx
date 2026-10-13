import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { useEffect, useState, type FormEvent } from 'react'
import {
  Activity,
  CheckCircle2,
  Clock,
  FlaskConical,
  MessageSquare,
  Send,
  ChevronDown,
} from 'lucide-react'
import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import './App.css'

type DataRecord = Record<string, unknown>

type Experiment = {
  experiment_id?: string
  id?: string
  name?: string
  experiment?: string
  title?: string
  category?: string
  status?: string
  summary?: unknown
  decision?: unknown
  conclusion?: unknown
  interpretation?: unknown
  configuration?: DataRecord
  fixed_configuration?: DataRecord
  metrics?: DataRecord
  baseline?: DataRecord
  reranked?: DataRecord
  results?: DataRecord[]
  findings?: unknown[]
  limitations?: unknown[]
  warnings?: unknown[]
  failures_reported?: DataRecord[]
  [key: string]: unknown
}

type EvaluationData = {
  project?: string
  experiments: Experiment[]
  pending_evaluations: DataRecord[]
}

type ChatSource = {
  text: string
  metadata: DataRecord
  distance: number
  rank: number
}

type ChatResponse = {
  question: string
  answer: string
  sources: ChatSource[]
  timings_ms: {
    embedding: number
    retrieval: number
    generation: number
    total: number
  }
}

type Trace = {
  id: string
  name: string | null
  status: string | null
  start_time: string | null
  end_time: string | null
  duration_ms: number | null
  question: string | null
  answer: string | null
  generation?: {
    model?: string
    tokens?: {
      input?: number
      output?: number
      total?: number
    }
  }
  timings_ms?: {
    embedding?: number
    retrieval?: number
    generation?: number
    total?: number
  }
  error: string | null
}

type TraceResponse = {
  project: string
  total: number
  traces: Trace[]
}


type ChatMessage = {
  role: 'user' | 'assistant'
  content: string
  response?: ChatResponse
}

function formatLabel(key: string): string {
  return key
    .replace(/_percent$/, ' (%)')
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (letter) => letter.toUpperCase())
}

function renderText(value: unknown): string {
  if (value === null || value === undefined) return ''

  if (
    typeof value === 'string' ||
    typeof value === 'number' ||
    typeof value === 'boolean'
  ) {
    return String(value)
  }

  if (Array.isArray(value)) {
    return value.map(renderText).filter(Boolean).join('; ')
  }

  if (typeof value === 'object') {
    return Object.entries(value as DataRecord)
      .map(([key, item]) => `${formatLabel(key)}: ${renderText(item)}`)
      .join(' · ')
  }

  return ''
}

function formatValue(value: unknown): string {
  if (value === null || value === undefined) return 'Not reported'

  if (typeof value === 'number') {
    return Number.isInteger(value)
      ? value.toLocaleString()
      : value.toLocaleString(undefined, { maximumFractionDigits: 3 })
  }

  if (typeof value === 'boolean') return value ? 'Yes' : 'No'

  if (typeof value === 'string') return value

  return renderText(value)
}

function MetricGrid({ values }: { values: DataRecord }) {
  const entries = Object.entries(values).filter(
    ([, value]) =>
      value === null ||
      ['string', 'number', 'boolean'].includes(typeof value),
  )

  if (!entries.length) return null

  return (
    <div className="experiment-metrics">
      {entries.map(([key, value]) => (
        <div className="experiment-metric" key={key}>
          <span>{formatLabel(key)}</span>
          <strong>{formatValue(value)}</strong>
        </div>
      ))}
    </div>
  )
}

function DataTable({ rows }: { rows: DataRecord[] }) {
  if (!rows.length) return null

  const columns = [...new Set(rows.flatMap((row) => Object.keys(row)))]

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column}>{formatLabel(column)}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, index) => (
            <tr key={index}>
              {columns.map((column) => (
                <td key={column}>{formatValue(row[column])}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function DetailSection({
  title,
  value,
}: {
  title: string
  value: unknown
}) {
  if (value === null || value === undefined || value === '') return null

  return (
    <div className="decision-block">
      <strong>{title}</strong>
      <p>{renderText(value)}</p>
    </div>
  )
}

function ExperimentCard({ experiment }: { experiment: Experiment }) {
  const title =
    experiment.name ??
    experiment.experiment ??
    experiment.title ??
    experiment.id ??
    experiment.experiment_id ??
    'Untitled experiment'

  const configuration =
    experiment.configuration ?? experiment.fixed_configuration

  const comparisons = [
    { label: 'Baseline', values: experiment.baseline },
    { label: 'Tested alternative', values: experiment.reranked },
  ].filter(
    (item): item is { label: string; values: DataRecord } =>
      Boolean(item.values),
  )

  return (
    <details className="experiment">
      <summary>
        <span className="experiment-title">
          <strong>{title}</strong>
          <small>
            {experiment.category ?? 'Evaluation'} |{' '}
            {experiment.status ?? 'recorded'}
          </small>
        </span>
        <span className="pill">{experiment.status ?? 'recorded'}</span>
      </summary>

      <div className="experiment-body">
        <DetailSection title="Summary" value={experiment.summary} />

        {configuration && (
          <>
            <h4>Configuration</h4>
            <MetricGrid values={configuration} />
          </>
        )}

        {experiment.metrics && (
          <>
            <h4>Metrics</h4>
            <MetricGrid values={experiment.metrics} />
          </>
        )}

        {experiment.results && (
          <>
            <h4>Results by configuration</h4>
            <DataTable rows={experiment.results} />
          </>
        )}

        {comparisons.length > 0 && (
          <>
            <h4>Comparison</h4>
            {comparisons.map(({ label, values }) => (
              <div key={label}>
                <p><strong>{label}</strong></p>
                <MetricGrid values={values} />
              </div>
            ))}
          </>
        )}

        <DetailSection title="Decision" value={experiment.decision} />

        {Array.isArray(experiment.findings) &&
          experiment.findings.length > 0 && (
            <>
              <h4>Findings</h4>
              <ul>
                {experiment.findings.map((item, index) => (
                  <li key={index}>{renderText(item)}</li>
                ))}
              </ul>
            </>
          )}

        {Array.isArray(experiment.warnings) &&
          experiment.warnings.length > 0 && (
            <>
              <h4>Warnings</h4>
              <ul>
                {experiment.warnings.map((item, index) => (
                  <li key={index}>{renderText(item)}</li>
                ))}
              </ul>
            </>
          )}
      </div>
    </details>
  )
}

function ChatPage() {
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function sendQuestion(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()

    const value = question.trim()
    if (!value || loading) return

    setMessages((previous) => [
      ...previous,
      { role: 'user', content: value },
    ])
    setQuestion('')
    setError('')
    setLoading(true)

    try {
      const result = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: value }),
      })

      if (!result.ok) {
        const detail = await result.json().catch(() => null)
        throw new Error(detail?.detail ?? 'The RAG request failed.')
      }

      const response: ChatResponse = await result.json()

      setMessages((previous) => [
        ...previous,
        {
          role: 'assistant',
          content: response.answer,
          response,
        },
      ])
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Something went wrong.',
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="chat-layout">
      <header className="chat-header">
        <div>
          <h2>Ask the company knowledge base</h2>
          <p className="muted">
            Ask questions and inspect the passages used to answer them.
          </p>
        </div>
        <span className="status">Top 3 retrieved chunks</span>
      </header>

      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="chat-empty">
            <MessageSquare size={30} />
            <h3>Ask a question</h3>
            <p>
              Explore the company knowledge base and inspect the retrieved
              context behind each answer.
            </p>

            <button
              type="button"
              className="suggestion"
              onClick={() =>
                setQuestion('What is the company operating philosophy?')
              }
            >
              What is the company operating philosophy?
            </button>

            <button
              type="button"
              className="suggestion"
              onClick={() =>
                setQuestion(
                  'What security and privacy practices are documented?',
                )
              }
            >
              What security and privacy practices are documented?
            </button>

            <button
              type="button"
              className="suggestion"
              onClick={() =>
                setQuestion(
                  'What engineering practices are described in the documents?',
                )
              }
            >
              What engineering practices are described?
            </button>
          </div>
        )}

        {messages.map((message, index) => (
          <article
            className={`chat-message ${message.role}`}
            key={index}
          >
            <span className="message-role">
              {message.role === 'user' ? 'You' : 'ReportIQ'}
            </span>

            <div className="message-content markdown-content">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {message.content}
              </ReactMarkdown>
            </div>

            {message.response && (
              <>
                <div className="latency-row">
                  <span>
                    Total: {message.response.timings_ms.total} ms
                  </span>
                  <span>
                    Retrieval: {message.response.timings_ms.retrieval} ms
                  </span>
                  <span>
                    Generation: {message.response.timings_ms.generation} ms
                  </span>
                </div>

                <details className="sources-panel">
                  <summary>
                    <span>
                      Retrieved sources ({message.response.sources.length})
                    </span>
                    <ChevronDown size={15} />
                  </summary>

                  {message.response.sources.map((source) => {
                    const metadata = source.metadata ?? {}

                    const file = String(metadata.source ?? 'Not available')
                    const topic = [
                      metadata.h1,
                      metadata.h2,
                      metadata.h3,
                      metadata.h4,
                    ]
                      .filter(Boolean)
                      .map((heading) => String(heading).replace(/\*\*/g, '').trim())
                      .join(' › ')

                    const pdfName = file
                      .split(/[\\/]/)
                      .pop()
                      ?.replace(/\.md$/i, '.pdf') ?? 'Not available'
                    const pageValue =
                      metadata.page == null ? 'Not available' : String(metadata.page)

                    return (
                      <article className="source-card" key={source.rank}>
                        <div className="source-heading">
                          <strong>Source {source.rank}</strong>
                        </div>

                        <dl className="source-details">
                          <div>
                            <dt>PDF</dt>
                            <dd>{pdfName}</dd>
                          </div>
                          <div>
                            <dt>Page</dt>
                            <dd>{pageValue}</dd>
                          </div>
                          <div>
                            <dt>Topic</dt>
                            <dd>{topic || 'Not available'}</dd>
                          </div>
                        </dl>
                      </article>
                    )
                  })}

                </details>

                <details className="timings-panel">
                  <summary>Request performance</summary>
                  <div className="timing-grid">
                    {Object.entries(message.response.timings_ms).map(
                      ([key, value]) => (
                        <div className="experiment-metric" key={key}>
                          <span>{formatLabel(key)}</span>
                          <strong>{value} ms</strong>
                        </div>
                      ),
                    )}
                  </div>
                </details>
              </>
            )}
          </article>
        ))}

        {loading && (
          <p className="loading-message">
            Retrieving context and generating an answer...
          </p>
        )}

        {error && <p className="error">{error}</p>}
      </div>

      <form className="chat-form" onSubmit={sendQuestion}>
        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Ask a question about the company knowledge base..."
          rows={2}
          maxLength={2000}
          disabled={loading}
        />

        <button
          type="submit"
          disabled={loading || !question.trim()}
        >
          <Send size={16} />
          {loading ? 'Working...' : 'Ask'}
        </button>
      </form>

      <p className="chat-disclaimer">
        Answers use retrieved document context. Inspect the source passages
        to understand the evidence behind a response.
      </p>
    </section>
  )
}

function OnlineDashboard() {
  const [data, setData] = useState<TraceResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  async function loadTraces() {
    setLoading(true)
    setError('')

    try {
      const response = await fetch('/api/traces?limit=100')

      if (!response.ok) {
        throw new Error(`Failed to load traces (${response.status})`)
      }

      const result: TraceResponse = await response.json()
      setData(result)
    } catch (err) {
      setError(
        err instanceof Error ? err.message : 'Could not load traces.'
      )
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void loadTraces()

    const intervalId = window.setInterval(() => {
      void loadTraces()
    }, 30_000)

    return () => {
      window.clearInterval(intervalId)
    }
  }, [])

  const traces = data?.traces ?? []
  const successful = traces.filter(
    (trace) => trace.status === 'success'
  ).length
  const failed = traces.filter(
    (trace) => trace.status === 'error' || Boolean(trace.error)
  ).length
  const durations = traces
    .map((trace) => trace.duration_ms)
    .filter((duration): duration is number => duration !== null)

  const averageDuration = durations.length
    ? Math.round(
        durations.reduce((sum, duration) => sum + duration, 0) /
          durations.length
      )
    : null

  return (
    <section className="online-dashboard">
      <div className="online-header">
        <div>
          <h2>Online Observability</h2>
          <p>Live RAG request traces from LangSmith.</p>
          {data && (
            <p className="online-muted">
              Project: {data.project}
            </p>
          )}
        </div>

        <button
          type="button"
          className="online-refresh"
          onClick={() => void loadTraces()}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Refresh traces'}
        </button>
      </div>

      {error && (
        <div className="online-error" role="alert">
          {error}
        </div>
      )}

      <div className="online-metrics">
        <article className="online-metric">
          <span>Total requests loaded</span>
          <strong>{data?.total ?? '—'}</strong>
        </article>

        <article className="online-metric">
          <span>Successful requests</span>
          <strong>{successful}</strong>
        </article>

        <article className="online-metric">
          <span>Failed requests</span>
          <strong>{failed}</strong>
        </article>

        <article className="online-metric">
          <span>Average latency</span>
          <strong>
            {averageDuration === null
              ? '—'
              : `${averageDuration} ms`}
          </strong>
        </article>
      </div>
      <div className="online-chart">
        <h3>Latest Request Latency Breakdown</h3>
        <p className="online-muted">
          Execution time in milliseconds for the most recent trace.
        </p>

        {traces.length > 0 ? (
          <ResponsiveContainer width="100%" height={280}>
            <BarChart
              data={[
                {
                  stage: 'Embedding',
                  duration: traces[0].timings_ms?.embedding ?? 0,
                },
                {
                  stage: 'Retrieval',
                  duration: traces[0].timings_ms?.retrieval ?? 0,
                },
                {
                  stage: 'Generation',
                  duration: traces[0].timings_ms?.generation ?? 0,
                },
                {
                  stage: 'Pipeline Total',
                  duration: traces[0].timings_ms?.total ?? 0,
                },
              ]}
              margin={{ top: 16, right: 20, left: 8, bottom: 8 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="stage" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="duration" name="Duration (ms)" fill="#4f46e5" />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <p>No trace timings available yet.</p>
        )}
      </div>

      <div className="online-traces">
        <h3>Recent RAG requests</h3>

        {loading && !data ? (
          <p>Loading traces from LangSmith...</p>
        ) : !error && traces.length === 0 ? (
          <p>No traces found for this project yet.</p>
        ) : (
          traces.map((trace) => (
            <details className="online-trace" key={trace.id}>
              <summary>
                <span className="online-trace-question">
                  {trace.question || trace.name || 'Unnamed request'}
                </span>

                <span
                  className={`online-status ${
                    trace.status === 'success'
                      ? 'online-status-success'
                      : trace.status === 'error'
                        ? 'online-status-error'
                        : ''
                  }`}
                >
                  {trace.status || 'unknown'}
                </span>

                <span className="online-duration">
                  {trace.duration_ms === null
                    ? '—'
                    : `${trace.duration_ms} ms`}
                </span>
              </summary>

              <div className="online-trace-details">
                <p>
                  <strong>Started:</strong>{' '}
                  {trace.start_time
                    ? new Date(trace.start_time).toLocaleString()
                    : '—'}
                </p>

                <p>
                  <strong>Model:</strong>{' '}
                  {trace.generation?.model || '—'}
                </p>

                <p>
                  <strong>Tokens:</strong>{' '}
                  {trace.generation?.tokens?.total ?? '—'}
                  {' '}(
                  {trace.generation?.tokens?.input ?? '—'} input /{' '}
                  {trace.generation?.tokens?.output ?? '—'} output)
                </p>

                <h4>Stage timings</h4>

                <div className="online-timings">
                  <span>
                    Embedding: {trace.timings_ms?.embedding ?? '—'} ms
                  </span>
                  <span>
                    Retrieval: {trace.timings_ms?.retrieval ?? '—'} ms
                  </span>
                  <span>
                    Generation: {trace.timings_ms?.generation ?? '—'} ms
                  </span>
                  <span>
                    Pipeline total: {trace.timings_ms?.total ?? '—'} ms
                  </span>
                </div>

                {trace.answer && (
                  <>
                    <h4>Answer</h4>
                    <p>{trace.answer}</p>
                  </>
                )}

                {trace.error && (
                  <p className="online-error">
                    {trace.error}
                  </p>
                )}

                <p className="online-muted">
                  Trace ID: {trace.id}
                </p>
              </div>
            </details>
          ))
        )}
      </div>
    </section>
  )
}


function App() {
  const [data, setData] = useState<EvaluationData | null>(null)
  const [error, setError] = useState('')
  const [page, setPage] = useState<'evaluation' | 'chat' | 'online'>('evaluation')

  useEffect(() => {
    fetch('/api/evaluations')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Could not load evaluation data.')
        }
        return response.json()
      })
      .then((result: EvaluationData) => setData(result))
      .catch((err: Error) => setError(err.message))
  }, [])

  const experiments = data?.experiments ?? []

  const visibleExperiments = experiments.filter((experiment) => {
    const title = String(
      experiment.name ??
        experiment.experiment ??
        experiment.title ??
        experiment.id ??
        experiment.experiment_id ??
        '',
    ).toLowerCase()

    const hiddenTitles = [
      'chunking strategy comparison: v1 recursive vs v3 structure-aware + merge',
      'answer-level retrieval comparison: v1 recursive vs v3 structure-aware + merge',
      'rag baseline generation evaluation',
    ]

    return !hiddenTitles.includes(title)
  })

  const chunkSweep = experiments.find(
    (experiment) =>
      experiment.experiment_id ===
      'chunk_size_sweep_v3_bge_small_ranx_results_001',
  )

  const sweepRows = (chunkSweep?.results ?? [])
    .filter(
      (item) =>
        typeof item.recall_at_5_percent === 'number' &&
        typeof item.mrr_at_5 === 'number',
    )
    .map((item) => ({
      configuration: `${formatValue(item.chunk_size)} / ${formatValue(item.chunk_overlap)}`,
      recall: Number(item.recall_at_5_percent),
      mrr: Number(item.mrr_at_5) * 100,
    }))

  return (
    <main className="app">
      <header className="topbar">
        <div>
          <p className="eyebrow">RAG ENGINEERING | EVALUATION</p>
          <h1>ReportIQ</h1>
          <p className="muted">
            Understand the numbers behind every decision.
          </p>
        </div>

        <span className="status">
          <Activity size={15} />
          {page === 'evaluation'
          ? 'Offline evaluation'
          : page === 'chat'
            ? 'RAG chat'
            : 'Online observability'}
        </span>
      </header>

      <nav className="nav">
        <button
          type="button"
          className={
            page === 'evaluation'
              ? 'nav-button nav-active'
              : 'nav-button'
          }
          onClick={() => setPage('evaluation')}
        >
          Offline Evaluation
        </button>

        <button
          type="button"
          className={
            page === 'chat' ? 'nav-button nav-active' : 'nav-button'
          }
          onClick={() => setPage('chat')}
        >
          RAG Chat
        </button>

        <button
          type="button"
          className={page === 'online' ? 'nav-button nav-active' : 'nav-button'}
          onClick={() => setPage('online')}
        >
          Online Dashboard
        </button>
      </nav>

      {page === 'evaluation' && (
        <>
          {error && <p className="error">{error}</p>}
          {!data && !error && <p>Loading evaluation data...</p>}

          {data && (
            <>
              <section className="metrics">
                <Metric
                  icon={<FlaskConical />}
                  label="Recorded experiments"
                  value={visibleExperiments.length}
                />

                <Metric
                  icon={<CheckCircle2 />}
                  label="Completed experiments"
                  value={
                    visibleExperiments.filter(
                      (experiment) =>
                        experiment.status === 'completed',
                    ).length
                  }
                />

                <Metric
                  icon={<Clock />}
                  label="Other recorded experiments"
                  value={
                    visibleExperiments.filter(
                      (experiment) =>
                        experiment.status !== 'completed',
                    ).length
                  }
                />
              </section>

              {sweepRows.length > 0 && (
                <section className="panel">
                  <h2>Chunk-size comparison</h2>
                  <p className="muted">
                    Reported results | V3 | BGE-small | Ranx
                  </p>

                  <div className="chart">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={sweepRows}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="configuration" />
                        <YAxis domain={[0, 100]} />
                        <Tooltip />

                        <Bar
                          dataKey="recall"
                          name="Recall@5 (%)"
                          fill="#2563eb"
                          radius={[4, 4, 0, 0]}
                        />

                        <Bar
                          dataKey="mrr"
                          name="MRR@5 (x100)"
                          fill="#14b8a6"
                          radius={[4, 4, 0, 0]}
                        />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </section>
              )}

              <section className="panel">
                <h2>Experiment history</h2>
                <p className="muted">
                  Expand an experiment to inspect its configuration, metrics,
                  decision reasoning, and findings.
                </p>

                {visibleExperiments.map((experiment, index) => (
                  <ExperimentCard
                    key={
                      experiment.experiment_id ??
                      experiment.id ??
                      index
                    }
                    experiment={experiment}
                  />
                ))}
              </section>
            </>
          )}
        </>
      )}

      {page === 'chat' && <ChatPage />}
      {page === 'online' && <OnlineDashboard />}

    </main>
  )
}

function Metric({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode
  label: string
  value: number
}) {
  return (
    <article className="metric-card">
      <div className="metric-icon">{icon}</div>
      <p className="muted">{label}</p>
      <strong className="metric-value">{value}</strong>
    </article>
  )
}

export default App
