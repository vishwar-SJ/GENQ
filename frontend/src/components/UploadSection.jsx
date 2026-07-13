import { useState, useRef } from 'react';
import api from '../api/axios';

export default function UploadSection({ onResults, onError, loading, setLoading }) {
  const [consent, setConsent] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const [fileName, setFileName] = useState('');
  const fileInputRef = useRef(null);

  const handleUpload = async (file) => {
    if (!consent) {
      onError('Please check the consent box before uploading.');
      return;
    }
    if (!file || !file.name.toLowerCase().endsWith('.pdf')) {
      onError('Please upload a PDF file.');
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      onError('File size exceeds the 10MB limit.');
      return;
    }

    setLoading(true);
    setFileName(file.name);
    onError('');

    try {
      const formData = new FormData();
      formData.append('file', file);

      const res = await api.post('/upload-report', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      onResults(res.data);
    } catch (err) {
      const msg = err.response?.data?.detail || 'Upload failed. Please try again.';
      onError(msg);
    } finally {
      setLoading(false);
    }
  };

  const handleFileInput = (e) => {
    const file = e.target.files?.[0];
    if (file) handleUpload(file);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file) handleUpload(file);
  };

  return (
    <div className="card-flat fade-in">
      <h2 className="text-lg font-bold mb-1" style={{ color: 'var(--color-text-primary)' }}>
        Upload Genetic Report
      </h2>
      <p className="text-sm mb-4" style={{ color: 'var(--color-text-secondary)' }}>
        Upload a PDF containing your genetic report with rsID and genotype data.
      </p>

      {/* Consent checkbox */}
      <label className="flex items-start gap-2.5 mb-4 cursor-pointer select-none">
        <input
          type="checkbox"
          checked={consent}
          onChange={(e) => setConsent(e.target.checked)}
          className="mt-1 w-4 h-4 rounded cursor-pointer accent-[#0f766e]"
        />
        <span className="text-sm" style={{ color: 'var(--color-text-secondary)' }}>
          I understand that this analysis provides <strong>genetic risk information only</strong> and is{' '}
          <strong>not a medical diagnosis</strong>. I consent to the processing of my genetic data.
        </span>
      </label>

      {/* Drop zone */}
      <div
        className={`relative rounded-xl border-2 border-dashed p-8 text-center transition-all cursor-pointer ${
          dragOver ? 'scale-[1.01]' : ''
        }`}
        style={{
          borderColor: dragOver ? 'var(--color-primary)' : consent ? 'var(--color-border)' : '#e2e8f0',
          backgroundColor: dragOver ? 'rgba(15, 118, 110, 0.04)' : consent ? 'white' : '#f8fafc',
          opacity: consent ? 1 : 0.5,
          pointerEvents: consent ? 'auto' : 'none',
        }}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        onClick={() => consent && fileInputRef.current?.click()}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileInput}
          accept=".pdf"
          className="hidden"
        />

        {loading ? (
          <div className="flex flex-col items-center gap-3">
            <div className="flex gap-1.5">
              <div className="w-2.5 h-2.5 rounded-full pulse-dot" style={{ backgroundColor: 'var(--color-primary)', animationDelay: '0s' }} />
              <div className="w-2.5 h-2.5 rounded-full pulse-dot" style={{ backgroundColor: 'var(--color-primary)', animationDelay: '0.2s' }} />
              <div className="w-2.5 h-2.5 rounded-full pulse-dot" style={{ backgroundColor: 'var(--color-primary)', animationDelay: '0.4s' }} />
            </div>
            <p className="text-sm font-medium" style={{ color: 'var(--color-primary)' }}>
              Analyzing {fileName || 'your report'}...
            </p>
            <p className="text-xs" style={{ color: 'var(--color-text-muted)' }}>
              Extracting genetic markers and running analysis engines
            </p>
          </div>
        ) : (
          <div className="flex flex-col items-center gap-2">
            <svg className="w-10 h-10" style={{ color: 'var(--color-text-muted)' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            <p className="text-sm font-medium" style={{ color: 'var(--color-text-primary)' }}>
              Drop your PDF here or <span style={{ color: 'var(--color-primary)' }}>click to browse</span>
            </p>
            <p className="text-xs" style={{ color: 'var(--color-text-muted)' }}>
              PDF files up to 10MB • Genetic reports with rsID data
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
