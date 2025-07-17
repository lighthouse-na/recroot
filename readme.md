# Telecom Recruitment System

## Project Overview

The Telecom Recruitment System is a web-based platform designed to streamline the recruitment process. It helps in managing job postings, candidate applications, and interview schedules.

## Features

- Job posting and management
- Candidate application tracking
- Interview scheduling
- Notifications and reminders for recruiters and candidates
- Admin panel for managing all aspects of the recruitment process

## Development Requirements

- Python 3.8 +
- Docker (optional, for containerized setup)
- SQLite3

<<<<<<< HEAD
## Setup

### Disclaimer

- This script has not been fully tested on Windows or Mac systems so there might be challenges. Please use the internet and then contact [Sakaria Ndadi](https://www.linkedin.com/in/sakaria-ndadi/) if that is not sufficient.

Windows: Run as administrator `python setup.py`
Unix: `sudo python3 setup.py`
=======
## Legacy Setup

Run the setup.py file and follow the prompts

### Disclaimer

- This script has not been fully tested on Windows or Mac systems so there might be challenges. Please use the internet and then contact [Sakaria Ndadi](https://sakariandadi.com/#contact) if that is not sufficient.

Windows: Run as administrator `python setup.py`
Unix: `sudo python3 setup.py`

## My Recommendation

1. Install [UV](https://docs.astral.sh/uv/getting-started/installation/).
2. From `template.env` create `.env` file, provide `DJANGO_SECRET_KEY`,
3. In your terminal run `uv sync`, this will install all dependencies and set up .venv for you.
4. Make migrations, `uv run manage.py makemigrations`
5. Migrate to database, `uv run manage.py migrate`, a sqlite database will be created.
6. Collect static files, `uv run manage.py collectstatic --no-input`.
7. Create the superuser, `uv run manage.py createsuperuser`.
8. Run the project, `uv run manage.py runserver`
>>>>>>> upstream/main
