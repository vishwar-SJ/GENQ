export default function DisclaimerBanner() {
  return (
    <div
      className="w-full rounded-lg px-4 py-3 text-sm font-medium fade-in"
      style={{
        backgroundColor: '#fef3c7',
        color: '#92400e',
        border: '1px solid #fde68a',
      }}
    >
      <div className="flex items-start gap-2">
        <svg className="w-5 h-5 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
          <path
            fillRule="evenodd"
            d="M8.485 2.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.168 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 2.495zM10 5a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-3.5A.75.75 0 0110 5zm0 9a1 1 0 100-2 1 1 0 000 2z"
            clipRule="evenodd"
          />
        </svg>
        <p>
          <strong>Medical Disclaimer:</strong> This is genetic risk information, not a medical diagnosis.
          Results are based on published research and simplified scoring models. Please consult a doctor
          or genetic counselor before making any medical decisions.
        </p>
      </div>
    </div>
  );
}
