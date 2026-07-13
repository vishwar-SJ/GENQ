"""
GENQ Offspring Risk Engine

Predicts offspring genetic disorder risks based on the genetic profiles of two parents.
"""
from services.disease_risk import (
    DISEASE_CONFIGS, 
    _check_thalassemia_carrier, 
    _calculate_prs, 
    _score_to_percentile, 
    _percentile_to_label
)

def analyze_offspring_risk(mother_genotypes: dict[str, str], father_genotypes: dict[str, str]) -> list[dict]:
    """
    Analyze offspring risk based on mother and father genotypes.
    """
    # Normalize genotypes to lower-case rsid keys
    mom_geno = {rsid.lower(): geno.upper() for rsid, geno in mother_genotypes.items()}
    dad_geno = {rsid.lower(): geno.upper() for rsid, geno in father_genotypes.items()}

    results = []

    for disease_name, config in DISEASE_CONFIGS.items():
        if config["type"] == "carrier":
            # Thalassemia - Mendelian Inheritance
            mom_res = _check_thalassemia_carrier(mom_geno)
            dad_res = _check_thalassemia_carrier(dad_geno)

            mom_carrier = mom_res.get("risk_label") == "Carrier detected"
            dad_carrier = dad_res.get("risk_label") == "Carrier detected"

            if mom_carrier and dad_carrier:
                prob = "25% High Risk (Disease), 50% Carrier"
                label = "High Risk"
            elif mom_carrier or dad_carrier:
                prob = "0% Disease, 50% Carrier"
                label = "Average Risk (Carrier possible)"
            else:
                prob = "0% Risk"
                label = "No Risk"

            results.append({
                "disease_name": disease_name,
                "risk_label": label,
                "probability_text": prob,
                "is_polygenic": "false",
                "percentile": None
            })

        else:
            # Polygenic Risk Score (PRS) - Quantitative Inheritance
            mom_raw, mom_matched, _ = _calculate_prs(mom_geno, config["file"])
            dad_raw, dad_matched, _ = _calculate_prs(dad_geno, config["file"])

            if mom_matched == 0 or dad_matched == 0:
                results.append({
                    "disease_name": disease_name,
                    "risk_label": "Insufficient data",
                    "probability_text": "Missing data for one or both parents",
                    "is_polygenic": "true",
                    "percentile": None
                })
                continue

            # Expected raw score is roughly the average of the parents
            expected_raw = (mom_raw + dad_raw) / 2.0
            
            percentile = _score_to_percentile(
                expected_raw, config["population_mean"], config["population_sd"]
            )
            label = _percentile_to_label(percentile)

            results.append({
                "disease_name": disease_name,
                "risk_label": label,
                "probability_text": f"Expected risk level: {label}",
                "is_polygenic": "true",
                "percentile": percentile
            })

    return results
