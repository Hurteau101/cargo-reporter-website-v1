# Cargo Report Website V1

A Django web application for tracking cargo Service Level Agreements (SLAs) and monitoring individual Air Waybills (AWBs), helping the cargo team prioritize shipments that need urgent attention.

## Features

- **SLA Tracking** - Monitor service level agreement status across all active cargo shipments. Just upload a CSV of all the airwaybills and allow the system to organize and sort all the data for you.

- **AWB Monitoring** - Track individual Air Waybills and their current status

- **Priority Visibility** - Quickly identify which shipments require urgent action vs. which can wait

## Tech Stack

- **Backend:** - Django (Python)
- **Database:** - SQLite
- **Frontend:** - Django Templates / Javascript
- **Hosted:** - Heroku

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/cargo-report-website.git
cd cargo-report-website

# Create and activate a virtual environment
python -m venv venv
Windows - venv/scripts/activate | Linux - venv/bin/activate


# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Run the development server
python manage.py runserver
```

The app will be available at `http://127.0.0.1:8000/`.
