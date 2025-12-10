# Universal Sentiment Analyzer

A machine learning application that predicts the sentiment (Positive, Negative, or Intermediate) of any text. Built with Python, Scikit-learn, and Streamlit.

![Universal Sentiment Analyzer Demo](demo_screenshot.png)

## 🚀 Features

*   **Universal Analysis**: Works on product reviews, social media posts, general feedback, and more.
*   **Three-Tier Sentiment**: Classifies text as **Positive**, **Negative**, or **Intermediate** (for neutral/mixed content).
*   **Input Validation**: Rejects nonsense or extremely short inputs.
*   **Interactive UI**: Modern, responsive dashboard with Dark Blue/White theme.
*   **Data Insights**: Visualizes the training data distribution.

## 🛠️ Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd sentiment-analysis
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Prepare Data & Model**:
    *   The dataset and model are not included in the repo (to keep it light). Run the following scripts to generate them:
    ```bash
    # 1. Download the IMDB Dataset
    python download_data.py
    
    # 2. Process Data and Visualize
    python eda.py
    
    # 3. Train the Model (Generates sentiment_pipeline.pkl)
    python model_trainer.py
    ```

4.  **Run the Application**:
    ```bash
    streamlit run app.py
    ```

## 📂 Project Structure

*   `app.py`: Main Streamlit application.
*   `inference_service.py`: Logic for prediction and validation.
*   `model_trainer.py`: Script to train the Logistic Regression model.
*   `eda.py`: Exploratory Data Analysis and data splitting.
*   `download_data.py`: Helper to download the dataset.
*   `requirements.txt`: Python dependencies.

## 🧠 Model Details

*   **Algorithm**: Logistic Regression.
*   **Vectorization**: TF-IDF (Term Frequency-Inverse Document Frequency).
*   **Training Data**: 50,000 IMDB Movie Reviews (Generalizes well to English sentiment).
*   **Accuracy**: ~90% on test set.
