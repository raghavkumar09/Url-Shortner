from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Url
from api.schemas import UrlWithAnalytics

router = APIRouter()


@router.get("/views", response_model=UrlWithAnalytics)
def get_url_views(shortURL: str, db: Session = Depends(get_db)):
    # Get url object from database
    url = db.query(Url).filter(Url.shortUrl == shortURL).first()

    # Return 404 if url not in database
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"URL with shortURL {shortURL} not found.")

    # Return url response with views
    return url


@router.get("/most_viewed", response_model=list[UrlWithAnalytics])
def get_most_viewed_urls(count: int, db: Session = Depends(get_db)):
    # Return top "count" most viewed url objects
    return db.query(Url).order_by(Url.views.desc()).limit(count).all()
