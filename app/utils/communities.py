from sqlite3 import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.models import CommunityModel
from app.schemas import Community, DefaultResponse

class CommunitiesService:

    def __init__(self, db: Session):
        self.db = db

    def get_communities(self):
        communities = self.db.query(CommunityModel).all()
        if not communities:
            return []
        return communities
        
    def get_community_by_id(self, community_id: int) -> Community:
        result = self.db.query(CommunityModel).filter(CommunityModel.id == community_id).first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comunidade não encontrada")
        return result
        
    def get_communities_by_name(self, community_name: str) -> list[Community]:
        return self.db.query(CommunityModel).filter(CommunityModel.name.ilike(f"%{community_name}%")).all()
    
    def create_community(self, community: Community):
        db_community = CommunityModel(
            id=community.id,
            name=community.name,
        )
        try:
            self.db.add(db_community)
            self.db.commit()
            self.db.refresh(db_community)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Comunidade já cadastrada")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        
    def update_community(self, community_id: int, community: Community) -> DefaultResponse:
        db_community = self.get_community_by_id(community_id)
        try:
            db_community.name = community.name
            self.db.commit()
            self.db.refresh(db_community)
        except IntegrityError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Comunidade já cadastrada")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        return DefaultResponse(msg="Comunidade atualizada com sucesso")
    
    def delete_community(self, community_id: int):
        db_community = self.get_community_by_id(community_id)
        if not db_community:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comunidade não encontrada")
        try:
            self.db.delete(db_community)
            self.db.commit()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
        return DefaultResponse(msg="Comunidade deletada com sucesso")
            
        
    