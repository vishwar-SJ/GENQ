"""
GENQ Health Advisor Chatbot — Rule-based lifestyle and health guidance.

Provides contextual health advice based on the user's genetic report results,
including dietary recommendations, exercise guidance, screening schedules,
and lifestyle modifications.
"""

# Knowledge base: disease-specific lifestyle advice
DISEASE_ADVICE = {
    "Type 2 Diabetes": {
        "diet": [
            "Reduce refined carbohydrates and added sugars. Choose whole grains over white bread/rice.",
            "Increase fiber intake (beans, lentils, vegetables) — aim for 25-30g daily.",
            "Include healthy fats: olive oil, avocados, nuts, and fatty fish.",
            "Practice portion control and consider the glycemic index of foods.",
            "Limit sugary beverages and fruit juices; drink water or unsweetened tea.",
        ],
        "exercise": [
            "Aim for at least 150 minutes of moderate aerobic activity per week.",
            "Include resistance training 2-3 times per week to improve insulin sensitivity.",
            "Walking after meals (even 10-15 minutes) helps regulate blood sugar.",
        ],
        "lifestyle": [
            "Maintain a healthy body weight — even 5-7% weight loss reduces diabetes risk significantly.",
            "Monitor blood glucose levels if recommended by your doctor.",
            "Get adequate sleep (7-9 hours) — poor sleep impairs glucose metabolism.",
            "Manage stress, as cortisol raises blood sugar levels.",
        ],
        "screening": [
            "Fasting blood glucose or HbA1c test annually.",
            "Regular eye exams for diabetic retinopathy screening.",
        ],
    },
    "Coronary Artery Disease": {
        "diet": [
            "Follow a Mediterranean or DASH diet pattern.",
            "Increase omega-3 fatty acids: salmon, mackerel, sardines, walnuts, flaxseeds.",
            "Limit saturated fats to less than 7% of total calories.",
            "Reduce sodium intake to less than 2,300 mg/day.",
            "Eat plenty of fruits, vegetables, and whole grains.",
        ],
        "exercise": [
            "30-60 minutes of moderate cardio most days of the week.",
            "Include walking, cycling, swimming, or other aerobic activities.",
            "Avoid sudden intense exertion if not regularly active.",
        ],
        "lifestyle": [
            "Quit smoking — the single most impactful lifestyle change for heart health.",
            "Manage blood pressure and cholesterol through lifestyle and medication if needed.",
            "Reduce alcohol consumption to moderate levels.",
            "Practice stress management: meditation, deep breathing, yoga.",
        ],
        "screening": [
            "Lipid panel (cholesterol) every 4-6 years, more often if elevated.",
            "Blood pressure monitoring at each healthcare visit.",
            "Coronary calcium score if indicated by your doctor.",
        ],
    },
    "Breast Cancer": {
        "diet": [
            "Maintain a plant-rich diet with cruciferous vegetables (broccoli, cauliflower, kale).",
            "Limit alcohol — even moderate drinking increases breast cancer risk.",
            "Choose organic produce when possible to reduce pesticide exposure.",
            "Include soy foods in moderation (associated with reduced risk in studies).",
        ],
        "exercise": [
            "Regular physical activity reduces breast cancer risk by 10-20%.",
            "Aim for 4-7 hours of moderate-to-vigorous exercise per week.",
        ],
        "lifestyle": [
            "Maintain a healthy weight, especially after menopause.",
            "Discuss hormone replacement therapy risks with your doctor.",
            "Breastfeeding may offer protective benefits.",
        ],
        "screening": [
            "Mammography screening as recommended by your doctor (typically starting at age 40-50).",
            "Clinical breast exams annually.",
            "Consider genetic counseling for BRCA testing if family history is present.",
        ],
    },
    "Alzheimer's Disease": {
        "diet": [
            "Follow the MIND diet (Mediterranean-DASH Intervention for Neurodegenerative Delay).",
            "Include berries (especially blueberries) — rich in neuroprotective antioxidants.",
            "Eat leafy greens daily and fatty fish at least once a week.",
            "Limit red meat, butter, cheese, pastries, and fried foods.",
            "Include turmeric and cinnamon which have anti-inflammatory properties.",
        ],
        "exercise": [
            "Regular aerobic exercise (walking, dancing, swimming) is strongly associated with reduced dementia risk.",
            "Aim for 150+ minutes per week.",
        ],
        "lifestyle": [
            "Stay mentally active: puzzles, reading, learning new skills, social engagement.",
            "Prioritize quality sleep — poor sleep is linked to amyloid plaque buildup.",
            "Maintain strong social connections.",
            "Manage cardiovascular risk factors (hypertension, diabetes, high cholesterol).",
        ],
        "screening": [
            "Cognitive screening tests if memory concerns arise.",
            "Discuss APOE genotype implications with a genetic counselor.",
        ],
    },
    "Thalassemia": {
        "diet": [
            "Avoid iron supplements unless specifically prescribed.",
            "Limit iron-rich foods if you are a carrier with elevated iron stores.",
            "Ensure adequate folate intake for healthy red blood cell production.",
        ],
        "exercise": [
            "Moderate regular exercise is generally safe for carriers.",
            "Monitor for fatigue during exercise if you experience mild anemia.",
        ],
        "lifestyle": [
            "Inform your healthcare provider about your carrier status.",
            "Genetic counseling is recommended if planning a family.",
        ],
        "screening": [
            "Complete blood count (CBC) annually.",
            "Iron studies if clinically indicated.",
            "Partner testing before family planning.",
        ],
    },
    "Parkinson's Disease": {
        "diet": [
            "Increase antioxidant-rich foods: berries, dark leafy greens, green tea.",
            "Consider caffeine — moderate coffee consumption is associated with reduced risk.",
            "Ensure adequate vitamin D and B12 intake.",
            "Include foods rich in omega-3 fatty acids.",
        ],
        "exercise": [
            "Regular vigorous exercise may slow progression — 2.5+ hours per week.",
            "Tai chi and yoga improve balance and flexibility.",
            "Dance and boxing-style fitness are increasingly recommended.",
        ],
        "lifestyle": [
            "Avoid pesticide exposure when possible.",
            "Prioritize quality sleep and manage REM sleep behavior disorder.",
            "Stay socially engaged and mentally active.",
        ],
        "screening": [
            "Neurological assessment if tremor, stiffness, or movement changes occur.",
            "DAT scan if symptoms are ambiguous.",
        ],
    },
    "Lung Cancer": {
        "diet": [
            "Eat a variety of colorful fruits and vegetables (rich in carotenoids and flavonoids).",
            "Include cruciferous vegetables (broccoli, Brussels sprouts) for their sulforaphane content.",
            "Avoid beta-carotene supplements if you smoke (may increase risk).",
        ],
        "exercise": [
            "Regular physical activity is associated with reduced lung cancer risk.",
            "Aim for at least 150 minutes of moderate exercise per week.",
        ],
        "lifestyle": [
            "Do not smoke. If you smoke, quitting is the most important step.",
            "Avoid secondhand smoke exposure.",
            "Test your home for radon gas.",
            "Use protective equipment if working with industrial chemicals.",
        ],
        "screening": [
            "Low-dose CT screening if 50+ years old with 20+ pack-year smoking history.",
        ],
    },
    "Prostate Cancer": {
        "diet": [
            "Increase tomato-based foods (lycopene may offer protective benefits).",
            "Include cruciferous vegetables and green tea.",
            "Limit dairy and high-calcium diets to moderate levels.",
            "Choose healthy fats over saturated fats.",
        ],
        "exercise": [
            "Regular exercise may reduce risk and improve outcomes.",
            "Aim for 3+ hours of vigorous activity per week.",
        ],
        "lifestyle": [
            "Maintain a healthy weight.",
            "Discuss PSA screening with your doctor based on age and risk factors.",
        ],
        "screening": [
            "PSA test and digital rectal exam — discuss timing with your doctor (typically age 50+).",
            "Earlier screening (age 40-45) if family history or African ancestry.",
        ],
    },
    "Celiac Disease": {
        "diet": [
            "If diagnosed, strict lifelong gluten-free diet is essential.",
            "Avoid wheat, barley, rye, and their derivatives.",
            "Check labels for hidden gluten in sauces, processed foods, and medications.",
            "Ensure adequate calcium, iron, fiber, and B-vitamin intake on a GF diet.",
        ],
        "exercise": [
            "Regular exercise supports bone health, which can be affected by celiac disease.",
            "Weight-bearing exercises help prevent osteoporosis.",
        ],
        "lifestyle": [
            "Get screened if experiencing GI symptoms, unexplained anemia, or fatigue.",
            "Inform family members — celiac has a strong genetic component.",
        ],
        "screening": [
            "tTG-IgA antibody test if symptomatic.",
            "Bone density scan if diagnosed, to check for osteoporosis.",
            "Regular follow-up to confirm mucosal healing on GF diet.",
        ],
    },
    "Rheumatoid Arthritis": {
        "diet": [
            "Anti-inflammatory diet: rich in omega-3s, fruits, vegetables, and whole grains.",
            "Limit processed foods, refined sugars, and red meat.",
            "Consider Mediterranean diet pattern.",
            "Some evidence supports reducing nightshade vegetables if they trigger flares.",
        ],
        "exercise": [
            "Low-impact exercise: swimming, cycling, walking.",
            "Range-of-motion exercises to maintain joint flexibility.",
            "Strength training to support joint stability.",
        ],
        "lifestyle": [
            "Early diagnosis and treatment is key to preventing joint damage.",
            "Manage stress — it can trigger RA flares.",
            "Quit smoking — it worsens RA and reduces treatment effectiveness.",
        ],
        "screening": [
            "Rheumatoid factor (RF) and anti-CCP antibody tests.",
            "Joint imaging if symptoms develop.",
        ],
    },
    "Asthma": {
        "diet": [
            "Mediterranean diet is associated with reduced asthma severity.",
            "Increase fruits and vegetables rich in vitamin C and E.",
            "Omega-3 fatty acids may reduce airway inflammation.",
            "Identify and avoid food triggers (sulfites, preservatives in some individuals).",
        ],
        "exercise": [
            "Regular exercise improves lung function and fitness.",
            "Warm up gradually before vigorous exercise.",
            "Swimming is often well-tolerated due to warm, humid environment.",
        ],
        "lifestyle": [
            "Identify and avoid triggers: dust mites, pet dander, mold, pollen.",
            "Keep indoor humidity between 30-50%.",
            "Use allergen-proof bedding covers.",
            "Get annual flu vaccination.",
        ],
        "screening": [
            "Spirometry and peak flow monitoring.",
            "Allergy testing to identify triggers.",
        ],
    },
    "Atrial Fibrillation": {
        "diet": [
            "Moderate caffeine is generally safe, but monitor individual response.",
            "Limit alcohol — binge drinking is a known AFib trigger.",
            "Reduce sodium to help manage blood pressure.",
            "Maintain electrolyte balance (potassium, magnesium).",
        ],
        "exercise": [
            "Regular moderate exercise is recommended.",
            "Avoid extreme endurance exercise, which may increase AFib risk.",
            "Walking, cycling, and swimming are excellent choices.",
        ],
        "lifestyle": [
            "Manage blood pressure, diabetes, and weight — all AFib risk factors.",
            "Treat sleep apnea if present (strong AFib connection).",
            "Monitor heart rate and report palpitations to your doctor.",
        ],
        "screening": [
            "ECG monitoring if palpitations or irregular heartbeat occur.",
            "Regular blood pressure monitoring.",
            "Thyroid function tests (hyperthyroidism can trigger AFib).",
        ],
    },
}

