# StartupSignal 🚀

A Streamlit app that detects early signs of emerging startups by scraping and analyzing multiple content sources.

## Features

- **Multi-source aggregation**: TechCrunch, SEC filings, university press sites, and startup accelerators
- **Signal detection**: Keyword-based system to identify startup activity mentions
- **Interactive dashboard**: Filter by keyword, region, sector, and timeframe
- **Analytics**: Visual charts showing signal distribution and trends
- **Export capabilities**: Download filtered results as JSON or CSV
- **Signal scoring**: Articles ranked by strength of startup indicators

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

## Usage

1. **Data Collection**: Use the sidebar to set your time range and click "Refresh Signals"
2. **Filtering**: Apply filters for keywords, regions, sectors, sources, and signal scores
3. **Analysis**: View signals in card format or explore analytics charts
4. **Export**: Download filtered results for further analysis

## Signal Sources

- **RSS Feeds**: TechCrunch, VentureBeat, The Verge, MIT News, Stanford News, etc.
- **SEC Filings**: Form D filings and other startup-related documents
- **University News**: Press releases from innovation hubs
- **Full Articles**: Deep content analysis using newspaper3k

## Keywords Detected

The system looks for startup-related terms including:
- Funding rounds: seed, Series A/B, venture capital
- Company stages: stealth startup, launch, founded
- Business events: acquisition, IPO, pivot
- Industry terms: unicorn, MVP, beta launch

## Technology Stack

- **Streamlit**: Frontend dashboard
- **feedparser**: RSS feed parsing
- **requests-html**: Dynamic content scraping
- **BeautifulSoup**: HTML parsing
- **newspaper3k**: Article extraction and summarization
- **pandas**: Data manipulation
- **plotly**: Interactive visualizations

## Configuration

Edit the `scrapers.py` file to:
- Add new RSS sources
- Modify startup keywords
- Adjust region/sector detection logic
- Add new content sources

## Notes

- Some sources may require rate limiting or API keys for production use
- SEC filing scraping is simplified - use official SEC EDGAR API for production
- University news scraping may need site-specific customization
- Consider implementing caching for better performance

## License

This project is for educational and research purposes.
