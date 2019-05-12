# Python REST API --  Pet Hotel 

REST API using Flask, performs basic CRUD operations on two data tables in a PostreSQL db. It's paired with a React front end. Made as part of a team challenge to spin up a web server in an unfamiliar language.

[React front-end](https://github.com/wabens/react_pet_hotel)

## Built With

* Python3
* Flask
* Psycopg3
* PostgreSQL on Postico

## Getting Started

### Prerequisites

- [Python3](https://www.python.org/download/releases/3.0/)
- [Pip3](https://pip.pypa.io/en/stable/quickstart/)
- [PostgreSQL client like Postico](https://eggerapps.at/postico/)
- [Node.js](https://nodejs.org/en/) (to get front-end packages)


Should come with repo, if not install with pip3:
- [Flask](http://flask.pocoo.org/docs/1.0/)
- [psycopg2](https://www.python.org/download/releases/3.0/)


### Installing

Steps to get the development environment running.

1. Download this project.
2. Run queries in `python_hotel.sql`
3. Configure database stored in `mainConnection`
2. `export FLASK_APP=server/server.py`
3. `flask run`

To start front-end
1. Download [React UI](https://github.com/wabens/react_pet_hotel/)
2. `npm install`
3. `npm start`
4. Navigate to http://localhost:3000/


### Completed Features

- [x] CRUD for two tables
- [x] Database information displayed on DOM

### Next Steps

- [ ] Break up routes with a router
- [ ] More readable file structure


## Authors

* [Bradley Hennen](https://github.com/BradleyHennen)
* [Lili Bourgeois](https://github.com/lbourgeois90)
* [Jarvis Yang](https://github.com/jwhy89)
