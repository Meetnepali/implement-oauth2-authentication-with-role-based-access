from fastapi import APIRouter, HTTPException, status, BackgroundTasks, Request
from schemas import ProfileCreate, ProfileUpdate, ProfileOut, ErrorResponse
from typing import Dict
from fastapi.responses import JSONResponse
import asyncio

router = APIRouter()

# Simulated in-memory 'database'
PROFILES: Dict[int, dict] = {}
NEXT_ID = 1

# Error utility
class ProfileAPIException(Exception):
    def __init__(self, detail: str, code: int = 400):
        self.detail = detail
        self.code = code

# Custom error handler
@router.exception_handler(ProfileAPIException)
async def profile_exception_handler(request: Request, exc: ProfileAPIException):
    return JSONResponse(
        status_code=exc.code,
        content=ErrorResponse(detail=exc.detail, code=exc.code).dict()
    )

@router.post("/", response_model=ProfileOut, status_code=201, responses={
    400: {"model": ErrorResponse},
    422: {"model": ErrorResponse},
})
async def create_profile(profile: ProfileCreate):
    global NEXT_ID, PROFILES
    for p in PROFILES.values():
        if profile.email == p['email']:
            raise ProfileAPIException('A profile with this email already exists.', 400)
    pid = NEXT_ID
    NEXT_ID += 1
    data = profile.dict()
    data['id'] = pid
    PROFILES[pid] = data
    return ProfileOut(**data)

@router.get("/{profile_id}", response_model=ProfileOut, responses={
    404: {"model": ErrorResponse},
    422: {"model": ErrorResponse},
})
async def get_profile(profile_id: int):
    profile = PROFILES.get(profile_id)
    if not profile:
        raise ProfileAPIException('Profile not found', 404)
    return ProfileOut(**profile)

async def process_avatar_update(profile_id: int, avatar_url: str):
    # Dummy background avatar update (simulate delay)
    await asyncio.sleep(0.2)
    # In real use, process image/copy to CDN etc.
    PROFILES[profile_id]['avatar_url'] = avatar_url

@router.put("/{profile_id}", response_model=ProfileOut, responses={
    400: {"model": ErrorResponse},
    404: {"model": ErrorResponse},
    422: {"model": ErrorResponse},
})
async def update_profile(
    profile_id: int,
    update: ProfileUpdate,
    background_tasks: BackgroundTasks
):
    profile = PROFILES.get(profile_id)
    if not profile:
        raise ProfileAPIException('Profile not found', 404)
    if update.email is not None:
        for pid, p in PROFILES.items():
            if pid != profile_id and p['email'] == update.email:
                raise ProfileAPIException('A profile with this email already exists.', 400)
    updated_data = profile.copy()
    for field, value in update.dict(exclude_unset=True).items():
        if value is not None:
            if field == 'avatar_url':
                # Launch background update for avatar_url
                background_tasks.add_task(process_avatar_update, profile_id, value)
            else:
                updated_data[field] = value
    # Only set avatar_url in foreground if NOT updated (to preserve background flow)
    if 'avatar_url' not in update.dict(exclude_unset=True):
        updated_data['avatar_url'] = profile.get('avatar_url')
    PROFILES[profile_id] = updated_data
    return ProfileOut(**updated_data)
