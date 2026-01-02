import { useState } from "react";

/* ---------- CLEAN TEXT ---------- */
const clean = (text = "") =>
  text
    .replace(/\\\(|\\\)|\\\[|\\\]/g, "")
    .replace(/\*\*/g, "")
    .replace(/\$/g, "")
    .trim();

export default function App() {
  const [mode, setMode] = useState("text");
  const [question, setQuestion] = useState("");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [comment, setComment] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  /* -------- TEXT ---------- */
  const askQuestion = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Backend error");
      setResult(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  /* -------- IMAGE / AUDIO ---------- */
  const submitFile = async () => {
    if (!file) return;
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch("http://127.0.0.1:8000/ask_multimodal", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Multimodal error");
      console.log("📦 Response from backend:", data); // ← Add this to debug
      setResult(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  /* -------- FEEDBACK ---------- */
  const sendFeedback = async (correct) => {
    try {
      await fetch("http://127.0.0.1:8000/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          question: result?.detected_text || question,
          answer: result?.answer || "",
          correct,
          comment,
        }),
      });
      alert("Feedback saved");
    } catch (e) {
      alert("Feedback failed: " + e.message);
    }
  };

  const answer = result?.answer || "";
  const steps = Array.isArray(result?.steps) ? result.steps : [];
  const confidence = typeof result?.confidence === "number" ? result.confidence : 0;
  const trace = Array.isArray(result?.trace) ? result.trace : [];
  const context = Array.isArray(result?.context) ? result.context : [];
  const detectedText = result?.detected_text || "";

  return (
    <div style={{ maxWidth: 900, margin: "auto", padding: 20 }}>
      <h1>🧠 Math AI Agent</h1>

      <label>
        <input type="radio" checked={mode === "text"} onChange={() => setMode("text")} /> Text
      </label>{" "}
      <label>
        <input type="radio" checked={mode === "image"} onChange={() => setMode("image")} /> Image
      </label>{" "}
      <label>
        <input type="radio" checked={mode === "audio"} onChange={() => setMode("audio")} /> Audio
      </label>

      <br />
      <br />

      {mode === "text" && (
        <>
          <textarea
            placeholder="Enter math question..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            style={{ width: "100%", height: 80 }}
          />
          <button onClick={askQuestion} disabled={loading}>
            {loading ? "Thinking..." : "Submit"}
          </button>
        </>
      )}

      {(mode === "image" || mode === "audio") && (
        <>
          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <button onClick={submitFile} disabled={loading}>
            {loading ? "Processing..." : "Submit"}
          </button>
        </>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div style={{ marginTop: 20, padding: 20, background: "#f5f5f5", borderRadius: 8 }}>
          {detectedText && (
            <>
              <h3>Extraction Preview</h3>
              <pre style={{ background: "#fff", padding: 10, borderRadius: 4 }}>
                {clean(detectedText)}
              </pre>
            </>
          )}

          <h3>Final Answer</h3>
          <pre style={{ background: "#fff", padding: 10, borderRadius: 4, fontSize: 18, fontWeight: "bold" }}>
            {clean(answer) || "No answer available"}
          </pre>

          <h3>Steps</h3>
          {steps.length > 0 ? (
            <ul style={{ background: "#fff", padding: 20, borderRadius: 4 }}>
              {steps.map((s, i) => (
                <li key={i}>{clean(s)}</li>
              ))}
            </ul>
          ) : (
            <p>No steps available</p>
          )}

          <h3>Confidence</h3>
          <div style={{ background: "#ddd", height: 20, borderRadius: 4, overflow: "hidden" }}>
            <div
              style={{
                width: `${Math.round(confidence * 100)}%`,
                background: confidence > 0.5 ? "green" : "orange",
                height: 20,
                color: "white",
                textAlign: "center",
                lineHeight: "20px",
              }}
            >
              {Math.round(confidence * 100)}%
            </div>
          </div>

          <h3>Agent Trace</h3>
          <pre style={{ background: "#fff", padding: 10, borderRadius: 4 }}>
            {trace.length > 0 ? JSON.stringify(trace, null, 2) : "[]"}
          </pre>

          <h3>Retrieved Context</h3>
          <pre style={{ background: "#fff", padding: 10, borderRadius: 4, maxHeight: 200, overflow: "auto" }}>
            {context.length > 0 ? JSON.stringify(context, null, 2) : "[]"}
          </pre>

          <h3>Feedback</h3>
          <textarea
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            style={{ width: "100%", height: 60, marginBottom: 10 }}
            placeholder="Optional comment..."
          />
          <button onClick={() => sendFeedback(true)} style={{ marginRight: 10 }}>
            ✅ Correct
          </button>
          <button onClick={() => sendFeedback(false)}>❌ Incorrect</button>
        </div>
      )}
    </div>
  );
}