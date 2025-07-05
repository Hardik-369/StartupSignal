import feedparser
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from newspaper import Article
import pandas as pd
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time

class StartupSignalScraper:
    def __init__(self):
        self.session = HTMLSession()
        self.startup_keywords = [
            'seed round', 'series a', 'series b', 'funding round', 'venture capital',
            'stealth startup', 'stealth mode', 'new startup', 'launch', 'founded',
            'pre-seed', 'angel investment', 'incubator', 'accelerator', 'pivot',
            'startup announces', 'emerging company', 'tech startup', 'fintech startup',
            'biotech startup', 'ai startup', 'machine learning startup', 'blockchain startup',
            'cryptocurrency startup', 'healthtech startup', 'edtech startup', 'proptech startup',
            'acquired by', 'acquisition', 'merger', 'ipo', 'going public', 'spac',
            'unicorn', 'decacorn', 'valuation', 'pre-revenue', 'mvp', 'beta launch',
            'product launch', 'soft launch', 'stealth', 'coming out of stealth'
        ]
        
        self.rss_sources = {
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
        
        self.accelerator_urls = [
            'https://www.ycombinator.com/companies',
            'https://techstars.com/portfolio',
            'https://www.500.co/portfolio',
        ]

    def scrape_rss_feeds(self, days_back: int = 7) -> List[Dict]:
        """Scrape RSS feeds for startup signals"""
        signals = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        for source_name, feed_url in self.rss_sources.items():
            try:
                print(f"  Scraping {source_name}...")
                # Set user agent and timeout for feedparser
                import socket
                socket.setdefaulttimeout(10)
                
                feed = feedparser.parse(feed_url)
                
                if not feed.entries:
                    print(f"    No entries found for {source_name}")
                    continue
                
                # Limit entries per source for performance
                entries_to_process = feed.entries[:50]  # Max 50 entries per source
                signals_found = 0
                
                for entry in entries_to_process:
                    # Parse publish date
                    try:
                        if hasattr(entry, 'published_parsed'):
                            pub_date = datetime(*entry.published_parsed[:6])
                        elif hasattr(entry, 'updated_parsed'):
                            pub_date = datetime(*entry.updated_parsed[:6])
                        else:
                            pub_date = datetime.now()
                    except:
                        pub_date = datetime.now()
                    
                    # Skip if too old
                    if pub_date < cutoff_date:
                        continue
                    
                    # Extract text content
                    content = entry.get('summary', '') + ' ' + entry.get('title', '')
                    
                    # Check for startup keywords
                    matching_keywords = self._find_startup_keywords(content)
                    
                    if matching_keywords:
                        signal = {
                            'title': entry.get('title', 'No title'),
                            'source': source_name,
                            'url': entry.get('link', ''),
                            'summary': entry.get('summary', ''),
                            'publish_date': pub_date,
                            'keywords': matching_keywords,
                            'signal_score': len(matching_keywords),
                            'content_type': 'RSS Feed'
                        }
                        signals.append(signal)
                        signals_found += 1
                        
                print(f"    Found {signals_found} signals from {source_name}")
                        
            except Exception as e:
                print(f"Error scraping {source_name}: {str(e)}")
                continue
                
        return signals

    def scrape_sec_filings(self, days_back: int = 30) -> List[Dict]:
        """Scrape SEC EDGAR for recent filings (simplified version)"""
        signals = []
        
        # This is a simplified version - in practice you'd use the SEC EDGAR API
        try:
            # Example: Search for recent Form D filings (private offerings)
            url = "https://www.sec.gov/cgi-bin/browse-edgar"
            params = {
                'action': 'getcompany',
                'type': 'D',
                'count': 100,
                'output': 'atom'
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                # Parse the atom feed
                feed = feedparser.parse(response.text)
                
                for entry in feed.entries:
                    # Extract filing information
                    title = entry.get('title', '')
                    content = entry.get('summary', '')
                    
                    # Look for startup indicators
                    matching_keywords = self._find_startup_keywords(content + ' ' + title)
                    
                    if matching_keywords:
                        signal = {
                            'title': title,
                            'source': 'SEC EDGAR',
                            'url': entry.get('link', ''),
                            'summary': content[:500] + '...' if len(content) > 500 else content,
                            'publish_date': datetime.now(),  # Would parse actual date
                            'keywords': matching_keywords,
                            'signal_score': len(matching_keywords),
                            'content_type': 'SEC Filing'
                        }
                        signals.append(signal)
                        
        except Exception as e:
            print(f"Error scraping SEC filings: {str(e)}")
            
        return signals

    def scrape_university_news(self, days_back: int = 14) -> List[Dict]:
        """Scrape university press releases for startup activity"""
        signals = []
        
        university_urls = [
            'https://news.mit.edu/topic/innovation-entrepreneurship',
            'https://news.stanford.edu/topics/business/',
            'https://news.berkeley.edu/topic/business/',
        ]
        
        for url in university_urls:
            try:
                response = self.session.get(url)
                soup = BeautifulSoup(response.html.html, 'html.parser')
                
                # Extract articles (this would need to be customized per site)
                articles = soup.find_all('article', limit=20)
                
                for article in articles:
                    title_elem = article.find('h2') or article.find('h3')
                    title = title_elem.get_text(strip=True) if title_elem else 'No title'
                    
                    content = article.get_text(strip=True)
                    
                    # Check for startup keywords
                    matching_keywords = self._find_startup_keywords(content)
                    
                    if matching_keywords:
                        signal = {
                            'title': title,
                            'source': 'University News',
                            'url': url,
                            'summary': content[:300] + '...' if len(content) > 300 else content,
                            'publish_date': datetime.now(),  # Would parse actual date
                            'keywords': matching_keywords,
                            'signal_score': len(matching_keywords),
                            'content_type': 'Press Release'
                        }
                        signals.append(signal)
                        
            except Exception as e:
                print(f"Error scraping university news: {str(e)}")
                continue
                
        return signals

    def scrape_full_article(self, url: str) -> Optional[Dict]:
        """Use newspaper3k to extract and summarize full articles"""
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            
            # Check for startup keywords in full text
            full_text = article.text
            matching_keywords = self._find_startup_keywords(full_text)
            
            if matching_keywords:
                return {
                    'title': article.title,
                    'source': 'Full Article',
                    'url': url,
                    'summary': article.summary[:500] + '...' if len(article.summary) > 500 else article.summary,
                    'publish_date': article.publish_date or datetime.now(),
                    'keywords': matching_keywords,
                    'signal_score': len(matching_keywords),
                    'content_type': 'Full Article',
                    'authors': article.authors
                }
                
        except Exception as e:
            print(f"Error scraping full article {url}: {str(e)}")
            
        return None

    def _find_startup_keywords(self, text: str) -> List[str]:
        """Find startup-related keywords in text"""
        text_lower = text.lower()
        found_keywords = []
        
        for keyword in self.startup_keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                found_keywords.append(keyword)
                
        return found_keywords

    def get_all_signals(self, days_back: int = 7) -> pd.DataFrame:
        """Aggregate all signals from different sources"""
        all_signals = []
        
        print("Scraping RSS feeds...")
        all_signals.extend(self.scrape_rss_feeds(days_back))
        
        print("Scraping SEC filings...")
        all_signals.extend(self.scrape_sec_filings(days_back))
        
        print("Scraping university news...")
        all_signals.extend(self.scrape_university_news(days_back))
        
        # Convert to DataFrame
        df = pd.DataFrame(all_signals)
        
        if not df.empty:
            # Sort by signal score and publish date
            df = df.sort_values(['signal_score', 'publish_date'], ascending=[False, False])
            
            # Add region and sector tags (simplified)
            df['region'] = df.apply(self._extract_region, axis=1)
            df['sector'] = df.apply(self._extract_sector, axis=1)
            
        return df

    def _extract_region(self, row) -> str:
        """Extract region from content (simplified)"""
        content = (row['title'] + ' ' + row['summary']).lower()
        
        if any(word in content for word in ['silicon valley', 'san francisco', 'bay area', 'palo alto']):
            return 'Silicon Valley'
        elif any(word in content for word in ['new york', 'nyc', 'manhattan']):
            return 'New York'
        elif any(word in content for word in ['boston', 'cambridge', 'mit']):
            return 'Boston'
        elif any(word in content for word in ['london', 'uk', 'england']):
            return 'London'
        elif any(word in content for word in ['tel aviv', 'israel']):
            return 'Tel Aviv'
        else:
            return 'Other'

    def _extract_sector(self, row) -> str:
        """Extract sector from content (simplified)"""
        content = (row['title'] + ' ' + row['summary']).lower()
        
        if any(word in content for word in ['ai', 'artificial intelligence', 'machine learning', 'ml']):
            return 'AI/ML'
        elif any(word in content for word in ['fintech', 'financial', 'banking', 'payment']):
            return 'FinTech'
        elif any(word in content for word in ['health', 'medical', 'biotech', 'pharma']):
            return 'HealthTech'
        elif any(word in content for word in ['education', 'edtech', 'learning']):
            return 'EdTech'
        elif any(word in content for word in ['blockchain', 'crypto', 'defi', 'nft']):
            return 'Blockchain'
        elif any(word in content for word in ['saas', 'software', 'platform']):
            return 'SaaS'
        else:
            return 'Other'
