# Django Nest 
# 📘 User Guide 📘

## Installation
To install Django Nest, use the following command:

```bash
🛠️ pip3 install django-nest     
```

## Create a New Project
To start a new Django Nest project, you can choose from the following options:

1. Using the startproject command:

```bash 
🌟 python3 -m django_nest startproject "myproject"
```

2. Cloning an existing project from the repository:

```bash
🌟 git clone "https://github.com/Pythonautas/DNest.git" "my_project"
```

After creating the project, navigate to the project directory:

```bash
📁 cd "my_project"
```

### Setting up the Database

To start the database, use the following command with Docker Compose:
```bash
🗃️ docker-compose up db -d
```
### Starting the Application
To start the application, use the following command with Docker Compose:

```bash
📱 docker-compose up app
 ```

**Note:**
[Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/) are required to run the application. Make sure to install them before starting the application.

Now you're ready to begin working on your Django Nest project! If you have any questions or need more information, refer to the official documentation at [DjangoNest]().
