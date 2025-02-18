# Data Management System for HackerFab
This web portal is designed for **logging**, **tracking**, **analyzing**, and **organizing** important data, including critical machine parameters for different processes, the fabrication progress of each individual chip, the results gathered in testing, and so forth, to make the fab more efficient and to help us better understand the potential improvements that can be made.

Future development may also include the following without limitation:
1. A central control panel for all lab automations.
2. A fully automatic fab monitoring and warning system.
3. An online job management system that accepts VHDL / GDSII files directly (integration with EDA).
4. A universal communication protocol that can be used to interface all machines in the fab.
5. ...

## Usage
This project is built on Django.

**Note:** The following walkthrough is for debugging and testing only. To deploy in production, consider using a Apache2 or Nginx gateway with reverse proxy and Gunicorn for better stability and performance.

### Intialization
First, clone this repo to your working directory:
```
git clone https://github.com/hacker-fab/data-management.git
cd data-management
```
Install the requirements:
```
pip install -r requirements.txt
```
Before the first run, you should initialize the database:
```
python manage.py migrate
```
Note that now there is file named `db.sqlite3` at the root of the repo. 
That is the database.
If you ever want to transfer the data in a database from a computer to another or to backup them to some other places, just copy `db.sqlite3`.

To start the server, simply run:
```
python manage.py runserver
```

## License
See [LICENSE](LICENSE).
