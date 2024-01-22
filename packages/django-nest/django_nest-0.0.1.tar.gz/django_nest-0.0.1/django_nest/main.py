
import requests
# import subprocess

def cli():
    response = requests.get('https://httpbin.org/get?arg=pythonautas')
    print(response.json()['args']['arg'])
# subprocess.call('ls django_nest', shell=True)
# result = subprocess.run(['ls django_nest'], stdout=subprocess.PIPE, text=True)
# print(result.stdout)
# subprocess.call(['django_nest/scripts/start-local.sh'])