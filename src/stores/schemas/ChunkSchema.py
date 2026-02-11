from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from pgvector.sqlalchemy import Vector

class Base(DeclarativeBase):
    pass

class ChunkSchema(Base):
    __tablename__ = "chunks"
    
    chunk_id = Column(Integer, primary_key=True, nullable=False)
    content = Column(Text, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    embedding = Column(Vector(1536))  
    new_col=Column(Integer(nullable=False))

    # Relationship back to project
    project = relationship("ProjectSchema", back_populates="chunks")