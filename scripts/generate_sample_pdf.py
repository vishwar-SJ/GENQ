"""
Generate a sample genetic report PDF for testing GENQ.

This script creates a PDF with realistic rsID + genotype data that matches
the scoring files and drug lookup tables used by GENQ's analysis engines.
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
import random
import os

# Path for output
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "backend", "temp_uploads")
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "sample_genetic_report.pdf")

# Real rsIDs from scoring files + drug lookup tables
KNOWN_SNPS = {
    # Type 2 Diabetes
    "rs7903146": "CT", "rs13266634": "CC", "rs1801282": "CG",
    "rs5219": "CT", "rs10811661": "TT", "rs4402960": "GT",
    "rs12255372": "GT", "rs1111875": "CC", "rs7754840": "GC",
    "rs10946398": "AC", "rs8050136": "CA", "rs9939609": "AT",
    # Coronary Artery Disease
    "rs4977574": "AG", "rs1333049": "GC", "rs10757278": "AG",
    "rs2383206": "AG", "rs6725887": "TC", "rs9818870": "CT",
    "rs12526453": "GC", "rs17465637": "CA",
    # Breast Cancer
    "rs2981582": "GA", "rs3803662": "GA", "rs889312": "AC",
    "rs13387042": "GA", "rs13281615": "AG",
    # Alzheimer's Disease (APOE markers)
    "rs429358": "TC", "rs7412": "CT", "rs6656401": "GA",
    "rs6733839": "CT",
    # Thalassemia
    "rs334": "TT",  # Normal — no sickle cell carrier
    "rs33930165": "GG",  # Normal
    # Parkinson's Disease
    "rs11931074": "AG", "rs356219": "GA", "rs17649553": "CT",
    "rs2736990": "GT", "rs329648": "GC", "rs34311866": "GT",
    # Lung Cancer
    "rs8034191": "TC", "rs1051730": "GA", "rs2736100": "GC",
    "rs401681": "TC", "rs7726159": "GA",
    # Prostate Cancer
    "rs1447295": "GA", "rs6983267": "GG", "rs10993994": "GT",
    "rs4430796": "GA", "rs16901979": "GA",
    # Celiac Disease
    "rs2187668": "GT", "rs7454108": "GT", "rs3184504": "GT",
    "rs6441961": "GC",
    # Rheumatoid Arthritis
    "rs2476601": "GA", "rs6920220": "GA", "rs3761847": "AG",
    "rs7574865": "GT", "rs10488631": "TC",
    # Asthma
    "rs7216389": "GT", "rs2305480": "AG", "rs1837253": "GT",
    "rs12936231": "GC", "rs9273349": "AG",
    # Atrial Fibrillation
    "rs2200733": "CT", "rs10033464": "GT", "rs6817105": "GT",
    "rs13376333": "CT", "rs6843082": "AG",
    # Clopidogrel / CYP2C19
    "rs4244285": "GA",  # Heterozygous *2 carrier
    "rs4986893": "GG",  # Normal
    "rs12248560": "CC",  # Normal
    # Isoniazid / NAT2
    "rs1801280": "TC",  # Heterozygous *5
    "rs1799930": "GG",  # Normal
    "rs1799931": "GG",  # Normal
    # Warfarin / CYP2C9 + VKORC1
    "rs1799853": "CT",  # Heterozygous CYP2C9*2
    "rs1057910": "AA",  # Normal CYP2C9
    "rs9923231": "GA",  # Heterozygous VKORC1
    # Codeine / CYP2D6
    "rs3892097": "GA",  # Heterozygous *4
    "rs5030655": "TT",  # Normal
    "rs1065852": "CT",  # Heterozygous *10
    # Simvastatin / SLCO1B1
    "rs4149056": "TC",  # Heterozygous *5
    # Abacavir / HLA-B
    "rs2395029": "TT",  # Negative (no *57:01)
}

# Add extra filler SNPs to ensure a realistic count
FILLER_SNPS = {}
for i in range(50):
    rsid = f"rs{random.randint(1000000, 99999999)}"
    alleles = random.choice(["AA", "AG", "GG", "CC", "CT", "TT", "AC", "GT"])
    FILLER_SNPS[rsid] = alleles


def generate_pdf():
    """Generate a sample genetic report PDF."""
    doc = SimpleDocTemplate(OUTPUT_PATH, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    title = Paragraph(
        "<b>Sample Genetic Report</b>",
        styles["Title"]
    )
    elements.append(title)
    elements.append(Spacer(1, 0.25 * inch))

    subtitle = Paragraph(
        "Generated for GENQ testing — Contains synthetic genetic data",
        styles["Normal"]
    )
    elements.append(subtitle)
    elements.append(Spacer(1, 0.15 * inch))

    info = Paragraph(
        "<b>Patient:</b> Test User &nbsp;&nbsp;&nbsp; "
        "<b>Date:</b> 2026-07-13 &nbsp;&nbsp;&nbsp; "
        "<b>Lab:</b> GENQ Test Lab",
        styles["Normal"]
    )
    elements.append(info)
    elements.append(Spacer(1, 0.3 * inch))

    # Section header
    section = Paragraph("<b>Genotype Results</b>", styles["Heading2"])
    elements.append(section)
    elements.append(Spacer(1, 0.15 * inch))

    # Build table data
    all_snps = {**KNOWN_SNPS, **FILLER_SNPS}
    table_data = [["rsID", "Chromosome", "Position", "Genotype"]]

    for rsid, genotype in sorted(all_snps.items()):
        chrom = random.randint(1, 22)
        pos = random.randint(10000000, 200000000)
        table_data.append([rsid, str(chrom), str(pos), genotype])

    # Create table
    table = Table(table_data, colWidths=[1.5*inch, 1.2*inch, 1.5*inch, 1.2*inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a5276")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#eaf2f8")]),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 0.3 * inch))

    # Disclaimer
    disclaimer = Paragraph(
        "<i>This is a synthetic genetic report generated for testing purposes only. "
        "It does not represent real patient data.</i>",
        styles["Normal"]
    )
    elements.append(disclaimer)

    # Build PDF
    doc.build(elements)
    print(f"Sample PDF generated: {OUTPUT_PATH}")
    print(f"Total SNPs: {len(all_snps)} ({len(KNOWN_SNPS)} known + {len(FILLER_SNPS)} filler)")


if __name__ == "__main__":
    generate_pdf()
