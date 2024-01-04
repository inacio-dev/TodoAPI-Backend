# Todo API with Django

This repository contains the implementation of a Todo API using Django with Python. The application is deployed on Heroku at [Todo API Heroku Deployment](https://todo-api-inacio-014fd3adf0e4.herokuapp.com/admin/). Docker Compose was utilized to run the app locally, and a `requirements.txt` file was included with all project dependencies.

## Table of contents

- [Technologies Used](#technologies-used)
- [Deploy on Heroku](#deploy-on-heroku)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Postman Collection](#postman-collection)
- [Author](#author)

## Technologies Used

- Django
- Python
- Heroku
- Docker Compose
- Django Rest Framework

## Getting Started

Follow the steps below to set up and run the project on your local environment:

1. Clone this repository:

   ```bash
   git clone git@github.com:inacio-dev/TodoAPI-Backend.git
   ```

2. Navigate to the project directory:

   ```bash
   cd TodoAPI-Backend
   ```

3. Install dependencies using one of the following package managers (choose one):

   ```bash
   docker-compose up
   ```

4. After installing dependencies and run, create new super user:

   ```bash
   docker ps
   docker exec -it <Your Docker Container Names> bash
   
   python manage.py createsuperuser
   ```

The site will be available at [http://0.0.0.0:8000](http://0.0.0.0:8000/).

## Deploy on Heroku

This project is deployed on Heroku. You can access the live site at [Heroku deploy](https://todo-api-inacio-014fd3adf0e4.herokuapp.com/admin/).

## Project Structure

Inside your Django project, you'll see the following folders and files:

```bash
   /
   ├── tasks/
   │ └── views.py
   ├── TodoAPI/
   │ ├── wsgi.py
   │ ├── urls.py
   │ └── settings.py
   ├── user/
   │ └── views.py
   ├── requirements.txt
   ├── Pipfile
   ├── Dockerfile
   ├── docker-compose.yml
   └── manage.py
```

## Postman Collection

The Postman collection includes all endpoints for testing the Todo API. You can import this collection into Postman and execute various API requests for testing purposes. The collection is available [here](https://www.postman.com/lunar-module-meteorologist-16957499/workspace/todo-api/collection/28810526-237c9353-d6e6-479f-a3cd-f4bca57580ea?action=share&creator=28810526).

## Author

- GitHub: [Inácio Rodrigues](https://github.com/inacio-dev)
- Email: inaciormgalvao@gmail.com
- Website: [Portfolio](https://inacio-rodrigues.vercel.app/en)
