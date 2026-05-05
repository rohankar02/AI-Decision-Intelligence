# 🚀 AI-Powered Decision Intelligence System

An enterprise-grade analytical platform that transforms raw business data into strategic growth recommendations using LLMs and mathematical simulations.

## 🌟 Key Features
- **Automated Data Engine**: Intelligent CSV cleaning and feature detection (Numeric, Categorical, Time-Series).
- **KPI Analytics Engine**: Automated calculation of core business health metrics (Revenue, Churn, AOV).
- **AI Strategic Consultant**: Leverages GPT-4 to generate narrative insights and prioritized business actions.
- **What-If Simulation Lab**: Mathematical modeling of business decisions (e.g., Price Elasticity, Retention ROI).
- **Interactive Dashboard**: High-fidelity Streamlit UI with Plotly visualizations.

## 🏗 Architecture
The system follows **Clean Architecture** principles to ensure modularity and scalability:
- `src/data_engine`: Data ingestion and preprocessing.
- `src/analytics`: Core statistical and KPI logic.
- `src/ai_module`: LLM integration and prompt engineering.
- `src/simulation`: Predictive mathematical modeling.
- `src/utils`: Centralized logging and custom exception handling.

## 🛠 Tech Stack
- **Language**: Python 3.9+
- **Data**: Pandas, Numpy, Scikit-learn
- **AI**: OpenAI GPT-4 API
- **UI**: Streamlit, Plotly
- **Observability**: Rotating File Logging, Custom Exceptions

## 🚀 Quick Start
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/decision-intelligence-sys.git
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set your API Key**:
   Create a `.env` file or export your key:
   ```bash
   export OPENAI_API_KEY='your-key-here'
   ```
4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## 📊 Sample Insights
> "The system identified a 15% drop in retention within the 'Electronics' segment and simulated that a 5% loyalty boost would recover $120k in projected annual revenue."

---
*Developed for strategic business optimization.*