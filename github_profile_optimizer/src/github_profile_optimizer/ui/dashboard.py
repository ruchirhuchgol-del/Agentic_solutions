"""
Enterprise GitHub Profile Optimizer Dashboard
A production-grade UI for AI-powered GitHub profile optimization

This module provides a comprehensive Streamlit dashboard for analyzing and
optimizing GitHub profiles with enterprise features including multi-tenancy,
caching, and ML-powered recommendations.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# =============================================================================
# CONSTANTS AND CONFIGURATION
# =============================================================================

class Config:
    """Application configuration constants."""
    
    # API Configuration
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    REQUEST_TIMEOUT: int = 120
    REQUEST_RETRIES: int = 3
    
    # Default Credentials (should be overridden via environment or UI)
    DEFAULT_GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    DEFAULT_OPENAI_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # UI Theme Colors (GitHub-inspired)
    COLOR_PRIMARY: str = "#58a6ff"
    COLOR_SECONDARY: str = "#8b949e"
    COLOR_SUCCESS: str = "#3fb950"
    COLOR_WARNING: str = "#d29922"
    COLOR_ERROR: str = "#f85149"
    BG_PRIMARY: str = "#0d1117"
    BG_SECONDARY: str = "#161b22"
    BG_TERTIARY: str = "#21262d"
    BORDER_COLOR: str = "#30363d"
    
    # Rate Limiting
    MIN_RATE_LIMIT: int = 100
    MAX_RATE_LIMIT: int = 10000
    DEFAULT_RATE_LIMIT: int = 5000
    RATE_LIMIT_STEP: int = 100
    
    # Cache Settings
    CACHE_STATUS_TIMEOUT: int = 10
    ML_STATUS_TIMEOUT: int = 10


class RepoScope(str, Enum):
    """Repository analysis scope options."""
    PUBLIC = "public"
    PRIVATE = "private"
    ALL = "all"


class OptimizationDepth(str, Enum):
    """Optimization analysis depth levels."""
    MINIMAL = "minimal"
    MODERATE = "moderate"
    COMPREHENSIVE = "comprehensive"


class ProfessionalRole(str, Enum):
    """Supported professional role targets."""
    SOFTWARE_ENGINEER = "Software Engineer"
    DATA_SCIENTIST = "Data Scientist"
    DEVOPS_ENGINEER = "DevOps Engineer"
    FRONTEND_DEVELOPER = "Frontend Developer"
    BACKEND_DEVELOPER = "Backend Developer"
    FULL_STACK_DEVELOPER = "Full Stack Developer"
    ML_ENGINEER = "ML Engineer"
    SECURITY_ENGINEER = "Security Engineer"


# GitHub-inspired CSS styling
GITHUB_STYLES = f"""
<style>
    /* Main container */
    .main {{
        background-color: {Config.BG_PRIMARY};
    }}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 2px;
        background-color: {Config.BG_SECONDARY};
        border-radius: 6px;
        padding: 4px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent;
        border-radius: 6px;
        color: {Config.COLOR_SECONDARY};
        font-weight: 500;
        padding: 8px 16px;
        transition: all 0.2s ease;
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {Config.BG_TERTIARY};
        color: #c9d1d9;
    }}
    
    /* Card components */
    .metric-card {{
        background-color: {Config.BG_SECONDARY};
        border: 1px solid {Config.BORDER_COLOR};
        border-radius: 6px;
        padding: 16px;
        margin: 8px 0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    
    .metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }}
    
    /* Header section */
    .header-section {{
        background: linear-gradient(135deg, {Config.BG_PRIMARY} 0%, {Config.BG_SECONDARY} 100%);
        border: 1px solid {Config.BORDER_COLOR};
        border-radius: 6px;
        padding: 24px;
        margin-bottom: 24px;
    }}
    
    /* Info boxes */
    .info-box {{
        background-color: #1c2128;
        border-left: 4px solid {Config.COLOR_PRIMARY};
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }}
    
    .warning-box {{
        background-color: #1c2128;
        border-left: 4px solid {Config.COLOR_ERROR};
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }}
    
    .success-box {{
        background-color: #1c2128;
        border-left: 4px solid {Config.COLOR_SUCCESS};
        padding: 16px;
        border-radius: 6px;
        margin: 16px 0;
    }}
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {{
        color: #c9d1d9;
        font-weight: 600;
    }}
    
    /* Data frames */
    .stDataFrame {{
        background-color: {Config.BG_SECONDARY};
    }}
    
    /* Buttons */
    .stButton > button {{
        border-radius: 6px;
        font-weight: 500;
    }}
