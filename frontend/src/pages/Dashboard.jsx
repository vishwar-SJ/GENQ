import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import api from '../api/axios';
import UploadSection from '../components/UploadSection';
import OffspringUpload from '../components/OffspringUpload';
import DiseaseRiskCard from '../components/DiseaseRiskCard';
import DrugResponseCard from '../components/DrugResponseCard';
import OffspringRiskCard from '../components/OffspringRiskCard';
import DisclaimerBanner from '../components/DisclaimerBanner';
import ReportDownload from '../components/ReportDownload';
import ChatBot from '../components/ChatBot';

export default function Dashboard() {
  const { user, isAuthenticated, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  
  const [activeTab, setActiveTab] = useState('personal'); // 'personal' or 'offspring'
  
  // Personal state
  const [personalResults, setPersonalResults] = useState(null);
  const [personalError, setPersonalError] = useState('');
  const [personalUploading, setPersonalUploading] = useState(false);
  const [loadingPrevious, setLoadingPrevious] = useState(true);

  // Offspring state
  const [offspringResults, setOffspringResults] = useState(null);
  const [offspringError, setOffspringError] = useState('');
  const [offspringUploading, setOffspringUploading] = useState(false);

  // Redirect if not authenticated
  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, authLoading, navigate]);

  // Load latest personal results on mount
  useEffect(() => {
    if (!isAuthenticated) return;

    const fetchLatest = async () => {
      try {
        const res = await api.get('/results/latest');
        setPersonalResults(res.data);
      } catch (err) {
        if (err.response?.status !== 404) {
          console.error('Failed to load previous results');
        }
      } finally {
        setLoadingPrevious(false);
      }
    };

    fetchLatest();
  }, [isAuthenticated]);

  const handlePersonalResults = (data) => {
    setPersonalResults(data);
    setPersonalError('');
  };

  const handleOffspringResults = (data) => {
    setOffspringResults(data);
    setOffspringError('');
  };

  if (authLoading) {
    return (
      <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center">
        <div className="flex gap-1.5">
          <div className="w-3 h-3 rounded-full pulse-dot" style={{ backgroundColor: 'var(--color-primary)' }} />
          <div className="w-3 h-3 rounded-full pulse-dot" style={{ backgroundColor: 'var(--color-primary)', animationDelay: '0.2s' }} />
          <div className="w-3 h-3 rounded-full pulse-dot" style={{ backgroundColor: 'var(--color-primary)', animationDelay: '0.4s' }} />
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-[calc(100vh-4rem)] pb-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        
        {/* Page Header */}
        <div className="mb-6 fade-in flex flex-col md:flex-row md:justify-between md:items-end gap-4">
          <div>
            <h1 className="text-2xl sm:text-3xl font-bold mb-1">Dashboard</h1>
            <p style={{ color: 'var(--color-text-secondary)' }}>
              Upload genetic reports to get personalized risk and drug response insights.
            </p>
          </div>
          {activeTab === 'personal' && personalResults && (
            <ReportDownload results={personalResults} user={user} />
          )}
        </div>

        {/* Tabs */}
        <div className="flex border-b mb-8 fade-in" style={{ borderColor: 'var(--color-border-light)' }}>
          <button
            className={`py-3 px-6 text-sm font-semibold border-b-2 transition-colors ${
              activeTab === 'personal' 
                ? 'border-[var(--color-primary)] text-[var(--color-primary)]' 
                : 'border-transparent text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)]'
            }`}
            onClick={() => setActiveTab('personal')}
          >
            Personal Analysis
          </button>
          <button
            className={`py-3 px-6 text-sm font-semibold border-b-2 transition-colors ${
              activeTab === 'offspring' 
                ? 'border-[var(--color-accent)] text-[var(--color-accent)]' 
                : 'border-transparent text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)]'
            }`}
            onClick={() => setActiveTab('offspring')}
          >
            Offspring Analysis
          </button>
        </div>

        {/* ---------------- PERSONAL TAB ---------------- */}
        {activeTab === 'personal' && (
          <div className="fade-in">
            {/* Upload Section */}
            <div className="mb-8">
              <UploadSection
                onResults={handlePersonalResults}
                onError={setPersonalError}
                loading={personalUploading}
                setLoading={setPersonalUploading}
              />
            </div>

            {/* Error message */}
            {personalError && (
              <div className="mb-6 rounded-lg px-4 py-3 text-sm font-medium fade-in"
                style={{ backgroundColor: '#fecaca', color: '#991b1b', border: '1px solid #fca5a5' }}>
                {personalError}
              </div>
            )}

            {/* Results */}
            {personalResults && (
              <div className="space-y-10 fade-in">
                <DisclaimerBanner />

                {/* Report metadata */}
                <div className="flex flex-wrap items-center gap-4 text-sm" style={{ color: 'var(--color-text-muted)' }}>
                  <span>Report #{personalResults.report_id}</span>
                  <span>•</span>
                  <span>{personalResults.snp_count} SNPs analyzed</span>
                  <span>•</span>
                  <span>{new Date(personalResults.uploaded_at).toLocaleDateString('en-US', {
                    year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit',
                  })}</span>
                </div>

                <section>
                  <div className="flex items-center gap-2.5 mb-5">
                    <span className="inline-block w-1 h-7 rounded-full" style={{ backgroundColor: 'var(--color-primary)' }} />
                    <h2 className="text-xl font-bold">Disease Risk Assessment</h2>
                  </div>
                  <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {personalResults.disease_risks.map((risk, i) => (
                      <DiseaseRiskCard key={risk.disease_name} result={risk} index={i} />
                    ))}
                  </div>
                </section>

                <section>
                  <div className="flex items-center gap-2.5 mb-5">
                    <span className="inline-block w-1 h-7 rounded-full" style={{ backgroundColor: 'var(--color-accent)' }} />
                    <h2 className="text-xl font-bold">Drug Response Analysis</h2>
                  </div>
                  <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {personalResults.drug_responses.map((drug, i) => (
                      <DrugResponseCard key={drug.drug_name} result={drug} index={i} />
                    ))}
                  </div>
                </section>

                <div className="pt-4">
                  <DisclaimerBanner />
                </div>
              </div>
            )}

            {/* No results yet + not loading */}
            {!personalResults && !loadingPrevious && !personalUploading && (
              <div className="text-center py-16 fade-in">
                <div className="flex justify-center mb-4 text-gray-400">
                  <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M8 4c0 4 8 4 8 8s-8 4-8 8" /><path d="M16 4c0 4-8 4-8 8s8 4 8 8" /><line x1="8" y1="8" x2="16" y2="8" /><line x1="8" y1="16" x2="16" y2="16" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold mb-2">No Results Yet</h3>
                <p className="text-sm max-w-md mx-auto" style={{ color: 'var(--color-text-secondary)' }}>
                  Upload a genetic report PDF above to see your personalized disease risk and drug response analysis.
                </p>
              </div>
            )}

            {/* Loading previous results */}
            {loadingPrevious && !personalResults && (
              <div className="text-center py-16">
                <div className="flex justify-center gap-1.5">
                  <div className="w-3 h-3 rounded-full pulse-dot" style={{ backgroundColor: 'var(--color-primary)' }} />
                  <div className="w-3 h-3 rounded-full pulse-dot" style={{ backgroundColor: 'var(--color-primary)', animationDelay: '0.2s' }} />
                  <div className="w-3 h-3 rounded-full pulse-dot" style={{ backgroundColor: 'var(--color-primary)', animationDelay: '0.4s' }} />
                </div>
                <p className="text-sm mt-3" style={{ color: 'var(--color-text-muted)' }}>Loading previous results...</p>
              </div>
            )}
            
            {/* Floating Chatbot */}
            {personalResults && (
              <ChatBot reportId={personalResults.report_id} />
            )}
          </div>
        )}

        {/* ---------------- OFFSPRING TAB ---------------- */}
        {activeTab === 'offspring' && (
          <div className="fade-in">
            <div className="mb-8">
              <OffspringUpload
                onResults={handleOffspringResults}
                onError={setOffspringError}
                loading={offspringUploading}
                setLoading={setOffspringUploading}
              />
            </div>

            {/* Error message */}
            {offspringError && (
              <div className="mb-6 rounded-lg px-4 py-3 text-sm font-medium fade-in"
                style={{ backgroundColor: '#fecaca', color: '#991b1b', border: '1px solid #fca5a5' }}>
                {offspringError}
              </div>
            )}

            {/* Results */}
            {offspringResults && (
              <div className="space-y-10 fade-in">
                <DisclaimerBanner />

                {/* Report metadata */}
                <div className="flex flex-wrap items-center gap-4 text-sm" style={{ color: 'var(--color-text-muted)' }}>
                  <span>Offspring Report #{offspringResults.id}</span>
                  <span>•</span>
                  <span>{new Date(offspringResults.created_at).toLocaleDateString('en-US', {
                    year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit',
                  })}</span>
                </div>

                <section>
                  <div className="flex items-center gap-2.5 mb-5">
                    <span className="inline-block w-1 h-7 rounded-full" style={{ backgroundColor: 'var(--color-accent)' }} />
                    <h2 className="text-xl font-bold">Predicted Offspring Disease Risks</h2>
                  </div>
                  <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                    {offspringResults.disease_risks.map((risk, i) => (
                      <OffspringRiskCard key={risk.disease_name} result={risk} index={i} />
                    ))}
                  </div>
                </section>

                <div className="pt-4">
                  <DisclaimerBanner />
                </div>
              </div>
            )}
            
            {/* No results yet + not loading */}
            {!offspringResults && !offspringUploading && (
              <div className="text-center py-16 fade-in">
                <div className="flex justify-center mb-4 text-gray-400">
                  <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                  </svg>
                </div>
                <h3 className="text-lg font-semibold mb-2">No Offspring Analysis Yet</h3>
                <p className="text-sm max-w-md mx-auto" style={{ color: 'var(--color-text-secondary)' }}>
                  Upload both parents' genetic report PDFs above to predict potential disease risks for their offspring.
                </p>
              </div>
            )}
          </div>
        )}

      </div>
    </div>
  );
}
