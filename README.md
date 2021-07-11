# Straattaal

Ever wanted to generate new Dutch slang? Look no further! This application makes use of Recurrent Neural Networks trained on a comprehensive database of Dutch slang to generate new slang. Some words may immediately bring up a visceral feeling of what they mean, and this application allows you to provide the community with your interpretation of what the newly created slang means.

## How to use?

Instructions on how to run this application locally. If you don't have Postgres set up (with the correct environment variables), it should run a SQLite database with more or less the same functionality. This should be sufficient for testing purposes and making tweaks to the code. Everything in ```these blocks``` are considered terminal commands.

*  ```git clone https://github.com/Sasafrass/straattaal```
* Navigate to the directory where you cloned using your terminal, e.g. ```cd straattaal```
* ```python3 -m venv venv ``` or ```python -m venv venv``` depending on your Python installation to create a new virtual environment within the working directory.
* ```source venv/bin/activate``` to activate your new virtual environment.
* ```python -m pip install -r requirements.txt``` or with python3 depending on your Python installation.
* ```flask db upgrade``` migrate your database to the latest schema.
* ```flask run```
* You should now be able to access a fully working local copy at http://localhost:5000

