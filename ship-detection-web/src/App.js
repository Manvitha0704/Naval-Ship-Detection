import React, { useState } from "react";
import "./App.css";

export default function App() {
  const [images, setImages] = useState([]);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  function handleFiles(e) {
    const files = Array.from(e.target.files).slice(0, 10);
    const withPreview = files.map(f => ({
      file: f,
      url: URL.createObjectURL(f)
    }));
    setImages(withPreview);
    setResults(null);
  }

  async function runDetection() {
    setError(null);
    if (images.length === 0) {
      setError("⚠️ Please upload at least one image.");
      return;
    }
    setLoading(true);

    // Mock detections
    await new Promise(r => setTimeout(r, 800));
    const mock = images.map(img => ({
      fileName: img.file.name,
      detections: [
        { class: "Cargo Ship", conf: (Math.random() * 0.4 + 0.5).toFixed(2) },
        { class: "Motorboat", conf: (Math.random() * 0.4 + 0.4).toFixed(2) }
      ]
    }));
    setResults(mock);
    setLoading(false);
  }

  function clearAll() {
    images.forEach(i => URL.revokeObjectURL(i.url));
    setImages([]);
    setResults(null);
    setError(null);
  }

  return (
    <div className="container">
      <h1>🚢 Ship Detection</h1>
      <p className="subtitle">Upload images, run mock detection, and view YOLO training results.</p>

      <div className="upload-section">
        <input type="file" accept="image/*" multiple onChange={handleFiles} />
        <div className="buttons">
          <button onClick={runDetection} disabled={loading}>
            {loading ? "Running..." : "▶ Run Detection"}
          </button>
          <button onClick={clearAll}>❌ Clear</button>
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      {/* Uploaded & Detection Results */}
      <div className="grid">
        {/* Uploaded Images */}
        <div className="card">
          <h3>📤 Uploaded Images</h3>
          {images.length === 0 && <p>No images yet.</p>}
          <div className="img-grid">
            {images.map((img, i) => (
              <div key={i} className="img-card">
                <img src={img.url} alt="upload" />
                <p>{img.file.name}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Detection Results */}
        <div className="card">
          <h3>🔍 Detections</h3>
          {!results && <p>No results yet. Click "Run Detection".</p>}
          {results &&
            results.map((r, idx) => (
              <div key={idx} className="result-card">
                <strong>{r.fileName}</strong>
                <table>
                  <thead>
                    <tr>
                      <th>Class</th>
                      <th>Confidence</th>
                    </tr>
                  </thead>
                  <tbody>
                    {r.detections.map((d, i) => (
                      <tr key={i}>
                        <td>{d.class}</td>
                        <td>{d.conf}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ))}
        </div>
      </div>

      {/* Training Results Section */}
      <div className="training-results">
        <h2>📊 YOLO Training Results</h2>
        <p>These images are taken directly from your <code>runs/train/</code> output folder.</p>
        <div className="results-grid">
          <div className="result-img">
            <h4>📈 Training Performance</h4>
            <img src="/results.png" alt="Training Results" />
          </div>
          <div className="result-img">
            <h4>🎯 Confusion Matrix</h4>
            <img src="/confusion_matrix.png" alt="Confusion Matrix" />
          </div>
          <div className="result-img">
            <h4>🏷 Labels Distribution</h4>
            <img src="/labels.jpg" alt="Labels" />
          </div>
        </div>
        
      </div>

      <footer>
        Built with <code>React</code> | Naval— Ship Detection
      </footer>
    </div>
  );
}
