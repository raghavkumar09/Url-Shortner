from datetime import datetime
from hashlib import sha256

from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import HttpUrl
from sqlalchemy.orm import Session

from api.database import get_db
from api.models import Url
from api.schemas import UrlResponse

router = APIRouter()


@router.get("/shorten", response_model=UrlResponse)
def shorten_url(longURL: HttpUrl, db: Session = Depends(get_db)):
    # Get url object from database
    url = db.query(Url).filter(Url.originalUrl == longURL).first()

    # Return URL if already exists
    if url:
        return url

    # Generate short url by adding current timestamp to url and taking first 10 characters of sha256 hash
    short_url = sha256(f"{longURL}-{datetime.now().timestamp()}".encode("utf-8")).hexdigest()[:10]

    # Add url to database
    url_obj = Url(originalUrl=longURL, shortUrl=short_url)
    db.add(url_obj)
    db.commit()

    # Return url response
    return url_obj


@router.get("/expand", response_model=UrlResponse)
def expand_url(shortURL: str, db: Session = Depends(get_db)):
    # Get url object from database
    url = db.query(Url).filter(Url.shortUrl == shortURL).first()

    # Return 404 if url not in database
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"URL with shortURL {shortURL} not found.")

    # Increase views to track opens
    url.views += 1

    # Add updated values to database
    db.add(url)
    db.commit()

    # Return url response
    return url


@router.get("/delete")
def delete_url(shortURL: str, db: Session = Depends(get_db)):
    # Get url object from database
    url = db.query(Url).filter(Url.shortUrl == shortURL).first()

    # Return 404 if url not in database
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"URL with shortURL {shortURL} not found.")

    # Delete url from database
    db.delete(url)
    db.commit()

    # Return url response
    return {"message": f"URL with shortURL {shortURL} deleted successfully."}
