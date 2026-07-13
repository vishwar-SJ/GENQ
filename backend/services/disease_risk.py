"""
GENQ Disease Risk Engine — Polygenic Risk Score (PRS) calculations.

Implements:
- PRS scoring for Type 2 Diabetes, Coronary Artery Disease, Breast Cancer, Alzheimer's
- Single-gene carrier detection for Thalassemia
- Percentile conversion via z-score normalization
"""
import pandas as pd
from scipy.stats import norm
from pathlib import Path
from config import SCORING_FILES_DIR

# Disease configurations with population statistics
# Population mean/SD are estimated from published PGS Catalog distributions
DISEASE_CONFIGS = {
    "Type 2 Diabetes": {
        "file": "type2_diabetes.csv",
        "population_mean": 1.50,
        "population_sd": 0.85,
        "is_estimated": "true",
        "type": "prs",
    },
    "Coronary Artery Disease": {
        "file": "coronary_artery_disease.csv",
        "population_mean": 1.20,
        "population_sd": 0.75,
        "is_estimated": "true",
        "type": "prs",
    },
    "Breast Cancer": {
        "file": "breast_cancer.csv",
        "population_mean": 0.60,
        "population_sd": 0.55,
        "is_estimated": "true",
        "type": "prs",
    },
    "Alzheimer's Disease": {
        "file": "alzheimers.csv",
        "population_mean": 0.30,
        "population_sd": 0.90,
        "is_estimated": "true",
        "type": "prs",
    },
    "Thalassemia": {
        "file": "thalassemia.csv",
        "type": "carrier",
    },
    "Parkinson's Disease": {
        "file": "parkinsons.csv",
        "population_mean": 1.10,
        "population_sd": 0.80,
        "is_estimated": "true",
        "type": "prs",
    },
    "Lung Cancer": {
        "file": "lung_cancer.csv",
        "population_mean": 0.90,
        "population_sd": 0.65,
        "is_estimated": "true",
        "type": "prs",
    },
    "Prostate Cancer": {
        "file": "prostate_cancer.csv",
        "population_mean": 1.00,
        "population_sd": 0.70,
        "is_estimated": "true",
        "type": "prs",
    },
    "Celiac Disease": {
        "file": "celiac_disease.csv",
        "population_mean": 0.80,
        "population_sd": 1.10,
        "is_estimated": "true",
        "type": "prs",
    },
    "Rheumatoid Arthritis": {
        "file": "rheumatoid_arthritis.csv",
        "population_mean": 0.70,
        "population_sd": 0.60,
        "is_estimated": "true",
        "type": "prs",
    },
    "Asthma": {
        "file": "asthma.csv",
        "population_mean": 0.85,
        "population_sd": 0.55,
        "is_estimated": "true",
        "type": "prs",
    },
    "Atrial Fibrillation": {
        "file": "atrial_fibrillation.csv",
        "population_mean": 0.95,
        "population_sd": 0.65,
        "is_estimated": "true",
        "type": "prs",
    },
}


def _count_effect_alleles(user_genotype: str, effect_allele: str) -> int:
    """
    Count how many copies of the effect allele are present in the user's genotype.
    E.g., genotype 'AG' with effect_allele 'A' → 1
          genotype 'AA' with effect_allele 'A' → 2
          genotype 'GG' with effect_allele 'A' → 0
    """
    return sum(1 for base in user_genotype.upper() if base == effect_allele.upper())


def _calculate_prs(user_genotypes: dict[str, str], scoring_file: str) -> tuple[float, int, int]:
    """
    Calculate raw PRS for a disease.

    Args:
        user_genotypes: dict of {rsid: genotype}
        scoring_file: filename of the scoring CSV

    Returns:
        (raw_score, snps_matched, total_snps_in_file)
    """
    filepath = SCORING_FILES_DIR / scoring_file
    df = pd.read_csv(filepath)

    raw_score = 0.0
    snps_matched = 0

    for _, row in df.iterrows():
        rsid = row["rsid"].lower()
        if rsid in user_genotypes:
            allele_count = _count_effect_alleles(user_genotypes[rsid], row["effect_allele"])
            raw_score += allele_count * row["effect_weight"]
            snps_matched += 1

    return raw_score, snps_matched, len(df)


