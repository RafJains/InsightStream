from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.db.session import get_db

router = APIRouter()

@router.get("/content")
def get_all_content(db: Session = Depends(get_db)):
    query = text("SELECT * FROM content ORDER BY id;")
    result = db.execute(query)
    rows = result.mappings().all()
    return rows

@router.get("/content/{content_id}")
def get_content_by_id(content_id: int, db: Session = Depends(get_db)):
    query = text("SELECT * FROM content WHERE id = :content_id;")
    result = db.execute(query, {"content_id": content_id})
    row = result.mappings().first()

    if not row:
        return {"message": "Content not found"}

    return row

@router.get("/content/{content_id}/details")
def get_content_details(content_id: int, db: Session = Depends(get_db)):
    content_query = text("""
        SELECT *
        FROM content
        WHERE id = :content_id;
    """)
    content_result = db.execute(content_query, {"content_id": content_id})
    content_row = content_result.mappings().first()

    if not content_row:
        return {"message": "Content not found"}

    genres_query = text("""
        SELECT g.name
        FROM content_genres cg
        JOIN genres g ON cg.genre_id = g.id
        WHERE cg.content_id = :content_id
        ORDER BY g.name;
    """)
    genres_result = db.execute(genres_query, {"content_id": content_id})
    genres_rows = genres_result.mappings().all()
    genres = [row["name"] for row in genres_rows]

    platforms_query = text("""
        SELECT p.name
        FROM content_platforms cp
        JOIN platforms p ON cp.platform_id = p.id
        WHERE cp.content_id = :content_id
        ORDER BY p.name;
    """)
    platforms_result = db.execute(platforms_query, {"content_id": content_id})
    platforms_rows = platforms_result.mappings().all()
    platforms = [row["name"] for row in platforms_rows]

    ratings_query = text("""
        SELECT *
        FROM ratings
        WHERE content_id = :content_id
        ORDER BY id;
    """)
    ratings_result = db.execute(ratings_query, {"content_id": content_id})
    ratings_rows = ratings_result.mappings().all()
    ratings = [dict(row) for row in ratings_rows]

    summary_query = text("""
        SELECT content_id, unified_score, critic_score, audience_score, review_summary
        FROM content_summary
        WHERE content_id = :content_id;
    """)
    summary_result = db.execute(summary_query, {"content_id": content_id})
    summary_row = summary_result.mappings().first()

    summary = dict(summary_row) if summary_row else None

    return {
        "content": dict(content_row),
        "genres": genres,
        "platforms": platforms,
        "ratings": ratings,
        "summary": summary
    }