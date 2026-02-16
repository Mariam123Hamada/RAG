# from sqlalchemy.orm import Session
# from fastapi import UploadFile, HTTPException
# from ..stores.schemas import ProjectSchema, ChunkSchema
# from ..models.Project import ProjectSplitters

# class ProjectServices:
#     def __init__(self):
#         # Your helper that handles the logic/splitting
#         self.splitter_helper = ProjectSplitters(chunk_size=500, chunk_overlap=50)

#     async def push_project(self, file: UploadFile, db: Session):
#         try:
#             # 1. Logic: Extract and Split text
#             await self.splitter_helper.initialize_splitter()
#             await self.splitter_helper.read_file(file)
#             raw_text_list = await self.splitter_helper.make_splitting()
            
#             # 2. Database: Create the Parent (Project)
#             new_project = ProjectSchema(
#                 total_chunks=len(raw_text_list),
#                 new_col=f"File: {file.filename}"
#             )
#             db.add(new_project)
            
            
#             db.flush() 

#             # 3. Database: Create the Children (Chunks)
#             for text in raw_text_list:
#                 # We take an INSTANCE of the Schema (The Table Class)
#                 db_chunk = ChunkSchema(
#                     content=text,
#                     project_id=new_project.project_id,
#                     embedding=[0.0] * 1536  # Must be 1536 to match Vector(1536)
#                 )
#                 db.add(db_chunk)

#             # 4. Make it permanent
#             db.commit()
            
#             return {
#                 "project_id": new_project.project_id,
#                 "chunks_saved": len(raw_text_list)
#             }

#         except Exception as e:
#             db.rollback()
#             raise HTTPException(status_code=500, detail=f"Failed to save: {str(e)}")


from sqlalchemy.orm import Session
from fastapi import UploadFile, HTTPException
from ..stores.schemas import ProjectSchema, ChunkSchema
from ..models.Project import ProjectSplitters


class ProjectServices:
    def __init__(self):
        self.splitter_helper = ProjectSplitters(
            chunk_size=500,
            chunk_overlap=50
        )

    async def push_project(self, file: UploadFile, db: Session):
        try:
            # 1️⃣ Extract and split text
            await self.splitter_helper.initialize_splitter()
            await self.splitter_helper.read_file(file)
            raw_text_list = await self.splitter_helper.make_splitting()

            if not raw_text_list:
                raise HTTPException(status_code=400, detail="File is empty or could not be processed.")

            # 2️⃣ Create parent project
            new_project = ProjectSchema(
                total_chunks=len(raw_text_list),
                new_col=f"File: {file.filename}",
                extra=""  # provide value if column not nullable
            )

            db.add(new_project)
            db.flush()  # get project_id without committing

            # 3️⃣ Create chunks
            for text in raw_text_list:
                db_chunk = ChunkSchema(
                    content=text,
                    project_id=new_project.project_id,
                    embedding=[0.0] * 1536  # must match Vector(1536)
                )
                db.add(db_chunk)

            # 4️⃣ Commit transaction
            db.commit()

            return {
                "project_id": new_project.project_id,
                "chunks_saved": len(raw_text_list)
            }

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Failed to save: {str(e)}"
            )
