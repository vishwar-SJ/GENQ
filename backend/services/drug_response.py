"""
GENQ Drug Response Engine — Pharmacogenomic metabolizer status lookup.

Implements rule-based genotype-to-phenotype mapping for:
- Clopidogrel / CYP2C19 (star allele diplotyping)
- Isoniazid / NAT2 (acetylator status)
- Warfarin / CYP2C9 + VKORC1 (sensitivity classification)
- Codeine / CYP2D6 (metabolizer status)
- Simvastatin / SLCO1B1 (transporter function)
- Omeprazole / CYP2C19 (metabolizer status)
- Tamoxifen / CYP2D6 (metabolizer status)
- Abacavir / HLA-B (hypersensitivity risk)
"""
import json
from pathlib import Path
from config import DRUG_LOOKUP_DIR


def _load_drug_config(filename: str) -> dict:
    """Load a drug lookup JSON configuration file."""
    filepath = DRUG_LOOKUP_DIR / filename
    with open(filepath, "r") as f:
        return json.load(f)


def _determine_star_alleles(
    user_genotypes: dict[str, str],
    defining_variants: dict,
) -> tuple[list[str], bool]:
    """
    Determine which star alleles are present based on user genotypes
    at defining variant positions.

    Returns:
        (list of variant star alleles detected, has_all_required_data)
    """
    detected_variants = []
    missing_data = False

    for rsid, variant_info in defining_variants.items():
        rsid_lower = rsid.lower()
        if rsid_lower not in user_genotypes:
            missing_data = True
            continue

        user_geno = user_genotypes[rsid_lower].upper()
        variant_allele = variant_info["variant_allele"].upper()
        normal_allele = variant_info["normal_allele"].upper()

        # Count variant alleles
        variant_count = sum(1 for base in user_geno if base == variant_allele)

        if variant_count > 0:
            detected_variants.append({
                "star_allele": variant_info["star_allele"],
                "count": variant_count,
                "rsid": rsid,
            })

    return detected_variants, missing_data


def _analyze_star_allele_drug(
    user_genotypes: dict[str, str],
    config_file: str,
    drug_name: str,
    gene_name: str,
    wildtype_allele: str = "*1",
) -> dict:
    """
    Generic analyzer for star allele-based drugs (CYP2C19, CYP2D6, NAT2, etc.).
    """
    config = _load_drug_config(config_file)
    detected, missing = _determine_star_alleles(
        user_genotypes, config["defining_variants"]
    )

    if missing and not detected:
        return {
            "drug_name": drug_name,
            "gene": gene_name,
            "metabolizer_status": "Insufficient data",
            "guidance_text": f"Not all required {gene_name} variant positions were found in your genetic data.",
        }

    # Build diplotype from detected variants
    if not detected:
        diplotype = f"{wildtype_allele}/{wildtype_allele}"
    else:
        alleles = [wildtype_allele, wildtype_allele]
        for var in detected:
            star = var["star_allele"]
            count = var["count"]
            if count >= 2:
                alleles = [star, star]
                break
            elif count == 1:
                if alleles[1] == wildtype_allele:
                    alleles[1] = star
                else:
                    alleles[0] = star

        alleles.sort()
        diplotype = f"{alleles[0]}/{alleles[1]}"

    # Look up the default phenotype based on the wildtype diplotype
    default_phenotype = list(config["phenotype_to_guidance"].keys())[0]
    phenotype = config["diplotype_to_phenotype"].get(diplotype, default_phenotype)
    guidance = config["phenotype_to_guidance"].get(phenotype, "No specific guidance available.")

    return {
        "drug_name": drug_name,
        "gene": gene_name,
        "metabolizer_status": phenotype,
        "guidance_text": guidance,
    }


def _analyze_clopidogrel(user_genotypes: dict[str, str]) -> dict:
    """Analyze Clopidogrel/CYP2C19 metabolizer status."""
    return _analyze_star_allele_drug(
        user_genotypes, "clopidogrel_cyp2c19.json", "Clopidogrel", "CYP2C19", "*1"
    )


def _analyze_isoniazid(user_genotypes: dict[str, str]) -> dict:
    """Analyze Isoniazid/NAT2 acetylator status."""
    return _analyze_star_allele_drug(
        user_genotypes, "isoniazid_nat2.json", "Isoniazid", "NAT2", "*4"
    )


def _analyze_codeine(user_genotypes: dict[str, str]) -> dict:
    """Analyze Codeine/CYP2D6 metabolizer status."""
    return _analyze_star_allele_drug(
        user_genotypes, "codeine_cyp2d6.json", "Codeine", "CYP2D6", "*1"
    )


def _analyze_omeprazole(user_genotypes: dict[str, str]) -> dict:
    """Analyze Omeprazole/CYP2C19 metabolizer status."""
    return _analyze_star_allele_drug(
        user_genotypes, "omeprazole_cyp2c19.json", "Omeprazole", "CYP2C19", "*1"
    )


def _analyze_tamoxifen(user_genotypes: dict[str, str]) -> dict:
    """Analyze Tamoxifen/CYP2D6 metabolizer status."""
    return _analyze_star_allele_drug(
        user_genotypes, "tamoxifen_cyp2d6.json", "Tamoxifen", "CYP2D6", "*1"
    )


