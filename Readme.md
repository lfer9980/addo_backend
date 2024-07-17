# ADDO
## Setting Up

### Create env
```shell
conda create --name <PROEJCT NAME> python=3.10
```

```shell
conda activate <PROEJCT NAME>
```

### Install dependencies
```shell
pip install -r requiriments.txt
```

## ENV
Create .env on core folder with the next data
```shell
DB_URL=db_url
ADMIN_USERNAME=admin_username
ADMIN_PASSWORD=admin_pss
ENV=production | development
```

## Setup Alembic
### create directory versions
```shell
	cd alembic 
	mkdir versions
```
### Generate Initial Migration
```shell
alembic revision --autogenerate -m "Initial migration"
```

### Apply Migrations
```shell
alembic upgrade head
```

## Run the test
```shell
python -m unittest .\app\test\<TEST_NAME>.py
```

## Run the Application

### uvicorn (Best Option)
```shell
uvicorn app:app --reload
```

### Python
```shell
python main.py
```
