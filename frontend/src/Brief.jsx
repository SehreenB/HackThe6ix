import ReactMarkdown from "react-markdown"
import { useEffect } from "react"

export default function Brief({ isOpen, onClose, content, isLoading }) {

  // Escape key to close
  useEffect(() => {
    const handler = (e) => { if (e.key === "Escape" && isOpen) onClose() }
    window.addEventListener("keydown", handler)
    return () => window.removeEventListener("keydown", handler)
  }, [isOpen, onClose])

  function copyToClipboard() {
    navigator.clipboard.writeText(content)
  }

  function download() {
    const blob = new Blob([content], { type: "text/plain" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "apogee-policy-brief.txt"
    a.click()
  }

  return (
    <div style={{
      position: "fixed",
      top: "64px",
      right: 0,
      height: "calc(100vh - 64px)",
      width: "500px",
      background: "#0f1318",
      borderLeft: "1px solid rgba(0,229,255,0.2)",
      transform: isOpen ? "translateX(0)" : "translateX(100%)",
      transition: "transform 0.35s ease",
      zIndex: 1000,
      display: "flex",
      flexDirection: "column",
      boxShadow: "-10px 0 40px rgba(0,0,0,0.5)"
    }}>

      {/* Header */}
      <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "16px 20px", borderBottom: "1px solid rgba(0,229,255,0.15)", background: "#0A0E1A" }}>
        <div>
          <div style={{ color: "#00E5FF", fontWeight: "700", fontSize: "14px", letterSpacing: "1px" }}>POLICY BRIEF</div>
          <div style={{ color: "rgba(255,255,255,0.35)", fontSize: "10px", marginTop: "2px" }}>Apogee Solutions · Liberia NSOAP</div>
        </div>
        <button
          onClick={onClose}
          style={{
            display: "flex", alignItems: "center", gap: "6px",
            background: "rgba(255,75,110,0.12)",
            border: "1px solid rgba(255,75,110,0.35)",
            color: "#FF4B6E",
            padding: "7px 14px",
            borderRadius: "8px",
            cursor: "pointer",
            fontSize: "12px",
            fontWeight: "700",
            letterSpacing: "0.08em",
            transition: "all 0.15s ease"
          }}
          onMouseEnter={e => { e.currentTarget.style.background = "rgba(255,75,110,0.25)"; e.currentTarget.style.borderColor = "rgba(255,75,110,0.6)" }}
          onMouseLeave={e => { e.currentTarget.style.background = "rgba(255,75,110,0.12)"; e.currentTarget.style.borderColor = "rgba(255,75,110,0.35)" }}
        >
          <span style={{ fontSize: "14px", lineHeight: 1 }}>✕</span>
          <span>Close Brief</span>
        </button>
      </div>

      {/* Content */}
      <div style={{ flex: 1, overflowY: "auto", padding: "20px", color: "rgba(255,255,255,0.85)", fontSize: "13px", lineHeight: "1.7" }}>
        {isLoading && content === "" && (
          <div style={{ color: "rgba(0,229,255,0.6)", fontSize: "13px" }}>⟳ Generating brief...</div>
        )}
        <div style={{ color: "rgba(255,255,255,0.85)" }}>
          <ReactMarkdown
            components={{
              h1: ({ children }) => <h1 style={{ color: "#00E5FF", fontSize: "18px", fontWeight: "700", marginBottom: "12px", marginTop: "0" }}>{children}</h1>,
              h2: ({ children }) => <h2 style={{ color: "#00E5FF", fontSize: "15px", fontWeight: "600", marginBottom: "8px", marginTop: "20px", borderBottom: "1px solid rgba(0,229,255,0.15)", paddingBottom: "6px" }}>{children}</h2>,
              h3: ({ children }) => <h3 style={{ color: "rgba(0,229,255,0.8)", fontSize: "13px", fontWeight: "600", marginBottom: "6px", marginTop: "14px" }}>{children}</h3>,
              p: ({ children }) => <p style={{ marginBottom: "10px", color: "rgba(255,255,255,0.8)" }}>{children}</p>,
              li: ({ children }) => <li style={{ marginBottom: "5px", color: "rgba(255,255,255,0.75)" }}>{children}</li>,
              strong: ({ children }) => <strong style={{ color: "#00E5FF", fontWeight: "600" }}>{children}</strong>,
              ul: ({ children }) => <ul style={{ paddingLeft: "18px", marginBottom: "10px" }}>{children}</ul>,
              ol: ({ children }) => <ol style={{ paddingLeft: "18px", marginBottom: "10px" }}>{children}</ol>,
            }}
          >
            {content}
          </ReactMarkdown>
        </div>
        {isLoading && <span style={{ color: "#00E5FF", animation: "pulse 1s infinite" }}>▌</span>}
      </div>

      {/* Actions */}
      {!isLoading && content && (
        <div style={{ padding: "14px 20px", borderTop: "1px solid rgba(0,229,255,0.15)", display: "flex", gap: "10px", background: "#0A0E1A" }}>
          <button
            onClick={copyToClipboard}
            style={{ flex: 1, padding: "10px", borderRadius: "7px", fontSize: "12px", fontWeight: "600", cursor: "pointer", background: "rgba(0,229,255,0.1)", color: "#00E5FF", border: "1px solid rgba(0,229,255,0.3)" }}
          >
            Copy
          </button>
          <button
            onClick={download}
            style={{ flex: 1, padding: "10px", borderRadius: "7px", fontSize: "12px", fontWeight: "600", cursor: "pointer", background: "#00E5FF", color: "#0A0E1A", border: "none" }}
          >
            Download .txt
          </button>
        </div>
      )}
    </div>
  )
}