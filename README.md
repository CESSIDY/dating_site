# dating_site
Dating site - (Make Love)
dating site with a percentage search for matches.

---------------------------
install postgresql:
- sudo apt-get -y install postgresql
---------------------------
install redis-server:
- sudo apt install redis-server
---------------------------
comands for starting project:
1. python3 -m venv venv
2. source venv
3. pip3 install -r requirements.txt
4. sudo service postgresql restart - (if you need it)
5. sudo service redis-server start
6. python manage.py runserver