# Drug-specific lifestyle considerations
DRUG_ADVICE = {
    "Clopidogrel": "If you are a poor or intermediate metabolizer of clopidogrel, discuss alternative antiplatelet medications with your cardiologist. Maintain a heart-healthy diet and exercise routine.",
    "Isoniazid": "If you are a slow acetylator, you may need adjusted isoniazid dosing. Monitor for liver function changes and avoid alcohol during treatment.",
    "Warfarin": "If you are warfarin-sensitive, maintain consistent vitamin K intake (green leafy vegetables). Avoid sudden dietary changes and inform your doctor about all medications and supplements.",
    "Codeine": "If you are a poor metabolizer, codeine will be ineffective for pain. Ask your doctor about alternative pain medications. If ultra-rapid, avoid codeine entirely.",
    "Simvastatin": "If you have impaired SLCO1B1 function, report any muscle pain, tenderness, or weakness immediately. Lower statin doses or alternative statins may be needed.",
    "Omeprazole": "If you are a rapid metabolizer, you may need higher PPI doses for acid reflux. Consider dietary changes: avoid spicy foods, eat smaller meals, don't lie down after eating.",
    "Tamoxifen": "If you are a poor metabolizer, tamoxifen may be less effective. Discuss with your oncologist about alternative endocrine therapies.",
    "Abacavir": "If HLA-B*57:01 positive, NEVER take abacavir. Ensure this is noted in your medical records and alert all healthcare providers.",
}


