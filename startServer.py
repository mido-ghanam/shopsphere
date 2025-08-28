from os import system

defaultPort = 8000
try:
  port = input("Open in port: ")
except:
  port = defaultPort
try:
  system(f"python manage.py makemigrations && python manage.py migrate && clear && python manage.py runserver 0.0.0.0:{port if port else defaultPort}")
except:
  system(f"python3 manage.py makemigrations && python3 manage.py migrate && clear && python3 manage.py runserver 0.0.0.0:{port if port else defaultPort}")