</style>
"""


# =============================================================================
# DATA MODELS
# =============================================================================

@dataclass(frozen=True)
class TenantConfiguration:
    """
    Immutable tenant configuration for multi-tenant isolation.
    
    Attributes:
        tenant_id: Unique identifier for the tenant
        github_token: GitHub Personal Access Token for API authentication
        openai_key: OpenAI API key for AI-powered recommendations
        rate_limit: Maximum API requests allowed per hour
        allowed_roles: List of professional roles available for optimization
    """
    tenant_id: str
    github_token: str
    openai_key: str
    rate_limit: int
    allowed_roles: List[str]
    
    def __post_init__(self):
        """Validate tenant configuration."""
        if self.rate_limit < Config.MIN_RATE_LIMIT or self.rate_limit > Config.MAX_RATE_LIMIT:
            raise ValueError(
                f"Rate limit must be between {Config.MIN_RATE_LIMIT} and {Config.MAX_RATE_LIMIT}"
            )
        if not self.allowed_roles:
            raise ValueError("At least one allowed role must be specified")


@dataclass(frozen=True)
class OptimizationRequest:
    """
    Immutable optimization request parameters.
    
    Attributes:
        github_handle: Target GitHub username
        target_roles: List of professional roles to optimize for
        repos_scope: Scope of repositories to analyze
        dry_run: If True, preview changes without applying them
        limits: Depth of analysis and recommendations
        tenant_id: Tenant identifier for multi-tenant isolation
    """
    github_handle: str
    target_roles: List[str]
    repos_scope: str
    dry_run: bool
    limits: str
    tenant_id: str
    
    def __post_init__(self):
        """Validate optimization request parameters."""
        if not self.github_handle or not self.github_handle.strip():
            raise ValueError("GitHub handle cannot be empty")
        if not self.target_roles:
            raise ValueError("At least one target role must be specified")
        if self.repos_scope not in [scope.value for scope in RepoScope]:
            raise ValueError(f"Invalid repository scope: {self.repos_scope}")
        if self.limits not in [depth.value for depth in OptimizationDepth]:
            raise ValueError(f"Invalid optimization depth: {self.limits}")


@dataclass
class OptimizationResult:
    """
    Structured optimization result with metadata.
    
    Attributes:
        timestamp: When the optimization was performed
        github_handle: Target GitHub username
        result: Raw API response data
        success: Whether the optimization completed successfully
        error_message: Error description if optimization failed
    """
    timestamp: datetime
    github_handle: str
    result: Dict[str, Any]
    success: bool = True
    error_message: Optional[str] = None


# =============================================================================
# SESSION STATE MANAGEMENT
# =============================================================================

class SessionStateManager:
    """
    Manages Streamlit session state with type safety and validation.
    
    This class provides a centralized interface for managing application state
    across Streamlit reruns, ensuring consistency and type safety.
    """
    
    # Session state keys
    KEY_OPTIMIZATION_HISTORY = "optimization_history"
    KEY_TENANT_CONFIG = "tenant_config"
    
    @classmethod
    def initialize(cls) -> None:
        """Initialize session state with default values if not already set."""
        try:
            # Check if session state exists
            if 'session_state' not in dir(st):
                # Create session state if it doesn't exist
                st.session_state = {}
        except:
            # Fallback: create session state
            st.session_state = {}
            
        # Import Config locally to avoid circular imports
        from src.github_profile_optimizer.ui.dashboard import Config, ProfessionalRole
            
        if cls.KEY_OPTIMIZATION_HISTORY not in st.session_state:
            st.session_state[cls.KEY_OPTIMIZATION_HISTORY] = []
            logger.info("Initialized optimization history in session state")
        
        if cls.KEY_TENANT_CONFIG not in st.session_state:
            st.session_state[cls.KEY_TENANT_CONFIG] = {
                "github_token": Config.DEFAULT_GITHUB_TOKEN,
                "openai_key": Config.DEFAULT_OPENAI_KEY,
                "rate_limit": Config.DEFAULT_RATE_LIMIT,
                "allowed_roles": [role.value for role in ProfessionalRole]
            }
            logger.info("Initialized tenant configuration in session state")
    
    @classmethod
    def add_optimization_result(
        cls,
        github_handle: str,
        result: Dict[str, Any],
        success: bool = True,
        error_message: Optional[str] = None
    ) -> None:
        """
        Add an optimization result to the history.
        
        Args:
            github_handle: GitHub username that was optimized
            result: Raw optimization result data
            success: Whether the optimization succeeded
            error_message: Error description if optimization failed
        """
        # Ensure session state is initialized
        cls.initialize()
        
        optimization_result = OptimizationResult(
            timestamp=datetime.now(),
            github_handle=github_handle,
            result=result,
            success=success,
            error_message=error_message
        )
        
        st.session_state[cls.KEY_OPTIMIZATION_HISTORY].append(optimization_result)
        logger.info(f"Added optimization result for {github_handle} to history")
    
    @classmethod
    def get_latest_optimization(cls) -> Optional[OptimizationResult]:
        """
        Retrieve the most recent optimization result.
        
        Returns:
            The latest optimization result, or None if history is empty
        """
        # Ensure session state is initialized
        cls.initialize()
        
        # Handle case where optimization history might not exist
        if cls.KEY_OPTIMIZATION_HISTORY not in st.session_state:
            st.session_state[cls.KEY_OPTIMIZATION_HISTORY] = []
        
        history = st.session_state[cls.KEY_OPTIMIZATION_HISTORY]
        return history[-1] if history else None
    
    @classmethod
    def get_optimization_history(cls) -> List[OptimizationResult]:
        """
        Retrieve the complete optimization history.
        
        Returns:
            List of all optimization results, ordered chronologically
        """
        # Ensure session state is initialized
        cls.initialize()
        
        # Handle case where optimization history might not exist
        if cls.KEY_OPTIMIZATION_HISTORY not in st.session_state:
            st.session_state[cls.KEY_OPTIMIZATION_HISTORY] = []
        
        return st.session_state[cls.KEY_OPTIMIZATION_HISTORY]
    
    @classmethod
    def clear_history(cls) -> None:
        """Clear all optimization history."""
        # Ensure session state is initialized
        cls.initialize()
        
        # Handle case where optimization history might not exist
        if cls.KEY_OPTIMIZATION_HISTORY not in st.session_state:
            st.session_state[cls.KEY_OPTIMIZATION_HISTORY] = []
        else:
            st.session_state[cls.KEY_OPTIMIZATION_HISTORY] = []
        logger.info("Cleared optimization history")
    
    @classmethod
    def get_tenant_config(cls) -> Dict[str, Any]:
        """
        Retrieve current tenant configuration.
        
        Returns:
            Dictionary containing tenant configuration
        """
        # Ensure session state is initialized
        cls.initialize()
        
        # Handle case where tenant config might not exist
        if cls.KEY_TENANT_CONFIG not in st.session_state:
            # Import Config locally to avoid circular imports
            from src.github_profile_optimizer.ui.dashboard import Config, ProfessionalRole
            st.session_state[cls.KEY_TENANT_CONFIG] = {
                "github_token": Config.DEFAULT_GITHUB_TOKEN,
                "openai_key": Config.DEFAULT_OPENAI_KEY,
                "rate_limit": Config.DEFAULT_RATE_LIMIT,
                "allowed_roles": [role.value for role in ProfessionalRole]
            }
        
        return st.session_state[cls.KEY_TENANT_CONFIG]
    
    @classmethod
    def update_tenant_config(cls, config: Dict[str, Any]) -> None:
        """
        Update tenant configuration.
        
        Args:
            config: New configuration dictionary
        """
        # Ensure session state is initialized
        cls.initialize()
        
        # Handle case where tenant config might not exist
        if cls.KEY_TENANT_CONFIG not in st.session_state:
            # Import Config locally to avoid circular imports
            from src.github_profile_optimizer.ui.dashboard import Config, ProfessionalRole
            st.session_state[cls.KEY_TENANT_CONFIG] = {
                "github_token": Config.DEFAULT_GITHUB_TOKEN,
                "openai_key": Config.DEFAULT_OPENAI_KEY,
                "rate_limit": Config.DEFAULT_RATE_LIMIT,
                "allowed_roles": [role.value for role in ProfessionalRole]
            }
        
        st.session_state[cls.KEY_TENANT_CONFIG].update(config)
        logger.info("Updated tenant configuration")


# =============================================================================
# API CLIENT
# =============================================================================

class APIClient:
    """
    Handles all API communication with retry logic and error handling.
    
    This class provides a robust interface for communicating with the
    optimization backend API, including automatic retries, timeout handling,
    and comprehensive error logging.
    """
    
    def __init__(self):
        """Initialize API client with retry configuration."""
        self.session = self._create_session_with_retries()
    
    @staticmethod
    def _create_session_with_retries() -> requests.Session:
        """
        Create a requests session with retry logic.
        
        Returns:
            Configured requests Session with retry adapter
        """
        session = requests.Session()
        
        retry_strategy = Retry(
            total=Config.REQUEST_RETRIES,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    def optimize_profile(
        self,
        request: OptimizationRequest,
        github_token: str,
        openai_key: str
    ) -> Optional[Dict[str, Any]]:
        """
        Execute profile optimization via API.
        
        Args:
            request: Optimization request parameters
            github_token: GitHub authentication token
            openai_key: OpenAI API key
        
        Returns:
            Optimization result dictionary, or None if request failed
        """
        url = f"{Config.API_BASE_URL}/optimize"
        
        payload = {
            "github_handle": request.github_handle,
            "target_roles": request.target_roles,
            "repos_scope": request.repos_scope,
            "dry_run": request.dry_run,
            "limits": request.limits,
            "tenant_id": request.tenant_id
        }
        
        headers = {
            "X-GitHub-Token": github_token,
            "X-OpenAI-Key": openai_key,
            "Content-Type": "application/json"
        }
        
        try:
            logger.info(f"Sending optimization request for {request.github_handle}")
            
            response = self.session.post(
                url,
                json=payload,
                headers=headers,
                timeout=Config.REQUEST_TIMEOUT
            )
            
            if response.status_code == 200:
                logger.info(f"Optimization successful for {request.github_handle}")
                return response.json()
            else:
                error_msg = f"API request failed: {response.status_code} - {response.text}"
                logger.error(error_msg)
                st.error(f"Optimization failed with status {response.status_code}")
                
                # Display detailed error for debugging
                with st.expander("View Error Details"):
                    st.code(response.text)
                
                return None
        
        except requests.exceptions.Timeout:
            error_msg = f"Request timeout after {Config.REQUEST_TIMEOUT}s"
            logger.error(error_msg)
            st.error(f"{error_msg}. The optimization is taking longer than expected.")
            return None
        
        except requests.exceptions.ConnectionError:
            error_msg = f"Connection error to {Config.API_BASE_URL}"
            logger.error(error_msg)
            st.error(f"Unable to connect to API server at {Config.API_BASE_URL}")
            return None
        
        except requests.exceptions.RequestException as e:
            logger.exception("Request exception during optimization")
            st.error(f"Request error: {str(e)}")
            return None
        
        except Exception as e:
            logger.exception("Unexpected error during optimization")
            st.error(f"Unexpected error: {str(e)}")
            return None
    
    def get_cache_status(self) -> Dict[str, Any]:
        """
        Retrieve current caching system status.
        
        Returns:
            Dictionary containing cache metrics and status
        """
        url = f"{Config.API_BASE_URL}/cache/status"
        
        try:
            response = self.session.get(url, timeout=Config.CACHE_STATUS_TIMEOUT)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Failed to fetch cache status: {response.status_code}")
        
        except Exception as e:
            logger.warning(f"Exception fetching cache status: {str(e)}")
        
        return self._get_default_cache_status()
    
    def get_ml_status(self) -> Dict[str, Any]:
        """
        Retrieve ML model status and metrics.
        
        Returns:
            Dictionary containing ML model information
        """
        url = f"{Config.API_BASE_URL}/ml/status"
        
        try:
            response = self.session.get(url, timeout=Config.ML_STATUS_TIMEOUT)
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"Failed to fetch ML status: {response.status_code}")
        
        except Exception as e:
            logger.warning(f"Exception fetching ML status: {str(e)}")
        
        return self._get_default_ml_status()
    
    @staticmethod
    def _get_default_cache_status() -> Dict[str, Any]:
        """Return default cache status when API is unavailable."""
        return {
            "l1_cache": {"status": "Unknown", "items": 0, "hit_rate": "N/A"},
            "l2_cache": {"status": "Unknown", "items": 0, "hit_rate": "N/A"},
            "l3_cache": {"status": "Unknown", "items": 0, "hit_rate": "N/A"}
        }
    
    @staticmethod
    def _get_default_ml_status() -> Dict[str, Any]:
        """Return default ML status when API is unavailable."""
        return {
            "model_loaded": False,
            "model_type": "Unknown",
            "last_trained": "N/A",
            "accuracy": "N/A",
            "features": [],
            "predictions": []
        }


# =============================================================================
# DASHBOARD UI COMPONENTS
# =============================================================================

class DashboardUI:
    """Main dashboard UI component orchestrator."""
    
    @staticmethod
    def render_header() -> None:
        """Render application header with branding."""
        st.markdown(GITHUB_STYLES, unsafe_allow_html=True)
        st.markdown("""
        <div class="header-section">
            <h1 style="color:#58a6ff;margin-bottom:8px;font-size:32px;">
                GitHub Profile Optimizer
            </h1>
            <p style="color:#8b949e;font-size:16px;margin:0;">
                Enterprise-grade AI-powered GitHub profile optimization platform
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_sidebar(api_client: APIClient) -> Tuple[bool, str, List[str], str, str, bool, str]:
        """
        Render sidebar configuration panel.
        
        Args:
            api_client: API client instance for status checks
        
        Returns:
            Tuple containing user inputs and action trigger
        """
        with st.sidebar:
            st.header("Configuration")
            
            # Tenant Management Section
            tenant_id = DashboardUI._render_tenant_section()
            
            # API Credentials Section
            DashboardUI._render_credentials_section()
            
            # Rate Limiting Section
            DashboardUI._render_rate_limiting_section()
            
            # Optimization Parameters Section
            github_handle, target_roles, repos_scope, limits, dry_run = (
                DashboardUI._render_optimization_parameters()
            )
            
            # System Status Section
            DashboardUI._render_system_status(api_client)
            
            # Action Button
            st.markdown("---")
            optimize_clicked = st.button(
                "Execute Optimization",
                type="primary",
                use_container_width=True,
                help="Start the profile optimization analysis"
            )
            
            # History Management
            DashboardUI._render_history_controls()
            
            return (
                optimize_clicked,
                github_handle,
                target_roles,
                repos_scope,
                limits,
                dry_run,
                tenant_id
            )
    
    @staticmethod
    def _render_tenant_section() -> str:
        """Render tenant management section."""
        st.subheader("Tenant Management")
        tenant_id = st.text_input(
            "Tenant ID",
            value="default",
            help="Unique identifier for multi-tenant isolation",
            key="tenant_id_input"
        )
        return tenant_id
    
    @staticmethod
    def _render_credentials_section() -> None:
        """Render API credentials section."""
        st.subheader("API Credentials")
        
        tenant_config = SessionStateManager.get_tenant_config()
        
        github_token = st.text_input(
            "GitHub Personal Access Token",
            value=tenant_config["github_token"],
            type="password",
            help="Required for GitHub API access. Generate at: https://github.com/settings/tokens",
            key="github_token_input"
        )
        
        openai_key = st.text_input(
            "OpenAI API Key",
            value=tenant_config["openai_key"],
            type="password",
            help="Required for AI-powered recommendations",
            key="openai_key_input"
        )
        
        SessionStateManager.update_tenant_config({
            "github_token": github_token,
            "openai_key": openai_key
        })
    
    @staticmethod
    def _render_rate_limiting_section() -> None:
        """Render rate limiting configuration."""
        st.subheader("Rate Limiting")
        
        tenant_config = SessionStateManager.get_tenant_config()
        
        rate_limit = st.slider(
            "Maximum Requests per Hour",
            min_value=Config.MIN_RATE_LIMIT,
            max_value=Config.MAX_RATE_LIMIT,
            value=tenant_config["rate_limit"],
            step=Config.RATE_LIMIT_STEP,
            help="Enterprise rate limit configuration",
            key="rate_limit_slider"
        )
        
        SessionStateManager.update_tenant_config({"rate_limit": rate_limit})
    
    @staticmethod
    def _render_optimization_parameters() -> Tuple[str, List[str], str, str, bool]:
        """Render optimization parameters section."""
        st.subheader("Optimization Parameters")
        
        tenant_config = SessionStateManager.get_tenant_config()
        
        github_handle = st.text_input(
            "GitHub Username",
            value="",
            placeholder="Enter GitHub username",
            help="Target GitHub profile username to optimize",
            key="github_handle_input"
        )
        
        target_roles = st.multiselect(
            "Target Professional Roles",
            options=tenant_config["allowed_roles"],
            default=[ProfessionalRole.SOFTWARE_ENGINEER.value],
            help="Select one or more target roles for optimization",
            key="target_roles_select"
        )
        
        repos_scope = st.selectbox(
            "Repository Scope",
            options=[scope.value for scope in RepoScope],
            index=0,
            help="Scope of repositories to analyze",
            key="repos_scope_select"
        )
        
        limits = st.selectbox(
            "Optimization Depth",
            options=[depth.value for depth in OptimizationDepth],
            index=1,
            help="Depth of analysis and recommendations",
            key="limits_select"
        )
        
        dry_run = st.checkbox(
            "Dry Run Mode",
            value=True,
            help="Preview changes without applying them (recommended)",
            key="dry_run_checkbox"
        )
        
        return github_handle, target_roles, repos_scope, limits, dry_run
    
    @staticmethod
    def _render_system_status(api_client: APIClient) -> None:
        """Render system status indicators."""
        st.subheader("System Status")
        
        with st.expander("Cache Status", expanded=False):
            cache_status = api_client.get_cache_status()
            st.json(cache_status)
        
        with st.expander("ML Model Status", expanded=False):
            ml_status = api_client.get_ml_status()
            st.json(ml_status)
    
    @staticmethod
    def _render_history_controls() -> None:
        """Render history management controls."""
        history = SessionStateManager.get_optimization_history()
        
        if history:
            st.markdown("---")
            st.caption(f"{len(history)} optimization(s) in history")
            
            if st.button("Clear History", use_container_width=True):
                SessionStateManager.clear_history()
                st.rerun()
    
    @staticmethod
    def render_welcome_screen() -> None:
        """Render welcome screen with feature overview."""
        st.markdown("""
        <div class="info-box">
            <p style="color:#8b949e;margin:0;">
                Configure your optimization parameters in the sidebar and click 
                <strong>Execute Optimization</strong> to begin the analysis.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.subheader("Enterprise Capabilities")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <h4 style="color:#58a6ff;margin-bottom:8px;">Multi-Tier Caching</h4>
                <p style="color:#8b949e;font-size:14px;margin:0;">
                    Advanced caching architecture with memory, Redis, and disk layers 
                    to minimize API calls and optimize performance
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <h4 style="color:#58a6ff;margin-bottom:8px;">Predictive Analytics</h4>
                <p style="color:#8b949e;font-size:14px;margin:0;">
                    Machine learning-powered recommendations for proactive profile 
                    enhancement and optimization
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="metric-card">
                <h4 style="color:#58a6ff;margin-bottom:8px;">Multi-Tenancy Support</h4>
                <p style="color:#8b949e;font-size:14px;margin:0;">
                    Isolated tenant environments with dedicated configurations for 
                    enterprise-scale deployment
                </p>
            </div>
            """, unsafe_allow_html=True)


