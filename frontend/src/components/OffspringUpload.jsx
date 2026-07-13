import { useState, useRef } from 'react';
import api from '../api/axios';

export default function OffspringUpload({ onResults, onError, loading, setLoading }) {
  const [motherFile, setMotherFile] = useState(null);
  const [fatherFile, setFatherFile] = useState(null);
  
  const handleFileChange = (e, setFile) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setFile(file);
    } else if (file) {
      onError('Please select a valid PDF file.');
    }
  };

  const handleUpload = async () => {
    if (!motherFile || !fatherFile) {
      onError('Please upload both the mother\'s and father\'s genetic reports.');
      return;
    }

    setLoading(true);
    onError('');
    
    const formData = new FormData();
    formData.append('mother_file', motherFile);
    formData.append('father_file', fatherFile);

    try {
      const res = await api.post('/upload-offspring', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 60000,
      });
      onResults(res.data);
    } catch (err) {
      console.error(err);
      onError(err.response?.data?.detail || 'Failed to process the reports.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card-flat fade-in">
      <div className="text-center mb-6">
        <h2 className="text-xl font-bold mb-2">Upload Parents' Genetic Reports</h2>
        <p className="text-sm" style={{ color: 'var(--color-text-secondary)' }}>
          Select the PDF reports for both parents to predict the genetic disease risks for their offspring.
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6 mb-6">
        {/* Mother Upload */}
        <div>
          <label className="block text-sm font-bold mb-2 text-center" style={{ color: 'var(--color-text-primary)' }}>Mother's Report</label>
          <div className="border-2 border-dashed rounded-xl p-6 text-center transition-colors"
               style={{ 
                 borderColor: motherFile ? 'var(--color-primary)' : 'var(--color-border-light)',
                 backgroundColor: motherFile ? 'rgba(15, 118, 110, 0.05)' : 'var(--color-surface)'
               }}>
            {motherFile ? (
              <div>
                <svg className="mx-auto mb-2" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="13"></line>
                  <line x1="16" y1="17" x2="8" y2="17"></line>
                  <polyline points="10 9 9 9 8 9"></polyline>
                </svg>
                <p className="text-sm font-medium" style={{ color: 'var(--color-text-primary)' }}>{motherFile.name}</p>
                <p className="text-xs mt-1 cursor-pointer hover:underline" style={{ color: 'var(--color-accent)' }} onClick={() => setMotherFile(null)}>Remove</p>
              </div>
            ) : (
              <div>
                <svg className="mx-auto mb-2 opacity-50" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                  <polyline points="17 8 12 3 7 8" />
                  <line x1="12" y1="3" x2="12" y2="15" />
                </svg>
                <label className="cursor-pointer text-sm font-semibold hover:underline" style={{ color: 'var(--color-primary)' }}>
                  Browse PDF
                  <input type="file" className="hidden" accept="application/pdf" onChange={(e) => handleFileChange(e, setMotherFile)} disabled={loading} />
                </label>
              </div>
            )}
          </div>
        </div>

        {/* Father Upload */}
        <div>
          <label className="block text-sm font-bold mb-2 text-center" style={{ color: 'var(--color-text-primary)' }}>Father's Report</label>
          <div className="border-2 border-dashed rounded-xl p-6 text-center transition-colors"
               style={{ 
                 borderColor: fatherFile ? 'var(--color-primary)' : 'var(--color-border-light)',
                 backgroundColor: fatherFile ? 'rgba(15, 118, 110, 0.05)' : 'var(--color-surface)'
               }}>
            {fatherFile ? (
              <div>
                <svg className="mx-auto mb-2" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--color-primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                  <polyline points="14 2 14 8 20 8"></polyline>
                  <line x1="16" y1="13" x2="8" y2="13"></line>
                  <line x1="16" y1="17" x2="8" y2="17"></line>
                  <polyline points="10 9 9 9 8 9"></polyline>
                </svg>
                <p className="text-sm font-medium" style={{ color: 'var(--color-text-primary)' }}>{fatherFile.name}</p>
                <p className="text-xs mt-1 cursor-pointer hover:underline" style={{ color: 'var(--color-accent)' }} onClick={() => setFatherFile(null)}>Remove</p>
              </div>
            ) : (
              <div>
                <svg className="mx-auto mb-2 opacity-50" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                  <polyline points="17 8 12 3 7 8" />
                  <line x1="12" y1="3" x2="12" y2="15" />
                </svg>
                <label className="cursor-pointer text-sm font-semibold hover:underline" style={{ color: 'var(--color-primary)' }}>
                  Browse PDF
                  <input type="file" className="hidden" accept="application/pdf" onChange={(e) => handleFileChange(e, setFatherFile)} disabled={loading} />
                </label>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="flex justify-center">
        <button
          onClick={handleUpload}
          disabled={!motherFile || !fatherFile || loading}
          className="btn-primary w-full md:w-auto px-8"
        >
          {loading ? (
            <span className="flex items-center gap-2">
              <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              Analyzing reports...
            </span>
          ) : (
            'Analyze Offspring Risk'
          )}
        </button>
      </div>
    </div>
  );
}
