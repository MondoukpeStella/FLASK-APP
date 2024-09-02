# FLASK APP
## Description

This is a Flask-based web application designed to manage tasks, provide a user authentification system. This README provides instructions for setting up the application, running it locally.

## Features

- User authentication and registration
- Database integration with SQLITE3
- RESTful API for users and product management

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your machine
- Flask and other dependencies listed in requirements.txt

## Installation

Follow these steps to set up the application on your local machine:

1. *Clone the repository:*
```sh
git clone git@github.com:EpitechCodingAcademyPromo2024/C-COD-240-COT-2-3-flaskd01-stella.aguemon.git
cd C-COD-240-COT-2-3-flaskd01-stella.aguemon
```
   

2. *Create a virtual environment:*

```sh
python3 -m venv virtual_env_name
source virtual_env_name/bin/activate  
   # On Windows use `virtual_env_name\Scripts\activate`
```

3. *Install the required packages:*

```sh
pip install -r requirements.txt  
```

## Usage

To run the application locally:

```sh
flask run
```

Visit http://127.0.0.1:5000/ in your browser to see the application in action.