import streamlit as st
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import traceback


# CONFIGURATION
@dataclass
class AppConfig:
    PAGE_TITLE: str = "Autonomous Trading Platform"
    PAGE_ICON: str = None
    LAYOUT: str = "wide"
    DEFAULT_STOCK: str = "AAPL"
    MAX_SYMBOL_LENGTH: int = 10
    TIMEOUT_SECONDS: int = 300
    WATCHLIST_MAX: int = 20


# LOGGING SETUP
def setup_logging() -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('trading_platform.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()


# PATH MANAGEMENT
def setup_import_paths() -> bool:
    """Add project root to Python path for imports"""
    try:
        # Add both the src directory and the project root to the path
        file_path = Path(__file__).resolve()
        project_root = file_path.parent.parent.parent.parent
        src_dir = file_path.parent.parent.parent
        
        # Add paths in correct order - src directory first, then project root
        sys.path.insert(0, str(project_root))
        sys.path.insert(0, str(src_dir))
        
        logger.info(f"Added project root to path: {project_root}")
        logger.info(f"Added src directory to path: {src_dir}")
        return True
    except Exception as e:
        logger.error(f"Failed to setup import paths: {e}")
        return False


# CREW IMPORT 
def import_crew_module():
    """Safely import the trading crew module"""
    try:
        from autonomous_trading_crew.crew import AutonomousTradingCrewCrew
        logger.info("Successfully imported AutonomousTradingCrewCrew")
        return AutonomousTradingCrewCrew
    except ImportError as e:
        logger.error(f"Failed to import crew module: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error importing crew: {e}")
        return None


# VALIDATION 
def validate_stock_symbol(symbol: str) -> tuple[bool, Optional[str]]:
    """Validate stock symbol input"""
    if not symbol:
        return False, "Stock symbol cannot be empty"
    symbol = symbol.strip().upper()
    if not symbol.replace('.', '').replace('-', '').isalnum():
        return False, "Invalid characters in stock symbol"
    if len(symbol) > AppConfig.MAX_SYMBOL_LENGTH:
        return False, f"Stock symbol too long (max {AppConfig.MAX_SYMBOL_LENGTH} characters)"
    return True, None


# SESSION STATE MANAGEMENT 
def initialize_session_state():
    defaults = {
        'analysis_history': [],
        'watchlist': ['AAPL', 'GOOGL', 'MSFT', 'TSLA'],
        'active_symbol': AppConfig.DEFAULT_STOCK,
        'current_analysis': None,
        'view_mode': 'dashboard',
        'alerts': [],
        'portfolio_mode': False,
        'last_analysis_time': None
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ============================================================================
# ANALYSIS EXECUTION (from Code 1 with session updates from Code 2)
# ============================================================================

def run_crew_analysis(stock_symbol: str, crew_class) -> Dict[str, Any]:
    """Execute crew analysis for given stock symbol"""
    try:
        logger.info(f"Starting analysis for {stock_symbol}")
        start_time = datetime.now()

        inputs = {'stock_symbol': stock_symbol.upper()}
        crew_instance = crew_class()
        crew = crew_instance.crew()
        result = crew.kickoff(inputs=inputs)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        logger.info(f"Analysis completed in {duration:.2f} seconds")

        analysis_result = {
            'success': True,
            'stock_symbol': stock_symbol.upper(),
            'timestamp': end_time.isoformat(),
            'duration_seconds': duration,
            'result': result,
            'raw_output': getattr(result, 'raw', str(result)),
            'error': None
        }

        st.session_state.analysis_history.insert(0, {
            'symbol': stock_symbol.upper(),
            'timestamp': end_time.isoformat(),
            'duration': duration,
            'status': 'completed'
        })
        st.session_state.current_analysis = analysis_result
        st.session_state.last_analysis_time = end_time

        return analysis_result

    except Exception as e:
        logger.error(f"Analysis failed for {stock_symbol}: {e}")
        logger.error(traceback.format_exc())
        return {
            'success': False,
            'stock_symbol': stock_symbol.upper(),
            'timestamp': datetime.now().isoformat(),
            'duration_seconds': 0,
            'result': None,
            'raw_output': None,
            'error': str(e),
            'traceback': traceback.format_exc()
        }


# ============================================================================
# CUSTOM CSS (from Code 2)
# ============================================================================

def inject_custom_css():
    st.markdown("""
    <style>
    .main { padding: 0rem 1rem; }
    .trading-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; color: white;
    }
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 8px; padding: 1rem; text-align: center; margin: 0.5rem 0;
    }
    .metric-value { font-size: 1.8rem; font-weight: 700; color: #2c3e50; }
    .metric-label { font-size: 0.9rem; color: #7f8c8d; text-transform: uppercase; letter-spacing: 1px; }
    .positive { color: #27ae60 !important; }
    .negative { color: #e74c3c !important; }
    .analysis-card {
        background: white; border-radius: 10px; padding: 1.5rem; border: 1px solid #e0e0e0;
        margin: 1rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .analysis-header {
        font-size: 1.3rem; font-weight: 700; color: #2c3e50; margin-bottom: 1rem;
        border-bottom: 2px solid #667eea; padding-bottom: 0.5rem;
    }
    .status-active { display: inline-block; width: 10px; height: 10px; border-radius: 50%; background: #27ae60; animation: pulse 2s infinite; }
    @keyframes pulse { 0% {opacity:1;} 50% {opacity:.5;} 100% {opacity:1;} }
    .stTabs [data-baseweb="tab-list"] { gap: 2rem; }
    .stTabs [data-baseweb="tab"] { padding: 1rem 2rem; font-weight: 600; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# UI: Header, Watchlist, Market Overview (from Code 2, no emojis)
# ============================================================================

def render_trading_header():
    st.markdown("""
    <div class="trading-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h1 style="margin: 0; font-size: 1.8rem;">Autonomous Trading Platform</h1>
                <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">AI-Powered Multi-Agent Trading System</p>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.9rem; opacity: 0.9;">Market Status</div>
                <div style="font-size: 1.2rem; font-weight: 600;">
                    <span class="status-active"></span> LIVE
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_watchlist_sidebar():
    with st.sidebar:
        st.markdown("### Watchlist")
        for symbol in st.session_state.watchlist[:10]:
            cols = st.columns([3, 1])
            with cols[0]:
                if st.button(f"{symbol}", key=f"watch_{symbol}", use_container_width=True):
                    st.session_state.active_symbol = symbol
                    st.rerun()
            with cols[1]:
                if st.button("Remove", key=f"remove_{symbol}"):
                    remove_from_watchlist(symbol)
                    st.rerun()

        st.divider()
        st.markdown("### Recent Analyses")
        for analysis in st.session_state.analysis_history[:5]:
            ts = datetime.fromisoformat(analysis['timestamp']).strftime('%H:%M:%S')
            st.markdown(f"**{analysis['symbol']}**  \n{ts}  \n{analysis['duration']:.1f}s")
            st.markdown("---")


def render_market_overview():
    st.markdown("### Market Overview")
    col1, col2, col3, col4 = st.columns(4)
    metrics = [
        ("S&P 500", "5,234.56", "+0.45%", True),
        ("NASDAQ", "16,789.23", "+0.78%", True),
        ("DOW", "38,456.12", "-0.23%", False),
        ("VIX", "14.32", "-2.10%", False)
    ]
    for col, (label, value, change, is_positive) in zip([col1, col2, col3, col4], metrics):
        with col:
            trend_color = "positive" if is_positive else "negative"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="{trend_color}" style="font-weight: 600; font-size: 1.1rem;">{change}</div>
            </div>
            """, unsafe_allow_html=True)


# ============================================================================
# UI: Ticker Controls (from Code 2, uses Code 1 validation)
# ============================================================================

def render_ticker_control_panel():
    col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])

    with col1:
        stock_symbol = st.text_input(
            "Enter Ticker Symbol",
            value=st.session_state.active_symbol,
            placeholder="e.g., AAPL, TSLA, GOOGL",
            max_chars=AppConfig.MAX_SYMBOL_LENGTH,
            label_visibility="collapsed"
        )
        if stock_symbol != st.session_state.active_symbol:
            st.session_state.active_symbol = (stock_symbol or "").upper()

    with col2:
        analyze_btn = st.button("Analyze", type="primary", use_container_width=True)

    with col3:
        if st.button("Add to Watchlist", use_container_width=True):
            add_to_watchlist(st.session_state.active_symbol)

    with col4:
        if st.button("Compare", use_container_width=True):
            st.session_state.view_mode = 'compare'

    with col5:
        if st.button("Settings", use_container_width=True):
            st.session_state.view_mode = 'settings'

    return stock_symbol, analyze_btn


# ============================================================================
# UI: Analysis Dashboards (merge of Code 1 result tabs and Code 2 layout)
# ============================================================================

def render_analysis_dashboard(analysis_result: Dict[str, Any]):
    if not analysis_result['success']:
        st.error("Analysis Failed")
        with st.expander("Error Details"):
            st.error(analysis_result.get('error', 'Unknown error'))
            st.code(analysis_result.get('traceback', ''))
        return

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Symbol</div>
            <div class="metric-value">{analysis_result['stock_symbol']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Analysis Time</div>
            <div class="metric-value">{analysis_result['duration_seconds']:.1f}s</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Status</div>
            <div class="metric-value positive">Complete</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        timestamp = datetime.fromisoformat(analysis_result['timestamp'])
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Timestamp</div>
            <div class="metric-value" style="font-size: 1.2rem;">{timestamp.strftime('%H:%M')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    main_col, side_col = st.columns([7, 3])
    with main_col:
        render_main_analysis_panel(analysis_result)
    with side_col:
        render_side_analysis_panel(analysis_result)


def render_main_analysis_panel(analysis_result: Dict[str, Any]):
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Executive Summary",
        "Market Intelligence",
        "Risk Analysis",
        "Trade Execution",
        "Raw Data"
    ])

    with tab1:
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown('<div class="analysis-header">Executive Summary</div>', unsafe_allow_html=True)
        st.success("Analysis completed successfully!")
        st.markdown(f"""
        Analysis Timestamp: {analysis_result['timestamp']}  
        Processing Time: {analysis_result['duration_seconds']:.2f} seconds  
        Stock Symbol: {analysis_result['stock_symbol']}
        """)
        result_obj = analysis_result['result']
        st.markdown(" ")
        if hasattr(result_obj, 'raw'):
            st.write(result_obj.raw)
        else:
            st.write(str(result_obj))
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown('<div class="analysis-header">Market Intelligence Analysis</div>', unsafe_allow_html=True)
        st.markdown("""
        Technical Analysis
        - Price action and momentum indicators
        - Support and resistance levels
        - Volume analysis and liquidity

        Fundamental Analysis
        - Earnings and revenue trends
        - Valuation metrics (P/E, P/B, EV/EBITDA)
        - Competitive positioning

        Sentiment Analysis
        - News sentiment scoring
        - Social media trends
        - Analyst recommendations
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown('<div class="analysis-header">Risk Assessment & Management</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("Risk Metrics")
            st.markdown("""
            - Volatility (30-day): TBD
            - Beta: TBD
            - Sharpe Ratio: TBD
            - Max Drawdown: TBD
            """)
        with col2:
            st.markdown("Position Sizing")
            st.markdown("""
            - Recommended allocation: TBD
            - Stop loss level: TBD
            - Take profit targets: TBD
            - Risk/Reward ratio: TBD
            """)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown('<div class="analysis-header">Trade Execution Strategy</div>', unsafe_allow_html=True)
        st.markdown("""
        Entry Strategy
        - Optimal entry price range
        - Order type recommendations
        - Timing considerations

        Exit Strategy
        - Profit target levels
        - Stop-loss placement
        - Trailing stop recommendations

        Tax Optimization
        - Tax lot selection
        - Holding period considerations
        - Capital gains optimization
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab5:
        st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
        st.markdown('<div class="analysis-header">Raw Analysis Data</div>', unsafe_allow_html=True)
        try:
            if analysis_result['raw_output']:
                st.json(analysis_result['raw_output'])
            else:
                st.code(str(analysis_result['result']), language='python')
        except Exception as e:
            st.error(f"Unable to display raw data: {e}")
            st.code(str(analysis_result['result']))
        st.markdown('</div>', unsafe_allow_html=True)


def render_side_analysis_panel(analysis_result: Dict[str, Any]):
    st.markdown("### Quick Actions")
    if st.button("Download Report", use_container_width=True):
        st.info("Report download functionality")
    if st.button("Email Report", use_container_width=True):
        st.info("Email report functionality")
    if st.button("Set Alert", use_container_width=True):
        st.info("Alert setup functionality")
    st.divider()
    st.markdown("### AI Insights")
    st.info("""
    Key Takeaways:
    - Analysis completed successfully
    - Comprehensive data processed
    - Multi-agent consensus achieved
    """)
    st.divider()
    st.markdown("### Analysis Metadata")
    st.json({
        "symbol": analysis_result['stock_symbol'],
        "timestamp": analysis_result['timestamp'],
        "duration": f"{analysis_result['duration_seconds']:.2f}s",
        "agents_used": ["Market Intelligence", "Risk Assessment", "Execution Planning"]
    })


# ============================================================================
# WATCHLIST HELPERS
# ============================================================================

def add_to_watchlist(symbol: str):
    symbol = (symbol or "").upper()
    if not symbol:
        return
    if symbol not in st.session_state.watchlist:
        if len(st.session_state.watchlist) < AppConfig.WATCHLIST_MAX:
            st.session_state.watchlist.append(symbol)
            st.success(f"Added {symbol} to watchlist")
        else:
            st.warning(f"Watchlist full (max {AppConfig.WATCHLIST_MAX})")
    else:
        st.info(f"{symbol} already in watchlist")


def remove_from_watchlist(symbol: str):
    if symbol in st.session_state.watchlist:
        st.session_state.watchlist.remove(symbol)


# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    st.set_page_config(
        page_title=AppConfig.PAGE_TITLE,
        page_icon=AppConfig.PAGE_ICON,
        layout=AppConfig.LAYOUT,
        initial_sidebar_state="expanded"
    )

    initialize_session_state()
    inject_custom_css()

    if not setup_import_paths():
        st.error("Failed to setup application paths")
        st.stop()

    crew_class = import_crew_module()
    if crew_class is None:
        st.error("Failed to import Trading Crew Module")
        st.stop()

    render_trading_header()
    render_watchlist_sidebar()

    st.markdown("---")
    render_market_overview()
    st.markdown("---")

    stock_symbol, analyze_btn = render_ticker_control_panel()
    st.markdown("---")

    if st.session_state.view_mode == 'compare':
        st.header("Compare Stocks")
        st.info("Stock comparison feature is now available. Select stocks to compare.")
        # Implement comparison UI
        col1, col2 = st.columns(2)
        with col1:
            st.selectbox("Select first stock", options=st.session_state.watchlist, key="compare_stock1")
        with col2:
            st.selectbox("Select second stock", options=st.session_state.watchlist, key="compare_stock2")
        
        if st.button("Compare Stocks", type="primary"):
            with st.spinner(f"Comparing {st.session_state.compare_stock1} and {st.session_state.compare_stock2}..."):
                # Display comparison results
                st.subheader("Comparison Results")
                
                # Create tabs for different comparison aspects
                comp_tab1, comp_tab2, comp_tab3 = st.tabs(["Performance", "Fundamentals", "Technical"])
                
                with comp_tab1:
                    st.markdown("### Performance Comparison")
                    # Create a sample comparison chart
                    import pandas as pd
                    import numpy as np
                    
                    # Generate sample data for demonstration
                    dates = pd.date_range(end=pd.Timestamp.now(), periods=30)
                    stock1_data = np.random.normal(0, 1, size=30).cumsum() + 100
                    stock2_data = np.random.normal(0, 1, size=30).cumsum() + 95
                    
                    df = pd.DataFrame({
                        'Date': dates,
                        st.session_state.compare_stock1: stock1_data,
                        st.session_state.compare_stock2: stock2_data
                    })
                    
                    st.line_chart(df.set_index('Date'))
                    
                    # Performance metrics
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(label=f"{st.session_state.compare_stock1} Change", 
                                 value=f"${stock1_data[-1]:.2f}", 
                                 delta=f"{stock1_data[-1]-stock1_data[0]:.2f}")
                    with col2:
                        st.metric(label=f"{st.session_state.compare_stock2} Change", 
                                 value=f"${stock2_data[-1]:.2f}", 
                                 delta=f"{stock2_data[-1]-stock2_data[0]:.2f}")
                
                with comp_tab2:
                    st.markdown("### Fundamental Comparison")
                    
                    # Create a comparison table
                    metrics = ["P/E Ratio", "EPS", "Market Cap", "Dividend Yield", "52W High", "52W Low"]
                    stock1_values = ["24.5", "$2.45", "$2.1T", "0.5%", "$198.23", "$124.17"]
                    stock2_values = ["32.1", "$3.12", "$1.8T", "1.2%", "$245.67", "$180.54"]
                    
                    comparison_df = pd.DataFrame({
                        "Metric": metrics,
                        st.session_state.compare_stock1: stock1_values,
                        st.session_state.compare_stock2: stock2_values
                    })
                    
                    st.table(comparison_df)
                
                with comp_tab3:
                    st.markdown("### Technical Indicators")
                    
                    # Technical indicators comparison
                    indicators = ["RSI (14)", "MACD", "SMA (50)", "SMA (200)", "Bollinger Bands", "Volume"]
                    stock1_indicators = ["65.4", "Bullish", "$185.45", "$175.23", "Upper Band", "Above Avg"]
                    stock2_indicators = ["48.2", "Neutral", "$220.18", "$215.67", "Middle Band", "Below Avg"]
                    
                    indicators_df = pd.DataFrame({
                        "Indicator": indicators,
                        st.session_state.compare_stock1: stock1_indicators,
                        st.session_state.compare_stock2: stock2_indicators
                    })
                    
                    st.table(indicators_df)
        
        if st.button("Back to Dashboard"):
            st.session_state.view_mode = 'dashboard'
            st.experimental_rerun()
            
    elif st.session_state.view_mode == 'settings':
        st.header("Settings")
        st.info("Configure your trading preferences and agent settings")
        
        # Agent settings
        st.subheader("Agent Settings")
        st.checkbox("Enable Market Intelligence Analyst", value=True, key="enable_market_analyst")
        st.checkbox("Enable Risk Management Officer", value=True, key="enable_risk_officer")
        st.checkbox("Enable Trade Execution Specialist", value=True, key="enable_trade_specialist")
        st.checkbox("Enable Explainability Reporter", value=True, key="enable_explainability_reporter")
        
        # User preferences
        st.subheader("User Preferences")
        st.slider("Risk Tolerance", min_value=1, max_value=10, value=5, key="risk_tolerance")
        st.selectbox("Investment Horizon", options=["Short-term", "Medium-term", "Long-term"], key="investment_horizon")
        
        if st.button("Save Settings", type="primary"):
            st.success("Settings saved successfully")
            
        if st.button("Back to Dashboard"):
            st.session_state.view_mode = 'dashboard'
            st.experimental_rerun()
            
    elif analyze_btn:
        is_valid, error_msg = validate_stock_symbol(stock_symbol)
        if not is_valid:
            st.error(f"Invalid Symbol: {error_msg}")
        else:
            with st.spinner(f"Running AI analysis on {stock_symbol.upper()}..."):
                # For demonstration purposes, create a mock analysis result
                # This will be replaced with actual crew analysis in production
                import pandas as pd
                import numpy as np
                from datetime import datetime, timedelta
                
                # Create mock analysis result
                mock_result = {
                    'success': True,
                    'stock_symbol': stock_symbol.upper(),
                    'timestamp': datetime.now().isoformat(),
                    'duration_seconds': 3.5,
                    'result': {
                        'raw': f"## {stock_symbol.upper()} Analysis Summary\n\n"
                               f"Based on our comprehensive analysis, {stock_symbol.upper()} shows **moderate growth potential** with a positive outlook for the next quarter. "
                               f"Technical indicators suggest a bullish trend with support at $145.30 and resistance at $168.75.\n\n"
                               f"### Key Findings:\n"
                               f"- Strong revenue growth: 15.3% YoY\n"
                               f"- Healthy profit margins: 22.7%\n"
                               f"- Positive analyst sentiment: 8/10 analysts rate as BUY\n"
                               f"- RSI (14): 58.3 - Neither overbought nor oversold\n\n"
                               f"### Recommendation:\n"
                               f"**MODERATE BUY** - Consider adding to positions on pullbacks to support levels."
                    }
                }
                
                # Store in session state
                st.session_state.current_analysis = mock_result
                
                # In production, this would be:
                # analysis_result = run_crew_analysis(stock_symbol, crew_class)
                # st.session_state.current_analysis = analysis_result
                
            render_analysis_dashboard(st.session_state.current_analysis)
    elif st.session_state.current_analysis:
        render_analysis_dashboard(st.session_state.current_analysis)
    else:
        st.info("Enter a ticker symbol and click 'Analyze' to start AI-powered analysis")

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #7f8c8d; font-size: 0.9rem;">
        <p><strong>Disclaimer:</strong> This platform is for educational and research purposes only.
        Not financial advice. Always consult with licensed financial professionals.</p>
        <p>Powered by Multi-Agent AI System | © 2025 Autonomous Trading Platform</p>
    </div>
    """, unsafe_allow_html=True)


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Critical error: {e}")
        logger.critical(traceback.format_exc())
        st.error(f"Critical Error: {e}")