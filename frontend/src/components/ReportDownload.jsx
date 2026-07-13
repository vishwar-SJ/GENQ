import { useState } from 'react';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

export default function ReportDownload({ results, user }) {
  const [downloading, setDownloading] = useState(false);

  const handleDownload = () => {
    setDownloading(true);

    try {
      // Create PDF
      const doc = new jsPDF();
      
      // Set font to Times New Roman
      doc.setFont("times", "normal");
      
      const pageWidth = doc.internal.pageSize.getWidth();
      
      // Helper for centered text
      const centerText = (text, y, size = 12, style = "normal") => {
        doc.setFontSize(size);
        doc.setFont("times", style);
        const textWidth = doc.getStringUnitWidth(text) * size / doc.internal.scaleFactor;
        const x = (pageWidth - textWidth) / 2;
        doc.text(text, x, y);
      };

      // Header
      centerText("GENQ Health Report", 20, 24, "bold");
      centerText("Personalized Genetic Disease Risk & Drug Response", 30, 14, "italic");

      doc.setFontSize(11);
      doc.setFont("times", "normal");
      doc.text(`Patient: ${user?.username || 'Unknown'}`, 14, 45);
      doc.text(`Email: ${user?.email || 'Unknown'}`, 14, 52);
      
      const dateStr = new Date(results.uploaded_at).toLocaleDateString('en-US', {
        year: 'numeric', month: 'long', day: 'numeric'
      });
      doc.text(`Report Date: ${dateStr}`, pageWidth - 14, 45, { align: 'right' });
      doc.text(`Report ID: ${results.report_id}`, pageWidth - 14, 52, { align: 'right' });

      // Line separator
      doc.setLineWidth(0.5);
      doc.line(14, 58, pageWidth - 14, 58);

      // Section: Disease Risk
      doc.setFontSize(16);
      doc.setFont("times", "bold");
      doc.text("1. Disease Risk Assessment", 14, 70);

      const diseaseData = results.disease_risks.map(r => [
        r.disease_name,
        r.risk_label,
        r.percentile != null ? `${r.percentile}%` : 'N/A',
        r.is_estimated === 'true' ? 'Yes' : 'No'
      ]);

      autoTable(doc, {
        startY: 75,
        head: [['Disease', 'Risk Level', 'Percentile', 'Estimated']],
        body: diseaseData,
        theme: 'striped',
        headStyles: { fillColor: [15, 118, 110], font: 'times', fontStyle: 'bold' },
        bodyStyles: { font: 'times' },
        styles: { font: 'times' }
      });

      // Section: Drug Response
      let finalY = doc.lastAutoTable.finalY || 75;
      
      // Check if we need a page break
      if (finalY > 200) {
        doc.addPage();
        finalY = 20;
      } else {
        finalY += 15;
      }

      doc.setFontSize(16);
      doc.setFont("times", "bold");
      doc.text("2. Pharmacogenomic Drug Response", 14, finalY);

      const drugData = results.drug_responses.map(d => [
        d.drug_name,
        d.gene,
        d.metabolizer_status,
        d.guidance_text
      ]);

      autoTable(doc, {
        startY: finalY + 5,
        head: [['Medication', 'Gene', 'Metabolizer Status', 'Clinical Guidance']],
        body: drugData,
        theme: 'striped',
        headStyles: { fillColor: [55, 48, 163], font: 'times', fontStyle: 'bold' },
        bodyStyles: { font: 'times' },
        styles: { font: 'times' },
        columnStyles: { 3: { cellWidth: 80 } } // Give guidance more space
      });

      // Footer
      const pageCount = doc.internal.getNumberOfPages();
      for (let i = 1; i <= pageCount; i++) {
        doc.setPage(i);
        doc.setFontSize(10);
        doc.setFont("times", "italic");
        doc.text(
          "Disclaimer: This report is for educational purposes only and is not a medical diagnosis.",
          pageWidth / 2,
          doc.internal.pageSize.getHeight() - 10,
          { align: 'center' }
        );
      }

      // Save PDF
      doc.save(`GENQ_Report_${results.report_id}.pdf`);
    } catch (err) {
      console.error("Failed to generate PDF", err);
      alert("Failed to generate PDF report.");
    } finally {
      setDownloading(false);
    }
  };

  return (
    <button 
      onClick={handleDownload}
      disabled={downloading}
      className="btn-secondary text-sm px-4 py-2 flex items-center gap-2"
    >
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
        <polyline points="7 10 12 15 17 10" />
        <line x1="12" y1="15" x2="12" y2="3" />
      </svg>
      {downloading ? 'Generating PDF...' : 'Download Report'}
    </button>
  );
}
