**steps to run**
1. git clone git@github.com:Arianhf/martin_deliver.git
2. cd martin_deliver
3. pip install pipenv
4. pipenv shell 
5. pipenv install -r requirements.txt
6. ./manage.py createsuperuser
7. ./manage.py makemigrations && ./manage.py migrate
8. ./manage.py runserver 8000
9. import postman collections and environment
