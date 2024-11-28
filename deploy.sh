#!/bin/bash

echo "deleting old app"
sudo rm -rf /var/www/

echo "creating app folder"
sudo mkdir -p /var/www/langchain-app

echo "moving files to app folder"
sudo mv * /var/www/langchain-app

# Navigate to the app directory
cd /var/www/langchain-app/
sudo mv env .env

sudo apt-get update
echo "installing python3 and virtualenv"
sudo apt-get install -y python3 python3-pip python3-venv

# Create a virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment"
    python3 -m venv venv
fi

# Activate the virtual environment and install dependencies
echo "Activating virtual environment and installing dependencies"
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

# Update and install Nginx if not already installed
if ! command -v nginx > /dev/null; then
    echo "Installing Nginx"
    sudo apt-get install -y nginx
fi

# Configure Nginx to act as a reverse proxy if not already configured
if [ ! -f /etc/nginx/sites-available/myapp ]; then
    echo "Configuring Nginx"
    sudo rm -f /etc/nginx/sites-enabled/default
    sudo bash -c 'cat > /etc/nginx/sites-available/myapp <<EOF
server {
    listen 80;
    server_name _;

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/langchain-app/myapp.sock;
    }
}
EOF'

    sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled
    sudo systemctl restart nginx
else
    echo "Nginx reverse proxy configuration already exists."
fi

# Stop any existing Gunicorn process
echo "Stopping existing Gunicorn process if running"
sudo pkill gunicorn
sudo rm -rf myapp.sock

# Start Gunicorn using the virtual environment
echo "Starting Gunicorn"
source venv/bin/activate
gunicorn --workers 3 --bind unix:/var/www/langchain-app/myapp.sock app:app --daemon --user www-data --group www-data
deactivate
echo "Gunicorn started 🚀"
