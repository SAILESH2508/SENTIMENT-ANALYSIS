import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
import os

# ---------------------------------------------------------
# DIRECT LINK TO DATASET:
# https://www.kaggle.com/datasets/lakshmi25npathi/imdb-dataset-of-50k-movie-reviews
# Alternate (used below for automation): 
# https://raw.githubusercontent.com/Ankit152/IMDB-sentiment-analysis/master/IMDB-Dataset.csv
# ---------------------------------------------------------

def load_and_analyze():
    print("Loading dataset...")
    # Using a reliable GitHub mirror for the 50K IMDB dataset to allow automatic running
    url = "https://raw.githubusercontent.com/Ankit152/IMDB-sentiment-analysis/master/IMDB-Dataset.csv"
    
    try:
        df = pd.read_csv(url)
        print("Dataset loaded successfully from URL.")
    except Exception as e:
        print(f"Failed to load from URL: {e}")
        if os.path.exists("IMDB Dataset.csv"):
            print("Loading from local file 'IMDB Dataset.csv'...")
            df = pd.read_csv("IMDB Dataset.csv")
        else:
            print("Please download the dataset and save it as 'IMDB Dataset.csv'")
            return

    # Map labels: positive -> 1, negative -> 0
    print("Mapping labels...")
    df['sentiment'] = df['sentiment'].map({'positive': 1, 'negative': 0})
    
    # Stratified Split 80/20
    print("Performing Stratified Split (80/20)...")
    train_df, test_df = train_test_split(df, test_size=0.2, stratify=df['sentiment'], random_state=42)
    print(f"Train size: {len(train_df)}, Test size: {len(test_df)}")

    # Visualization 1: Class Distribution
    plt.figure(figsize=(6, 4))
    sns.countplot(x='sentiment', data=df)
    plt.title('Class Distribution (1=Pos, 0=Neg)')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    plt.savefig('class_distribution.png')
    print("Saved class_distribution.png")

    # Visualization 2: Review Length by Sentiment
    df['review_length'] = df['review'].apply(len)
    plt.figure(figsize=(8, 5))
    sns.barplot(x='sentiment', y='review_length', data=df)
    plt.title('Average Review Length by Sentiment')
    plt.xlabel('Sentiment')
    plt.ylabel('Avg Length (chars)')
    plt.savefig('review_length.png')
    print("Saved review_length.png")

    # Optional: Save split data for training
    train_df.to_csv('train.csv', index=False)
    test_df.to_csv('test.csv', index=False)
    print("Saved train.csv and test.csv")

if __name__ == "__main__":
    load_and_analyze()
