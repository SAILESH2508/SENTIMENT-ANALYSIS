"""
Dataset Loader for Universal Sentiment Analyzer
Provides easy access to all generated datasets
"""

import pandas as pd
import os
import json
from typing import Dict, List, Optional


class DatasetLoader:
    """Load and manage datasets for sentiment analysis testing"""

    def __init__(self):
        self.available_datasets = self._discover_datasets()
        self.stats = self._load_statistics()

    def _discover_datasets(self) -> Dict[str, str]:
        """Discover all available dataset files"""
        datasets = {}
        data_dir = "data"

        # Look for dataset files in data directory
        if os.path.exists(data_dir):
            for file in os.listdir(data_dir):
                if file.startswith("dataset_") and file.endswith(".csv"):
                    # Extract dataset name from filename
                    name = (
                        file.replace("dataset_", "")
                        .replace(".csv", "")
                        .replace("_", " ")
                        .title()
                    )
                    datasets[name] = os.path.join(data_dir, file)

        return datasets

    def _load_statistics(self) -> Dict:
        """Load dataset statistics if available"""
        try:
            with open("data/enhanced_dataset_statistics.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def list_datasets(self) -> List[str]:
        """Get list of available dataset names"""
        return list(self.available_datasets.keys())

    def load_dataset(self, name: str) -> Optional[pd.DataFrame]:
        """Load a specific dataset by name"""
        if name not in self.available_datasets:
            print(f"Dataset '{name}' not found. Available: {self.list_datasets()}")
            return None

        try:
            df = pd.read_csv(self.available_datasets[name])
            print(f"✅ Loaded {name}: {len(df)} samples")
            return df
        except Exception as e:
            print(f"❌ Error loading {name}: {e}")
            return None

    def get_sample_texts(
        self, dataset_name: str, sentiment: str = None, count: int = 5
    ) -> List[str]:
        """Get sample texts from a dataset"""
        df = self.load_dataset(dataset_name)
        if df is None:
            return []

        if sentiment and "sentiment" in df.columns:
            df = df[df["sentiment"].str.lower() == sentiment.lower()]

        if "text" in df.columns:
            return df["text"].sample(min(count, len(df))).tolist()
        else:
            return []

    def get_mixed_sample(self, count: int = 10) -> pd.DataFrame:
        """Get a mixed sample from all datasets"""
        try:
            mixed_df = pd.read_csv("data/dataset_mixed_samples.csv")
            return mixed_df.sample(min(count, len(mixed_df)))
        except FileNotFoundError:
            print("Mixed samples dataset not found")
            return pd.DataFrame()

    def get_statistics(self) -> Dict:
        """Get dataset statistics"""
        return self.stats

    def print_summary(self):
        """Print a summary of all available datasets"""
        print("📊 Available Datasets for Sentiment Analysis Testing")
        print("=" * 60)

        for name, filename in self.available_datasets.items():
            try:
                df = pd.read_csv(filename)
                sentiment_dist = (
                    df["sentiment"].value_counts()
                    if "sentiment" in df.columns
                    else "N/A"
                )
                print(f"📁 {name:<30} {len(df):>6} samples")
                if isinstance(sentiment_dist, pd.Series):
                    for sentiment, count in sentiment_dist.items():
                        print(f"   └─ {sentiment}: {count}")
            except Exception as e:
                print(f"📁 {name:<30} Error loading")

        print("\n💡 Usage Examples:")
        print("  loader = DatasetLoader()")
        print("  df = loader.load_dataset('Mixed Samples')")
        print("  samples = loader.get_sample_texts('Ecommerce Reviews', 'positive', 3)")


def create_quick_test_samples():
    """Create quick test samples for immediate use"""

    quick_samples = {
        "positive": [
            "This product is absolutely amazing! Best purchase I've made all year!",
            "Outstanding customer service and incredible quality. Highly recommend!",
            "Perfect! Exactly what I needed and arrived super fast!",
            "Love this so much! It's made my life so much easier and more enjoyable!",
            "Fantastic experience from start to finish. Will definitely buy again!",
        ],
        "negative": [
            "Terrible quality and completely broke after one day. Total waste of money!",
            "Worst customer service ever! Rude staff and no help whatsoever!",
            "Complete garbage! Nothing like the description and doesn't work at all!",
            "Horrible experience! Product arrived damaged and return process is nightmare!",
            "Avoid this at all costs! Poor quality and misleading advertising!",
        ],
        "neutral": [
            "It's okay, does what it's supposed to do but nothing particularly special.",
            "Average product with decent quality for the price. Nothing more, nothing less.",
            "Fair experience overall. Met basic expectations without exceeding them.",
            "Standard quality and performance. Could be better but not terrible either.",
            "Reasonable product that serves its purpose adequately. It's fine.",
        ],
    }

    # Save as CSV for easy loading
    quick_data = []
    for sentiment, texts in quick_samples.items():
        for text in texts:
            quick_data.append(
                {
                    "text": text,
                    "sentiment": sentiment.title(),
                    "source": "Quick Test Samples",
                    "category": "Mixed",
                }
            )

    quick_df = pd.DataFrame(quick_data)
    quick_df.to_csv("data/dataset_quick_test_samples.csv", index=False)

    return quick_df


if __name__ == "__main__":
    # Create quick test samples
    print("🚀 Creating quick test samples...")
    quick_df = create_quick_test_samples()
    print(f"✅ Created {len(quick_df)} quick test samples")

    # Initialize loader and show summary
    loader = DatasetLoader()
    loader.print_summary()

    # Show some examples
    print(f"\n🎯 Example Usage:")
    print("Getting positive samples from ecommerce reviews:")

    if "Ecommerce Reviews" in loader.list_datasets():
        samples = loader.get_sample_texts("Ecommerce Reviews", "positive", 3)
        for i, sample in enumerate(samples, 1):
            print(f"  {i}. {sample[:80]}...")

    print(f"\n📈 Dataset Statistics:")
    stats = loader.get_statistics()
    if stats:
        print(
            f"  • Total Samples: {stats.get('generation_info', {}).get('total_samples', 'N/A'):,}"
        )
        dist = stats.get("sentiment_distribution", {})
        if dist:
            print(
                f"  • Positive: {dist.get('positive', 0)} ({dist.get('positive_percentage', 0)}%)"
            )
            print(
                f"  • Negative: {dist.get('negative', 0)} ({dist.get('negative_percentage', 0)}%)"
            )
            print(
                f"  • Neutral: {dist.get('neutral', 0)} ({dist.get('neutral_percentage', 0)}%)"
            )
