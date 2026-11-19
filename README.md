# Government Scheme Eligibility & Recommendation Assistant (Yojana Sarthi)

A full-stack web application that analyzes a citizen's **age, annual income, occupation, location, and social category** to determine eligible government welfare schemes and rank personalized benefits using a hybrid **Rule-Based + Machine Learning** engine.

## Technologies Used
- **Backend:** Python, Flask
- **Data Processing:** Pandas, NumPy
- **Machine Learning & Logic:** Scikit-learn (TF-IDF Vectorizer, Cosine Similarity, MinMaxScaler) + Rule-Based Eligibility Engine
- **Database:** MySQL (`schema.sql`) with automatic CSV fallback (`schemes_data.csv`)
- **Frontend:** HTML5, CSS3

## Project Structure (Single Flat Folder)
All files are placed in a single root folder for easy setup and GitHub upload:
```text
government-scheme-assistant/
├── app.py               # Flask web server & MySQL connector
├── recommender.py       # Rule-based eligibility filter & Scikit-learn ML ranking engine
├── schema.sql           # MySQL database schema & sample government schemes
├── schemes_data.csv     # Local dataset fallback so the app runs out-of-the-box
├── index.html           # Frontend HTML interface
├── style.css            # Responsive CSS styling
├── requirements.txt     # Python dependencies
├── .env.example         # Environment configuration template
├── .gitignore           # Git ignore rules
└── README.md            # Project documentation
```

## How to Run Locally

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/your-username/government-scheme-assistant.git
cd government-scheme-assistant
pip install -r requirements.txt
```

### 2. Configure MySQL Database (Optional — Works out-of-the-box with CSV too!)
1. Open MySQL Workbench or terminal and run `schema.sql`:
   ```bash
   mysql -u root -p < schema.sql
   ```
2. Copy `.env.example` to `.env` and update your MySQL credentials:
   ```bash
   cp .env.example .env
   ```
*(Note: If MySQL is not running, the app automatically falls back to `schemes_data.csv` so you can test it immediately.)*

### 3. Start the Flask Application
```bash
python app.py
```
Open your browser and go to: **http://127.0.0.1:5000**
