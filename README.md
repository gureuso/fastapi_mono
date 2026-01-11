# FastAPI Mono
FastAPI Mono example

python >= 3.12

# Usage

### 1. install virtualenv
```sh
$ pip install virtualenv
$ virtualenv -p python3 venv
```

```sh
$ . venv/bin/activate # mac, linux
$ call venv\Scripts\activate # windows
$ . venv/Scripts/activate # windows git bash
```

```sh
$ pip install -r requirements.txt
```

### 2. set environment or create config.json
| Name             | Description                                  |
| ---------------- |----------------------------------------------|
| APP_MODE         | choose from production, development, testing |
| APP_HOST         | ip address ex) 0.0.0.0                       |
| APP_PORT         | port number ex) 8888                         |
| DB_USER_NAME     | db user name                                 |
| DB_USER_PASSWD   | db user password                             |
| DB_HOST          | db host ex) devmaker.kr                      |
| DB_NAME          | db name                                      |
| REDIS_HOST       | redis ip address default) localhost          |
| REDIS_PASSWD     | redis password default) None                 |

### 3. db migrate
```mysql
# mysql
create database Mono
```

```sh
$ alembic upgrade head
```
create db and migrate tables
