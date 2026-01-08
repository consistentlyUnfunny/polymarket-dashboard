# Polymarket Opportunity Dashboard

A Python-based dashboard that tracks active Polymarket binary markets closing within the next **48 hours**. It automatically highlights high-potential "Focus Markets" (Crypto & Sports) and provides real-time pricing via the CLOB API.

## Features

* **Gamma API Integration:** Fetches market metadata and resolves JSON string fields safely.
* **CLOB API Integration:** Batch-fetches live "Buy" side prices for accurate market data.
* **Smart Filtering:** * Active markets only (Order Book enabled, not closed).
    * Closing time window: > 0 hours and <= 48 hours.
    * Validates binary (Yes/No) outcomes.
* **Focus Logic:** Automatically selects 1 Crypto and 1 Sports market to highlight.
* **UI:** Built with Streamlit, supporting sorting and missing-price filtering.

## How to Run

### Prerequisites
* Python 3.10+
* Git

1. **Clone the repository**
```
   git clone [https://github.com/YOUR_USERNAME/polymarket-dashboard.git](https://github.com/YOUR_USERNAME/polymarket-dashboard.git)
```
```
   cd polymarket-dashboard
```
2. **Create virtual environment**
```
python -m venv .venv

# Activate it (Windows)
.\.venv\Scripts\activate

# Activate it (Mac/Linux)
source .venv/bin/activate
```
3. **Install Dependencies**
```
pip install -r requirements.txt
```
4. Run the Dashboard
```
streamlit run app.py
```
5. To Run Unit Test:
```
python -m unittest discover tests
```
