
## Rodar o django
python manage.py runserver

## Rodar as migrações
python manage.py makemigration && python manage.py migrate

## Django shell
python manage.py shell

## Testar com pytest com Runner
pytest

## Gerar o relatório html com coverage
coverage -m pytest && coverage html