from typing import Optional, List

from fastapi import APIRouter, Depends
from starlette import status
from starlette.responses import JSONResponse

from src.models.repository import Repository as ModelRepository
from src.models.user import ProviderType, User as ModelUser
from src.providers.dealer import Dealer
from src.schemas.repository import Repository
from src.schemas.user import UserOutputRepos
from src.services.database import get_con, SESSION

router = APIRouter()


@router.get('/{username}', response_model=UserOutputRepos, status_code=status.HTTP_200_OK)
def get_user(username: str, provider: ProviderType,
             from_local: Optional[bool] = False, data_base: SESSION = Depends(get_con)):
    if from_local:
        user = ModelUser.get_user_by_username(username=username, db_session=data_base)
        if not user:
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                                content='User not found in database')

        repositories = ModelRepository.get_all_from_local(db_session=data_base, user_id=user.id)
        names = [repository.name for repository in repositories]
        return UserOutputRepos(id=user.id,
                               login=user.login,
                               email=user.email,
                               twitter_username=user.twitter_username,
                               repos=names)
    source = Dealer.get_provider(provider=provider)
    user = source.get_user(username=username)
    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content='User not found remotely')

    repositories = source.get_all_repos(username=username)
    names = [repository.name for repository in repositories]

    return UserOutputRepos(id=user.id,
                           login=user.login,
                           email=user.email,
                           twitter_username=user.twitter_username,
                           repos=names)


@router.get('/repos/{username}', status_code=status.HTTP_200_OK, response_model=List[Repository])
def get_all_repositories(username: str, provider: ProviderType):
    source = Dealer.get_provider(provider=provider)

    repositories = source.get_all_repos(username=username)
    if not repositories:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content='User not found in remotely')
    return repositories


@router.get('/{username}/{repository_name}', status_code=status.HTTP_200_OK,
            response_model=Repository)
def get_repositories(username: str, repository_name: str, provider: ProviderType,
                     save_data: bool, data_base: SESSION = Depends(get_con)):
    source = Dealer.get_provider(provider=provider)

    repository = source.get_repository(username=username,
                                       repository_name=repository_name)
    if save_data:
        user = source.get_user(username=username)
        if not ModelUser.get_user_by_id(db_session=data_base, index=user.id, provider=provider):
            model_user = ModelUser(id=user.id,
                                   login=user.login,
                                   email=user.email,
                                   twitter_username=user.twitter_username,
                                   provider=provider)
            status_user, message = model_user.save(connection=data_base)

            if not status_user:
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    content=dict(message='Database error', details=message))

        if not ModelRepository.get_by_id(db_session=data_base, index=repository.id):
            model_repository = ModelRepository(id=repository.id,
                                               user_id=user.id,
                                               name=repository.name,
                                               private=repository.private,
                                               created_at=repository.created_at,
                                               updated_at=repository.updated_at,
                                               size=repository.size,
                                               stars=repository.stars,
                                               watchers=repository.watchers)
            status_repository, message = model_repository.save(connection=data_base)

            if not status_repository:
                return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                    content=dict(message='Database error', details=message))
    return repository


@router.delete('delete/{username}')
def delete_user(username: str, provider: ProviderType, data_base: SESSION = Depends(get_con)):
    source = Dealer.get_provider(provider=provider)
    user = source.get_user(username=username)
    user = ModelUser.get_user_by_id(db_session=data_base, index=user.id, provider=provider)
    if user:
        user.delete(connection=data_base)
    return 'User deleted'


@router.delete('delete/{username}/{repository_name}')
def delete_repo(username: str, repository_name: str,
                provider: ProviderType, data_base: SESSION = Depends(get_con)):
    source = Dealer.get_provider(provider=provider)
    repository = source.get_repository(username=username,
                                       repository_name=repository_name)
    repository = ModelRepository.get_by_id(db_session=data_base, index=repository.id)
    if repository:
        repository.delete(connection=data_base)
    return 'Repository deleted'


