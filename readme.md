# このAPIを使用するための準備

	1.	必要なパッケージのインストール
	    • SQLAlchemyのインストール
	    • FastAPIのインストール
	    • Alembicのインストール
	2.	Alembicの設定
	    • alembicの初期化後に設定ファイルを編集します。
	    • alembic.ini: データベースの接続情報を設定します。
	    • env.py: 使用するモデルをインポートしてください。
	注意: 詳細設定手順についてはここでは省略しています。

## ルーティングの設定

FastAPIでは、ルーティングを利用してAPIエンドポイントを定義します。ファイルを分割することでコードの可読性が向上します。

1. ルーターの作成 router.py

        from fastapi import APIRouter

        api_router = APIRouter()  # ルーターのインスタンスを作成

2. ルーターへの紐付け

        ルーターにエンドポイントを追加し、main.pyのFastAPIインスタンスに紐付けることで、エンドポイントにアクセス可能になります。

## サブルーターの作成
各APIのページでサブルーターを宣言<br>
router = APIRouter()

## ルーターの紐付け
router.py<br>
api_router.include_router(router, prefix="/hoge")

## main.py で FastAPI インスタンスに紐付け
app.include_router(api_router, prefix="/foo")

この設定で、http://localhost:8000/foo/hoge にアクセスできます。

## APIエンドポイントの実装例

    from fastapi import APIRouter, Depends
    from sqlalchemy.orm import Session
    from .schemas import HogeResponse
    from .database import get_db
    from .services import hogehoge  # サービス層の関数をインポート

    router = APIRouter()

    @router.get("/foo/{hoge}", response_model=HogeResponse, tags=["bar"])
    def hogehoge_api(hoge: int, db: Session = Depends(get_db)):
        return hogehoge(hoge, db)

## 説明

	1.	エンドポイントデコレーター

        @router.get("/foo/{hoge}", response_model=HogeResponse, tags=["bar"])

	    • パスパラメータ: "/foo/{hoge}"のhoge部分がパスパラメータとして使用されます。
	    • レスポンスモデル: response_modelで返却するデータの型を指定します。
	    • タグ: tagsでAPIの関連タグを指定します。

	2.	関数宣言

        def hogehoge_api(hoge: int, db: Session = Depends(get_db)):

	    • 引数:
	    • hoge: パスパラメータとして受け取る値。
	    • db: Session = Depends(get_db): get_db関数からデータベースのセッションを注入します。

	3.	戻り値
	    •response_modelで指定した型に基づき、戻り値を構成します。

## db: Session = Depends(get_db) の説明

	• get_dbはデータベースのセッションを提供するための関数で、database.py内で定義されていると仮定します。
	• Dependsを使用することで、APIが呼び出されるたびにデータベースの接続が確立され、処理が完了後に閉じられます。

# 非同期なAPIを作成する
データベースを扱う場合、非同期で行う方が効率的です。そこで非同期に対応した書き方の例を載せます。
まず、準備としてデータベースのドライバを非同期に対応したものをインストールする必要があります。

    • SQLiteを使用する場合
        pip install aiosqlite

次にFastAPIで非同期通信を行うためのプラグインをインストールします

    pip install greenlet

以下のコードでAPIのコードを記述します。

    @router.get("/async/todos",response_model=list[TodoResponse], tags=["async"])
    async def async_get_all_todos(db: AsyncSession = Depends(get_db)):
        """ 全てのTodoを取得する """
        return await get_all_todos(db)

pythonの非同期通信にはasync/awaitを使用します。<br>
またSessionクラスをAsyncSessionに変更しています。<br>

そのほかの書き方は同期通信のAPIと変わりないと思います。<br>

実装例

    ./async_database.py
    ./api/v1/todo/async_api.py