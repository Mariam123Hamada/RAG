from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import  relationship
from pgvector.sqlalchemy import Vector
from sqlalchemy.dialects.postgresql import UUID
import  uuid
from .BaseSchema import Base

class ChunkSchema(Base):
    __tablename__ = "chunks"
    
    chunk_id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    embedding = Column(Vector(3072))  
    
    # Relationship back to project
    project = relationship("ProjectSchema", back_populates="chunks")