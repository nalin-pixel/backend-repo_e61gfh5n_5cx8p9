import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import db, create_document, get_documents
from schemas import Inquiry as InquirySchema, Project as ProjectSchema, Testimonial as TestimonialSchema

app = FastAPI(title="Mohamad Jamalo Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Mohamad Jamalo API Running"}


@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response


# --------- Schemas endpoint (for admin viewers) ---------
@app.get("/schema")
def get_schema_definitions():
    return {
        "models": [
            "inquiry",
            "project",
            "testimonial"
        ]
    }


# --------- Portfolio Projects ---------
class ProjectCreate(ProjectSchema):
    pass


@app.get("/projects", response_model=List[ProjectSchema])
def list_projects(niche: Optional[str] = None):
    if db is None:
        return []

    # Seed sample projects if collection empty
    if db["project"].count_documents({}) == 0:
        samples: List[dict] = [
            {
                "title": "SaaS Dashboard Promo",
                "niche": "UI Animation",
                "description": "Product-first motion with smooth UI transitions and feature highlights.",
                "tools": ["After Effects", "Figma", "Premiere"],
                "video_url": "https://cdn.coverr.co/videos/coverr-dashboard-5830/1080p.mp4",
                "thumbnail_url": "https://images.unsplash.com/photo-1551281044-8d8d0d8d0b68?q=80&w=1200&auto=format&fit=crop"
            },
            {
                "title": "E‑Commerce App Launch",
                "niche": "UI Animation",
                "description": "Hook-driven spot with animated flows, testimonials, and pricing moments.",
                "tools": ["After Effects", "Illustrator"],
                "video_url": "https://cdn.coverr.co/videos/coverr-mobile-app-8068/1080p.mp4",
                "thumbnail_url": "https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=1200&auto=format&fit=crop"
            },
            {
                "title": "Luxury Villa Walkthrough",
                "niche": "Real Estate",
                "description": "Cinematic pacing, gimbal shots, refined color grade, elegant overlays.",
                "tools": ["Premiere", "After Effects", "DaVinci"],
                "video_url": "https://cdn.coverr.co/videos/coverr-modern-house-6134/1080p.mp4",
                "thumbnail_url": "https://images.unsplash.com/photo-1505691938895-1758d7feb511?q=80&w=1200&auto=format&fit=crop"
            },
            {
                "title": "Urban Loft Showcase",
                "niche": "Real Estate",
                "description": "Edgy cuts, rhythmic beats, modern title cards, amenities focus.",
                "tools": ["Premiere", "After Effects"],
                "video_url": "https://cdn.coverr.co/videos/coverr-modern-apartment-4275/1080p.mp4",
                "thumbnail_url": "https://images.unsplash.com/photo-1524758631624-e2822e304c36?q=80&w=1200&auto=format&fit=crop"
            },
            {
                "title": "Restaurant Launch Reel",
                "niche": "Commercial Reels",
                "description": "High-tempo macro shots, logo sting, offer CTA.",
                "tools": ["Premiere", "After Effects"],
                "video_url": "https://cdn.coverr.co/videos/coverr-cooking-in-a-pan-8697/1080p.mp4",
                "thumbnail_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=1200&auto=format&fit=crop"
            },
            {
                "title": "Retail Brand Drop",
                "niche": "Commercial Reels",
                "description": "Drop reveals, split screens, kinetic type, price tags in motion.",
                "tools": ["Premiere", "After Effects"],
                "video_url": "https://cdn.coverr.co/videos/coverr-a-woman-shopping-8157/1080p.mp4",
                "thumbnail_url": "https://images.unsplash.com/photo-1544441893-675973e31985?q=80&w=1200&auto=format&fit=crop"
            }
        ]
        for s in samples:
            create_document("project", s)

    filter_dict = {"niche": niche} if niche else {}
    docs = get_documents("project", filter_dict)

    # Convert ObjectId and timestamps to serializable
    for d in docs:
        d["id"] = str(d.pop("_id", ""))
        if "created_at" in d:
            d["created_at"] = str(d["created_at"])
        if "updated_at" in d:
            d["updated_at"] = str(d["updated_at"])
    return docs


# --------- Inquiries ---------
class InquiryCreate(InquirySchema):
    pass


@app.post("/inquiries")
def create_inquiry(payload: InquiryCreate):
    try:
        inserted_id = create_document("inquiry", payload)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------- Testimonials (placeholder read-only) ---------
@app.get("/testimonials", response_model=List[TestimonialSchema])
def list_testimonials():
    if db is None:
        return []
    # Seed sample placeholders if empty
    if db["testimonial"].count_documents({}) == 0:
        placeholders = [
            {"quote": "Super fast and super clean. The UI motion felt premium and on-brand.", "client_name": None, "role": None, "region": None},
            {"quote": "Our property sold faster with the video front and center.", "client_name": None, "role": None, "region": None},
            {"quote": "The reel outperformed our previous ads — clear hooks and sharp pacing.", "client_name": None, "role": None, "region": None},
            {"quote": "Great communication and delivery exactly as promised.", "client_name": None, "role": None, "region": None}
        ]
        for t in placeholders:
            create_document("testimonial", t)

    docs = get_documents("testimonial")
    for d in docs:
        d["id"] = str(d.pop("_id", ""))
    return docs


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
