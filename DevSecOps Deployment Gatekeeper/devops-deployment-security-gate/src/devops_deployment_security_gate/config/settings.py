"""
Configuration settings for the DevSecOps Deployment Gatekeeper.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    # Application Settings
    app_name: str = "DevSecOps Deployment Gatekeeper"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Security Settings
    secret_key: str = Field(default="dev-secret-key", env="SECRET_KEY")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # GitHub Integration
    github_token: str = Field(default="dev-github-token", env="GITHUB_TOKEN")
    github_webhook_secret: str = Field(default="dev-webhook-secret", env="GITHUB_WEBHOOK_SECRET")
    github_api_base_url: str = "https://api.github.com"
    
    # SonarQube Integration
    sonarqube_url: str = Field(default="https://sonarqube.example.com", env="SONARQUBE_URL")
    sonarqube_token: str = Field(default="dev-sonarqube-token", env="SONARQUBE_TOKEN")
    sonarqube_timeout: int = 300
    sonarqube_poll_interval: int = 10
    
    # Slack Integration
    slack_bot_token: str = Field(default="dev-slack-token", env="SLACK_BOT_TOKEN")
    slack_signing_secret: str = Field(default="dev-slack-signing-secret", env="SLACK_SIGNING_SECRET")
    slack_notification_channel: str = "#security-alerts"
    
    # AI/ML Settings
    openai_api_key: str = Field(default="dev-openai-key", env="OPENAI_API_KEY")
    openai_model: str = "gpt-4"
    openai_temperature: float = 0.2
    
    # Security Policies
    critical_vulnerability_threshold: int = 0
    major_vulnerability_threshold: int = 5
    allow_manual_override: bool = False
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Monitoring
    enable_metrics: bool = True
    metrics_port: int = 8090
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

# Create global settings instance
settings = Settings()