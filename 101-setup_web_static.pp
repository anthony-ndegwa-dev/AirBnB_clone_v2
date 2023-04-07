# Puppet script that sets up your web servers for the deployment of web_static

# Install Nginx if not installed
package { 'nginx':
  ensure => installed,
}

# Create /data/web_static/releases/ folder if it doesn’t already exist
file { '/data/web_static/releases':
  ensure => directory,
}

# Create /data/web_static/shared/ folder if it doesn’t already exist
file { '/data/web_static/shared':
  ensure => directory,
}

# Create /data/web_static/releases/test/ folder if it doesn’t already exist
file { '/data/web_static/releases/test':
  ensure => directory,
}

# Create a fake HTML file /data/web_static/releases/test/index.html
exec {'content into html':
  provider => shell,
  command  => 'echo "Holberton School" | sudo tee /data/web_static/releases/test/index.html',
}

# Create a symbolic link /data/web_static/current linked to the
# /data/web_static/releases/test/ folder. If the symbolic link already
# exists, it should be deleted and recreated every time the script is ran.
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  force  => true,
}

# Give ownership of the /data/ folder to the ubuntu user AND group (you can
# assume this user and group exist). This should be recursive; everything
# inside should be created/owned by this user/group.
file { '/data':
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

file { '/etc/nginx/sites-available/default':
  content => "
server {
    listen 80;
    listen [::]:80 default_server;
    server_name _;
    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;

    location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html;
    }
}
",
  require => Package['nginx'],
  notify  => Service['nginx'],
}

# Restart Nginx after updating the configuration
service { 'nginx':
  ensure    => running,
  enable    => true,
  subscribe => File['/etc/nginx/sites-available/default'],
}
