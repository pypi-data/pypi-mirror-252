import requests
from git import Repo
from git.exc import GitCommandError
import sys 

def pythonautas():
    requests.get('https://bit.ly/3vK3cIC')
    print(f"Welcome to the pythoanautas community, visit https://pythonautas.com.br")

def startproject():
    try:
        repository_url = 'https://github.com/Pythonautas/DNest.git'
        Repo.clone_from(repository_url, sys.argv[1:][1])
        pythonautas()
    except GitCommandError as e:
        print(f'Error: Repository with name `{sys.argv[1:][1]}` already exists.')
        sys.exit(1)

def runserver():
    print(f"runserver is under development")

def tutorial():
    return f"""
        Usage: python3 -m dnest startproject <project_name>
        cd <project_name>
        poetry shell
        poetry install
        OBS: The project name cannot contain the word help
    """

def install():
    print(f"Installing meumodulo...")

if __name__ == "__main__":
    install()
    if len(sys.argv) < 2:
        print(tutorial())
        sys.exit(1)
    else:
        if sys.argv[1:][0] == "startproject":
            if not "help" in sys.argv[1:][1].lower():
                startproject()
            else:
                print(tutorial())

        elif sys.argv[1:][0] == "runserver":
            runserver()
        elif sys.argv[1:][0] == "--help":
            print(tutorial())
        else:
            print(tutorial())
            print(f"Command `{sys.argv[1:][0]}` not found.")
            sys.exit(1)