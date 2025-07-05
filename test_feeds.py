import feedparser
import requests
from datetime import datetime

# Comprehensive list of potential RSS feeds for startup/tech news
TEST_FEEDS = {
    # Major Tech News
    'TechCrunch': 'https://techcrunch.com/feed/',
    'VentureBeat': 'https://venturebeat.com/feed/',
    'The Verge': 'https://www.theverge.com/rss/index.xml',
    'Ars Technica': 'https://feeds.arstechnica.com/arstechnica/index',
    'Wired': 'https://www.wired.com/feed/rss',
    'Engadget': 'https://www.engadget.com/rss.xml',
    'TechRadar': 'https://www.techradar.com/rss',
    'ZDNet': 'https://www.zdnet.com/news/rss.xml',
    'Mashable Tech': 'https://mashable.com/feeds/rss/tech',
    
    # Startup/Business Focused
    'Entrepreneur': 'https://www.entrepreneur.com/latest.rss',
    'Inc.com': 'https://www.inc.com/rss.xml',
    'Fast Company': 'https://www.fastcompany.com/latest/rss',
    'Business Insider Tech': 'https://www.businessinsider.com/rss',
    'Forbes Technology': 'https://www.forbes.com/innovation/feed2/',
    'Crunchbase News': 'https://news.crunchbase.com/feed/',
    
    # University/Research
    'MIT News': 'https://news.mit.edu/rss/feed',
    'Stanford News': 'https://news.stanford.edu/feed/',
    'Berkeley News': 'https://news.berkeley.edu/feed/',
    'Harvard Innovation Labs': 'https://innovationlabs.harvard.edu/feed/',
    'Carnegie Mellon': 'https://www.cmu.edu/news/rss/news.xml',
    
    # Product/Startup Discovery
    'Product Hunt': 'https://www.producthunt.com/feed',
    'Hacker News': 'https://hnrss.org/newest',
    'AngelList': 'https://angel.co/feed',
    'Y Combinator': 'https://www.ycombinator.com/blog/feed',
    
    # Industry Specific
    'AI News': 'https://artificialintelligence-news.com/feed/',
    'VentureFizz': 'https://venturefizz.com/feed',
    'TechStars Blog': 'https://www.techstars.com/blog/feed',
    '500 Startups': 'https://500.co/blog/feed/',
    'First Round Review': 'https://review.firstround.com/rss',
    'a16z': 'https://a16z.com/feed/',
    
    # Alternative sources
    'Silicon Valley Business Journal': 'https://www.bizjournals.com/sanjose/feeds/news.xml',
    'GeekWire': 'https://www.geekwire.com/feed/',
    'TechCrunch Startups': 'https://techcrunch.com/category/startups/feed/',
    'Startup Grind': 'https://startupgrind.com/feed/',
}

def test_rss_feed(name, url):
    """Test if an RSS feed is working and return sample data"""
    try:
        # Test with requests first
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None, f"HTTP {response.status_code}"
        
        # Parse with feedparser
        feed = feedparser.parse(url)
        
        if not feed.entries:
            return None, "No entries found"
        
        # Check if feed has required fields
        first_entry = feed.entries[0]
        title = first_entry.get('title', 'No title')
        summary = first_entry.get('summary', 'No summary')
        
        return {
            'title': feed.feed.get('title', name),
            'entries_count': len(feed.entries),
            'sample_title': title[:100],
            'sample_summary': summary[:100] if summary else 'No summary',
            'has_dates': bool(first_entry.get('published_parsed') or first_entry.get('updated_parsed'))
        }, None
        
    except Exception as e:
        return None, str(e)

def main():
    print("Testing RSS Feeds for StartupSignal")
    print("=" * 50)
    
    working_feeds = {}
    failed_feeds = {}
    
    for name, url in TEST_FEEDS.items():
        print(f"Testing {name}... ", end="")
        
        result, error = test_rss_feed(name, url)
        
        if result:
            print(f"✅ Working ({result['entries_count']} entries)")
            working_feeds[name] = {
                'url': url,
                'info': result
            }
        else:
            print(f"❌ Failed: {error}")
            failed_feeds[name] = error
    
    print("\n" + "=" * 50)
    print(f"Working feeds: {len(working_feeds)}")
    print(f"Failed feeds: {len(failed_feeds)}")
    
    print("\n📊 WORKING FEEDS:")
    for name, data in working_feeds.items():
        info = data['info']
        print(f"  ✅ {name}")
        print(f"     URL: {data['url']}")
        print(f"     Entries: {info['entries_count']}")
        print(f"     Sample: {info['sample_title']}")
        print()
    
    # Generate updated config
    print("=" * 50)
    print("UPDATED RSS_SOURCES for config.py:")
    print("RSS_SOURCES = {")
    for name, data in working_feeds.items():
        print(f"    '{name}': '{data['url']}',")
    print("}")
    
    return working_feeds

if __name__ == "__main__":
    working_feeds = main()
