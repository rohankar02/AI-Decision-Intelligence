import os
import json
import logging
from typing import Dict, Any, Optional
try:
    import openai
except ImportError:
    openai = None

logger = logging.getLogger(__name__)

class AIAnalyzer:
    """
    Integrates LLM capabilities to generate high-level business insights
    and strategic recommendations from structured analytical data.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4-turbo"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        if openai and self.api_key:
            openai.api_key = self.api_key

    def generate_business_insights(self, kpi_summary: Dict, analysis_output: Dict) -> Dict[str, Any]:
        """
        Refined function to generate high-impact business insights using 
        strong prompt engineering and role-based persona.
        """
        if not self.api_key or not openai:
            return {"error": "OpenAI API Key or library missing."}

        # Constructing a structured prompt with clear persona and constraints
        prompt = self._build_strategic_prompt(kpi_summary, analysis_output)
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "You are a Senior Business Strategy Consultant with 20 years of experience. "
                            "Your goal is to translate complex data into clear, actionable, and "
                            "executive-level business insights. Use professional, encouraging, "
                            "but realistic language."
                        )
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            return {"insight_report": response.choices[0].message.content}

        except Exception as e:
            logger.error(f"AI Generation Error: {e}")
            return {"error": str(e)}

    def _build_strategic_prompt(self, kpi_summary: Dict, analysis_output: Dict) -> str:
        """
        Strong Prompt Engineering: Role-based, structured context, and specific output constraints.
        """
        return f"""
        EXECUTIVE DATA CONTEXT:
        - Core Metrics: {json.dumps(kpi_summary, indent=2)}
        - Trend & Anomaly Analysis: {json.dumps(analysis_output, indent=2)}

        YOUR TASK:
        As a Senior Consultant, review the data above and provide a 'Strategic Insight Report'. 
        
        REQUIRED STRUCTURE:
        1. **Key Insights**: Provide 3-5 high-level bullet points explaining exactly what is happening in the business right now.
        2. **The 'Why' Behind the Trends**: Analyze the reasons for growth or decline. Is it a seasonal pattern, an anomaly, or a shift in customer behavior?
        3. **Executive Summary**: A 2-sentence summary of the business's current health.

        CONSTRAINTS:
        - Use professional business-friendly language.
        - Avoid technical jargon (don't say 'standard deviation', say 'unusual spike').
        - Be concise and action-oriented.
        """

    def generate_structured_recommendations(self, insight_report: str) -> List[Dict[str, Any]]:
        """
        Takes the text-based insight report and extracts/generates 
        structured, actionable recommendations.
        """
        if not self.api_key or not openai:
            return []

        prompt = f"""
        Based on the following Strategic Insight Report, generate a list of 
        at least 3-5 high-impact business recommendations.
        
        REPORT:
        {insight_report}
        
        REQUIRED JSON FORMAT:
        [
          {{
            "action": "Short actionable title",
            "reasoning": "Brief explanation of why this is recommended based on the data",
            "impact": "High/Medium/Low",
            "effort": "Easy/Moderate/Complex"
          }}
        ]
        
        Return ONLY the JSON array.
        """
        
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a Business Optimization Specialist. You only output valid JSON arrays."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3 # Lower temperature for structural consistency
            )
            
            content = response.choices[0].message.content
            return self._parse_json_list(content)

        except Exception as e:
            logger.error(f"Error generating structured recommendations: {e}")
            return []

    def _parse_json_list(self, content: str) -> List[Dict]:
        """Strictly parses JSON arrays from LLM output."""
        try:
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            data = json.loads(content)
            return data if isinstance(data, list) else []
        except:
            return []

if __name__ == "__main__":
    print("AI Analyzer module ready.")
