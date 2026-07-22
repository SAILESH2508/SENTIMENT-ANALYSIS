"""
Setup script for the Universal Sentiment Analyzer.
Automates the complete setup process.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n{'='*50}")
    print(f"🔄 {description}")
    print(f"{'='*50}")

    try:
        result = subprocess.run(
            command, shell=True, check=True, capture_output=True, text=True
        )
        print(f"✅ {description} completed successfully!")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False


def check_file_exists(filepath, description):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print(f"✅ {description} found: {filepath}")
        return True
    else:
        print(f"❌ {description} not found: {filepath}")
        return False


def main():
    """Main setup function."""
    print("🚀 Universal Sentiment Analyzer Setup")
    print("This script will set up the complete environment and train the model.")

    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        sys.exit(1)

    print(f"✅ Python version: {sys.version}")

    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print(
            "❌ Failed to install dependencies. Please check your internet connection."
        )
        sys.exit(1)

    # Check if data files exist
    data_files_exist = check_file_exists(
        "data/train.csv", "Training data"
    ) and check_file_exists("data/test.csv", "Test data")

    if not data_files_exist:
        print("\n📊 Preparing data...")
        if not run_command("python eda.py", "Running EDA and data preparation"):
            print("❌ Data preparation failed!")
            sys.exit(1)

    # Check if model exists
    if not check_file_exists("sentiment_pipeline.pkl", "Trained model"):
        print("\n🤖 Training model...")
        if not run_command(
            "python model_trainer.py", "Training sentiment analysis model"
        ):
            print("❌ Model training failed!")
            sys.exit(1)

    # Run tests
    print("\n🧪 Running tests...")
    if not run_command(
        "python -m pytest test_sentiment_analyzer.py -v", "Running test suite"
    ):
        print("⚠️ Some tests failed, but setup can continue.")

    # Generate initial performance report
    print("\n📈 Generating initial performance report...")
    run_command("python monitoring.py", "Generating performance report")

    print(f"\n{'='*60}")
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print(f"{'='*60}")

    print("\n📋 Next Steps:")
    print("1. Run the Streamlit app: streamlit run app.py")
    print("2. Or start the API server: python api.py")
    print("3. View API docs at: http://localhost:8000/docs")
    print("4. Monitor performance: python monitoring.py")
    print("5. Run tests: python -m pytest test_sentiment_analyzer.py")

    print("\n📁 Generated Files:")
    files_to_check = [
        "sentiment_pipeline.pkl",
        "model_metrics.pkl",
        "data/train.csv",
        "data/test.csv",
        "config.yaml",
        "sentiment_analyzer.log",
    ]

    for file in files_to_check:
        if os.path.exists(file):
            size = os.path.getsize(file) / (1024 * 1024)  # Size in MB
            print(f"  ✅ {file} ({size:.1f} MB)")
        else:
            print(f"  ❌ {file} (missing)")

    print(f"\n🔧 Configuration:")
    print(f"  - Model: Logistic Regression with TF-IDF")
    print(f"  - Features: 1-2 gram TF-IDF vectors")
    print(f"  - Caching: Enabled with TTL")
    print(f"  - Logging: Enabled to sentiment_analyzer.log")
    print(f"  - API: FastAPI with monitoring endpoints")


if __name__ == "__main__":
    main()
