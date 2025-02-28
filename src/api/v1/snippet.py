from fastapi import APIRouter, Depends, HTTPException

from src.schemas.snippet import SnippetsCode, SnippetCreate
from src.auth.auth import get_current_user
from src.services.snippet import *

snippet_router = APIRouter(prefix="/snippet", tags=['snippet'])


@snippet_router.get("/", responses={
    200: {"model": list},
    404: {"description": "Response not found"},
    400: {"description": "Invalid request"},
})
async def get_snippets(db: db_dependency, user: User = Depends(get_current_user)):
    snippets = await get_snippets_all(db)
    if snippets is None:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return snippets


@snippet_router.get("/{snippet_id}", responses={
    200: {"model": SnippetsCode},
    404: {"description": "Response not found"},
    400: {"description": "Invalid request"},
})
async def get_snippet(snippet_id: int, db: db_dependency, user: User = Depends(get_current_user)):
    snippet = await get_snippet_id(db, snippet_id)
    if snippet is None:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return snippet


@snippet_router.post("/create", response_model=SnippetsCode)
async def snippet_create(code: SnippetCreate, db: db_dependency, user: User = Depends(get_current_user)):
    return await create_snippet(db, code.text, user)


@snippet_router.put("/update/{snippet_id}", response_model=SnippetsCode)
async def snippet_update(snippet_id: int, text: SnippetCreate, db: db_dependency, user: User = Depends(get_current_user)):
    updated_snippet = await update_snippet(db=db, snippet_id=snippet_id, snippet=text.text)
    if updated_snippet is None:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return updated_snippet


@snippet_router.delete("/delete/{snippet_id}")
async def snippet_delete(snippet_id: int, db: db_dependency, user: User = Depends(get_current_user)):
    deleted_snippet = await delete_snippet(db, snippet_id)
    if deleted_snippet is None:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return deleted_snippet


@snippet_router.post("/create_share")
async def snippet_create_share(snippet_id: int, db: db_dependency, user: User = Depends(get_current_user)):
    snippet = await get_snippet_id(db, snippet_id)
    return {"share_url": f"http://localhost:8000/snippet/share/{snippet.share_id}"}


@snippet_router.get("/share/{share_id}", response_model=SnippetsCode)
async def snippet_get_share(share_id: str, db: db_dependency):
    snippet = await get_snippet_share(db, share_id)
    if snippet is None:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return snippet
