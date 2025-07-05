#!/usr/bin/env python3
"""
Test script to verify StartupSignal setup and dependencies
"""

import sys
import importlib

def test_imports():
    """Test if all required packages can be imported"""
    required_packages = [
        'streamlit',
        'feedparser', 
        'requests',
        'requests_html',
        'bs4',  # beautifulsoup4
        'newspaper',  # newspaper3k
        'pandas',
        'plotly',
        're',
        'datetime'
    ]
    
    print("Testing imports...")
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package}: {e}")
            failed_imports.append(package)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        print("Please install missing packages with: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All imports successful!")
        return True

def test_scraper():
    """Test basic scraper functionality"""
    try:
        print("\nTesting scraper initialization...")
        from scrapers import StartupSignalScraper
        
        scraper = StartupSignalScraper()
        print("✅ Scraper initialized successfully")
        
        # Test keyword detection
        test_text = "This startup just raised a seed round from venture capital investors"
        keywords = scraper._find_startup_keywords(test_text)
        
        if keywords:
            print(f"✅ Keyword detection working: {keywords}")
        else:
            print("⚠️ No keywords detected in test text")
        
        return True
        
    except Exception as e:
        print(f"❌ Scraper test failed: {e}")
        return False

def test_config():
    """Test configuration file"""
    try:
        print("\nTesting configuration...")
        import config
        
        print(f"✅ Custom keywords: {len(config.CUSTOM_KEYWORDS)} items")
        print(f"✅ RSS sources: {len(config.RSS_SOURCES)} sources")
        print(f"✅ Region patterns: {len(config.REGION_PATTERNS)} regions")
        print(f"✅ Sector patterns: {len(config.SECTOR_PATTERNS)} sectors")
        
        return True
        
    except Exception as e:
        print(f"❌ Config test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("StartupSignal Setup Test")
    print("=" * 40)
    
    tests_passed = 0
    total_tests = 3
    
    if test_imports():
        tests_passed += 1
    
    if test_scraper():
        tests_passed += 1
        
    if test_config():
        tests_passed += 1
    
    print("\n" + "=" * 40)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 Setup verification complete! You can now run: streamlit run app.py")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
