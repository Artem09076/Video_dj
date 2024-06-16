## Запуск


### 1. Clone
```
git clone https://github.com/Artem09076/Video_dj.git
cd Video_dj
```

### 2. Create docker
* Postgres(values can be different)
  ```
  docker run -d --name project -p 38700:5432 \
  -e POSTGRES_USER=sirius \
  -e POSTGRES_PASSWORD=123 \
  -e POSTGRES_DB=videos_db \
  postgres
  ```
* Minio(values can be different)
  ```
  docker run -d -p 9000:9000 -p 9001:9001 \
  -e "MINIO_ROOT_USER=sirius" \
  -e "MINIO_ROOT_PASSWORD=123" \
   minio/minio server /data --console-address ":9001"
  ```
### 3. Create schema in db
```
psql -h 127.0.0.1 -p 38700 -U sirius videos_db #password 123
CREATE SCHEMA video_data;
```

### 4. Creating an environment file
Now you need to create an .env file with the variables
* `PG_HOST` - postgres URL.
* `PG_PORT` - the port on which the database is launched.
* `PG_DBNAME` - Database name.
* `PG_USER` - postgres username.
* `PG_PASSWORD` - пароль postgres.
* `MINIO_ACCESS_KEY_ID` - minio username.
* `MINIO_SECRET_ACCESS_KEY` - minio password.
* `MINIO_STORAGE_BUCKET_NAME` - your created bucket.
* `MINIO_API` - minio url.

