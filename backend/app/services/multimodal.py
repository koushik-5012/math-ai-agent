from fastapi import HTTPException
from typing import Dict

# These stubs must exist so imports do not break

async def process_image(file) -> Dict[str, str]:
    raise HTTPException(
        status_code=501,
        detail="Image processing temporarily disabled. Logic moved to router."
    )

async def process_audio(file) -> Dict[str, str]:
    raise HTTPException(
        status_code=501,
        detail="Audio processing temporarily disabled. Logic moved to router."
    )
