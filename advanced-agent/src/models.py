from typing import List, Optional, Dict, Any
from pydantic import BaseModel

# This module defines data models for structured outputs from LLMs.

# CompanyAnalysis is used to represent the structured output of an LLM analysis of a company or tool related to developer technologies.
class CompanyAnalysis(BaseModel):
    """Structured output for LLM company analysis focused on developer tools"""
    pricing_model: str  # Free, Freemium, Paid, Enterprise, Unknown
    is_open_source: Optional[bool] = None
    tech_stack: List[str] = []
    description: str = ""
    api_available: Optional[bool] = None
    language_support: List[str] = []
    integration_capabilities: List[str] = []

# CompanyInfo is used to represent detailed information about a company, including its name, description, website, and developer-specific fields.
class CompanyInfo(BaseModel):
    name: str
    description: str
    website: str
    pricing_model: Optional[str] = None
    is_open_source: Optional[bool] = None
    tech_stack: List[str] = []
    competitors: List[str] = []
    # Developer-specific fields
    api_available: Optional[bool] = None
    language_support: List[str] = []
    integration_capabilities: List[str] = []
    developer_experience_rating: Optional[str] = None  # Poor, Good, Excellent

# ResearchState is used to represent the state of a research session, including the query, extracted tools, companies found, search results, and analysis.
class ResearchState(BaseModel):
    query: str
    extracted_tools: List[str] = []  # Tools extracted from articles
    companies: List[CompanyInfo] = []
    search_results: List[Dict[str, Any]] = []
    analysis: Optional[str] = None