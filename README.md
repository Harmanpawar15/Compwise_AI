<<<<<<< HEAD
# 🏘️ CompWise_AI

**CompWise_AI** is an AI-powered dashboard for analyzing and explaining comparable property rankings based on machine learning and natural language explanations. Forked and customized from an original ML property-ranking system, this version emphasizes interactivity and visualization with a polished Streamlit frontend.

---

## 🚀 Features

- 📊 Visualizes comparable property data
- 🧠 Uses GPT-3.5 to generate explanations for property ranking
- 📝 Collects user feedback on suggestions
- 💡 Interactive and intuitive UI using Streamlit

---



## 🧠 How It Works

1. **Input Data**: Loads `top3_gpt_explanations.csv` which includes candidate property data and GPT-generated explanations.
2. **Filtering**: Users can select specific appraisal orders, apply score thresholds, and filter by bedroom count.
3. **Visualization**:
   - Bar charts for score ranking and price distribution
   - Feature-level comparisons between subject and candidate properties
4. **Feedback Loop**: Users provide input on whether the ranked comparables are relevant, which gets logged to `feedback_log.csv`.
5. **Suggested Valuation**: Uses valid close prices of top candidates to estimate a valuation range and midpoint.

---

## 🖥️ Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/CompWise_AI.git
cd CompWise_AI
```
### 2. Install dependencies**

```bash
pip install -r requirements.txt
```

### 3.Set your OpenAI API key**

Make sure your OpenAI API key is exported as an environment variable:

```bash
export OPENAI_API_KEY=your-key-here
```

### 4.Run the app**

```bash
streamlit run app.py
```
📁 **Files Overview**

| File Name                  | Description                                                  |
|---------------------------|--------------------------------------------------------------|
| `app.py`                  | Main Streamlit application                                   |
| `top3_gpt_explanations.csv` | Ranked candidates with GPT-generated explanations           |
| `feedback_log.csv`        | Stores user responses on comparable property suggestions     |
| `requirements.txt`        | Python dependencies                                          |

---

📊 **Tech Stack**

- Python with Streamlit  
- Altair for data visualization  
- OpenAI GPT-3.5 for explanations  
- Pandas for data manipulation  

---

🙋‍♀️ **Author**

Built with ❤️ by Harman

=======
# Compwise AI

This project is an interactive AI-powered tool for evaluating and explaining comparable property rankings.
>>>>>>> a026970 (readme updated)

