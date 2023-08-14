# Host Flask Webapp on OCI with SSL and dns

# Get Domain
In my example i got the domain from ionos


# Set up Webserver
Create Instance.
Create a new Oracle Cloud Infrastructure (OCI) instance with the specifications you mentioned (A1.Flex, 1 OCPU, 6GB Memory, Ubuntu).
Set up a new Virtual Cloud Network (VCN).
Generate SSH Keys


# Set up Domain
Point Domain to Instance Public IP Adress


# Allow incoming HTTP and HTTPS traffic in OCI Security List
Add rule in Security List to allow ingress Rule port 5000, 443 and 80


# Allow incoming HTTP and HTTPS traffic
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 5000 -j ACCEPT
sudo iptables -I INPUT 7 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo iptables -I INPUT 8 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo netfilter-persistent save

# Update the package list and install Python 3 and pip
sudo apt update
sudo apt install -y python3-pip

# Install virtualenv and virtualenvwrapper
pip3 install virtualenv virtualenvwrapper

# Configure virtualenvwrapper in .bashrc
echo 'export WORKON_HOME=~/envs' >> ~/.bashrc
echo 'export PATH=$PATH:/home/ubuntu/.local/bin' >> ~/.bashrc
echo 'export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3' >> ~/.bashrc
echo 'export VIRTUALENVWRAPPER_VIRTUALENV_ARGS=" -p /usr/bin/python3 "' >> ~/.bashrc
echo 'source /home/ubuntu/.local/bin/virtualenvwrapper.sh' >> ~/.bashrc
source ~/.bashrc

# Create a new virtual environment
mkvirtualenv flask01

# Install Flask
pip3 install Flask

# Clone your Flask project repository
git clone <your project>

cd flask-project

# Activate the virtual environment
workon flask01

# Set up the environment variable for your Flask app
export FLASK_APP=app.py

# Run the Flask app with Gunicorn (install Gunicorn if not already installed)
pip3 install gunicorn

# Replace paths with your SSL certificate and private key paths
sudo /home/ubuntu/envs/flask01/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

# If everything is working fine, Ctrl + C and install Nginx.

# Install Nginx
sudo apt-get update
sudo apt-get install nginx

# Create an Nginx server block configuration file
sudo nano /etc/nginx/sites-available/my_flask_app

# Add the following configuration (replace with your details):
# Replace "your_domain.com" with your actual domain or IP
# Replace "/path/to/your/app" with the actual path to your Flask app
server {
    listen 80;
    server_name your_domain.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name your_domain.com;
    ssl_certificate /path/to/your/cert.pem;  # Path to your SSL certificate
    ssl_certificate_key /path/to/your/key.pem;  # Path to your SSL private key
    # U might need to convert the files to .pem with openssl
    location / {
        proxy_pass http://127.0.0.1:8000;  # Gunicorn bind address
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        # Additional proxy settings if needed
	# Cert: openssl x509 -in your_existing_certificate.crt -outform PEM -out your_domain.pem
	# Key:  openssl rsa -in your_existing_private_key.key -outform PEM -out your_domain.key
    }
}

# Enable the server block
sudo ln -s /etc/nginx/sites-available/my_flask_app /etc/nginx/sites-enabled

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo service nginx restart


# Start gunicorn 
sudo /home/ubuntu/envs/flask01/bin/gunicorn -w 1 -b 0.0.0.0:5000 app:app

If everything is working fine Ctrl+C and go to next step

# Make automatically start up on boot
sudo nano /etc/systemd/system/flask-app.service

[Unit]
Description=Gunicorn instance to serve Flask application
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/flask-project
Environment="PATH=/home/ubuntu/envs/flask01/bin"
ExecStart=/home/ubuntu/envs/flask01/bin/gunicorn --workers 4 --bind 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target

# Save

sudo systemctl daemon-reload

sudo systemctl enable flask-app
sudo systemctl start flask-app

sudo systemctl status flask-app

Now, Gunicorn will start automatically on machine startup using the systemd service. You can also manage the service with commands like stop, restart, and status using systemctl.

