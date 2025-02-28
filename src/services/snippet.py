from sqlalchemy.future import select

from src.db.db import db_dependency
from src.models.snippet import SnippetCode
from src.models.user import User


async def get_snippets_all(db: db_dependency, skip: int = 0, limit: int = 10):
    result = await db.execute(select(SnippetCode).offset(skip).limit(limit))
    return result.scalars().all()


async def get_snippet_id(db: db_dependency, snippet_id: int):
    result = await db.execute(select(SnippetCode).filter(SnippetCode.id == snippet_id))
    return result.scalars().first()


async def create_snippet(db: db_dependency, snippet: str, user: User):
    author = await db.execute(select(User).filter(User.email == user.get("sub")))
    db_user = author.scalar_one_or_none()
    if db_user is None:
        raise ValueError("User not found")
    db_snippet = SnippetCode(code=snippet, user=db_user)
    db.add(db_snippet)
    await db.commit()
    await db.refresh(db_snippet)
    return db_snippet


async def update_snippet(db: db_dependency, snippet_id: int, snippet: str):
    db_snippet = await get_snippet_id(db, snippet_id)
    if db_snippet:
        db_snippet.code = snippet
    await db.commit()
    await db.refresh(db_snippet)
    return db_snippet


async def delete_snippet(db: db_dependency, snippet_id: int):
    db_snippet = await get_snippet_id(db, snippet_id)
    if db_snippet:
        await db.delete(db_snippet)
        await db.commit()
    return db_snippet


async def get_snippet_share(db: db_dependency, share_id: str):
    result = await db.execute(select(SnippetCode).filter(SnippetCode.share_id == share_id))
    return result.scalars().first()

