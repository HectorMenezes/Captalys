import json
from typing import Optional
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.models.user import User as ModelUser
from src.models.repository import Repository as ModelRepository
from src.schemas.user import UserOutput
from src.services.database import get_con, SESSION
import requests

router = APIRouter()


@router.get('/{username}')
def hi(username: str, from_local: Optional[bool] = False):
    user = ModelUser.create_from_git(username)

    if not from_local:
        repositories = ModelRepository.get_all_from_github(username)
        repositories_names = []

        for repository in repositories:
            repositories_names.append(repository.name)

        return dict(id=user.id,
                    login=user.login,
                    twitter_username=user.twitter_username,
                    email=user.email,
                    repositories=repositories_names)
    """
    repositories = ModelRepository.get_all_from_local(user.id)

    repositories_names = []

    for repository in repositories:
        repositories_names.append(repository.name)

    return dict(id=user.id,
                login=user.login,
                twitter_username=user.twitter_username,
                email=user.email,
                repositories=repositories_names)
    """


@router.get('/{username}/{reponame}')
def get_repo(username: str, reponame: str, save_data: bool, db: SESSION = Depends(get_con)):
    repo = ModelRepository.get_one_from_github(username=username, reponame=reponame)
    if repo.user_id is not None:
        try:
            ModelUser.exists(db_session=db, index=repo.user_id)
            return 'works'
        except Exception as error:
            print(error)
        return f'is not none but don work, {repo.user_id}'
    return 'Is none'


@router.delete('/{id}')
def delete_repo(index: int, db: SESSION = Depends(get_con)):
    repo = ModelRepository.get_by_id(index=index, db_session=db)
    if not repo:
        return
    status_user, message = repo.delete(connection=db)
    if status_user:
        return
    return JSONResponse(status_code=500,
                        content=dict(message='Database error', details=message))
