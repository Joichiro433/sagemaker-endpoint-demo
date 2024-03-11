# SageMaker エンドポイント プロジェクト

このプロジェクトは、AWS SageMaker 上で 既に学習済みのモデル SageMaker エンドポイントにデプロイし、推論サーバーを構築するためのものです。

アーキテクチャは以下の通りです。

![sagemaker-lightgbm](https://github.com/Joichiro433/vertex_ai_endpints_demo/assets/64533928/90691d58-f054-4441-a4d3-468978decb1a)

以下のステップに従って、モデルのデプロイを行えます。

### 1. 学習済みモデルを SageMaker にデプロイする

SageMaker は jupyter notebook 上から直接リソースの管理が行えます。

1. AWS で、SageMaker ノートブックインスタンスを立ち上げる
2. `sagemaker_src/` にあるファイル一式をノートブックインスタンスにアップロードする
3. インスタンス上で `sagemaker_src/deploy.ipynb` を開き、セルを上から実行する（アップロードする S3 URI 等必要な変数を置き換えてください）
4. これでデプロイ完了。AWSコンソール上で、Amazon SageMaker / 推論 / エンドポイント から 確認できる

（以下は REST API を作成する際に必要）

### 2. Lambda の作成

1. AWS コンソールで Lambda 関数を作成する
2. `lambda_src/lambda_function.py` をデプロイする
3. 環境変数に `SAGEMAKER_ENDPOINT={デプロイしたSageMakerエンドポイントの名前}` を設定する。エンドポイントの名前は AWS コンソールで確認できる
4. lambda 関数に SageMaker を呼び出せる適切な権限が付与されていることを確認する

### 3. API Gateway の作成

1. AWS コンソールから API Gateway で API (REST API の構築を選ぶ) を作成する
2. メソッドの作成から POST で 統合タイプを Lambda 関数 にする
3. ② で作成した lambda 関数を選択する

以上。