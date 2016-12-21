sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart
sudo ln -sf /home/box/web/etc/hello.py /etc/gunicorn.d/hello.py
sudo gunicorn -c /etc/gunicorn.d/hello.py hello:application

sudo ln -sf /home/box/web/etc/django.conf /etc/gunicorn.d/ask

sudo gunicorn -c /home/box/web/etc/django.conf ask.wsgi:application
sudo /etc/init.d/gunicorn restart
