from fastapi import APIRouter

router = APIRouter()


@router.get('/')
def hi():
    return 'heyyyyy'
