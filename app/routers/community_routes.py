from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas import Community, CommunityUpdate, DefaultResponse, HTTPErrorRequest
from app.utils.communities import CommunitiesService
from app.depends import get_db_session


community_router = APIRouter(prefix="/community", tags=["Community"])

@community_router.get("/")
def get_communities(db: Session = Depends(get_db_session)):
    communitiesService = CommunitiesService(db)
    return communitiesService.get_communities()

@community_router.get("/{community_id}", response_model=Community, status_code=status.HTTP_200_OK)
def get_community_by_id(community_id: int, db: Session = Depends(get_db_session)):
    communitiesService = CommunitiesService(db)
    return communitiesService.get_community_by_id(community_id)

@community_router.get("/search/{community_name}", response_model=list[Community], status_code=status.HTTP_200_OK)
def get_communities_by_name(community_name: str, db: Session = Depends(get_db_session)):
    communitiesService = CommunitiesService(db)
    return communitiesService.get_communities_by_name(community_name)

@community_router.post("/", status_code=201, response_model=DefaultResponse, responses={400: {"description": "Comunidade já cadastrada", "model": HTTPErrorRequest}})
def create_community(community: Community, db: Session = Depends(get_db_session)):
    communitiesService = CommunitiesService(db)
    communitiesService.create_community(community)
    return JSONResponse(content={'msg':'Sucesso na criação da comunidade'} ,status_code=status.HTTP_201_CREATED)

@community_router.put("/{community_id}", response_model=DefaultResponse, responses={400: {"description": "Comunidade já cadastrada", "model": HTTPErrorRequest}, 500: {"description": "Erro interno", "model": HTTPErrorRequest}})
def update_community(community_id: int, community: CommunityUpdate, db: Session = Depends(get_db_session)):
    communitiesService = CommunitiesService(db)
    return communitiesService.update_community(community_id, community)

@community_router.delete("/{community_id}", response_model=DefaultResponse, status_code=status.HTTP_200_OK, responses={404: {"description": "Comunidade não encontrada", "model": HTTPErrorRequest}, 500: {"description": "Erro interno", "model": HTTPErrorRequest}})
def delete_community(community_id: int, db: Session = Depends(get_db_session)):
    communitiesService = CommunitiesService(db)
    return communitiesService.delete_community(community_id)


