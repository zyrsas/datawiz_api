web: gunicorn runp-datawiz_api:app
init: python db_create.py && pybabel compile -d app/datawiz_api
upgrade: python db_upgrade.py && pybabel compile -d app/datawiz_api
