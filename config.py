# Configuration file for StartupSignal

# Additional startup keywords to detect
CUSTOM_KEYWORDS = [
    'pre-ipo', 'late stage', 'growth equity', 'private equity',
    'venture debt', 'convertible note', 'safe note', 'revenue share',
    'bootstrapped', 'profitable', 'break-even', 'cash flow positive',
    'market leader', 'disrupting', 'innovative', 'cutting edge',
    'patent pending', 'intellectual property', 'trade secret',
    'b2b', 'b2c', 'b2b2c', 'saas', 'paas', 'iaas',
    'freemium', 'subscription', 'recurring revenue', 'arr', 'mrr',
    'customer acquisition', 'product-market fit', 'scaling',
    'go-to-market', 'gtm', 'channel partner', 'strategic partnership'
]

# Region detection patterns
REGION_PATTERNS = {
    'Silicon Valley': ['silicon valley', 'san francisco', 'bay area', 'palo alto', 'mountain view', 'menlo park'],
    'New York': ['new york', 'nyc', 'manhattan', 'brooklyn', 'queens'],
    'Boston': ['boston', 'cambridge', 'mit', 'harvard', 'massachusetts'],
    'London': ['london', 'uk', 'england', 'united kingdom'],
    'Tel Aviv': ['tel aviv', 'israel', 'jerusalem'],
    'Berlin': ['berlin', 'germany', 'munich'],
    'Paris': ['paris', 'france'],
    'Toronto': ['toronto', 'canada', 'vancouver'],
    'Singapore': ['singapore', 'asia pacific'],
    'Austin': ['austin', 'texas', 'dallas'],
    'Seattle': ['seattle', 'washington', 'redmond'],
    'Los Angeles': ['los angeles', 'la', 'california', 'santa monica'],
    'Chicago': ['chicago', 'illinois'],
    'Miami': ['miami', 'florida'],
    'Amsterdam': ['amsterdam', 'netherlands', 'holland'],
    'Stockholm': ['stockholm', 'sweden', 'nordic'],
    'Bangalore': ['bangalore', 'india', 'mumbai', 'delhi'],
    'Sydney': ['sydney', 'australia', 'melbourne']
}

# Sector detection patterns
SECTOR_PATTERNS = {
    'AI/ML': ['ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning', 'neural network', 'nlp', 'computer vision'],
    'FinTech': ['fintech', 'financial', 'banking', 'payment', 'cryptocurrency', 'blockchain', 'defi', 'regtech', 'insurtech'],
    'HealthTech': ['health', 'medical', 'biotech', 'pharma', 'telemedicine', 'digital health', 'medtech', 'therapeutics'],
    'EdTech': ['education', 'edtech', 'learning', 'e-learning', 'online education', 'mooc', 'lms'],
    'E-commerce': ['e-commerce', 'ecommerce', 'online retail', 'marketplace', 'dropshipping', 'fulfillment'],
    'SaaS': ['saas', 'software', 'platform', 'cloud', 'enterprise software', 'productivity'],
    'Hardware': ['hardware', 'iot', 'robotics', 'semiconductor', 'electronics', 'manufacturing'],
    'Gaming': ['gaming', 'esports', 'mobile games', 'console', 'vr', 'ar', 'virtual reality'],
    'Media': ['media', 'content', 'streaming', 'entertainment', 'publishing', 'social media'],
    'Transportation': ['transportation', 'mobility', 'autonomous', 'electric vehicle', 'logistics', 'delivery'],
    'Energy': ['energy', 'cleantech', 'renewable', 'solar', 'wind', 'battery', 'sustainable'],
    'Real Estate': ['proptech', 'real estate', 'property', 'construction', 'smart building'],
    'Agriculture': ['agtech', 'agriculture', 'farming', 'food tech', 'precision agriculture'],
    'Space': ['space', 'satellite', 'aerospace', 'space tech', 'orbital'],
    'Cybersecurity': ['cybersecurity', 'security', 'privacy', 'encryption', 'firewall', 'threat detection'],
    'Developer Tools': ['developer tools', 'devtools', 'api', 'infrastructure', 'devops', 'cicd']
}

# RSS feed sources (verified working)
RSS_SOURCES = {
    'TechCrunch': 'https://techcrunch.com/feed/',
    'VentureBeat': 'https://venturebeat.com/feed/',
    'The Verge': 'https://www.theverge.com/rss/index.xml',
    'Ars Technica': 'https://feeds.arstechnica.com/arstechnica/index',
    'Wired': 'https://www.wired.com/feed/rss',
    'Engadget': 'https://www.engadget.com/rss.xml',
    'TechRadar': 'https://www.techradar.com/rss',
    'ZDNet': 'https://www.zdnet.com/news/rss.xml',
    'Mashable Tech': 'https://mashable.com/feeds/rss/tech',
    'Entrepreneur': 'https://www.entrepreneur.com/latest.rss',
    'Fast Company': 'https://www.fastcompany.com/latest/rss',
    'Business Insider Tech': 'https://www.businessinsider.com/rss',
    'Forbes Technology': 'https://www.forbes.com/innovation/feed2/',
    'MIT News': 'https://news.mit.edu/rss/feed',
    'Stanford News': 'https://news.stanford.edu/feed/',
    'Hacker News': 'https://hnrss.org/newest',
    'Y Combinator': 'https://www.ycombinator.com/blog/feed',
    'AI News': 'https://artificialintelligence-news.com/feed/',
    'TechCrunch Startups': 'https://techcrunch.com/category/startups/feed/',
}

# Signal scoring weights
SIGNAL_WEIGHTS = {
    'funding_keywords': 3,  # seed, series a, etc.
    'launch_keywords': 2,   # launch, founded, etc.
    'business_keywords': 2, # acquisition, ipo, etc.
    'tech_keywords': 1,     # ai, blockchain, etc.
    'source_credibility': {
        'TechCrunch': 1.8,
        'TechCrunch Startups': 2.0,
        'VentureBeat': 1.6,
        'Y Combinator': 2.0,
        'MIT News': 1.7,
        'Stanford News': 1.7,
        'Entrepreneur': 1.5,
        'Fast Company': 1.4,
        'Business Insider Tech': 1.3,
        'Forbes Technology': 1.4,
        'AI News': 1.3,
        'Hacker News': 1.2,
        'The Verge': 1.2,
        'Ars Technica': 1.2,
        'Wired': 1.1,
        'Engadget': 1.1,
        'TechRadar': 1.1,
        'ZDNet': 1.1,
        'Mashable Tech': 1.0,
        'SEC EDGAR': 2.0,
        'University News': 1.4,
        'Full Article': 1.1
    }
}

# Scraping settings
SCRAPING_SETTINGS = {
    'request_timeout': 30,
    'retry_attempts': 3,
    'delay_between_requests': 1,
    'max_articles_per_source': 50,
    'user_agent': 'StartupSignal/1.0 (Educational Research Tool)'
}
