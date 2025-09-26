import PyPDF2
import re

def parse_soil_report(filepath):
    # Extract text from PDF
    text = ''
    with open(filepath, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text()

    # Extract nutrients (this example assumes soil report contains keywords like pH, N, P, K and values)
    def extract_value(pattern):
        match = re.search(pattern, text, re.IGNORECASE)
        return float(match.group(1)) if match else None

    ph = extract_value(r"pH\s*[:=]?\s*([\d.]+)")
    nitrogen = extract_value(r"N(?:itrogen)?\s*[:=]?\s*([\d.]+)")
    phosphorus = extract_value(r"P(?:hosphorus)?\s*[:=]?\s*([\d.]+)")
    potassium = extract_value(r"K(?:alium)?\s*[:=]?\s*([\d.]+)")

    return {
        "pH": ph,
        "Nitrogen": nitrogen,
        "Phosphorus": phosphorus,
        "Potassium": potassium,
    }

def recommend_crop(soil, crop):
    # Example simple rule-based crop suitability based on pH
    ph = soil.get("pH", 7)
    suitable = True
    reason = ""
    if ph < 5.5 or ph > 7.5:
        suitable = False
        reason = "Soil pH is not ideal for most crops."

    # You could add more rules here e.g. Nitrogen, Phosphorus checks

    if suitable:
        return f"The crop '{crop}' is suitable for this soil."
    else:
        return f"The crop '{crop}' may not be suitable. {reason}"

def recommend_fertilizer(soil, crop):
    # Helper to safely get numeric values
    def safe_get(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    n = safe_get(soil.get("Nitrogen"))
    p = safe_get(soil.get("Phosphorus"))
    k = safe_get(soil.get("Potassium"))

    recommendations = []
    if n < 10:
        recommendations.append("Apply Nitrogen-rich fertilizer like Urea.")
    if p < 15:
        recommendations.append("Apply Phosphate fertilizer like SSP.")
    if k < 15:
        recommendations.append("Apply Potassium fertilizer like MOP.")

    if not recommendations:
        recommendations.append("No additional fertilizer needed, soil nutrient levels are sufficient.")

    return " ".join(recommendations)

import os
import google.generativeai as genai

def gemini_soil_analysis(soil_data, crop):
    # Use your Gemini API key from the environment
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Gemini API key not set."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash") # or whichever model is appropriate

    prompt = (
        f"Here is a soil test report:\n"
        f"pH: {soil_data.get('pH')}\n"
        f"Nitrogen: {soil_data.get('Nitrogen')}\n"
        f"Phosphorus: {soil_data.get('Phosphorus')}\n"
        f"Potassium: {soil_data.get('Potassium')}\n"
        f"Crop: {crop}\n"
        f"Analyze this for:\n"
        f"- Soil suitability for the given crop\n"
        f"- If suitable, confirm and explain why\n"
        f"- If unsuitable, suggest better crops for this soil\n"
        f"- Recommend fertilizer types and approximate amounts required\n"
        f"Provide the response in markdown format."
        
    )

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error communicating with Gemini API: {e}"