def _analyze_simvastatin(user_genotypes: dict[str, str]) -> dict:
    """Analyze Simvastatin/SLCO1B1 transporter function."""
    config = _load_drug_config("simvastatin_slco1b1.json")
    rsid = "rs4149056"
    rsid_lower = rsid.lower()

    if rsid_lower not in user_genotypes:
        return {
            "drug_name": "Simvastatin",
            "gene": "SLCO1B1",
            "metabolizer_status": "Insufficient data",
            "guidance_text": "Required SLCO1B1 variant position was not found in your genetic data.",
        }

    user_geno = user_genotypes[rsid_lower].upper()
    variant_allele = config["defining_variants"][rsid]["variant_allele"].upper()
    variant_count = sum(1 for b in user_geno if b == variant_allele)

    if variant_count == 0:
        diplotype = "*1A/*1A"
    elif variant_count == 1:
        diplotype = "*1A/*5"
    else:
        diplotype = "*5/*5"

    phenotype = config["diplotype_to_phenotype"].get(diplotype, "Normal Function")
    guidance = config["phenotype_to_guidance"].get(phenotype, "No specific guidance available.")

    return {
        "drug_name": "Simvastatin",
        "gene": "SLCO1B1",
        "metabolizer_status": phenotype,
        "guidance_text": guidance,
    }


def _analyze_abacavir(user_genotypes: dict[str, str]) -> dict:
    """Analyze Abacavir/HLA-B*57:01 hypersensitivity risk."""
    config = _load_drug_config("abacavir_hlab.json")
    rsid = "rs2395029"
    rsid_lower = rsid.lower()

    if rsid_lower not in user_genotypes:
        return {
            "drug_name": "Abacavir",
            "gene": "HLA-B",
            "metabolizer_status": "Insufficient data",
            "guidance_text": "Required HLA-B*57:01 tag SNP was not found in your genetic data.",
        }

    user_geno = user_genotypes[rsid_lower].upper()
    variant_allele = config["defining_variants"][rsid]["variant_allele"].upper()
    variant_count = sum(1 for b in user_geno if b == variant_allele)

    if variant_count == 0:
        phenotype = "HLA-B*57:01 Negative"
    else:
        phenotype = "HLA-B*57:01 Positive"

    guidance = config["phenotype_to_guidance"].get(phenotype, "No specific guidance available.")

    return {
        "drug_name": "Abacavir",
        "gene": "HLA-B",
        "metabolizer_status": phenotype,
        "guidance_text": guidance,
    }


def _analyze_warfarin(user_genotypes: dict[str, str]) -> dict:
    """Analyze Warfarin/CYP2C9+VKORC1 sensitivity."""
    config = _load_drug_config("warfarin_cyp2c9_vkorc1.json")
    variants = config["defining_variants"]

    # Count CYP2C9 variant alleles
    cyp2c9_variant_count = 0
    cyp2c9_data_found = False
    for rsid in ["rs1799853", "rs1057910"]:
        rsid_lower = rsid.lower()
        if rsid_lower in user_genotypes:
            cyp2c9_data_found = True
            user_geno = user_genotypes[rsid_lower].upper()
            variant_allele = variants[rsid]["variant_allele"].upper()
            cyp2c9_variant_count += sum(1 for b in user_geno if b == variant_allele)

    # Count VKORC1 variant alleles
    vkorc1_variant_count = 0
    vkorc1_data_found = False
    rsid_vkorc1 = "rs9923231"
    if rsid_vkorc1.lower() in user_genotypes:
        vkorc1_data_found = True
        user_geno = user_genotypes[rsid_vkorc1.lower()].upper()
        variant_allele = variants[rsid_vkorc1]["variant_allele"].upper()
        vkorc1_variant_count = sum(1 for b in user_geno if b == variant_allele)

    if not cyp2c9_data_found and not vkorc1_data_found:
        return {
            "drug_name": "Warfarin",
            "gene": "CYP2C9 / VKORC1",
            "metabolizer_status": "Insufficient data",
            "guidance_text": "Required CYP2C9 and VKORC1 variant positions were not found in your genetic data.",
        }

    # Match against sensitivity rules (ordered from least to most sensitive)
    rules = config["sensitivity_rules"]
    matched_rule = rules[0]  # Default: normal sensitivity

    if cyp2c9_variant_count >= 2:
        matched_rule = rules[4]
    elif cyp2c9_variant_count >= 1 and vkorc1_variant_count >= 1:
        matched_rule = rules[3]
    elif vkorc1_variant_count >= 1:
        matched_rule = rules[2]
    elif cyp2c9_variant_count >= 1:
        matched_rule = rules[1]

    return {
        "drug_name": "Warfarin",
        "gene": "CYP2C9 / VKORC1",
        "metabolizer_status": matched_rule["phenotype"],
        "guidance_text": matched_rule["guidance"],
    }


def analyze_drug_response(genotype_list: list[dict]) -> list[dict]:
    """
    Run drug response analysis for all configured drug-gene pairs.

    Args:
        genotype_list: list of {rsid, genotype} dicts from PDF extraction

    Returns:
        list of {drug_name, gene, metabolizer_status, guidance_text}
    """
    # Build lookup dict
    user_genotypes = {g["rsid"].lower(): g["genotype"].upper() for g in genotype_list}

    results = [
        _analyze_clopidogrel(user_genotypes),
        _analyze_isoniazid(user_genotypes),
        _analyze_warfarin(user_genotypes),
        _analyze_codeine(user_genotypes),
        _analyze_simvastatin(user_genotypes),
        _analyze_omeprazole(user_genotypes),
        _analyze_tamoxifen(user_genotypes),
        _analyze_abacavir(user_genotypes),
    ]

    return results
