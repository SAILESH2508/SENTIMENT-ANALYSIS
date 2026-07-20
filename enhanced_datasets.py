"""
Enhanced Dataset Generator with More Realistic and Diverse Data
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime, timedelta
import random

def create_realistic_datasets():
    """Create realistic datasets for all sentiment analyzer features"""
    
    # 1. E-commerce Product Reviews (Most Common Use Case)
    ecommerce_data = []
    
    # Positive reviews (40%)
    positive_reviews = [
        "Amazing product! Exceeded my expectations in every way. Fast shipping too!",
        "Love this! Great quality and exactly as described. Will buy again!",
        "Perfect! Works flawlessly and looks fantastic. Highly recommend!",
        "Outstanding quality for the price. Customer service was excellent too!",
        "Incredible value! This has made my life so much easier. 5 stars!",
        "Fantastic product with amazing build quality. Arrived quickly!",
        "Best purchase I've made this year! Absolutely love everything about it!",
        "Superb quality and great design. Worth every penny and more!",
        "Excellent product that works perfectly. Great customer support!",
        "Amazing! This product is even better than I hoped it would be!"
    ]
    
    # Negative reviews (30%)
    negative_reviews = [
        "Terrible quality! Broke after just one day of use. Complete waste of money!",
        "Worst purchase ever! Nothing like the description. Requesting refund immediately!",
        "Poor quality materials and shoddy construction. Very disappointed!",
        "Overpriced junk! Product arrived damaged and customer service is unhelpful!",
        "Complete garbage! Doesn't work as advertised. Save your money!",
        "Horrible experience! Product is defective and return process is nightmare!",
        "Cheap quality that falls apart immediately. Not worth any price!",
        "Misleading description and terrible quality. Avoid this seller!",
        "Awful product with zero quality control. Very frustrated with purchase!",
        "Completely useless! Product doesn't do what it claims to do!"
    ]
    
    # Neutral reviews (30%)
    neutral_reviews = [
        "It's okay, does the job but nothing special. Average quality for the price.",
        "Decent product with some good points and some bad ones. Fair overall.",
        "Works as expected though not particularly impressive. It's fine.",
        "Average quality and performance. Could be better but not terrible.",
        "It's alright, serves its purpose but lacks wow factor. Standard product.",
        "Fair product that meets basic expectations without exceeding them.",
        "Reasonable quality for the price point. Nothing more, nothing less.",
        "It works but there are probably better options available elsewhere.",
        "Acceptable product with average performance. Does what it says.",
        "Mediocre quality but functional. Not amazing but not awful either."
    ]
    
    categories = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Sports', 'Beauty', 'Toys']
    
    for i in range(600):
        if i < 240:  # 40% positive
            text = random.choice(positive_reviews)
            sentiment = 'Positive'
            rating = random.randint(4, 5)
        elif i < 420:  # 30% negative
            text = random.choice(negative_reviews)
            sentiment = 'Negative'
            rating = random.randint(1, 2)
        else:  # 30% neutral
            text = random.choice(neutral_reviews)
            sentiment = 'Neutral'
            rating = 3
        
        ecommerce_data.append({
            'text': text,
            'sentiment': sentiment,
            'rating': rating,
            'category': random.choice(categories),
            'verified_purchase': random.choice([True, False]),
            'helpful_votes': random.randint(0, 100),
            'price_range': random.choice(['$0-25', '$25-50', '$50-100', '$100+'])
        })
    
    # 2. Social Media Posts Dataset
    social_data = []
    
    # Social media positive posts
    social_positive = [
        "Just had the most amazing day at the beach! Life is beautiful! 🌊☀️ #blessed",
        "Finished my first 5K run today! Feeling so accomplished! 🏃‍♀️ #fitness #goals",
        "This new coffee shop has the best latte I've ever tasted! ☕ #coffeelover",
        "Beautiful sunset tonight! Nature never fails to amaze me 🌅 #grateful #photography",
        "Got the job I interviewed for! Dreams do come true! 🎉 #career #success",
        "Amazing concert last night! The energy was incredible! 🎵 #music #liveshow",
        "Perfect weather for a picnic in the park with friends! 🌞 #friendship #outdoors",
        "Just adopted the sweetest rescue dog! My heart is so full ❤️ 🐶 #rescue #love",
        "Loving this new book series! Can't put it down! 📚 #reading #bookworm",
        "Best vacation ever! The mountains here are breathtaking! 🏔️ #travel #adventure"
    ]
    
    # Social media negative posts
    social_negative = [
        "Stuck in traffic for 3 hours because of construction! So frustrated! 😤 #traffic",
        "My flight got delayed again! Worst airline experience ever! ✈️ #travel #angry",
        "Phone died right before important meeting. Technology fails when you need it most! 📱 #frustrated",
        "Terrible service at this restaurant. Waited 2 hours for cold food! 😠 #disappointed",
        "Rain completely ruined our outdoor wedding plans. Heartbroken! 😢 #wedding #disaster",
        "Lost my keys and locked out of my apartment. Could this day get worse? 🔑 #badday",
        "This movie was a complete waste of 3 hours of my life! 🎬 #terrible #regret",
        "Customer service hung up on me three times today! Absolutely ridiculous! 📞 #angry",
        "My car broke down in the middle of nowhere. Having the worst luck! 🚗 #stranded",
        "Food poisoning from that new restaurant. Never eating there again! 🤢 #sick"
    ]
    
    # Social media neutral posts
    social_neutral = [
        "Just finished grocery shopping for the week. Standard Sunday routine 🛒 #weekend",
        "Weather is pretty average today. Not too hot, not too cold 🌤️ #weather",
        "Watching Netflix after work. Nothing exciting planned tonight 📺 #relaxing",
        "Had lunch at the usual spot downtown. Same as always 🍽️ #lunch #routine",
        "Commute was normal today. No delays or major issues 🚌 #commute #work",
        "Finished that book I was reading. It was okay, nothing special 📖 #reading",
        "Went for my regular evening walk around the neighborhood 🚶‍♀️ #exercise",
        "Standard workout at the gym today. Keeping up with routine 💪 #fitness",
        "Team meeting went as expected. Covered the usual topics 💼 #work #meeting",
        "Made pasta for dinner tonight. Simple and satisfying 🍝 #cooking #dinner"
    ]
    
    platforms = ['Twitter', 'Facebook', 'Instagram', 'LinkedIn', 'TikTok', 'Reddit']
    
    for i in range(400):
        if i < 160:  # 40% positive
            text = random.choice(social_positive)
            sentiment = 'Positive'
            engagement = random.randint(50, 1000)
        elif i < 280:  # 30% negative
            text = random.choice(social_negative)
            sentiment = 'Negative'
            engagement = random.randint(20, 500)
        else:  # 30% neutral
            text = random.choice(social_neutral)
            sentiment = 'Neutral'
            engagement = random.randint(5, 200)
        
        social_data.append({
            'text': text,
            'sentiment': sentiment,
            'platform': random.choice(platforms),
            'likes': random.randint(0, engagement),
            'shares': random.randint(0, engagement//5),
            'comments': random.randint(0, engagement//10),
            'hashtags': random.randint(0, 5),
            'time_of_day': random.choice(['Morning', 'Afternoon', 'Evening', 'Night'])
        })
    
    # 3. Customer Service Feedback
    service_data = []
    
    service_positive = [
        "Outstanding customer service! The representative was knowledgeable and solved my issue in minutes.",
        "Excellent support team! They went above and beyond to help me with my problem.",
        "Quick response and professional service. Couldn't be happier with the experience!",
        "Amazing customer service! Patient, helpful, and resolved everything perfectly.",
        "Best support experience I've ever had! The team was incredibly helpful and friendly.",
        "Fantastic service! They made a complicated issue seem simple to resolve.",
        "Wonderful customer support! Professional, courteous, and very efficient.",
        "Exceptional service quality! The representative was expert and very patient.",
        "Outstanding help from the support team! They exceeded all my expectations.",
        "Perfect customer service experience! Quick, professional, and very effective."
    ]
    
    service_negative = [
        "Terrible customer service! Waited 2 hours on hold just to be transferred again.",
        "Worst support experience ever! Rude staff and no resolution to my problem.",
        "Completely unhelpful customer service! They made my issue even worse.",
        "Awful experience! Multiple calls with different representatives and still no solution.",
        "Horrible customer support! Unprofessional and clearly don't know their products.",
        "Terrible service! Long wait times and staff who seem annoyed to help.",
        "Worst customer service department! Transferred me 5 times with no resolution.",
        "Completely disappointed! Rude representatives and incorrect information provided.",
        "Awful support experience! They hung up on me twice during the call.",
        "Terrible customer service! No one seems to know how to solve basic problems."
    ]
    
    service_neutral = [
        "Standard customer service experience. Got my issue resolved but took a while.",
        "Average support quality. The representative was polite but not particularly helpful.",
        "Okay service overall. They solved my problem but the process could be better.",
        "Fair customer service experience. Met basic expectations without exceeding them.",
        "Decent support but nothing exceptional. Issue was resolved eventually.",
        "Average experience with customer service. Could be more efficient but it's fine.",
        "Standard service level. The representative was adequate and resolved the issue.",
        "Okay customer support. Not great but not terrible either. Got what I needed.",
        "Fair service experience. Process was a bit slow but they did help in the end.",
        "Average customer service quality. Nothing to complain about but nothing special."
    ]
    
    departments = ['Technical Support', 'Billing', 'Sales', 'Returns', 'General Inquiry']
    
    for i in range(300):
        if i < 120:  # 40% positive
            text = random.choice(service_positive)
            sentiment = 'Positive'
            satisfaction = random.randint(4, 5)
        elif i < 210:  # 30% negative
            text = random.choice(service_negative)
            sentiment = 'Negative'
            satisfaction = random.randint(1, 2)
        else:  # 30% neutral
            text = random.choice(service_neutral)
            sentiment = 'Neutral'
            satisfaction = 3
        
        service_data.append({
            'text': text,
            'sentiment': sentiment,
            'department': random.choice(departments),
            'satisfaction_rating': satisfaction,
            'resolution_time_minutes': random.randint(5, 180),
            'call_transfers': random.randint(0, 5),
            'issue_type': random.choice(['Technical', 'Billing', 'Product', 'Account', 'Other'])
        })
    
    # 4. News and Media Headlines
    news_data = []
    
    news_positive = [
        "Scientists Discover Revolutionary Treatment for Alzheimer's Disease",
        "Local Community Raises Record $500K for Children's Hospital",
        "Unemployment Drops to Historic Low as Economy Continues Strong Growth",
        "Breakthrough in Renewable Energy Could Power Entire Cities Cleanly",
        "Young Entrepreneur's Innovation Helps Solve Global Water Crisis",
        "New Medical Research Shows 90% Success Rate in Cancer Treatment",
        "City Opens Largest Public Park in Decades with Free Family Activities",
        "Technology Startup Creates 2,000 High-Paying Jobs in Local Area",
        "Environmental Cleanup Project Successfully Restores Polluted Lake",
        "Education Initiative Dramatically Improves Student Performance Rates"
    ]
    
    news_negative = [
        "Major Cyber Attack Compromises Personal Data of 10 Million Users",
        "Economic Downturn Forces Closure of Historic Local Businesses",
        "Severe Weather System Causes Widespread Power Outages and Damage",
        "Healthcare Crisis Deepens as Hospital Staff Shortages Reach Critical Level",
        "Environmental Disaster Threatens Local Wildlife and Water Supply",
        "Rising Crime Rates Prompt Increased Security Measures Downtown",
        "Transportation Strike Leaves Thousands Stranded During Rush Hour",
        "Housing Market Crash Leaves Many Families Facing Foreclosure",
        "Factory Explosion Injures Dozens and Raises Safety Concerns",
        "Budget Cuts Force School District to Eliminate Essential Programs"
    ]
    
    news_neutral = [
        "City Council Schedules Public Hearing on Proposed Budget Changes",
        "Weather Service Predicts Average Temperatures for Upcoming Season",
        "New Traffic Management System Installed at Major Intersection",
        "Public Library Announces Extended Hours and New Digital Services",
        "Annual Community Festival Planning Committee Releases Event Schedule",
        "School Board Reviews Updated Curriculum Standards for Next Year",
        "Municipal Elections Set for November with Several Contested Races",
        "Road Construction Project Moves into Final Phase of Completion",
        "Local Government Offices Transition to New Digital Filing System",
        "Community Center Expands Programming to Include Senior Activities"
    ]
    
    categories = ['Politics', 'Technology', 'Health', 'Environment', 'Economy', 'Education', 'Local']
    
    for i in range(200):
        if i < 80:  # 40% positive
            text = random.choice(news_positive)
            sentiment = 'Positive'
        elif i < 140:  # 30% negative
            text = random.choice(news_negative)
            sentiment = 'Negative'
        else:  # 30% neutral
            text = random.choice(news_neutral)
            sentiment = 'Neutral'
        
        news_data.append({
            'text': text,
            'sentiment': sentiment,
            'category': random.choice(categories),
            'source': random.choice(['Local News', 'National News', 'Online Media', 'Wire Service']),
            'word_count': random.randint(50, 500),
            'shares': random.randint(10, 10000),
            'publication_date': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
        })
    
    # 5. App Store Reviews
    app_data = []
    
    app_positive = [
        "Love this app! Super intuitive interface and works perfectly every time!",
        "Amazing app with great features! Makes my daily tasks so much easier!",
        "Perfect app! Clean design, fast performance, and excellent functionality!",
        "Outstanding app that does exactly what it promises! Highly recommend!",
        "Fantastic user experience! This app has become essential to my routine!",
        "Brilliant app with incredible attention to detail! Worth every penny!",
        "Excellent app that works flawlessly! Great customer support too!",
        "Amazing functionality and beautiful design! This app is a game changer!",
        "Perfect execution and great features! Best app I've downloaded this year!",
        "Incredible app that exceeds expectations! Simple yet powerful interface!"
    ]
    
    app_negative = [
        "Terrible app! Crashes constantly and loses all my data every time!",
        "Worst app ever! Doesn't work as advertised and customer support is useless!",
        "Horrible user experience! Confusing interface and full of bugs!",
        "Complete waste of money! App is slow, buggy, and completely unreliable!",
        "Awful app that never works properly! Constant crashes and data loss!",
        "Terrible design and even worse functionality! Avoid this app completely!",
        "Horrible performance and crashes every few minutes! Very frustrating!",
        "Worst app I've ever used! Nothing works and support doesn't respond!",
        "Completely broken app! Loses progress and crashes during important tasks!",
        "Terrible experience! App is full of bugs and completely unreliable!"
    ]
    
    app_neutral = [
        "Decent app that does the basics but could use some improvements.",
        "It's okay, works as expected but nothing particularly impressive.",
        "Fair app with standard features. Gets the job done adequately.",
        "Average app that meets basic needs but lacks advanced features.",
        "It works fine but the interface could be more user-friendly.",
        "Reasonable app for the price. Does what it says but nothing more.",
        "Standard functionality with average performance. It's acceptable.",
        "Okay app that serves its purpose but could be more polished.",
        "Fair quality app with room for improvement in several areas.",
        "Decent app overall but there are better alternatives available."
    ]
    
    app_categories = ['Productivity', 'Games', 'Social', 'Utilities', 'Entertainment', 'Education', 'Health']
    
    for i in range(350):
        if i < 140:  # 40% positive
            text = random.choice(app_positive)
            sentiment = 'Positive'
            rating = random.randint(4, 5)
        elif i < 245:  # 30% negative
            text = random.choice(app_negative)
            sentiment = 'Negative'
            rating = random.randint(1, 2)
        else:  # 30% neutral
            text = random.choice(app_neutral)
            sentiment = 'Neutral'
            rating = 3
        
        app_data.append({
            'text': text,
            'sentiment': sentiment,
            'app_category': random.choice(app_categories),
            'rating': rating,
            'app_version': f"{random.randint(1,5)}.{random.randint(0,9)}.{random.randint(0,9)}",
            'device_type': random.choice(['iPhone', 'Android', 'iPad', 'Tablet']),
            'review_length': len(text),
            'helpful_votes': random.randint(0, 50)
        })
    
    return {
        'ecommerce': pd.DataFrame(ecommerce_data),
        'social_media': pd.DataFrame(social_data),
        'customer_service': pd.DataFrame(service_data),
        'news_media': pd.DataFrame(news_data),
        'app_reviews': pd.DataFrame(app_data)
    }

def create_test_urls_dataset():
    """Create realistic URLs for testing URL analysis feature"""
    
    test_urls = [
        {
            'url': 'https://techcrunch.com/positive-startup-news',
            'title': 'Local Startup Raises $50M to Revolutionize Clean Energy',
            'expected_sentiment': 'Positive',
            'content_type': 'News Article',
            'domain': 'Technology News'
        },
        {
            'url': 'https://yelp.com/restaurant-negative-review',
            'title': 'Terrible Experience at Downtown Restaurant',
            'expected_sentiment': 'Negative',
            'content_type': 'Review',
            'domain': 'Restaurant Review'
        },
        {
            'url': 'https://wikipedia.org/neutral-topic-article',
            'title': 'History of Municipal Government Structure',
            'expected_sentiment': 'Neutral',
            'content_type': 'Encyclopedia',
            'domain': 'Educational'
        },
        {
            'url': 'https://amazon.com/product-amazing-review',
            'title': 'Best Product Purchase of the Year!',
            'expected_sentiment': 'Positive',
            'content_type': 'Product Review',
            'domain': 'E-commerce'
        },
        {
            'url': 'https://reddit.com/complaints-thread',
            'title': 'Worst Customer Service Experience Thread',
            'expected_sentiment': 'Negative',
            'content_type': 'Forum Discussion',
            'domain': 'Social Media'
        },
        {
            'url': 'https://cnn.com/breaking-news-update',
            'title': 'City Council Approves New Budget Proposal',
            'expected_sentiment': 'Neutral',
            'content_type': 'News Report',
            'domain': 'News Media'
        },
        {
            'url': 'https://medium.com/success-story-blog',
            'title': 'How I Built My Dream Business from Scratch',
            'expected_sentiment': 'Positive',
            'content_type': 'Blog Post',
            'domain': 'Business'
        },
        {
            'url': 'https://glassdoor.com/company-terrible-review',
            'title': 'Toxic Work Environment and Poor Management',
            'expected_sentiment': 'Negative',
            'content_type': 'Company Review',
            'domain': 'Employment'
        }
    ]
    
    return pd.DataFrame(test_urls)

def main():
    """Generate all enhanced datasets"""
    print("🚀 Generating Enhanced Datasets for Universal Sentiment Analyzer Pro")
    print("="*70)
    
    # Generate main datasets
    print("📊 Creating realistic datasets...")
    datasets = create_realistic_datasets()
    
    # Save individual datasets
    print("💾 Saving datasets to files...")
    
    datasets['ecommerce'].to_csv('data/dataset_ecommerce_reviews.csv', index=False)
    print(f"  ✅ E-commerce Reviews: {len(datasets['ecommerce'])} samples")
    
    datasets['social_media'].to_csv('data/dataset_social_media_posts.csv', index=False)
    print(f"  ✅ Social Media Posts: {len(datasets['social_media'])} samples")
    
    datasets['customer_service'].to_csv('data/dataset_customer_service.csv', index=False)
    print(f"  ✅ Customer Service: {len(datasets['customer_service'])} samples")
    
    datasets['news_media'].to_csv('data/dataset_news_media.csv', index=False)
    print(f"  ✅ News & Media: {len(datasets['news_media'])} samples")
    
    datasets['app_reviews'].to_csv('data/dataset_app_reviews.csv', index=False)
    print(f"  ✅ App Reviews: {len(datasets['app_reviews'])} samples")

    
    # Create URL test dataset
    url_tests = create_test_urls_dataset()
    url_tests.to_csv('data/dataset_url_test_cases.csv', index=False)
    print(f"  ✅ URL Test Cases: {len(url_tests)} samples")

    
    # Create combined sample dataset for quick testing
    print("🔗 Creating combined sample dataset...")
    combined_samples = []
    
    # Take samples from each dataset
    for name, df in datasets.items():
        sample_size = min(50, len(df))
        sample = df.sample(n=sample_size, random_state=42)
        for _, row in sample.iterrows():
            combined_samples.append({
                'text': row['text'],
                'sentiment': row['sentiment'],
                'source': name.replace('_', ' ').title(),
                'category': row.get('category', row.get('app_category', row.get('department', 'General')))
            })
    
    combined_df = pd.DataFrame(combined_samples)
    combined_df.to_csv('data/dataset_mixed_samples.csv', index=False)
    print(f"  ✅ Mixed Samples: {len(combined_df)} samples")

    
    # Generate comprehensive statistics
    print("📈 Generating statistics...")
    
    total_samples = sum(len(df) for df in datasets.values())
    
    # Calculate sentiment distribution across all datasets
    all_sentiments = []
    for df in datasets.values():
        all_sentiments.extend(df['sentiment'].tolist())
    
    sentiment_counts = pd.Series(all_sentiments).value_counts()
    
    stats = {
        'generation_info': {
            'total_datasets': len(datasets) + 2,  # +2 for URL tests and combined
            'total_samples': total_samples,
            'generated_at': datetime.now().isoformat(),
            'generator_version': '2.0'
        },
        'dataset_breakdown': {
            'ecommerce_reviews': len(datasets['ecommerce']),
            'social_media_posts': len(datasets['social_media']),
            'customer_service_feedback': len(datasets['customer_service']),
            'news_media_headlines': len(datasets['news_media']),
            'app_store_reviews': len(datasets['app_reviews']),
            'url_test_cases': len(url_tests),
            'mixed_samples': len(combined_df)
        },
        'sentiment_distribution': {
            'positive': int(sentiment_counts.get('Positive', 0)),
            'negative': int(sentiment_counts.get('Negative', 0)),
            'neutral': int(sentiment_counts.get('Neutral', 0)),
            'positive_percentage': round((sentiment_counts.get('Positive', 0) / len(all_sentiments)) * 100, 1),
            'negative_percentage': round((sentiment_counts.get('Negative', 0) / len(all_sentiments)) * 100, 1),
            'neutral_percentage': round((sentiment_counts.get('Neutral', 0) / len(all_sentiments)) * 100, 1)
        },
        'quality_metrics': {
            'average_text_length': round(np.mean([len(text) for text in all_sentiments]), 1),
            'text_length_range': {
                'min': min(len(text) for text in [df['text'].iloc[0] for df in datasets.values()]),
                'max': max(len(text) for text in [df['text'].iloc[0] for df in datasets.values()])
            },
            'balanced_distribution': bool(abs(sentiment_counts.get('Positive', 0) - sentiment_counts.get('Negative', 0)) < (len(all_sentiments) * 0.1))
        }
    }
    
    # Save statistics
    with open('data/enhanced_dataset_statistics.json', 'w') as f:
        json.dump(stats, f, indent=2)

    
    # Print summary
    print("\n" + "="*70)
    print("🎉 ENHANCED DATASET GENERATION COMPLETE!")
    print("="*70)
    
    print(f"\n📊 SUMMARY:")
    print(f"  • Total Datasets: {stats['generation_info']['total_datasets']}")
    print(f"  • Total Samples: {stats['generation_info']['total_samples']:,}")
    print(f"  • Generation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print(f"\n📁 DATASET FILES CREATED:")
    for name, count in stats['dataset_breakdown'].items():
        filename = f"dataset_{name}.csv"
        print(f"  • {filename:<35} {count:>6} samples")
    
    print(f"\n🎯 SENTIMENT DISTRIBUTION:")
    dist = stats['sentiment_distribution']
    print(f"  • Positive: {dist['positive']:>6} ({dist['positive_percentage']:>5.1f}%)")
    print(f"  • Negative: {dist['negative']:>6} ({dist['negative_percentage']:>5.1f}%)")
    print(f"  • Neutral:  {dist['neutral']:>6} ({dist['neutral_percentage']:>5.1f}%)")
    
    print(f"\n✨ QUALITY METRICS:")
    print(f"  • Balanced Distribution: {'✅ Yes' if stats['quality_metrics']['balanced_distribution'] else '❌ No'}")
    print(f"  • Average Text Length: {stats['quality_metrics']['average_text_length']} characters")
    
    print(f"\n🚀 READY FOR TESTING:")
    print("  • Single Text Analysis: Use any individual samples")
    print("  • Batch Analysis: Upload any CSV file")
    print("  • URL Analysis: Use dataset_url_test_cases.csv")
    print("  • Analytics Dashboard: Perform multiple analyses")
    print("  • Mixed Testing: Use dataset_mixed_samples.csv")
    
    print(f"\n💡 USAGE TIPS:")
    print("  • Start with dataset_mixed_samples.csv for quick testing")
    print("  • Use specific datasets for domain-focused analysis")
    print("  • URL test cases include expected sentiment for validation")
    print("  • All datasets have realistic, diverse content")
    
    print("\n🎊 Your sentiment analyzer now has comprehensive test data!")

if __name__ == "__main__":
    main()