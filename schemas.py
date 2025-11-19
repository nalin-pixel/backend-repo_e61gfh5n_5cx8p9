"""
Database Schemas for Mohamad Jamalo portfolio site

Each Pydantic model represents a collection in your database.
Class name lowercased = collection name
"""
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr

class Inquiry(BaseModel):
    """
    Client inquiries submitted via contact form
    Collection: "inquiry"
    """
    name: str = Field(..., description="Client full name")
    email: EmailStr = Field(..., description="Contact email")
    company: Optional[str] = Field(None, description="Company or brand")
    project_type: str = Field(..., description="UI Animation | Real Estate | Commercial Reels")
    budget: Optional[str] = Field(None, description="Budget range")
    deadline: Optional[str] = Field(None, description="Timeline or deadline")
    details: Optional[str] = Field(None, description="Project details and goals")
    consent: bool = Field(True, description="Consent to be contacted")

class Project(BaseModel):
    """
    Portfolio projects
    Collection: "project"
    """
    title: str
    niche: str = Field(..., description="UI Animation | Real Estate | Commercial Reels")
    description: str
    tools: List[str] = []
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None

class Testimonial(BaseModel):
    """
    Client testimonials (future use)
    Collection: "testimonial"
    """
    quote: str
    client_name: Optional[str] = None
    role: Optional[str] = None
    region: Optional[str] = None
