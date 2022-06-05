# Pre-requisites
For things to work as expected you need the following installed:

For development:
 - git
 - python3
 - pip

For running the api:
 - docker
 - docker-compose

# Setup
Clone the git
>git clone https://github.com/Zomgnomes/code-test.git

or download the zip file and extract it, then navigate to the folder you extracted or cloned into in your command prompt.

Next copy the `example.env` file to your own `.env` file
>cp example.env .env

Next, edit the `.env` file to use unique and complex passwords that meet your own security needs.  I would recommend changing the passwords in `DB_PASS`, `POSTGRES_PASSWORD`, and `SECRET_KEY` to something more secure at a minimum.

## Development Specific Setup (Optional)
I use a few development specific locally installed python packages to keep code formatted in a generic way and to alert me of any potential issues. If you'd like to contribute to this code base please follow these instructions for setup, so our code will match.

Using a virtual environment to avoid installing packages on your local system in the global space is optional, but highly recommended. 
To set one up run the following commands to create it and activate it.
>python3 -m venv .venv
>. .venv/bin/activate

Next install dev dependencies
>pip install -r requirements-dev.txt

Next install our pre-commit hooks
>pre-commit install

With pre-commit hooks and the dev dependencies installed, you should be all set to write and test the code.  To run the pre-commit hooks without running an actual commit you can run
`pre-commit run --all-files` otherwise they will just be run when you attempt to commit or push your code to the repo.

# Running the API
To run the api simply run
>docker-compose up --build --detach

The API should then be available for use on http://localhost:8000

## The Keys Routes
For the keys there are two main routes:
 - `http://localhost:8000/keys/`
   - which accepts a GET request to list all the available keys and their associated counter values in ascending alphabetical order by key name
 - `http://localhost:8000/keys/{name}`
   - Where {name} is replaced with the name of the key you'd like to interact with
   - This endpoint allows for GET, POST, PUT and DELETE requests, each with their own behavior:
     - GET - Returns the data about the key or a 404 not found status if no key is found.
     - POST - Creates a new key of the given name with a counter of 0 and return its data if one does not already exist and the length of the name is 100 characters or fewer.  Otherwise, a status of 400 bad request is returned.
     - PUT - Will increment the key and return its data or a 404 not found status if no key is found.
     - DELETE - Will delete the key with the corresponding name and return with a 204 no content status, or return a 404 not found status if no key is found.

