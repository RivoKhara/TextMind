import { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(false);

  const summarizeText = async () => {
    if (!text.trim()) return;

    setLoading(true);
    setSummary("");

    try {
      const res = await fetch("http://127.0.0.1:8000/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      const data = await res.json();
      setSummary(data.summary);
    } catch (err) {
      console.error("Error:", err);
      setSummary("Something went wrong!");
    }

    setLoading(false);
  };

  const clearText = () => {
    setText("");
    setSummary("");
  };

  return (
    <div className={`app-container ${darkMode ? "dark" : ""}`}>
      {/* Dark/Light Toggle */}
      <button
        className="toggle-btn fixed-toggle"
        onClick={() => setDarkMode(!darkMode)}
      >
        {darkMode ? "Light Mode" : "Dark Mode"}
      </button>

      <div className="content-box">
        <h1 className="title">AI Text Summarizer</h1>

        <textarea
          className="input-box"
          placeholder="Paste your text here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <div className="buttons">
          <button className="submit-btn" onClick={summarizeText}>
            {loading ? "Summarizing..." : "Summarize"}
          </button>
          <button className="clear-btn" onClick={clearText}>
            Clear
          </button>
        </div>

        {summary && (
          <div className="summary-box">
            <h2>Summary:</h2>
            <p>{summary}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
