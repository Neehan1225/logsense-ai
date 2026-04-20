from google import genai
from app.core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)
model = client.models

def analyze_log(service_name: str, level: str, message: str) -> str:
    try:
        prompt = f"""
You are a DevOps expert analyzing application logs.
Analyze this log entry and provide a brief, actionable insight:
Service: {service_name}
Level: {level}
Message: {message}
Respond in 2-3 sentences maximum:
1. What this log means
2. Possible cause
3. Recommended action
"""
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
        return response.text

    except Exception as e:
        return f"AI analysis unavailable: {str(e)}"