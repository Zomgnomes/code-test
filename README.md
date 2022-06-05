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

Next, edit the `.env` file to use unique and complex passwords that meet your own security needs.  I would recommend changing the password in `DB_PASS` and `POSTGRES_PASSWORD` to something more secure at a minimum.

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
`pre-commit` otherwise they will just be run when you attempt to commit or push your code to the repo.

# Running the API
To run the api simply run
>docker-compose up --build --detach

The API should then be available for use on http://localhost:8000