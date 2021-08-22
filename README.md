[![Build Status](https://app.travis-ci.com/Sasafrass/straattaal.svg?branch=master)](https://app.travis-ci.com/Sasafrass/straattaal)
# Straattaal
Ever wanted to generate new Dutch slang? Look no further! This application makes use of Recurrent Neural Networks trained on a comprehensive database of Dutch slang to generate new slang. Some words may immediately bring up a visceral feeling of what they mean, and this application allows you to provide the community with your interpretation of what the newly created slang means.

## Examples
We have several pre-trained models available to generate novel words from multiple classes. The following is a selection of some of our favorite generated words per category. Can you come up with a better meaning for the slang words?

### Straattaal
- **rampa:** Een grote ramp / A big disaster.
- **joeko:** Groot / Big.
- **opjo:** Cool / cool.
- **daggie:** Een mes / A knife.
- **zittie:** Irritant / Annoying.

### Plaatsnamen
- Boschem
- De Heel
- Echterberg
- Zeernenbroek
- Schoosnijk

### Dutch words in general
- tertokraat
- gebelenster
- besteerding
- verstrijf
- wulveroeking



## How to use?

Instructions on how to run this application locally. If you don't have Postgres set up (with the correct environment variables), it should run a SQLite database with more or less the same functionality. This should be sufficient for testing purposes and making tweaks to the code. Everything in ```these blocks``` are considered terminal commands.

*  ```git clone https://github.com/Sasafrass/straattaal```
* Navigate to the directory where you cloned using your terminal, e.g. ```cd straattaal```
* Use an environment manager to install the packages: either venv and pip
** ```python3 -m venv venv ``` or ```python -m venv venv``` depending on your Python installation to create a new virtual environment within the working directory.
** ```source venv/bin/activate``` to activate your new virtual environment.
** ```python -m pip install -r requirements.txt``` or with python3 depending on your Python installation.
* Or, alternatively, conda:
** ```conda env create -f environment.yml```
** ```conda activate straattaal```
* ```flask db upgrade``` migrate your database to the latest schema.
* ```flask run```
* You should now be able to access a fully working local copy at http://localhost:5000

#### Run with Docker

This project can also be run with Docker in the following way:

* Create a .env file in the parent directory with the following variables: ```POSTGRES_USER=<postgres_user> POSTGRES_DB=<postgres_db> POSTGRES_PASSWORD=<postgres_password> PG_PORT=<postgres_port>``` (standard port is 5432)
* Then build and run docker-compose with ```docker-compose up --build```
* Database should be mounted to a volume, and thus data should be persisted between container restarts.
