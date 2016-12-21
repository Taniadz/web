sudo ln -sf /home/box/web/etc/nginx.conf /etc/nginx/sites-enabled/default
sudo /etc/init.d/nginx restart
sudo ln -sf /home/box/web/etc/hello.py /etc/gunicorn.d/hello.py
sudo gunicorn -c /etc/gunicorn.d/hello.py hello:app

sudo ln -sf /home/box/web/etc/django.conf /etc/gunicorn.d/test

sudo gunicorn -c /home/box/web/etc/django.conf ask.wsgi
sudo /etc/init.d/gunicorn restart
s