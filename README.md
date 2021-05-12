![Dating_Site](https://user-images.githubusercontent.com/33484684/117993902-6ba22780-b340-11eb-82a3-4a1df776c091.png)
# dating_site
Dating site - (Make Love)
dating site with a percentage search for matches.

Site interface diagram - https://xd.adobe.com/view/b41176dc-2dff-4329-9bc6-946d9caa525b-e142/

---------------------------
install postgresql:
- sudo apt-get -y install postgresql
---------------------------
install redis-server:
- sudo apt install redis-server
---------------------------
You need to create a database and user from the beginning:
- sudo -u postgres psql
- CREATE DATABASE make_love_db;
- CREATE USER make_love_admin WITH PASSWORD 'makelovepassword';
- ALTER ROLE make_love_admin SET client_encoding TO 'utf8';
- ALTER ROLE make_love_admin SET default_transaction_isolation TO 'read committed';
- ALTER ROLE make_love_admin SET timezone TO 'UTC';
- GRANT ALL PRIVILEGES ON DATABASE make_love_db TO make_love_admin;
- \q

Then you need to add the hstore extension to your database:
https://docs.djangoproject.com/en/3.1/ref/contrib/postgres/operations/#creating-extension-using-migrations
---------------------------
comands for starting project:
1. python3 -m venv venv
2. source venv/bin/activate
3. pip3 install -r requirements.txt
4. sudo service postgresql restart - (if you need it)
5. sudo service redis-server start
6. python manage.py makemigrations
7. python manage.py migrate
8. python manage.py runserver
