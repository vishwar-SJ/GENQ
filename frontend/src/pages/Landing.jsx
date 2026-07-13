import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function FeatureIcon({ name }) {
  const props = { width: 32, height: 32, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 1.5, strokeLinecap: 'round', strokeLinejoin: 'round' };
  switch (name) {
    case 'upload':
      return <svg {...props}><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="17 8 12 3 7 8" /><line x1="12" y1="3" x2="12" y2="15" /></svg>;
    case 'analyze':
      return <svg {...props}><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" /></svg>;
    case 'view':
      return <svg {...props}><line x1="18" y1="20" x2="18" y2="10" /><line x1="12" y1="20" x2="12" y2="4" /><line x1="6" y1="20" x2="6" y2="14" /></svg>;
    default:
      return null;
  }
}

function SmallIcon({ name }) {
  const props = { width: 24, height: 24, viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: 2, strokeLinecap: 'round', strokeLinejoin: 'round' };
  switch (name) {
    case 'diabetes':
      return <svg {...props}><path d="M12 2.69l5.66 5.66a8 8 0 11-11.31 0z" /></svg>;
    case 'heart':
      return <svg {...props}><path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z" /></svg>;
    case 'pill':
      return <svg {...props}><path d="M10.5 1.5l-8 8a5 5 0 007 7l8-8a5 5 0 00-7-7z" /><line x1="8" y1="12" x2="12" y2="8" /></svg>;
    default:
      return null;
  }
}

