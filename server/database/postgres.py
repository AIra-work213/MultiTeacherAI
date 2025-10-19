from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import String, Integer, DateTime, func, BigInteger, select
import asyncio
import os

DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_NAME = os.getenv("DB_NAME", "dbname")
DB_HOST = os.getenv("DB_HOST", "postgres")
engine = create_async_engine(f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class DocumentMetadata(Base):
    __tablename__ = "document_metadata"

    document_id = mapped_column(Integer, primary_key=True) # Надо подумать
    uploader_id = mapped_column(BigInteger)
    file_name = mapped_column(String)
    file_type = mapped_column(String)
    topic = mapped_column(String)
    topic_id = mapped_column(Integer)
    uploaded_date = mapped_column(DateTime(timezone=True), server_default=func.now())

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def insert_metadata(metadata: dict):
    async with async_session_factory() as session:
        new_metadata = DocumentMetadata(
            uploader_id=metadata["user_id"],
            file_name=metadata["file_name"],
            file_type=metadata["file_type"],
            topic=metadata["topic"],
            topic_id=metadata["topic_id"]
        )
        session.add(new_metadata)
        await session.commit()

async def find_metadata_by_id(user_id: int):
    async with async_session_factory() as session:
        query = select(DocumentMetadata.topic, DocumentMetadata.topic_id).where(DocumentMetadata.uploader_id == user_id).order_by(DocumentMetadata.uploaded_date.desc())
        result = await session.execute(query)
        return [{"topic": row.topic, "topic_id": row.topic_id} for row in result.fetchall()]

async def find_max_topic_id():
    async with async_session_factory() as session:
        query = select(func.max(DocumentMetadata.topic_id))
        result = await session.execute(query)
        max_id = result.scalar()
        return max_id if max_id is not None else 0

async def find_topic_id(topic, user_id):
    async with async_session_factory() as session:
        query = select(DocumentMetadata.topic_id).where(DocumentMetadata.topic == topic, DocumentMetadata.uploader_id == user_id)
        result = await session.execute(query)
        if result.rowcount == 0:
            return
        return [{"topic_id": row.topic_id} for row in result.fetchall()][0]

if __name__ == "__main__":
    asyncio.run(init_db())