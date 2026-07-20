"""
Performance monitoring and analytics for the sentiment analyzer.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Any
import logging

logger = logging.getLogger(__name__)

class PerformanceMonitor:
    """Monitor and analyze sentiment analyzer performance."""
    
    def __init__(self, log_file: str = "sentiment_analyzer.log"):
        self.log_file = log_file
    
    def parse_prediction_logs(self, days_back: int = 7) -> pd.DataFrame:
        """
        Parse prediction logs from the last N days.
        
        Args:
            days_back: Number of days to look back
            
        Returns:
            DataFrame with parsed log data
        """
        if not os.path.exists(self.log_file):
            logger.warning(f"Log file {self.log_file} not found")
            return pd.DataFrame()
        
        predictions = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    if "Prediction logged:" in line:
                        try:
                            # Extract the JSON part
                            json_start = line.find('{')
                            if json_start != -1:
                                json_data = line[json_start:]
                                data = json.loads(json_data)
                                
                                # Parse timestamp
                                timestamp = datetime.fromisoformat(data['timestamp'])
                                if timestamp >= cutoff_date:
                                    predictions.append(data)
                        except (json.JSONDecodeError, KeyError, ValueError) as e:
                            logger.warning(f"Error parsing log line: {e}")
                            continue
        
        except FileNotFoundError:
            logger.error(f"Log file not found: {self.log_file}")
            return pd.DataFrame()
        
        if not predictions:
            return pd.DataFrame()
        
        df = pd.DataFrame(predictions)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    
    def generate_performance_report(self, days_back: int = 7) -> Dict[str, Any]:
        """
        Generate a comprehensive performance report.
        
        Args:
            days_back: Number of days to analyze
            
        Returns:
            Dictionary with performance metrics
        """
        df = self.parse_prediction_logs(days_back)
        
        if df.empty:
            return {'error': 'No prediction data available'}
        
        # Basic statistics
        total_predictions = len(df)
        unique_users = df['user_id'].nunique()
        
        # Sentiment distribution
        sentiment_dist = df['prediction'].value_counts().to_dict()
        
        # Confidence statistics
        confidence_stats = {
            'mean': df['confidence'].mean(),
            'median': df['confidence'].median(),
            'std': df['confidence'].std(),
            'min': df['confidence'].min(),
            'max': df['confidence'].max()
        }
        
        # Text length statistics
        text_length_stats = {
            'mean': df['text_length'].mean(),
            'median': df['text_length'].median(),
            'std': df['text_length'].std(),
            'min': df['text_length'].min(),
            'max': df['text_length'].max()
        }
        
        # Hourly usage pattern
        df['hour'] = df['timestamp'].dt.hour
        hourly_usage = df['hour'].value_counts().sort_index().to_dict()
        
        # Daily usage pattern
        df['date'] = df['timestamp'].dt.date
        daily_usage = df['date'].value_counts().sort_index().to_dict()
        
        return {
            'period_days': days_back,
            'total_predictions': total_predictions,
            'unique_users': unique_users,
            'sentiment_distribution': sentiment_dist,
            'confidence_statistics': confidence_stats,
            'text_length_statistics': text_length_stats,
            'hourly_usage_pattern': hourly_usage,
            'daily_usage_pattern': {str(k): v for k, v in daily_usage.items()},
            'generated_at': datetime.now().isoformat()
        }
    
    def plot_usage_analytics(self, days_back: int = 7, save_path: str = None) -> None:
        """
        Create visualizations for usage analytics.
        
        Args:
            days_back: Number of days to analyze
            save_path: Optional path to save the plot
        """
        df = self.parse_prediction_logs(days_back)
        
        if df.empty:
            print("No data available for plotting")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Sentiment Analyzer Usage Analytics (Last {days_back} days)', fontsize=16)
        
        # Sentiment distribution
        sentiment_counts = df['prediction'].value_counts()
        axes[0, 0].pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%')
        axes[0, 0].set_title('Sentiment Distribution')
        
        # Confidence distribution
        axes[0, 1].hist(df['confidence'], bins=20, alpha=0.7, color='skyblue')
        axes[0, 1].set_title('Confidence Score Distribution')
        axes[0, 1].set_xlabel('Confidence Score')
        axes[0, 1].set_ylabel('Frequency')
        
        # Hourly usage pattern
        df['hour'] = df['timestamp'].dt.hour
        hourly_usage = df['hour'].value_counts().sort_index()
        axes[1, 0].bar(hourly_usage.index, hourly_usage.values, color='lightgreen')
        axes[1, 0].set_title('Hourly Usage Pattern')
        axes[1, 0].set_xlabel('Hour of Day')
        axes[1, 0].set_ylabel('Number of Predictions')
        
        # Text length distribution
        axes[1, 1].hist(df['text_length'], bins=20, alpha=0.7, color='orange')
        axes[1, 1].set_title('Text Length Distribution')
        axes[1, 1].set_xlabel('Text Length (characters)')
        axes[1, 1].set_ylabel('Frequency')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Analytics plot saved to {save_path}")
        
        plt.show()
    
    def detect_anomalies(self, days_back: int = 7) -> List[Dict[str, Any]]:
        """
        Detect potential anomalies in usage patterns.
        
        Args:
            days_back: Number of days to analyze
            
        Returns:
            List of detected anomalies
        """
        df = self.parse_prediction_logs(days_back)
        
        if df.empty:
            return []
        
        anomalies = []
        
        # Check for unusual confidence patterns
        mean_confidence = df['confidence'].mean()
        std_confidence = df['confidence'].std()
        
        low_confidence_threshold = mean_confidence - 2 * std_confidence
        high_confidence_threshold = mean_confidence + 2 * std_confidence
        
        low_confidence_count = len(df[df['confidence'] < low_confidence_threshold])
        high_confidence_count = len(df[df['confidence'] > high_confidence_threshold])
        
        if low_confidence_count > len(df) * 0.1:  # More than 10% low confidence
            anomalies.append({
                'type': 'low_confidence_spike',
                'description': f'High number of low-confidence predictions: {low_confidence_count}',
                'severity': 'medium'
            })
        
        # Check for unusual text lengths
        mean_length = df['text_length'].mean()
        std_length = df['text_length'].std()
        
        very_short_texts = len(df[df['text_length'] < 10])
        very_long_texts = len(df[df['text_length'] > mean_length + 3 * std_length])
        
        if very_short_texts > len(df) * 0.2:  # More than 20% very short texts
            anomalies.append({
                'type': 'short_text_spike',
                'description': f'High number of very short texts: {very_short_texts}',
                'severity': 'low'
            })
        
        # Check for sentiment distribution skew
        sentiment_dist = df['prediction'].value_counts(normalize=True)
        if any(sentiment_dist > 0.8):  # More than 80% of one sentiment
            dominant_sentiment = sentiment_dist.idxmax()
            anomalies.append({
                'type': 'sentiment_skew',
                'description': f'Unusual skew towards {dominant_sentiment}: {sentiment_dist[dominant_sentiment]:.1%}',
                'severity': 'medium'
            })
        
        return anomalies

def generate_monitoring_report(days_back: int = 7) -> None:
    """Generate and display a monitoring report."""
    monitor = PerformanceMonitor()
    
    print(f"\n{'='*50}")
    print(f"SENTIMENT ANALYZER PERFORMANCE REPORT")
    print(f"{'='*50}")
    
    report = monitor.generate_performance_report(days_back)
    
    if 'error' in report:
        print(f"Error: {report['error']}")
        return
    
    print(f"Analysis Period: Last {report['period_days']} days")
    print(f"Total Predictions: {report['total_predictions']:,}")
    print(f"Unique Users: {report['unique_users']:,}")
    
    print(f"\nSentiment Distribution:")
    for sentiment, count in report['sentiment_distribution'].items():
        percentage = (count / report['total_predictions']) * 100
        print(f"  {sentiment}: {count:,} ({percentage:.1f}%)")
    
    print(f"\nConfidence Statistics:")
    conf_stats = report['confidence_statistics']
    print(f"  Mean: {conf_stats['mean']:.3f}")
    print(f"  Median: {conf_stats['median']:.3f}")
    print(f"  Std Dev: {conf_stats['std']:.3f}")
    
    print(f"\nText Length Statistics:")
    length_stats = report['text_length_statistics']
    print(f"  Mean: {length_stats['mean']:.1f} characters")
    print(f"  Median: {length_stats['median']:.1f} characters")
    
    # Check for anomalies
    anomalies = monitor.detect_anomalies(days_back)
    if anomalies:
        print(f"\n⚠️  ANOMALIES DETECTED:")
        for anomaly in anomalies:
            print(f"  [{anomaly['severity'].upper()}] {anomaly['description']}")
    else:
        print(f"\n✅ No anomalies detected")
    
    print(f"\nReport generated at: {report['generated_at']}")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    generate_monitoring_report()