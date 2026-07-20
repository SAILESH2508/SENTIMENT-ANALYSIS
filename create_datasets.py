"""
Dataset Generator for Universal Sentiment Analyzer
Creates comprehensive datasets for testing all features
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import random

def create_product_reviews_dataset():
    """Create a comprehensive product reviews dataset"""
    
    # Product categories
    categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports', 'Beauty', 'Automotive']
    
    # Positive reviews
    positive_reviews = [
        "This product exceeded all my expectations! Amazing quality and fast shipping.",
        "Absolutely love this purchase! Worth every penny and more.",
        "Outstanding quality and excellent customer service. Highly recommend!",
        "Perfect product, exactly as described. Will definitely buy again!",
        "Incredible value for money. Best purchase I've made this year!",
        "Fantastic quality and arrived quickly. Very satisfied with this buy.",
        "Excellent product! Works perfectly and looks great too.",
        "Amazing! This has made my life so much easier. Love it!",
        "Top-notch quality and great price. Couldn't be happier!",
        "Superb product with excellent build quality. Highly recommended!",
        "This is exactly what I was looking for. Perfect in every way!",
        "Outstanding performance and great design. Very impressed!",
        "Brilliant product! Exceeded my expectations in every aspect.",
        "Wonderful quality and fast delivery. Will shop here again!",
        "Exceptional value and quality. This company knows what they're doing!",
        "Love this product! It's become an essential part of my daily routine.",
        "Impressive quality and attention to detail. Very satisfied!",
        "Great product at an unbeatable price. Highly recommend to everyone!",
        "Perfect! Works exactly as advertised and looks fantastic.",
        "Amazing customer service and even better product quality!"
    ]
    
    # Negative reviews
    negative_reviews = [
        "Terrible quality and poor customer service. Would not recommend.",
        "Complete waste of money. Product broke after just one use.",
        "Disappointing purchase. Nothing like the description or photos.",
        "Poor quality materials and shoddy construction. Avoid this product.",
        "Worst purchase ever! Product arrived damaged and unusable.",
        "Overpriced and underdelivered. Very disappointed with this buy.",
        "Cheap quality and doesn't work as advertised. Save your money.",
        "Horrible experience from start to finish. Poor quality product.",
        "Not worth the money at all. Quality is much worse than expected.",
        "Defective product and unhelpful customer service. Very frustrated.",
        "Poor design and even worse execution. Regret this purchase.",
        "Completely useless product. Doesn't do what it claims to do.",
        "Terrible build quality and arrived late. Very disappointed.",
        "Overpriced junk! Product fell apart within days of use.",
        "Misleading description and poor quality. Requesting a refund.",
        "Awful product with terrible customer support. Avoid at all costs!",
        "Cheap materials and poor workmanship. Not recommended.",
        "Product doesn't match description at all. Very misleading.",
        "Broke immediately upon use. Clearly poor quality control.",
        "Worst customer service experience ever. Product is also terrible."
    ]
    
    # Neutral reviews
    neutral_reviews = [
        "It's okay, nothing special but does the job adequately.",
        "Average product with some good points and some bad ones.",
        "Decent quality for the price, though not outstanding.",
        "It works as expected, though nothing to write home about.",
        "Fair product, meets basic expectations but nothing more.",
        "Reasonable quality and price. Could be better, could be worse.",
        "It's fine, does what it's supposed to do without any issues.",
        "Average product that gets the job done. Nothing exceptional.",
        "Okay quality, though I've seen better for similar prices.",
        "It works, but there are probably better options available.",
        "Decent product overall, though some minor issues to note.",
        "Satisfactory purchase. Not amazing but not terrible either.",
        "It's alright, serves its purpose but lacks wow factor.",
        "Standard quality product. Does what it says on the tin.",
        "Mediocre product with average performance and quality.",
        "It's functional but not particularly impressive or exciting.",
        "Acceptable quality for the price point. Nothing more, nothing less.",
        "Works as advertised but doesn't exceed expectations.",
        "Fair product that does the basics well enough.",
        "It's okay, though I might look for alternatives next time."
    ]
    
    # Create dataset
    data = []
    
    for i in range(500):  # 500 reviews total
        if i < 200:  # 40% positive
            text = random.choice(positive_reviews)
            sentiment = 'Positive'
            rating = random.randint(4, 5)
        elif i < 350:  # 30% negative
            text = random.choice(negative_reviews)
            sentiment = 'Negative'
            rating = random.randint(1, 2)
        else:  # 30% neutral
            text = random.choice(neutral_reviews)
            sentiment = 'Neutral'
            rating = 3
        
        data.append({
            'review_id': f'REV_{i+1:04d}',
            'text': text,
            'sentiment': sentiment,
            'rating': rating,
            'category': random.choice(categories),
            'verified_purchase': random.choice([True, False]),
            'helpful_votes': random.randint(0, 50),
            'date': (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
        })
    
    return pd.DataFrame(data)

def create_social_media_dataset():
    """Create social media posts dataset"""
    
    # Social media posts
    positive_posts = [
        "Just had the most amazing coffee at this new cafe! ☕ #blessed #coffeelover",
        "Beautiful sunset tonight! Nature never fails to amaze me 🌅 #grateful",
        "Finished my first marathon today! Feeling incredible! 🏃‍♀️ #achievement #running",
        "Best vacation ever! The beaches here are absolutely stunning 🏖️ #paradise",
        "Got promoted at work today! Hard work really pays off! 🎉 #success #career",
        "This new restaurant is absolutely fantastic! Must try! 🍽️ #foodie #delicious",
        "Amazing concert last night! The band was incredible! 🎵 #music #livemusic",
        "Just adopted the cutest puppy! My heart is so full ❤️ 🐶 #puppylove",
        "Perfect weather for a picnic in the park! 🌞 #beautiful #outdoors",
        "Loving this new book! Can't put it down! 📚 #reading #bookworm"
    ]
    
    negative_posts = [
        "Stuck in traffic for 2 hours! This is ridiculous! 😤 #frustrated #traffic",
        "Terrible service at this restaurant. Never going back! 😠 #disappointed",
        "My flight got cancelled AGAIN! Worst airline ever! ✈️ #angry #travel",
        "Phone screen cracked for the third time this year 📱 #annoyed #technology",
        "Rain ruined our outdoor wedding plans 😢 #disappointed #weather",
        "Lost my wallet today. What a terrible day! 😞 #stressed #badday",
        "This movie was a complete waste of time and money 🎬 #terrible #regret",
        "Customer service was absolutely horrible today 📞 #frustrated #poorservice",
        "My car broke down on the highway. Could this day get worse? 🚗 #unlucky",
        "Food poisoning from that new place. Feeling awful! 🤢 #sick #foodpoisoning"
    ]
    
    neutral_posts = [
        "Just finished grocery shopping. Regular Tuesday stuff 🛒 #routine",
        "Weather is okay today, not too hot, not too cold 🌤️ #weather",
        "Watching TV after work. Nothing special planned tonight 📺 #relaxing",
        "Had lunch at the usual place. Same as always 🍽️ #lunch #routine",
        "Commute was normal today. No delays or issues 🚌 #commute",
        "Finished reading that book. It was alright, nothing special 📖 #reading",
        "Went for a walk in the neighborhood. Nice and quiet 🚶‍♀️ #walk",
        "Regular workout at the gym today. Keeping up the routine 💪 #fitness",
        "Meeting went as expected. Nothing surprising happened 💼 #work",
        "Cooked dinner at home tonight. Simple pasta dish 🍝 #cooking"
    ]
    
    data = []
    platforms = ['Twitter', 'Facebook', 'Instagram', 'LinkedIn', 'TikTok']
    
    for i in range(300):
        if i < 120:  # 40% positive
            text = random.choice(positive_posts)
            sentiment = 'Positive'
            engagement = random.randint(50, 500)
        elif i < 210:  # 30% negative
            text = random.choice(negative_posts)
            sentiment = 'Negative'
            engagement = random.randint(20, 200)
        else:  # 30% neutral
            text = random.choice(neutral_posts)
            sentiment = 'Neutral'
            engagement = random.randint(10, 100)
        
        data.append({
            'post_id': f'POST_{i+1:04d}',
            'text': text,
            'sentiment': sentiment,
            'platform': random.choice(platforms),
            'likes': random.randint(0, engagement),
            'shares': random.randint(0, engagement//5),
            'comments': random.randint(0, engagement//10),
            'timestamp': (datetime.now() - timedelta(hours=random.randint(1, 168))).isoformat(),
            'user_followers': random.randint(100, 10000)
        })
    
    return pd.DataFrame(data)

def create_customer_feedback_dataset():
    """Create customer service feedback dataset"""
    
    positive_feedback = [
        "The support team was incredibly helpful and resolved my issue quickly.",
        "Outstanding customer service! They went above and beyond to help me.",
        "Quick response time and very knowledgeable staff. Excellent experience!",
        "Professional and courteous service. Problem solved in minutes!",
        "Best customer service I've ever experienced. Truly impressed!",
        "The representative was patient and explained everything clearly.",
        "Fast, efficient, and friendly service. Couldn't ask for more!",
        "Exceeded my expectations with their helpfulness and expertise.",
        "Wonderful experience from start to finish. Great team!",
        "They made a difficult situation easy to resolve. Thank you!"
    ]
    
    negative_feedback = [
        "Waited on hold for over an hour just to be transferred again.",
        "Rude and unhelpful staff. Completely disappointed with the service.",
        "No one seems to know how to solve basic problems. Very frustrating!",
        "Terrible experience. Multiple calls with no resolution.",
        "Unprofessional behavior and lack of knowledge from support team.",
        "Worst customer service ever. They made my problem worse!",
        "Long wait times and no helpful solutions provided.",
        "Staff seemed annoyed to help and provided incorrect information.",
        "Multiple transfers and still no resolution to my simple issue.",
        "Completely unsatisfied with the level of service received."
    ]
    
    neutral_feedback = [
        "The service was adequate, though nothing particularly impressive.",
        "Standard customer service experience. Got my issue resolved eventually.",
        "It was fine, took a while but they did help in the end.",
        "Average experience. The representative was polite but not very helpful.",
        "Okay service, though I've had better experiences elsewhere.",
        "They resolved my issue but it took longer than expected.",
        "Decent service overall, though room for improvement.",
        "Fair experience. The process could be more streamlined.",
        "It was alright, nothing to complain about but nothing special either.",
        "Standard service level. Met basic expectations."
    ]
    
    data = []
    departments = ['Technical Support', 'Billing', 'Sales', 'General Inquiry', 'Complaints']
    
    for i in range(200):
        if i < 80:  # 40% positive
            text = random.choice(positive_feedback)
            sentiment = 'Positive'
            satisfaction = random.randint(4, 5)
        elif i < 140:  # 30% negative
            text = random.choice(negative_feedback)
            sentiment = 'Negative'
            satisfaction = random.randint(1, 2)
        else:  # 30% neutral
            text = random.choice(neutral_feedback)
            sentiment = 'Neutral'
            satisfaction = 3
        
        data.append({
            'ticket_id': f'TICKET_{i+1:04d}',
            'text': text,
            'sentiment': sentiment,
            'department': random.choice(departments),
            'satisfaction_rating': satisfaction,
            'resolution_time_hours': random.randint(1, 72),
            'priority': random.choice(['Low', 'Medium', 'High', 'Critical']),
            'date': (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d')
        })
    
    return pd.DataFrame(data)

def create_news_headlines_dataset():
    """Create news headlines dataset"""
    
    positive_headlines = [
        "Scientists Discover Breakthrough Treatment for Rare Disease",
        "Local Community Raises $100K for Children's Hospital",
        "Unemployment Rate Drops to Lowest Level in Decade",
        "New Renewable Energy Project Powers 50,000 Homes",
        "Student Wins International Science Competition",
        "City Opens New Public Park with Free Activities",
        "Technology Company Announces 1,000 New Jobs",
        "Medical Research Shows Promising Cancer Treatment Results",
        "Local School Receives Award for Excellence in Education",
        "Environmental Initiative Successfully Cleans Up River"
    ]
    
    negative_headlines = [
        "Major Data Breach Affects Millions of Users",
        "Economic Recession Fears Grow as Markets Tumble",
        "Natural Disaster Leaves Thousands Without Power",
        "Company Announces Massive Layoffs Due to Budget Cuts",
        "Crime Rate Increases in Downtown Area",
        "Environmental Pollution Reaches Dangerous Levels",
        "Healthcare System Faces Critical Staff Shortage",
        "Transportation Strike Disrupts City Services",
        "Cyber Attack Targets Government Infrastructure",
        "Housing Crisis Worsens as Prices Continue to Rise"
    ]
    
    neutral_headlines = [
        "City Council Meets to Discuss Budget Proposals",
        "Weather Forecast Predicts Average Temperatures This Week",
        "New Traffic Light Installed at Busy Intersection",
        "Local Library Extends Operating Hours",
        "Annual Festival Planning Committee Announces Dates",
        "School District Reviews Curriculum Changes",
        "Public Transportation Schedule Updates Announced",
        "Municipal Elections Scheduled for Next Month",
        "Road Construction Project Enters Second Phase",
        "Community Center Offers New Programming Options"
    ]
    
    data = []
    categories = ['Politics', 'Technology', 'Health', 'Environment', 'Economy', 'Sports', 'Entertainment']
    
    for i in range(150):
        if i < 60:  # 40% positive
            text = random.choice(positive_headlines)
            sentiment = 'Positive'
        elif i < 105:  # 30% negative
            text = random.choice(negative_headlines)
            sentiment = 'Negative'
        else:  # 30% neutral
            text = random.choice(neutral_headlines)
            sentiment = 'Neutral'
        
        data.append({
            'headline_id': f'NEWS_{i+1:04d}',
            'text': text,
            'sentiment': sentiment,
            'category': random.choice(categories),
            'source': random.choice(['Local News', 'National News', 'Online News', 'Wire Service']),
            'publish_date': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
            'views': random.randint(1000, 100000),
            'shares': random.randint(10, 5000)
        })
    
    return pd.DataFrame(data)

def create_movie_reviews_dataset():
    """Create movie reviews dataset"""
    
    positive_reviews = [
        "Absolutely brilliant film with outstanding performances and stunning visuals!",
        "A masterpiece of cinema that will be remembered for years to come.",
        "Incredible storytelling and amazing character development throughout.",
        "Visually stunning with a compelling plot that keeps you engaged.",
        "Fantastic acting and direction make this a must-see film.",
        "One of the best movies I've seen this year. Highly recommended!",
        "Brilliant screenplay with perfect casting and excellent cinematography.",
        "A cinematic triumph that exceeds all expectations.",
        "Outstanding film with incredible attention to detail and superb acting.",
        "Absolutely loved every minute of this incredible movie experience."
    ]
    
    negative_reviews = [
        "Terrible plot with poor acting and disappointing special effects.",
        "Complete waste of time and money. Avoid this movie at all costs.",
        "Boring storyline with unconvincing performances from the entire cast.",
        "Poorly written script with terrible direction and editing.",
        "One of the worst movies I've ever seen. Completely disappointing.",
        "Awful film with no redeeming qualities whatsoever.",
        "Terrible acting and a plot that makes absolutely no sense.",
        "Disappointing sequel that ruins the legacy of the original.",
        "Poor production values and uninspired performances throughout.",
        "Completely overrated film that fails to deliver on its promises."
    ]
    
    neutral_reviews = [
        "Decent movie with some good moments but nothing exceptional.",
        "It's okay, has its moments but overall pretty average.",
        "Fair film that entertains but doesn't leave a lasting impression.",
        "Watchable movie though not particularly memorable or outstanding.",
        "Average film with standard plot and acceptable performances.",
        "It's fine for a casual watch but nothing to get excited about.",
        "Decent entertainment value though somewhat predictable storyline.",
        "Okay movie that serves its purpose but lacks wow factor.",
        "Fair film with some good elements but also some weaknesses.",
        "Standard movie that meets basic expectations without exceeding them."
    ]
    
    data = []
    genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Thriller', 'Documentary']
    
    for i in range(250):
        if i < 100:  # 40% positive
            text = random.choice(positive_reviews)
            sentiment = 'Positive'
            rating = random.uniform(3.5, 5.0)
        elif i < 175:  # 30% negative
            text = random.choice(negative_reviews)
            sentiment = 'Negative'
            rating = random.uniform(1.0, 2.5)
        else:  # 30% neutral
            text = random.choice(neutral_reviews)
            sentiment = 'Neutral'
            rating = random.uniform(2.5, 3.5)
        
        data.append({
            'review_id': f'MOVIE_{i+1:04d}',
            'text': text,
            'sentiment': sentiment,
            'genre': random.choice(genres),
            'rating': round(rating, 1),
            'reviewer_age': random.randint(18, 65),
            'review_date': (datetime.now() - timedelta(days=random.randint(1, 180))).strftime('%Y-%m-%d'),
            'helpful_votes': random.randint(0, 100)
        })
    
    return pd.DataFrame(data)

def create_url_test_dataset():
    """Create dataset with URLs for testing URL analysis feature"""
    
    urls_data = [
        {
            'url': 'https://example-news.com/positive-breakthrough',
            'title': 'Scientists Achieve Major Breakthrough in Clean Energy',
            'expected_sentiment': 'Positive',
            'content_preview': 'Researchers have successfully developed a revolutionary clean energy technology...',
            'category': 'Technology'
        },
        {
            'url': 'https://example-blog.com/negative-review',
            'title': 'Disappointing Experience with New Restaurant',
            'expected_sentiment': 'Negative',
            'content_preview': 'After hearing great things about this new restaurant, I was completely disappointed...',
            'category': 'Review'
        },
        {
            'url': 'https://example-news.com/neutral-report',
            'title': 'City Council Discusses Budget Allocation',
            'expected_sentiment': 'Neutral',
            'content_preview': 'The city council met yesterday to review the proposed budget for the upcoming fiscal year...',
            'category': 'News'
        },
        {
            'url': 'https://example-tech.com/amazing-product',
            'title': 'Revolutionary New Smartphone Features',
            'expected_sentiment': 'Positive',
            'content_preview': 'The latest smartphone release includes incredible new features that will change how we use mobile devices...',
            'category': 'Technology'
        },
        {
            'url': 'https://example-review.com/terrible-service',
            'title': 'Worst Customer Service Experience Ever',
            'expected_sentiment': 'Negative',
            'content_preview': 'I have never experienced such poor customer service in my entire life...',
            'category': 'Review'
        }
    ]
    
    return pd.DataFrame(urls_data)

def main():
    """Generate all datasets"""
    print("🔄 Generating comprehensive datasets for Universal Sentiment Analyzer...")
    
    # Create datasets
    print("📊 Creating product reviews dataset...")
    product_reviews = create_product_reviews_dataset()
    product_reviews.to_csv('data/dataset_product_reviews.csv', index=False)
    
    print("📱 Creating social media dataset...")
    social_media = create_social_media_dataset()
    social_media.to_csv('data/dataset_social_media.csv', index=False)
    
    print("🎧 Creating customer feedback dataset...")
    customer_feedback = create_customer_feedback_dataset()
    customer_feedback.to_csv('data/dataset_customer_feedback.csv', index=False)
    
    print("📰 Creating news headlines dataset...")
    news_headlines = create_news_headlines_dataset()
    news_headlines.to_csv('data/dataset_news_headlines.csv', index=False)
    
    print("🎬 Creating movie reviews dataset...")
    movie_reviews = create_movie_reviews_dataset()
    movie_reviews.to_csv('data/dataset_movie_reviews.csv', index=False)
    
    print("🌐 Creating URL test dataset...")
    url_test = create_url_test_dataset()
    url_test.to_csv('data/dataset_url_tests.csv', index=False)

    
    # Create combined dataset
    print("🔗 Creating combined dataset...")
    combined_data = []
    
    # Add samples from each dataset
    for _, row in product_reviews.head(50).iterrows():
        combined_data.append({
            'text': row['text'],
            'sentiment': row['sentiment'],
            'source': 'Product Reviews',
            'category': row['category']
        })
    
    for _, row in social_media.head(50).iterrows():
        combined_data.append({
            'text': row['text'],
            'sentiment': row['sentiment'],
            'source': 'Social Media',
            'category': row['platform']
        })
    
    for _, row in customer_feedback.head(30).iterrows():
        combined_data.append({
            'text': row['text'],
            'sentiment': row['sentiment'],
            'source': 'Customer Feedback',
            'category': row['department']
        })
    
    for _, row in news_headlines.head(30).iterrows():
        combined_data.append({
            'text': row['text'],
            'sentiment': row['sentiment'],
            'source': 'News Headlines',
            'category': row['category']
        })
    
    for _, row in movie_reviews.head(40).iterrows():
        combined_data.append({
            'text': row['text'],
            'sentiment': row['sentiment'],
            'source': 'Movie Reviews',
            'category': row['genre']
        })
    
    combined_df = pd.DataFrame(combined_data)
    combined_df.to_csv('data/dataset_combined_samples.csv', index=False)
    
    # Create summary statistics
    print("📈 Generating dataset statistics...")
    
    stats = {
        'datasets_created': 6,
        'total_samples': len(combined_df),
        'product_reviews': len(product_reviews),
        'social_media_posts': len(social_media),
        'customer_feedback': len(customer_feedback),
        'news_headlines': len(news_headlines),
        'movie_reviews': len(movie_reviews),
        'url_test_cases': len(url_test),
        'sentiment_distribution': combined_df['sentiment'].value_counts().to_dict(),
        'source_distribution': combined_df['source'].value_counts().to_dict(),
        'generated_at': datetime.now().isoformat()
    }
    
    with open('data/dataset_statistics.json', 'w') as f:
        json.dump(stats, f, indent=2)

    
    print("\n" + "="*60)
    print("✅ DATASET GENERATION COMPLETE!")
    print("="*60)
    print(f"📊 Total datasets created: {stats['datasets_created']}")
    print(f"📝 Total samples: {stats['total_samples']}")
    print("\n📁 Files created:")
    print("  • dataset_product_reviews.csv (500 samples)")
    print("  • dataset_social_media.csv (300 samples)")
    print("  • dataset_customer_feedback.csv (200 samples)")
    print("  • dataset_news_headlines.csv (150 samples)")
    print("  • dataset_movie_reviews.csv (250 samples)")
    print("  • dataset_url_tests.csv (5 test cases)")
    print("  • dataset_combined_samples.csv (200 mixed samples)")
    print("  • dataset_statistics.json (summary stats)")
    print("\n🎯 Sentiment Distribution:")
    for sentiment, count in stats['sentiment_distribution'].items():
        percentage = (count / stats['total_samples']) * 100
        print(f"  • {sentiment}: {count} ({percentage:.1f}%)")
    print("\n🚀 Ready for testing all features of your sentiment analyzer!")

if __name__ == "__main__":
    main()