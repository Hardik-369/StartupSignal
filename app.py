import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
from scrapers import StartupSignalScraper
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict

# Page configuration
st.set_page_config(
    page_title="StartupSignal",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for minimal, info-dense design
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6B7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #F8FAFC;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #3B82F6;
        margin: 0.5rem 0;
    }
    .signal-card {
        background: white;
        border: 1px solid #E5E7EB;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .signal-title {
        font-weight: bold;
        color: #1F2937;
        margin-bottom: 0.5rem;
    }
    .signal-meta {
        font-size: 0.8rem;
        color: #6B7280;
        margin-bottom: 0.5rem;
    }
    .signal-tags {
        margin-top: 0.5rem;
    }
    .tag {
        background: #EBF8FF;
        color: #1E40AF;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.7rem;
        margin-right: 0.3rem;
        display: inline-block;
    }
    .score-badge {
        background: #10B981;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'signals_df' not in st.session_state:
        st.session_state.signals_df = pd.DataFrame()
    if 'scraper' not in st.session_state:
        st.session_state.scraper = StartupSignalScraper()
    if 'last_scrape_time' not in st.session_state:
        st.session_state.last_scrape_time = None

def scrape_signals(days_back: int = 7):
    """Scrape signals and update session state"""
    with st.spinner("🔍 Scraping startup signals..."):
        st.session_state.signals_df = st.session_state.scraper.get_all_signals(days_back)
        st.session_state.last_scrape_time = datetime.now()
        
        if not st.session_state.signals_df.empty:
            st.success(f"✅ Found {len(st.session_state.signals_df)} signals")
        else:
            st.warning("⚠️ No signals found. Try increasing the time range.")

def filter_signals(df: pd.DataFrame, filters: Dict) -> pd.DataFrame:
    """Apply filters to the signals DataFrame"""
    if df.empty:
        return df
    
    filtered_df = df.copy()
    
    # Keyword filter
    if filters['keyword']:
        mask = (
            filtered_df['title'].str.contains(filters['keyword'], case=False, na=False) |
            filtered_df['summary'].str.contains(filters['keyword'], case=False, na=False) |
            filtered_df['keywords'].astype(str).str.contains(filters['keyword'], case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    # Region filter
    if filters['region'] and filters['region'] != 'All':
        filtered_df = filtered_df[filtered_df['region'] == filters['region']]
    
    # Sector filter
    if filters['sector'] and filters['sector'] != 'All':
        filtered_df = filtered_df[filtered_df['sector'] == filters['sector']]
    
    # Date filter
    if filters['date_range']:
        start_date = datetime.now() - timedelta(days=filters['date_range'])
        filtered_df = filtered_df[filtered_df['publish_date'] >= start_date]
    
    # Source filter
    if filters['source'] and filters['source'] != 'All':
        filtered_df = filtered_df[filtered_df['source'] == filters['source']]
    
    # Signal score filter
    if filters['min_score'] > 0:
        filtered_df = filtered_df[filtered_df['signal_score'] >= filters['min_score']]
    
    return filtered_df

def display_signal_cards(df: pd.DataFrame):
    """Display signals as cards"""
    if df.empty:
        st.info("🔍 No signals match your current filters.")
        return
    
    for idx, row in df.iterrows():
        with st.container():
            st.markdown(f"""
            <div class="signal-card">
                <div class="signal-title">{row['title']}</div>
                <div class="signal-meta">
                    {row['source']} • {row['publish_date'].strftime('%Y-%m-%d %H:%M')} • 
                    <span class="score-badge">Score: {row['signal_score']}</span>
                </div>
                <div style="margin: 0.5rem 0;">
                    {row['summary'][:200]}{'...' if len(row['summary']) > 200 else ''}
                </div>
                <div class="signal-tags">
                    <span class="tag">{row['region']}</span>
                    <span class="tag">{row['sector']}</span>
                    <span class="tag">{row['content_type']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add expandable section for keywords and link
            with st.expander("🔍 Details"):
                st.write(f"**Keywords:** {', '.join(row['keywords'])}")
                if row['url']:
                    st.write(f"**URL:** {row['url']}")

def display_analytics(df: pd.DataFrame):
    """Display analytics charts"""
    if df.empty:
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Signals by Source")
        source_counts = df['source'].value_counts()
        fig_source = px.bar(
            x=source_counts.index,
            y=source_counts.values,
            labels={'x': 'Source', 'y': 'Count'},
            title="Signal Distribution by Source"
        )
        fig_source.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig_source, use_container_width=True)
    
    with col2:
        st.subheader("🏢 Signals by Sector")
        sector_counts = df['sector'].value_counts()
        fig_sector = px.pie(
            values=sector_counts.values,
            names=sector_counts.index,
            title="Signal Distribution by Sector"
        )
        fig_sector.update_layout(height=300)
        st.plotly_chart(fig_sector, use_container_width=True)
    
    # Timeline chart
    st.subheader("📈 Signal Timeline")
    df['date'] = df['publish_date'].dt.date
    daily_counts = df.groupby('date').size().reset_index(name='count')
    
    fig_timeline = px.line(
        daily_counts,
        x='date',
        y='count',
        title="Daily Signal Volume",
        markers=True
    )
    fig_timeline.update_layout(height=300)
    st.plotly_chart(fig_timeline, use_container_width=True)

def export_data(df: pd.DataFrame, format: str):
    """Export filtered data"""
    if df.empty:
        st.warning("No data to export")
        return
    
    if format == "JSON":
        # Convert DataFrame to JSON
        json_data = df.to_json(orient='records', date_format='iso', indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_data,
            file_name=f"startup_signals_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    elif format == "CSV":
        # Convert DataFrame to CSV
        csv_data = df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv_data,
            file_name=f"startup_signals_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

def main():
    """Main application function"""
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">🚀 StartupSignal</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Early detection of emerging startups</div>', unsafe_allow_html=True)
    
    # Sidebar filters
    st.sidebar.header("🔧 Controls")
    
    # Scraping controls
    st.sidebar.subheader("Data Collection")
    days_back = st.sidebar.selectbox(
        "Time Range",
        options=[1, 3, 7, 14, 30],
        index=2,
        help="Number of days back to scrape"
    )
    
    if st.sidebar.button("🔄 Refresh Signals", type="primary"):
        scrape_signals(days_back)
    
    # Auto-refresh on app load if no data
    if st.session_state.signals_df.empty:
        scrape_signals(days_back)
    
    # Display last scrape time
    if st.session_state.last_scrape_time:
        st.sidebar.info(f"Last updated: {st.session_state.last_scrape_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Filters
    st.sidebar.subheader("🔍 Filters")
    
    filters = {}
    
    # Keyword search
    filters['keyword'] = st.sidebar.text_input("Search Keywords", help="Search in title, summary, or keywords")
    
    # Region filter
    if not st.session_state.signals_df.empty:
        regions = ['All'] + sorted(st.session_state.signals_df['region'].unique().tolist())
        filters['region'] = st.sidebar.selectbox("Region", regions)
    else:
        filters['region'] = 'All'
    
    # Sector filter
    if not st.session_state.signals_df.empty:
        sectors = ['All'] + sorted(st.session_state.signals_df['sector'].unique().tolist())
        filters['sector'] = st.sidebar.selectbox("Sector", sectors)
    else:
        filters['sector'] = 'All'
    
    # Source filter
    if not st.session_state.signals_df.empty:
        sources = ['All'] + sorted(st.session_state.signals_df['source'].unique().tolist())
        filters['source'] = st.sidebar.selectbox("Source", sources)
    else:
        filters['source'] = 'All'
    
    # Date range filter
    filters['date_range'] = st.sidebar.slider(
        "Days Back",
        min_value=1,
        max_value=30,
        value=7,
        help="Filter signals from last N days"
    )
    
    # Signal score filter
    filters['min_score'] = st.sidebar.slider(
        "Minimum Signal Score",
        min_value=0,
        max_value=10,
        value=0,
        help="Filter by minimum signal strength"
    )
    
    # Export options
    st.sidebar.subheader("📥 Export")
    export_format = st.sidebar.selectbox("Export Format", ["JSON", "CSV"])
    
    # Apply filters
    filtered_df = filter_signals(st.session_state.signals_df, filters)
    
    # Main content area
    if not st.session_state.signals_df.empty:
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Signals", len(st.session_state.signals_df))
        
        with col2:
            st.metric("Filtered Signals", len(filtered_df))
        
        with col3:
            if not filtered_df.empty:
                avg_score = filtered_df['signal_score'].mean()
                st.metric("Avg Signal Score", f"{avg_score:.1f}")
            else:
                st.metric("Avg Signal Score", "N/A")
        
        with col4:
            if not filtered_df.empty:
                top_source = filtered_df['source'].value_counts().index[0]
                st.metric("Top Source", top_source)
            else:
                st.metric("Top Source", "N/A")
        
        # Tabs for different views
        tab1, tab2 = st.tabs(["📋 Signals", "📊 Analytics"])
        
        with tab1:
            # Export button
            if not filtered_df.empty:
                export_data(filtered_df, export_format)
            
            # Display signals
            display_signal_cards(filtered_df)
        
        with tab2:
            display_analytics(filtered_df)
    
    else:
        st.info("👋 Welcome to StartupSignal! Click 'Refresh Signals' to start detecting startup activity.")

if __name__ == "__main__":
    main()
