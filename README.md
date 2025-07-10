# 🧠 Smart Synthetic Data Generator

A powerful, customizable tool for generating and enriching synthetic datasets using state-of-the-art techniques like CTGAN and AI language models (via OpenRouter). Built for GenAI Hackathons, privacy-preserving applications, and rapid experimentation.

## 🚀 Features

- 🧬 **Synthetic Data Generation** using CTGAN
- 💬 **Prompt-based Generation** using LLMs via OpenRouter
- 🔁 **Combo Mode**: Generate → Enrich or Modify → Generate
- 🔐 **Privacy Postprocessing**: Gaussian noise, column masking, category swapping
- ✅ **Validation Dashboard**: Chi², KS-Test, Wasserstein Distance, Correlation Difference with visual graphs
- 📊 **Downloadable output files**
- 🖥️ **Modern Full Stack UI** with React + FastAPI

## 📦 Tech Stack

- **Frontend**: React + TailwindCSS + Recharts
- **Backend**: FastAPI, CTGAN, Pandas, Scipy
- **LLM Integration**: [OpenRouter](https://openrouter.ai/)
- **Deployment (Recommended)**:
  - Frontend: AWS S3 + CloudFront (static site)
  - Backend: AWS Lambda + API Gateway via AWS SAM

---

## 🛠️ Setup Instructions

### 1. Clone the repository

in bash...
git clone https://github.com/your-username/smart-synthetic-generator.git
cd smart-synthetic-generator

### 2. Set up backend

cd backend
python -m venv .venv310
source .venv310/bin/activate  # or `.venv310\Scripts\activate` on Windows
pip install -r requirements.txt
Create a .env file in the backend/ folder:
OPENROUTER_API_KEY=your_openrouter_api_key_here

### 3. Run backend
uvicorn main:app --reload
Backend will be live at http://localhost:8000

### 4. Set up frontend
In a separate terminal:
cd frontend
npm install
Create a .env file in the frontend/ folder:
REACT_APP_API_URL=http://localhost:8000

Run the frontend:
npm start

## 🧪 Testing Instructions

Once both frontend and backend are running:

Go to http://localhost:3000

Choose your input method:

Upload real dataset CSV

Write a natural language prompt

Or combine both

Select one of the generation modes:

ModGen (modify then generate)

GenEn (generate then enrich)

Mod (modify only)

Enable privacy options and validation if desired.

Click Generate

Wait for completion message and validation charts.

Download your synthetic dataset.

## 🌍 Deployment Instructions (Free AWS Plan)
Follow this full deployment guide using:

AWS S3 + CloudFront for frontend

AWS Lambda + API Gateway for backend (FastAPI + Mangum)

Environment variables stored securely in Lambda

OpenRouter handles prompt completion

Note: Ensure you stay within AWS Free Tier and OpenRouter's rate limits.

## 📁 Folder Structure

smart-synthetic-generator/  
├── backend/  
│   ├── main.py  
│   ├── ctgan_generator.py  
│   ├── text_generator.py  
│   ├── combo_generator.py  
│   ├── privacy_postprocessing.py  
│   ├── validator.py  
│   ├── requirements.txt  
│   └── .env  
├── frontend/  
│   ├── public/  
│   ├── src/  
│   │   ├── components/  
│   │   ├── pages/  
│   │   ├── App.js  
│   │   └── index.js  
│   ├── package.json  
│   └── .env  
├── README.md  
└── .gitignore  


## 🧠 Validation Metrics Explained
Each of these metrics helps compare your synthetic data to the real dataset to measure similarity and quality:

Chi² Statistic (chi2_stat)
Used for categorical columns. It checks whether the category distributions in real and synthetic data are significantly different.
→ Ideal range: The closer to 0, the better.

p-value (p_value)
Represents the probability that the real and synthetic data come from the same distribution. A higher value means better similarity.
→ Ideal range: Greater than 0.05.

Kolmogorov-Smirnov Statistic (ks_stat)
Used for numerical columns. Measures the largest difference between the cumulative distributions of real and synthetic values.
→ Ideal range: Less than 0.3.

Wasserstein Distance (wasserstein_distance)
Evaluates the difference in overall distribution shape for numerical columns. Sensitive to differences in central tendency and spread.
→ Ideal range: Less than 10.

Total Variation Distance (tvd)
Compares the normalized frequencies of categorical values. Measures the maximum probability difference between the real and synthetic distributions.
→ Ideal range: Less than 0.2.

Average Correlation Difference (average_correlation_difference)
Measures the average change in how features are correlated with each other between the real and synthetic datasets.
→ Ideal range: Less than 0.15.

🔴 Metrics above these thresholds are flagged in red on the dashboard to help you spot potential quality or privacy concerns.

## 📝 License
MIT License. You are free to use, modify, and share.

## 🙌 Acknowledgments
Built for the GenAI Hackathon on AWS using open tools like CTGAN, OpenRouter, and AWS.