def _score_to_percentile(raw_score: float, pop_mean: float, pop_sd: float) -> float:
    """Convert raw PRS to percentile using z-score normalization."""
    if pop_sd == 0:
        return 50.0
    z_score = (raw_score - pop_mean) / pop_sd
    percentile = norm.cdf(z_score) * 100
    return round(percentile, 1)


def _percentile_to_label(percentile: float) -> str:
    """Map percentile to risk label with color indicator."""
    if percentile < 33:
        return "Low"
    elif percentile <= 66:
        return "Average"
    else:
        return "Elevated"


def _check_thalassemia_carrier(user_genotypes: dict[str, str]) -> dict:
    """
    Check for Thalassemia carrier status via known HBB pathogenic variants.
    Returns a result dict.
    """
    filepath = SCORING_FILES_DIR / "thalassemia.csv"
    df = pd.read_csv(filepath)

    found_any_snp = False
    carrier_notes = []

    for _, row in df.iterrows():
        rsid = row["rsid"].lower()
        if rsid in user_genotypes:
            found_any_snp = True
            user_geno = user_genotypes[rsid].upper()
            pathogenic_geno = row["pathogenic_genotype"].upper()

            # Check if user's genotype matches the pathogenic genotype
            # Normalize both for comparison (sorted)
            user_sorted = "".join(sorted(user_geno))
            patho_sorted = "".join(sorted(pathogenic_geno))

            if user_sorted == patho_sorted:
                carrier_notes.append(row["carrier_note"])

    if carrier_notes:
        return {
            "disease_name": "Thalassemia",
            "risk_label": "Carrier detected",
            "percentile": None,
            "raw_score": None,
            "is_estimated": "false",
            "details": "; ".join(carrier_notes),
        }
    elif found_any_snp:
        return {
            "disease_name": "Thalassemia",
            "risk_label": "No mutation detected",
            "percentile": None,
            "raw_score": None,
            "is_estimated": "false",
        }
    else:
        return {
            "disease_name": "Thalassemia",
            "risk_label": "Insufficient data",
            "percentile": None,
            "raw_score": None,
            "is_estimated": "false",
        }


def analyze_disease_risk(genotype_list: list[dict]) -> list[dict]:
    """
    Run disease risk analysis across all configured diseases.

    Args:
        genotype_list: list of {rsid, genotype} dicts from PDF extraction

    Returns:
        list of {disease_name, risk_label, percentile, raw_score, is_estimated}
    """
    # Build lookup dict
    user_genotypes = {g["rsid"].lower(): g["genotype"].upper() for g in genotype_list}

    results = []

    for disease_name, config in DISEASE_CONFIGS.items():
        if config["type"] == "carrier":
            # Thalassemia — carrier detection
            result = _check_thalassemia_carrier(user_genotypes)
            results.append(result)
        else:
            # Standard PRS calculation
            raw_score, matched, total = _calculate_prs(user_genotypes, config["file"])

            if matched == 0:
                results.append({
                    "disease_name": disease_name,
                    "risk_label": "Insufficient data",
                    "percentile": None,
                    "raw_score": None,
                    "is_estimated": config.get("is_estimated", "false"),
                })
            else:
                percentile = _score_to_percentile(
                    raw_score, config["population_mean"], config["population_sd"]
                )
                label = _percentile_to_label(percentile)

                results.append({
                    "disease_name": disease_name,
                    "risk_label": label,
                    "percentile": percentile,
                    "raw_score": round(raw_score, 4),
                    "is_estimated": config.get("is_estimated", "false"),
                })

    return results
