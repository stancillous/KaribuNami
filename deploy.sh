#!/bin/bash

yes | sudo apt update

yes | sudo apt install python3

yes | sudo apt install python3-pip

yes | sudo apt-get install mysql-server

yes | sudo apt install nginx

# cd

# git clone https://github.com/Bot-on-Tapwater/KaribuNami.git

# cd ~/Karibunami

# pip freeze > requirements.txt

# pip install requirements.txt

# env_file=".env"

# env_content="MYSQLUSERNAME='botontapwater'\nPASSWORD='TwoGreen1.'\nHOST='localhost'\nDB='karibunami'"

# echo -e "$env_content" > "$env_file"

pip install Flask

pip install sqlalchemy

pip install python-dotenv

pip install mysql-connector-python

pip install gunicorn

# sudo mysql

# CREATE DATABASE karibunami

# CREATE USER 'botontapwater'@'localhost' IDENTIFIED BY 'TwoGreen1.';

# GRANT ALL PRIVILEGES ON karibunami.* TO 'botontapwater'@'localhost';

# FLUSH PRIVILEGES;

# exit;

file_path="/etc/nginx/sites-available/karibunami"

config_content="server {
    server_name 172.178.83.84 botontapwater.tech www.botontapwater.tech localhost;

    location / {
        proxy_pass http://127.0.0.1:5000;
    }
}"

echo "$config_content" > "$file_path"

sudo ln -s /etc/nginx/sites-available/karibunami /etc/nginx/sites-enabled

sudo nginx -t

sudo service nginx restart

# yes | sudo apt install certbot python3-certbot-nginx

# sudo certbot --nginx -d botontapwater.tech -d www.botontapwater.tech

# sudo nginx -t

# sudo systemctl restart nginx 

# sudo certbot renew --dry-run

file_path="/etc/nginx/sites-available/karibunami"

config_content="server {
    server_name 172.178.83.84 botontapwater.tech www.botontapwater.tech localhost;

    location / {
        proxy_pass http://127.0.0.1:5000;
    }
}"

echo "$config_content" > "$file_path"

username=$(whoami)

service_file="/etc/systemd/system/karibunami.service"

echo "[Unit]
Description=Flask app
After=network.target

[Service]
User=$username
Group=$username
WorkingDirectory=/home/$username/KaribuNami
ExecStart=/usr/bin/python3 -m server.flask_api.app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target" | sudo tee $service_file

sudo systemctl daemon-reload

sudo systemctl restart karibunami

sudo systemctl enable karibunami

sudo systemctl status karibunami


