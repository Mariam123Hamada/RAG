from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from .BaseSchema import Base

class ProjectSchema(Base):
    __tablename__ = "projects"
    
    project_id = Column(Integer, primary_key=True, nullable=False)
    total_chunks = Column(Integer, nullable=False)
    project_name=Column(Text, nullable=True)
    
    chunks = relationship("ChunkSchema", back_populates="project")


