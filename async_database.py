""" 非同期通信でSQLiteを使用するためのモジュール """
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# sqliteを非同期で使用するためにはドライバーを変更する必要がある
# pip install aiosqlite
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///test.db"

# データベースの設定
async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, 
    echo=False,
    connect_args={
        "check_same_thread": False,
        "timeout": 30
    }
)

# データベースとのやりとりを行うためのセッションを作成
AsyncSessionmaker = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine
)

# データベースとの接続を行う関数
async def get_db():
    """ Function to get a database session 
        Returns:
        Sessionmaker: A SQLAlchemy session to interact with the database
    """
    async with AsyncSessionmaker() as db:
        try:
            yield db
        finally:
            await db.close()
