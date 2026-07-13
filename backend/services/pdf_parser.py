"""
GENQ PDF Parser Service — Extracts rsID + genotype pairs from uploaded PDFs.

Supports:
- Plain text extraction with regex matching
- Structured table extraction via pdfplumber
- Handles various genetic report formats
"""
import re
import pdfplumber
from config import MIN_SNPS_THRESHOLD, PRODUCTION

# Regex pattern: rsID followed by genotype (two nucleotide letters)
# Handles formats like: rs1234567  AG, rs1234567\tAG, rs1234567 | AG, etc.
RSID_PATTERN = re.compile(
    r'(rs\d{3,12})\s*[|\t,;:\s]+\s*([ATCG]{2})\b',
    re.IGNORECASE
)

# Alternative pattern for formats like: rs1234567(A;G) or rs1234567 A/G
RSID_PATTERN_ALT = re.compile(
    r'(rs\d{3,12})\s*[\(\[]?\s*([ATCG])\s*[;/,]\s*([ATCG])\s*[\)\]]?',
    re.IGNORECASE
)

# Valid nucleotides for validation
VALID_NUCLEOTIDES = set("ATCG")


def _normalize_genotype(genotype: str) -> str:
    """Normalize genotype to uppercase sorted pair (e.g., 'ga' -> 'AG')."""
    g = genotype.upper().strip()
    if len(g) == 2 and all(c in VALID_NUCLEOTIDES for c in g):
        return "".join(sorted(g))
    return ""


def _extract_from_text(text: str) -> dict[str, str]:
    """
    Extract rsID -> genotype pairs from raw text using regex.
    Returns dict of {rsid: genotype} with deduplication.
    """
    results = {}

    # Try primary pattern: rs1234567  AG
    for match in RSID_PATTERN.finditer(text):
        rsid = match.group(1).lower()
        genotype = _normalize_genotype(match.group(2))
        if genotype:
            results[rsid] = genotype

    # Try alternative pattern: rs1234567(A;G)
    for match in RSID_PATTERN_ALT.finditer(text):
        rsid = match.group(1).lower()
        genotype = _normalize_genotype(match.group(2) + match.group(3))
        if genotype and rsid not in results:
            results[rsid] = genotype

    return results


def _extract_from_tables(tables: list) -> dict[str, str]:
    """
    Extract rsID -> genotype pairs from pdfplumber table data.
    Looks for columns containing rsID-like values and genotype-like values.
    """
    results = {}
    if not tables:
        return results

    for table in tables:
        if not table or len(table) < 2:
            continue

        # Find which columns contain rsIDs and genotypes
        header = table[0] if table[0] else []
        rsid_col = None
        geno_col = None

        # Try to identify columns by header names
        for i, col_name in enumerate(header):
            if col_name is None:
                continue
            col_lower = str(col_name).lower().strip()
            if "rsid" in col_lower or "rs id" in col_lower or "snp" in col_lower or "variant" in col_lower:
                rsid_col = i
            elif "genotype" in col_lower or "allele" in col_lower or "result" in col_lower:
                geno_col = i

        # If we couldn't find columns by header, scan data rows
        if rsid_col is None:
            for row in table[1:3]:  # Check first couple data rows
                for i, cell in enumerate(row):
                    if cell and re.match(r'rs\d+', str(cell), re.IGNORECASE):
                        rsid_col = i
                        break
                if rsid_col is not None:
                    break

        if rsid_col is None:
            continue

        # If genotype column not found, look in adjacent columns
        if geno_col is None:
            for row in table[1:3]:
                for i, cell in enumerate(row):
                    if i != rsid_col and cell:
                        cell_str = str(cell).strip().upper()
                        if len(cell_str) == 2 and all(c in VALID_NUCLEOTIDES for c in cell_str):
                            geno_col = i
                            break
                if geno_col is not None:
                    break

        if geno_col is None:
            continue

        # Extract data from identified columns
        for row in table[1:]:
            try:
                rsid_val = str(row[rsid_col]).strip().lower() if row[rsid_col] else ""
                geno_val = str(row[geno_col]).strip() if row[geno_col] else ""

                if re.match(r'rs\d+', rsid_val):
                    genotype = _normalize_genotype(geno_val)
                    if genotype:
                        results[rsid_val] = genotype
            except (IndexError, TypeError):
                continue

    return results


def extract_genotypes_from_pdf(pdf_path: str) -> list[dict]:
    """
    Main extraction function. Reads a PDF and returns a list of
    {rsid, genotype} dicts.

    Raises ValueError if fewer than MIN_SNPS_THRESHOLD valid SNPs are found.
    """
    all_genotypes: dict[str, str] = {}

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Extract from plain text
                text = page.extract_text() or ""
                text_results = _extract_from_text(text)
                all_genotypes.update(text_results)

                # Extract from tables
                try:
                    tables = page.extract_tables()
                    table_results = _extract_from_tables(tables)
                    # Table results don't overwrite text results (text is usually more reliable)
                    for rsid, geno in table_results.items():
                        if rsid not in all_genotypes:
                            all_genotypes[rsid] = geno
                except Exception:
                    # Table extraction can fail on some PDFs — continue with text results
                    pass

    except Exception as e:
        if not PRODUCTION:
            print(f"PDF parsing error: {e}")
        raise ValueError(f"Could not read PDF file: {str(e)}")

    # Check minimum threshold
    if len(all_genotypes) < MIN_SNPS_THRESHOLD:
        raise ValueError(
            f"We couldn't extract enough genetic markers from this file. "
            f"Found {len(all_genotypes)} valid SNPs, but need at least {MIN_SNPS_THRESHOLD}. "
            f"Please check the format and try again."
        )

    # Convert to list of dicts
    result = [
        {"rsid": rsid, "genotype": genotype}
        for rsid, genotype in sorted(all_genotypes.items())
    ]

    if not PRODUCTION:
        print(f"Extracted {len(result)} SNPs from PDF")

    return result
