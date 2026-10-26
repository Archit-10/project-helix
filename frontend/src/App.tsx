import { useRef, useState } from 'react'
import './App.css'

type Citation = {
  document_id: string
  chunk_id: string
  file_name: string
  path: string
}

type Message = {
  id: string
  role: 'user' | 'assistant'
  content: string
  citations?: Citation[]
}

type StreamEvent = {
  type: 'token' | 'citations' | 'done'
  content?: string | null
  citations?: Citation[] | null
}

const suggestions = [
  {
    icon: '⌘',
    title: 'Understand the architecture',
    description: 'Explain how Project Helix works end to end.',
    prompt: 'Explain the architecture of Project Helix end to end.',
  },
  {
    icon: '⌕',
    title: 'Find relevant information',
    description: 'How does semantic search retrieve documents?',
    prompt: 'How does semantic search retrieve relevant documents?',
  },
  {
    icon: '◈',
    title: 'Explore the knowledge base',
    description: 'What information is available in the indexed docs?',
    prompt: 'Summarize the main topics covered in the knowledge base.',
  },
  {
    icon: '⌁',
    title: 'Understand RAG',
    description: 'Explain retrieval-augmented generation simply.',
    prompt: 'Explain retrieval-augmented generation and why it is useful.',
  },
]

function App() {
  const [query, setQuery] = useState('')
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const abortRef = useRef<AbortController | null>(null)
  const bottomRef = useRef<HTMLDivElement>(null)

  function startNewConversation() {
    abortRef.current?.abort()
    abortRef.current = null
    setMessages([])
    setQuery('')
    setError('')
    setLoading(false)
  }

  async function sendMessage(text = query) {
    const question = text.trim()
    if (!question || loading) return

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: 'user',
      content: question,
    }
    const assistantId = crypto.randomUUID()

    setMessages((current) => [
      ...current,
      userMessage,
      { id: assistantId, role: 'assistant', content: '', citations: [] },
    ])
    setQuery('')
    setError('')
    setLoading(true)

    const controller = new AbortController()
    abortRef.current = controller

    try {
      const response = await fetch('/api/v1/generate/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: question, top_k: 5 }),
        signal: controller.signal,
      })

      if (!response.ok) {
        const detail = await response.text()
        throw new Error(
          `Request failed (${response.status})${detail ? `: ${detail.slice(0, 220)}` : ''}`,
        )
      }

      if (!response.body) {
        throw new Error('The server did not provide a response stream.')
      }

      const reader = response.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      function processEvent(frame: string) {
        const data = frame
          .split('\n')
          .filter((line) => line.startsWith('data:'))
          .map((line) => line.slice(5).trimStart())
          .join('\n')

        if (!data) return

        const event = JSON.parse(data) as StreamEvent

        if (event.type === 'token' && event.content) {
          setMessages((current) =>
            current.map((message) =>
              message.id === assistantId
                ? { ...message, content: message.content + event.content }
                : message,
            ),
          )
        } else if (event.type === 'citations') {
          setMessages((current) =>
            current.map((message) =>
              message.id === assistantId
                ? { ...message, citations: event.citations ?? [] }
                : message,
            ),
          )
        }
      }

      while (true) {
        const { value, done } = await reader.read()
        buffer += decoder.decode(value, { stream: !done })

        const frames = buffer.split(/\r?\n\r?\n/)
        buffer = frames.pop() ?? ''

        for (const frame of frames) {
          if (controller.signal.aborted) break
          processEvent(frame)
        }

        if (done || controller.signal.aborted) break
      }

      if (buffer.trim() && !controller.signal.aborted) {
        processEvent(buffer)
      }

      if (!controller.signal.aborted) {
        setMessages((current) =>
          current.map((message) =>
            message.id === assistantId && !message.content
              ? {
                  ...message,
                  content: 'No answer text was returned. Please try again.',
                }
              : message,
          ),
        )
      }
    } catch (cause) {
      if (cause instanceof Error && cause.name === 'AbortError') return

      const message =
        cause instanceof Error ? cause.message : 'An unexpected error occurred.'

      setError(
        `${message}. Check that the backend is running and the knowledge base is indexed.`,
      )
      setMessages((current) =>
        current.filter(
          (item) => item.id !== assistantId || item.content.length > 0,
        ),
      )
    } finally {
      if (abortRef.current === controller) {
        abortRef.current = null
        setLoading(false)
      }
    }
  }

  const hasMessages = messages.length > 0

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <a className="brand" href="/" aria-label="Project Helix home">
          <span className="brand-mark">H</span>
          <span className="brand-copy">
            <strong>helix</strong>
            <span>KNOWLEDGE WORKSPACE</span>
          </span>
        </a>

        <button
          className="new-chat-button"
          onClick={startNewConversation}
          type="button"
        >
          <span className="plus-icon">＋</span>
          <span>New conversation</span>
          <span className="shortcut">⌘ K</span>
        </button>

        <div className="sidebar-section">
          <p className="sidebar-label">WORKSPACE</p>
          <button className="nav-item active" type="button">
            <span className="nav-icon">◫</span>
            Ask Helix
          </button>
          <button className="nav-item" type="button">
            <span className="nav-icon">▤</span>
            Knowledge base
            <span className="nav-count">11</span>
          </button>
        </div>

        <div className="sidebar-section recent-section">
          <p className="sidebar-label">GETTING STARTED</p>
          <div className="sidebar-note">
            <span className="note-icon">✳</span>
            <div>
              <strong>Your knowledge, connected.</strong>
              <p>Ask questions and explore answers grounded in your documents.</p>
            </div>
          </div>
        </div>

        <div className="sidebar-bottom">
          <div className="connection-status">
            <span className="status-dot" />
            <span>Workspace ready</span>
          </div>
          <div className="profile-row">
            <div className="avatar">H</div>
            <div className="profile-copy">
              <strong>Helix Workspace</strong>
              <span>Personal workspace</span>
            </div>
            <span className="profile-menu">···</span>
          </div>
        </div>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div className="breadcrumb">
            <span>Workspace</span>
            <span className="breadcrumb-separator">/</span>
            <strong>{hasMessages ? 'Conversation' : 'Ask Helix'}</strong>
          </div>
          <div className="topbar-right">
            <span className="model-indicator">
              <span className="model-dot" />
              AI knowledge assistant
            </span>
            <button
              className="icon-button"
              type="button"
              aria-label="New conversation"
              onClick={startNewConversation}
            >
              ＋
            </button>
          </div>
        </header>

        <section className={`chat-area ${hasMessages ? 'conversation-area' : ''}`}>
          {!hasMessages ? (
            <div className="welcome-content">
              <div className="welcome-eyebrow">
                <span className="eyebrow-sparkle">✳</span>
                YOUR KNOWLEDGE, AT YOUR FINGERTIPS
              </div>

              <h1>
                Answers start
                <br />
                <span>with what you know.</span>
              </h1>

              <p className="welcome-description">
                Ask a question. Helix searches your knowledge base, brings
                relevant context together, and gives you an answer with sources
                you can explore.
              </p>

              <div className="suggestions-heading">
                <span>START EXPLORING</span>
                <span className="suggestion-hint">Choose a prompt to begin</span>
              </div>

              <div className="suggestions-grid">
                {suggestions.map((suggestion, index) => (
                  <button
                    className="suggestion-card"
                    key={suggestion.title}
                    onClick={() => void sendMessage(suggestion.prompt)}
                    type="button"
                    disabled={loading}
                  >
                    <span className={`suggestion-icon icon-${index}`}>
                      {suggestion.icon}
                    </span>
                    <span className="suggestion-title">
                      {suggestion.title}
                    </span>
                    <span className="suggestion-description">
                      {suggestion.description}
                    </span>
                    <span className="suggestion-arrow">↗</span>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="conversation-content">
              <div className="conversation-heading">
                <span className="welcome-eyebrow">
                  <span className="eyebrow-sparkle">✳</span>
                  HELIX CONVERSATION
                </span>
                <h2>Let’s explore your knowledge.</h2>
              </div>

              {messages.map((message) => (
                <article className={`message ${message.role}`} key={message.id}>
                  <div className="message-avatar">
                    {message.role === 'user' ? 'Y' : 'H'}
                  </div>
                  <div className="message-body">
                    <div className="message-label">
                      {message.role === 'user' ? 'You' : 'Helix'}
                      {message.role === 'assistant' && loading && !message.content
                        ? ' · Thinking…'
                        : ''}
                    </div>
                    <div className="message-text">
                      {message.content || (
                        <span className="typing-indicator">
                          <i />
                          <i />
                          <i />
                        </span>
                      )}
                    </div>

                    {message.role === 'assistant' &&
                      message.citations &&
                      message.citations.length > 0 && (
                        <div className="citations">
                          <div className="citations-heading">
                            <span>◈</span>
                            SOURCES
                            <span className="citation-count">
                              {message.citations.length}
                            </span>
                          </div>
                          <div className="citation-list">
                            {message.citations.map((citation, index) => (
                              <div
                                className="citation-card"
                                key={`${citation.document_id}-${citation.chunk_id}-${index}`}
                              >
                                <span className="citation-file-icon">▤</span>
                                <div className="citation-details">
                                  <strong>{citation.file_name}</strong>
                                  <span>{citation.path}</span>
                                </div>
                                <span className="citation-number">
                                  {String(index + 1).padStart(2, '0')}
                                </span>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                  </div>
                </article>
              ))}

              {error && (
                <div className="error-banner" role="alert">
                  <span>!</span>
                  <p>{error}</p>
                  <button type="button" onClick={() => setError('')}>
                    Dismiss
                  </button>
                </div>
              )}
              <div ref={bottomRef} />
            </div>
          )}
        </section>

        {error && !hasMessages && (
          <div className="global-error" role="alert">
            {error}
            <button type="button" onClick={() => setError('')}>
              Dismiss
            </button>
          </div>
        )}

        <div className="composer-dock">
          <form
            className="composer"
            onSubmit={(event) => {
              event.preventDefault()
              void sendMessage()
            }}
          >
            <textarea
              aria-label="Ask a question"
              placeholder="Ask anything about your knowledge base..."
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              onKeyDown={(event) => {
                if (
                  event.key === 'Enter' &&
                  !event.shiftKey &&
                  !event.nativeEvent.isComposing
                ) {
                  event.preventDefault()
                  if (!loading) void sendMessage()
                }
              }}
              rows={2}
              disabled={loading}
            />
            <div className="composer-footer">
              <div className="composer-tools">
                <span className="composer-hint">
                  <kbd>↵</kbd> to send · <kbd>⇧ ↵</kbd> for a new line
                </span>
              </div>
              {loading ? (
                <button
                  className="send-button stop-button"
                  type="button"
                  onClick={() => abortRef.current?.abort()}
                >
                  <span>Stop</span>
                  <span className="send-arrow">■</span>
                </button>
              ) : (
                <button
                  className="send-button"
                  type="submit"
                  disabled={!query.trim()}
                  aria-label="Send question"
                >
                  <span>Ask Helix</span>
                  <span className="send-arrow">↑</span>
                </button>
              )}
            </div>
          </form>
          <p className="privacy-note">
            <span>◈</span>
            Responses are generated from retrieved context. Verify important
            information against the cited sources.
          </p>
        </div>

        <footer className="main-footer">
          <span>PROJECT HELIX</span>
          <span>Retrieval-augmented intelligence</span>
        </footer>
      </main>
    </div>
  )
}

export default App