def _match_topic(message: str) -> list[str]:
    """Match user message to advice topics."""
    message_lower = message.lower()
    topics = []

    diet_keywords = ["diet", "food", "eat", "nutrition", "meal", "cook", "recipe", "fruit", "vegetable", "sugar", "carb", "fat", "protein", "drink", "alcohol", "coffee", "vitamin"]
    exercise_keywords = ["exercise", "workout", "gym", "run", "walk", "swim", "fitness", "sport", "physical", "active", "training", "yoga", "cardio"]
    lifestyle_keywords = ["lifestyle", "habit", "routine", "sleep", "stress", "smoke", "smoking", "weight", "mental", "social", "change", "improve", "prevent"]
    screening_keywords = ["screen", "test", "check", "doctor", "visit", "exam", "monitor", "diagnos"]

    if any(k in message_lower for k in diet_keywords):
        topics.append("diet")
    if any(k in message_lower for k in exercise_keywords):
        topics.append("exercise")
    if any(k in message_lower for k in lifestyle_keywords):
        topics.append("lifestyle")
    if any(k in message_lower for k in screening_keywords):
        topics.append("screening")

    # If no specific topic matched, return all
    if not topics:
        topics = ["diet", "exercise", "lifestyle", "screening"]

    return topics


def generate_chat_response(
    message: str,
    disease_risks: list[dict],
    drug_responses: list[dict],
) -> dict:
    """
    Generate a contextual health advice response based on the user's report and question.

    Returns:
        {response: str, sections: list[{title, items}]}
    """
    topics = _match_topic(message)
    message_lower = message.lower()

    # Check if asking about a specific disease
    target_diseases = []
    for risk in disease_risks:
        disease_name = risk.get("disease_name", "")
        if disease_name.lower() in message_lower or any(
            word in message_lower for word in disease_name.lower().split()
        ):
            target_diseases.append(risk)

    # Check if asking about a specific drug
    target_drugs = []
    for drug in drug_responses:
        drug_name = drug.get("drug_name", "")
        if drug_name.lower() in message_lower:
            target_drugs.append(drug)

    # If no specific target, focus on elevated/non-normal risks
    if not target_diseases and not target_drugs:
        target_diseases = [
            r for r in disease_risks
            if r.get("risk_label") in ["Elevated", "Carrier detected"]
        ]
        # If no elevated risks, include average ones too
        if not target_diseases:
            target_diseases = [
                r for r in disease_risks
                if r.get("risk_label") != "Insufficient data"
            ]

    sections = []
    response_parts = []

    # Disease-specific advice
    for risk in target_diseases[:4]:  # Limit to top 4 to avoid overwhelming
        disease_name = risk["disease_name"]
        risk_label = risk.get("risk_label", "Unknown")
        advice = DISEASE_ADVICE.get(disease_name, {})

        if not advice:
            continue

        disease_sections = []
        for topic in topics:
            items = advice.get(topic, [])
            if items:
                disease_sections.append({
                    "title": f"{topic.title()} — {disease_name} ({risk_label} Risk)",
                    "items": items,
                })

        sections.extend(disease_sections)

        if risk_label == "Elevated":
            response_parts.append(
                f"Your {disease_name} risk is elevated. Here are targeted recommendations."
            )
        elif risk_label == "Carrier detected":
            response_parts.append(
                f"You are a carrier for {disease_name}. Here is relevant guidance."
            )

    # Drug-specific advice
    for drug in target_drugs:
        drug_name = drug["drug_name"]
        advice_text = DRUG_ADVICE.get(drug_name, "")
        if advice_text:
            sections.append({
                "title": f"Medication Note — {drug_name} ({drug.get('metabolizer_status', 'Unknown')})",
                "items": [advice_text],
            })

    # Build response text
    if response_parts:
        response = " ".join(response_parts) + " I've organized my recommendations below."
    elif target_drugs:
        response = "Here's what your pharmacogenomic results mean for your medication management."
    elif "hello" in message_lower or "hi" in message_lower or "hey" in message_lower:
        # Greeting
        elevated = [r["disease_name"] for r in disease_risks if r.get("risk_label") == "Elevated"]
        if elevated:
            response = (
                f"Hello! I'm your GENQ Health Advisor. Based on your report, I noticed elevated risk for "
                f"{', '.join(elevated)}. I can help you with dietary changes, exercise routines, "
                f"lifestyle modifications, and screening recommendations. What would you like to know about?"
            )
        else:
            response = (
                "Hello! I'm your GENQ Health Advisor. Your genetic report looks good overall. "
                "I can provide personalized diet, exercise, and lifestyle advice based on your results. "
                "What would you like to know?"
            )
        return {"response": response, "sections": []}
    else:
        response = "Based on your genetic profile, here are my personalized recommendations."

    # If no sections were generated, provide general wellness advice
    if not sections:
        sections = [
            {
                "title": "General Wellness",
                "items": [
                    "Maintain a balanced diet rich in fruits, vegetables, whole grains, and lean proteins.",
                    "Aim for at least 150 minutes of moderate aerobic exercise per week.",
                    "Get 7-9 hours of quality sleep each night.",
                    "Manage stress through mindfulness, meditation, or relaxation techniques.",
                    "Stay hydrated and limit processed food intake.",
                    "Schedule regular health check-ups and age-appropriate screenings.",
                ],
            }
        ]
        response = "Here are general wellness recommendations that complement your genetic profile."

    return {"response": response, "sections": sections}