export default function Landing() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-[calc(100vh-4rem)]">
      {/* Hero Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 sm:py-24">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left: Copy */}
          <div className="fade-in">
            <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold mb-6"
              style={{ backgroundColor: 'rgba(15, 118, 110, 0.08)', color: 'var(--color-primary)' }}>
              <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: 'var(--color-primary)' }} />
              Genetic Risk Analysis
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-tight mb-6">
              Understand Your{' '}
              <span className="text-gradient">Genetic Risk</span>
              <br />
              in Minutes
            </h1>

            <p className="text-lg mb-8 max-w-lg leading-relaxed" style={{ color: 'var(--color-text-secondary)' }}>
              Upload your genetic report and get personalized insights on disease risk and drug response.
              Powered by published polygenic risk scores and pharmacogenomic guidelines.
            </p>

            <div className="flex flex-wrap gap-3">
              {isAuthenticated ? (
                <Link to="/dashboard" className="btn-primary no-underline text-base px-6 py-3">
                  Go to Dashboard →
                </Link>
              ) : (
                <>
                  <Link to="/signup" className="btn-primary no-underline text-base px-6 py-3">
                    Get Started — Free
                  </Link>
                  <Link to="/login" className="btn-secondary no-underline text-base px-6 py-3">
                    Log In
                  </Link>
                </>
              )}
            </div>
          </div>

          {/* Right: Feature illustration */}
          <div className="fade-in hidden lg:block" style={{ animationDelay: '0.2s', animationFillMode: 'both' }}>
            <div className="relative">
              {/* DNA helix illustration using CSS */}
              <div className="rounded-2xl p-8"
                style={{ backgroundColor: 'var(--color-surface-dark)', border: '1px solid rgba(255,255,255,0.1)' }}>
                <div className="space-y-4">
                  {/* Mock disease risk cards */}
                  <div className="rounded-lg p-4" style={{ backgroundColor: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.08)' }}>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <span style={{ color: 'var(--color-primary)' }}>
                          <SmallIcon name="diabetes" />
                        </span>
                        <div>
                          <p className="text-sm font-semibold" style={{ color: 'var(--color-text-light)' }}>Type 2 Diabetes</p>
                          <p className="text-xs" style={{ color: 'var(--color-text-muted)' }}>Polygenic Risk Score</p>
                        </div>
                      </div>
                      <span className="risk-badge risk-low">Low</span>
                    </div>
                  </div>
                  <div className="rounded-lg p-4" style={{ backgroundColor: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.08)' }}>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <span style={{ color: 'var(--color-primary)' }}>
                          <SmallIcon name="heart" />
                        </span>
                        <div>
                          <p className="text-sm font-semibold" style={{ color: 'var(--color-text-light)' }}>Coronary Artery Disease</p>
                          <p className="text-xs" style={{ color: 'var(--color-text-muted)' }}>Polygenic Risk Score</p>
                        </div>
                      </div>
                      <span className="risk-badge risk-average">Average</span>
                    </div>
                  </div>
                  <div className="rounded-lg p-4" style={{ backgroundColor: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.08)' }}>
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <span style={{ color: 'var(--color-accent)' }}>
                          <SmallIcon name="pill" />
                        </span>
                        <div>
                          <p className="text-sm font-semibold" style={{ color: 'var(--color-text-light)' }}>Clopidogrel Response</p>
                          <p className="text-xs" style={{ color: 'var(--color-text-muted)' }}>CYP2C19 Metabolizer Status</p>
                        </div>
                      </div>
                      <span className="risk-badge" style={{ backgroundColor: '#dbeafe', color: '#1e40af' }}>Normal</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16" style={{ backgroundColor: 'white' }}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-2xl sm:text-3xl font-bold mb-3">How It Works</h2>
            <p style={{ color: 'var(--color-text-secondary)' }}>Three simple steps to your personalized genetic insights</p>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                step: '01',
                title: 'Upload Your Report',
                desc: 'Upload a PDF genetic report from any DNA testing service. We extract rsID and genotype data automatically.',
                icon: 'upload',
              },
              {
                step: '02',
                title: 'Automated Analysis',
                desc: 'Our engines calculate polygenic risk scores for diseases and determine drug metabolizer status from your variants.',
                icon: 'analyze',
              },
              {
                step: '03',
                title: 'View Your Results',
                desc: 'See color-coded disease risk levels, percentile rankings, and pharmacogenomic drug response guidance.',
                icon: 'view',
              },
            ].map((feat) => (
              <div key={feat.step} className="card-flat text-center slide-up">
                <div className="flex justify-center mb-4" style={{ color: 'var(--color-primary)' }}>
                  <FeatureIcon name={feat.icon} />
                </div>
                <div className="text-xs font-bold mb-2 tracking-widest uppercase" style={{ color: 'var(--color-primary)' }}>
                  Step {feat.step}
                </div>
                <h3 className="text-lg font-bold mb-2">{feat.title}</h3>
                <p className="text-sm" style={{ color: 'var(--color-text-secondary)' }}>{feat.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Diseases & Drugs Section */}
      <section className="py-16" style={{ backgroundColor: 'var(--color-surface)' }}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-2 gap-12">
            <div>
              <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                <span className="inline-block w-1 h-6 rounded-full" style={{ backgroundColor: 'var(--color-primary)' }} />
                12 Disease Risk Analyzers
              </h3>
              <ul className="space-y-3">
                {['Type 2 Diabetes', 'Coronary Artery Disease', 'Breast Cancer', "Alzheimer's Disease", 'Thalassemia', "Parkinson's Disease", 'Lung Cancer', 'Prostate Cancer', 'Celiac Disease', 'Rheumatoid Arthritis', 'Asthma', 'Atrial Fibrillation'].map((d) => (
                  <li key={d} className="flex items-center gap-2 text-sm" style={{ color: 'var(--color-text-secondary)' }}>
                    <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: 'var(--color-primary)' }} />
                    {d}
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
                <span className="inline-block w-1 h-6 rounded-full" style={{ backgroundColor: 'var(--color-accent)' }} />
                8 Drug Response Predictors
              </h3>
              <ul className="space-y-3">
                {[
                  'Clopidogrel (CYP2C19)',
                  'Isoniazid (NAT2)',
                  'Warfarin (CYP2C9/VKORC1)',
                  'Codeine (CYP2D6)',
                  'Simvastatin (SLCO1B1)',
                  'Omeprazole (CYP2C19)',
                  'Tamoxifen (CYP2D6)',
                  'Abacavir (HLA-B)',
                ].map((d) => (
                  <li key={d} className="flex items-center gap-2 text-sm" style={{ color: 'var(--color-text-secondary)' }}>
                    <span className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: 'var(--color-accent)' }} />
                    {d}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8" style={{ backgroundColor: 'var(--color-surface-dark)' }}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-sm" style={{ color: 'var(--color-text-muted)' }}>
            © 2026 GENQ. For educational and research purposes only.
          </p>
          <p className="text-xs mt-2" style={{ color: 'var(--color-text-muted)', opacity: 0.6 }}>
            This is not a medical diagnosis tool. Always consult a healthcare professional.
          </p>
        </div>
      </footer>
    </div>
  );
}