# =============================================================================
# RESULTS DISPLAY COMPONENTS
# =============================================================================

class ResultsDisplay:
    """Handles rendering of optimization results across multiple tabs."""
    
    @staticmethod
    def render_tabs(result: Dict[str, Any]) -> None:
        """
        Render tabbed interface for comprehensive results display.
        
        Args:
            result: Optimization result dictionary from API
        """
        tabs = st.tabs([
            "Overview",
            "Profile Audit",
            "Recommendations",
            "Action Plan",
            "CI/CD Setup",
            "Safety & Compliance"
        ])
        
        with tabs[0]:
            ResultsDisplay.render_overview(result)
        
        with tabs[1]:
            ResultsDisplay.render_audit(result)
        
        with tabs[2]:
            ResultsDisplay.render_recommendations(result)
        
        with tabs[3]:
            ResultsDisplay.render_action_plan(result)
        
        with tabs[4]:
            ResultsDisplay.render_ci_setup(result)
        
        with tabs[5]:
            ResultsDisplay.render_safety_log(result)
    
    @staticmethod
    def render_overview(result: Dict[str, Any]) -> None:
        """Render overview dashboard with key metrics."""
        st.subheader("Optimization Overview")
        
        # Signal Model Weights Visualization
        ResultsDisplay._render_signal_weights(result)
        
        # Performance Benchmarking
        ResultsDisplay._render_benchmarking(result)
        
        # Profile Narrative
        ResultsDisplay._render_storytelling(result)
    
    @staticmethod
    def _render_signal_weights(result: Dict[str, Any]) -> None:
        """Render signal model weights chart."""
        st.markdown("### Recruiter Signal Importance")
        
        weights = result.get("signal_model", {}).get("weights", {})
        
        if not weights:
            st.info("No signal weight data available")
            return
        
        fig = go.Figure(data=[
            go.Bar(
                x=list(weights.keys()),
                y=list(weights.values()),
                marker_color=Config.COLOR_PRIMARY,
                marker_line_color=Config.BORDER_COLOR,
                marker_line_width=1,
                hovertemplate="<b>%{x}</b><br>Weight: %{y:.2f}<extra></extra>"
            )
        ])
        
        fig.update_layout(
            xaxis_title="Signal Type",
            yaxis_title="Weight",
            height=400,
            plot_bgcolor=Config.BG_PRIMARY,
            paper_bgcolor=Config.BG_PRIMARY,
            font_color='#c9d1d9',
            xaxis=dict(gridcolor=Config.BG_TERTIARY),
            yaxis=dict(gridcolor=Config.BG_TERTIARY),
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def _render_benchmarking(result: Dict[str, Any]) -> None:
        """Render performance benchmarking visualization."""
        benchmark = result.get("benchmarking", {})
        
        if not benchmark:
            return
        
        st.markdown("### Performance Benchmarking")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Baseline vs Target Metrics")
            baseline = benchmark.get("baseline", {})
            target = benchmark.get("targets", {})
            
            if baseline and target:
                # Ensure both dictionaries have the same keys
                metrics = list(set(baseline.keys()) & set(target.keys()))
                
                if not metrics:
                    st.info("No comparable metrics available")
                    return
                
                baseline_values = [baseline[m] for m in metrics]
                target_values = [target[m] for m in metrics]
                
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    name='Current Baseline',
                    x=metrics,
                    y=baseline_values,
                    marker_color=Config.COLOR_SECONDARY,
                    hovertemplate="<b>%{x}</b><br>Current: %{y}<extra></extra>"
                ))
                fig.add_trace(go.Bar(
                    name='Target Goal',
                    x=metrics,
                    y=target_values,
                    marker_color=Config.COLOR_PRIMARY,
                    hovertemplate="<b>%{x}</b><br>Target: %{y}<extra></extra>"
                ))
                
                fig.update_layout(
                    barmode='group',
                    height=400,
                    plot_bgcolor=Config.BG_PRIMARY,
                    paper_bgcolor=Config.BG_PRIMARY,
                    font_color='#c9d1d9',
                    xaxis=dict(gridcolor=Config.BG_TERTIARY),
                    yaxis=dict(gridcolor=Config.BG_TERTIARY),
                    legend=dict(bgcolor=Config.BG_SECONDARY),
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Scorecard")
            scorecard = benchmark.get("scorecard", [])
            
            if scorecard:
                scorecard_df = pd.DataFrame(scorecard)
                st.dataframe(
                    scorecard_df,
                    use_container_width=True,
                    height=400,
                    hide_index=True
                )
            else:
                st.info("No scorecard data available")
    
    @staticmethod
    def _render_storytelling(result: Dict[str, Any]) -> None:
        """Render profile narrative and storytelling elements."""
        storytelling = result.get("storytelling", {})
        
        if not storytelling:
            return
        
        st.markdown("### Profile Narrative")
        
        col1, col2 = st.columns(2)
        
        with col1:
            headline = storytelling.get("headline", "")
            if headline:
                st.markdown("#### Professional Headline")
                st.markdown(f"""
                <div class="metric-card">
                    <p style="color:#c9d1d9;font-size:16px;margin:0;">{headline}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            skills_matrix = storytelling.get("skills_matrix", [])
            if skills_matrix:
                st.markdown("#### Skills Matrix")
                skills_df = pd.DataFrame(skills_matrix)
                st.dataframe(skills_df, use_container_width=True, hide_index=True)
        
        # Flagship Projects
        flagship_projects = storytelling.get("flagship_projects", [])
        if flagship_projects:
            st.markdown("#### Flagship Projects")
            projects_df = pd.DataFrame(flagship_projects)
            st.dataframe(projects_df, use_container_width=True, hide_index=True)
    
    @staticmethod
    def render_audit(result: Dict[str, Any]) -> None:
        """Render comprehensive profile audit results."""
        st.subheader("Comprehensive Profile Audit")
        
        audit = result.get("current_audit", {})
        
        if not audit:
            st.info("No audit data available")
            return
        
        # Profile Summary
        ResultsDisplay._render_profile_summary(audit)
        
        # Pinned Repositories
        ResultsDisplay._render_pinned_repos(audit)
        
        # README Quality
        ResultsDisplay._render_readme_quality(audit)
        
        # Contribution Cadence
        ResultsDisplay._render_contribution_cadence(audit)
        
        # Discoverability
        ResultsDisplay._render_discoverability(audit)
        
        # CI Signals
        ResultsDisplay._render_ci_signals(audit)
    
    @staticmethod
    def _render_profile_summary(audit: Dict[str, Any]) -> None:
        """Render profile summary section."""
        profile_summary = audit.get("profile_summary", "")
        
        if profile_summary:
            st.markdown("### Profile Summary")
            st.markdown(f"""
            <div class="info-box">
                <p style="color:#c9d1d9;margin:0;">{profile_summary}</p>
            </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def _render_pinned_repos(audit: Dict[str, Any]) -> None:
        """Render pinned repositories analysis."""
        pinned_repos = audit.get("pinned_repos", [])
        
        if pinned_repos:
            st.markdown("### Pinned Repositories Analysis")
            pinned_df = pd.DataFrame(pinned_repos)
            st.dataframe(pinned_df, use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_readme_quality(audit: Dict[str, Any]) -> None:
        """Render README documentation quality assessment."""
        readme_quality = audit.get("readme_quality", [])
        
        if readme_quality:
            st.markdown("### README Documentation Quality")
            readme_df = pd.DataFrame(readme_quality)
            st.dataframe(readme_df, use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_contribution_cadence(audit: Dict[str, Any]) -> None:
        """Render contribution activity patterns."""
        cadence = audit.get("contribution_cadence", {})
        
        if cadence:
            st.markdown("### Contribution Activity Pattern")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                last_90d = cadence.get("last_90d", 0)
                st.metric("Last 90 Days", f"{last_90d} contributions")
            
            with col2:
                pattern = cadence.get("pattern", "Unknown")
                st.metric("Activity Pattern", pattern)
            
            with col3:
                consistency = cadence.get("consistency", "N/A")
                st.metric("Consistency Score", consistency)
    
    @staticmethod
    def _render_discoverability(audit: Dict[str, Any]) -> None:
        """Render profile discoverability analysis."""
        discoverability = audit.get("discoverability", {})
        
        if not discoverability:
            return
        
        st.markdown("### Profile Discoverability")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Profile Completeness")
            profile_elements = {
                "Biography": discoverability.get("bio", "Not set"),
                "Contact Information": discoverability.get("contact", "Not set"),
                "Skills": discoverability.get("skills", "Not set"),
                "Location": discoverability.get("location", "Not set"),
                "Website": discoverability.get("website", "Not set")
            }
            
            for key, value in profile_elements.items():
                status_icon = "✅" if value != "Not set" else "❌"
                st.markdown(f"{status_icon} **{key}:** {value}")
        
        with col2:
            links = discoverability.get("links", [])
            if links:
                st.markdown("#### External Links")
                for link in links:
                    st.markdown(f"🔗 {link}")
            else:
                st.info("No external links configured")
    
    @staticmethod
    def _render_ci_signals(audit: Dict[str, Any]) -> None:
        """Render CI/CD integration status."""
        ci_signals = audit.get("ci_signals", [])
        
        if ci_signals:
            st.markdown("### CI/CD Integration Status")
            ci_df = pd.DataFrame(ci_signals)
            st.dataframe(ci_df, use_container_width=True, hide_index=True)
    
    @staticmethod
    def render_recommendations(result: Dict[str, Any]) -> None:
        """Render actionable optimization recommendations."""
        st.subheader("Actionable Optimization Recommendations")
        
        recommendations = result.get("recommendations", [])
        
        if not recommendations:
            st.info("No recommendations available")
            return
        
        rec_df = pd.DataFrame(recommendations)
        
        # Validate required columns
        required_cols = ["effort", "impact", "category", "title"]
        if not all(col in rec_df.columns for col in required_cols):
            st.warning("Incomplete recommendation data structure")
            st.dataframe(rec_df, use_container_width=True, hide_index=True)
            return
        
        # Impact/Effort Matrix
        ResultsDisplay._render_impact_effort_matrix(rec_df)
        
        # Recommendations Table
        st.markdown("### Complete Recommendations List")
        st.dataframe(rec_df, use_container_width=True, hide_index=True)
        
        # Detailed View
        ResultsDisplay._render_recommendation_details(recommendations)
    
    @staticmethod
    def _render_impact_effort_matrix(rec_df: pd.DataFrame) -> None:
        """Render impact vs effort scatter plot."""
        st.markdown("### Impact vs Effort Analysis")
        
        fig = px.scatter(
            rec_df,
            x="effort",
            y="impact",
            color="category",
            hover_name="title",
            hover_data={"why": True} if "why" in rec_df.columns else {},
            size="impact",
            size_max=30,
            labels={
                "effort": "Effort Required",
                "impact": "Expected Impact",
                "category": "Category"
            }
        )
        
        fig.update_layout(
            height=500,
            xaxis_title="Effort Required (1-10)",
            yaxis_title="Expected Impact (1-10)",
            plot_bgcolor=Config.BG_PRIMARY,
            paper_bgcolor=Config.BG_PRIMARY,
            font_color='#c9d1d9',
            xaxis=dict(gridcolor=Config.BG_TERTIARY, range=[0, 11]),
            yaxis=dict(gridcolor=Config.BG_TERTIARY, range=[0, 11]),
            legend=dict(bgcolor=Config.BG_SECONDARY)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def _render_recommendation_details(recommendations: List[Dict[str, Any]]) -> None:
        """Render detailed view of selected recommendation."""
        st.markdown("### Detailed Recommendation Analysis")
        
        selected_rec = st.selectbox(
            "Select recommendation for detailed view",
            options=[rec["title"] for rec in recommendations],
            key="rec_detail_select"
        )
        
        for rec in recommendations:
            if rec["title"] == selected_rec:
                st.markdown(f"#### {rec['title']}")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Category", rec.get("category", "N/A"))
                
                with col2:
                    impact = rec.get("impact", 0)
                    st.metric("Impact Score", f"{impact}/10")
                
                with col3:
                    effort = rec.get("effort", 0)
                    st.metric("Effort Score", f"{effort}/10")
                
                st.markdown("**Rationale:**")
                why = rec.get("why", "No rationale provided")
                st.markdown(f"> {why}")
                
                signal_links = rec.get("signal_links", [])
                if signal_links:
                    st.markdown("**Related Signals:**")
                    for link in signal_links:
                        st.markdown(f"- {link}")
                
                break
    
    @staticmethod
    def render_action_plan(result: Dict[str, Any]) -> None:
        """Render execution action plan."""
        st.subheader("Execution Action Plan")
        
        plan = result.get("actions_plan", {})
        
        if not plan:
            st.info("No action plan available")
            return
        
        # Execution Mode Banner
        ResultsDisplay._render_execution_mode(plan)
        
        # Write Plan
        ResultsDisplay._render_write_plan(plan)
        
        # Commands
        ResultsDisplay._render_commands(plan)
        
        # Commit Messages
        ResultsDisplay._render_commit_messages(plan)
        
        # Pinned Plan
        ResultsDisplay._render_pinned_plan(result)
        
        # README Drafts
        ResultsDisplay._render_readme_drafts(result)
    
    @staticmethod
    def _render_execution_mode(plan: Dict[str, Any]) -> None:
        """Render execution mode indicator."""
        dry_run = plan.get("dry_run", True)
        mode_label = "Dry Run (Preview Only)" if dry_run else "Live Execution Mode"
        
        box_class = "info-box" if dry_run else "warning-box"
        
        st.markdown(f"""
        <div class="{box_class}">
            <p style="color:#c9d1d9;margin:0;"><strong>Execution Mode:</strong> {mode_label}</p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def _render_write_plan(plan: Dict[str, Any]) -> None:
        """Render planned file modifications."""
        write_plan = plan.get("write_plan", [])
        
        if write_plan:
            st.markdown("### Planned File Modifications")
            write_df = pd.DataFrame(write_plan)
            st.dataframe(write_df, use_container_width=True, hide_index=True)
        else:
            st.info("No file modifications planned")
    
    @staticmethod
    def _render_commands(plan: Dict[str, Any]) -> None:
        """Render shell commands to execute."""
        commands = plan.get("commands", [])
        
        if commands:
            st.markdown("### Shell Commands to Execute")
            for idx, cmd in enumerate(commands, 1):
                st.markdown(f"**Command {idx}:**")
                st.code(cmd, language="bash")
    
    @staticmethod
    def _render_commit_messages(plan: Dict[str, Any]) -> None:
        """Render generated commit messages."""
        commit_messages = plan.get("commit_messages", [])
        
        if commit_messages:
            st.markdown("### Generated Commit Messages")
            for idx, msg in enumerate(commit_messages, 1):
                st.markdown(f"**Commit {idx}:**")
                st.code(msg, language="text")
    
    @staticmethod
    def _render_pinned_plan(result: Dict[str, Any]) -> None:
        """Render repository pinning strategy."""
        pinned_plan = result.get("pinned_plan", {})
        
        if not pinned_plan:
            return
        
        st.markdown("### Repository Pinning Strategy")
        
        selected = pinned_plan.get("selected", [])
        if selected:
            st.markdown("#### Selected Repositories for Pinning")
            selected_df = pd.DataFrame(selected)
            st.dataframe(selected_df, use_container_width=True, hide_index=True)
        
        rerank_policy = pinned_plan.get("rerank_policy", {})
        if rerank_policy:
            st.markdown("#### Reranking Policy")
            st.json(rerank_policy)
    
    @staticmethod
    def _render_readme_drafts(result: Dict[str, Any]) -> None:
        """Render README documentation drafts."""
        readme_drafts = result.get("readme_drafts", {})
        
        if not readme_drafts:
            return
        
        st.markdown("### README Documentation Drafts")
        
        profile_readme = readme_drafts.get("profile", {})
        if profile_readme:
            st.markdown("#### Profile README")
            with st.expander("View Profile README Details"):
                st.json(profile_readme)
        
        repos_readme = readme_drafts.get("repos", [])
        if repos_readme:
            st.markdown("#### Repository README Updates")
            repo_readme_df = pd.DataFrame(repos_readme)
            st.dataframe(repo_readme_df, use_container_width=True, hide_index=True)
    
    @staticmethod
    def render_ci_setup(result: Dict[str, Any]) -> None:
        """Render CI/CD configuration recommendations."""
        st.subheader("CI/CD Configuration Recommendations")
        
        ci_setup = result.get("ci_setup", {})
        
        if not ci_setup:
            st.info("No CI/CD setup recommendations available")
            return
        
        # Workflows
        ResultsDisplay._render_workflows(ci_setup)
        
        # Coverage
        ResultsDisplay._render_coverage(ci_setup)
        
        # Badges
        ResultsDisplay._render_badges(ci_setup)
        
        # Contribution Coaching
        ResultsDisplay._render_contribution_coaching(result)
    
    @staticmethod
    def _render_workflows(ci_setup: Dict[str, Any]) -> None:
        """Render workflow configurations."""
        workflows = ci_setup.get("workflows", [])
        
        if workflows:
            st.markdown("### Recommended Workflow Configurations")
            workflows_df = pd.DataFrame(workflows)
            st.dataframe(workflows_df, use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_coverage(ci_setup: Dict[str, Any]) -> None:
        """Render code coverage configuration."""
        coverage = ci_setup.get("coverage", {})
        
        if coverage:
            st.markdown("### Code Coverage Configuration")
            st.json(coverage)
    
    @staticmethod
    def _render_badges(ci_setup: Dict[str, Any]) -> None:
        """Render recommended status badges."""
        badges = ci_setup.get("badges", [])
        
        if badges:
            st.markdown("### Recommended Status Badges")
            badges_df = pd.DataFrame(badges)
            st.dataframe(badges_df, use_container_width=True, hide_index=True)
    
    @staticmethod
    def _render_contribution_coaching(result: Dict[str, Any]) -> None:
        """Render contribution enhancement strategy."""
        coaching = result.get("contribution_coaching", {})
        
        if not coaching:
            return
        
        st.markdown("### Contribution Enhancement Strategy")
        
        weekly_plan = coaching.get("weekly_plan", [])
        if weekly_plan:
            st.markdown("#### Weekly Activity Plan")
            weekly_df = pd.DataFrame(weekly_plan)
            st.dataframe(weekly_df, use_container_width=True, hide_index=True)
        
        oss_suggestions = coaching.get("oss_suggestions", [])
        if oss_suggestions:
            st.markdown("#### Open Source Contribution Opportunities")
            oss_df = pd.DataFrame(oss_suggestions)
            st.dataframe(oss_df, use_container_width=True, hide_index=True)
        
        pr_checklist = coaching.get("pr_checklist", [])
        if pr_checklist:
            st.markdown("#### Pull Request Quality Checklist")
            for item in pr_checklist:
                st.markdown(f"- ✓ {item}")
        
        commit_style = coaching.get("commit_style", {})
        if commit_style:
            st.markdown("#### Commit Message Style Guide")
            st.json(commit_style)
    
    @staticmethod
    def render_safety_log(result: Dict[str, Any]) -> None:
        """Render safety and compliance audit log."""
        st.subheader("Safety & Compliance Audit Log")
        
        safety_log = result.get("safety_log", {})
        
        if not safety_log:
            st.info("No safety log data available")
            return
        
        # License Checks
        ResultsDisplay._render_license_checks(safety_log)
        
        # Ownership Verifications
        ResultsDisplay._render_ownership_verifications(safety_log)
        
        # Branch Protection
        ResultsDisplay._render_branch_protection(safety_log)
        
        # Secrets Scan
        ResultsDisplay._render_secrets_scan(safety_log)
        
        # Audit Trail
        ResultsDisplay._render_audit_trail(safety_log)
    
    @staticmethod
    def _render_license_checks(safety_log: Dict[str, Any]) -> None:
        """Render license compliance verification."""
        license_checks = safety_log.get("license_checks", [])
        
        if license_checks:
            st.markdown("### License Compliance Verification")
            for check in license_checks:
                st.code(check, language="text")
        else:
            st.info("No license checks recorded")
    
    @staticmethod
    def _render_ownership_verifications(safety_log: Dict[str, Any]) -> None:
        """Render repository ownership verification."""
        ownership_verifications = safety_log.get("ownership_verifications", [])
        
        if ownership_verifications:
            st.markdown("### Repository Ownership Verification")
            for verification in ownership_verifications:
                st.code(verification, language="text")
    
    @staticmethod
    def _render_branch_protection(safety_log: Dict[str, Any]) -> None:
        """Render branch protection analysis."""
        branch_protection_notes = safety_log.get("branch_protection_notes", [])
        
        if branch_protection_notes:
            st.markdown("### Branch Protection Analysis")
            for note in branch_protection_notes:
                st.code(note, language="text")
    
    @staticmethod
    def _render_secrets_scan(safety_log: Dict[str, Any]) -> None:
        """Render secrets detection scan results."""
        secrets_scan = safety_log.get("secrets_scan", [])
        
        if secrets_scan:
            st.markdown("### Secrets Detection Scan")
            for scan in secrets_scan:
                st.code(scan, language="text")
    
    @staticmethod
    def _render_audit_trail(safety_log: Dict[str, Any]) -> None:
        """Render complete audit trail."""
        audit_trail = safety_log.get("audit_trail", [])
        
        if audit_trail:
            st.markdown("### Complete Audit Trail")
            for entry in audit_trail:
                st.code(entry, language="text")


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def validate_inputs(
    github_handle: str,
    target_roles: List[str],
    github_token: str,
    openai_key: str
) -> Tuple[bool, Optional[str]]:
    """
    Validate user inputs before optimization.
    
    Args:
        github_handle: GitHub username
        target_roles: Selected target roles
        github_token: GitHub API token
        openai_key: OpenAI API key
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not github_handle or not github_handle.strip():
        return False, "GitHub username is required"
    
    if not target_roles:
        return False, "At least one target role must be selected"
    
    if not github_token or not github_token.strip():
        return False, "GitHub Personal Access Token is required"
    
    if not openai_key or not openai_key.strip():
        return False, "OpenAI API Key is required"
    
    return True, None


def main() -> None:
    """Main application entry point."""
    # Configure Streamlit page
    st.set_page_config(
        page_title="GitHub Profile Optimizer - Enterprise Edition",
        page_icon="⚙️",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://github.com/your-repo/issues',
            'Report a bug': 'https://github.com/your-repo/issues/new',
            'About': '# GitHub Profile Optimizer\nEnterprise-grade AI-powered optimization'
        }
    )
    
    # Initialize session state
    SessionStateManager.initialize()
    
    # Initialize API client
    api_client = APIClient()
    
    # Render header
    DashboardUI.render_header()
    
    # Render sidebar and get user inputs
    (
        optimize_clicked,
        github_handle,
        target_roles,
        repos_scope,
        limits,
        dry_run,
        tenant_id
    ) = DashboardUI.render_sidebar(api_client)
    
    # Handle optimization request
    if optimize_clicked:
        tenant_config = SessionStateManager.get_tenant_config()
        
        # Validate inputs
        is_valid, error_message = validate_inputs(
            github_handle,
            target_roles,
            tenant_config["github_token"],
            tenant_config["openai_key"]
        )
        
        if not is_valid:
            st.error(error_message)
            return
        
        # Create optimization request
        try:
            request = OptimizationRequest(
                github_handle=github_handle.strip(),
                target_roles=target_roles,
                repos_scope=repos_scope,
                dry_run=dry_run,
                limits=limits,
                tenant_id=tenant_id
            )
        except ValueError as e:
            st.error(f"Invalid request parameters: {str(e)}")
            return
        
        # Execute optimization
        with st.spinner(f"Executing profile optimization for {github_handle}..."):
            result = api_client.optimize_profile(
                request=request,
                github_token=tenant_config["github_token"],
                openai_key=tenant_config["openai_key"]
            )
            
            if result:
                SessionStateManager.add_optimization_result(
                    github_handle=github_handle,
                    result=result,
                    success=True
                )
                
                st.markdown(f"""
                <div class="success-box">
                    <p style="color:#c9d1d9;margin:0;">
                        Optimization analysis completed successfully for <strong>{github_handle}</strong>
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                ResultsDisplay.render_tabs(result)
            else:
                SessionStateManager.add_optimization_result(
                    github_handle=github_handle,
                    result={},
                    success=False,
                    error_message="Optimization failed"
                )
    
    elif SessionStateManager.get_latest_optimization():
        # Display most recent optimization
        latest = SessionStateManager.get_latest_optimization()
        
        if latest.success:
            st.markdown(f"""
            <div class="info-box">
                <p style="color:#c9d1d9;margin:0;">
                    Displaying most recent optimization for <strong>{latest.github_handle}</strong> 
                    (executed at {latest.timestamp.strftime('%Y-%m-%d %H:%M:%S')})
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            ResultsDisplay.render_tabs(latest.result)
        else:
            st.error(f"Previous optimization failed: {latest.error_message}")
            DashboardUI.render_welcome_screen()
    
    else:
        # Display welcome screen
        DashboardUI.render_welcome_screen()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align:center;color:#8b949e;font-size:14px;padding:16px 0;">
        <p style="margin:0;">GitHub Profile Optimizer - Enterprise Edition | Powered by AI</p>
        <p style="margin-top:8px;">For support and documentation, visit the project repository</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("Critical error in main application")
        st.error(f"Critical application error: {str(e)}")
        st.info("Please refresh the page or contact support if the issue persists.")
