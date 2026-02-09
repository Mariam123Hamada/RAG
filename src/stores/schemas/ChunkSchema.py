from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from pgvector.sqlalchemy import Vector

class Base(DeclarativeBase):
    pass

class ProjectSchema(Base):
    __tablename__ = "projects"
    
    project_id = Column(Integer, primary_key=True, nullable=False)
    total_chunks = Column(Integer, nullable=False)

    # One-to-many relationship with chunks
    chunks = relationship("ChunkSchema", back_populates="project")


