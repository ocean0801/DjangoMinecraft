cd ../
python3 manage.py makemigrations
python3 manage.py migrate
cd ../../server
python3 ../DjangoMinecraft/manage.py runserver & python3 ../DjangoMinecraft/code1.py & python3 ../DjangoMinecraft/code2.py & java -jar -Xmx4G server.jar nogui