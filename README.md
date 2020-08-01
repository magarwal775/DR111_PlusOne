# DR111_PlusOne
The Repository of Team PlusOne for SIH 2020 for the problem statement DR111 - Alumni Tracking System

To run this repository:

Run this command in your terminal first:
`sudo apt install python3-venv postgresql postgresql-contrib`

Then,
1. `sudo -u postgres psql`

A new type of terminal will open with `postgres=#` starting tag.

Next in that terminal,

2. `CREATE DATABASE <project_name>`;
3. `CREATE USER <project_user> WITH PASSWORD '<user_password>';`
4. `ALTER ROLE <project_user> SET client_encoding TO 'utf8';`
5. `ALTER ROLE <project_user> SET default_transaction_isolation TO 'read committed';`
6. `ALTER ROLE <project_user> SET timezone TO 'UTC';`
7. `GRANT ALL PRIVILEGES ON DATABASE <project_name> TO <project_user>;`
8. `\q`

You will be back to the original terminal.

9. `mkdir SIH-Final && cd SIH-Final`
10. `git clone https://github.com/magarwal775/DR111_PlusOne.git`
11. `python3 -m venv venv`
12. `source venv/bin/activate`
13. `cd DR111_PlusOne`
14. `pip install -r requirements.txt`
15. `cp .env.example .env`
16. `Add your database name, user and password to the .env file. Keep host as localhost and port as null.`
17. `python manage.py makemigrations`
18. `python manage.py migrate`
19. `python manage.py runserver`

The website is now up and running at `http://localhost:8000/`
