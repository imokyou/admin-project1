# 一. prepare
1. sudo apt-get update && sudo apt-get upgrade
2. check LC_ALL
locale看一下LC_ALL有没有设置成功，如果就配置上：
sudo locale-gen "en_US.UTF-8"
sudo dpkg-reconfigure locales

# 二. install php7
sudo apt-get install software-properties-common python-software-properties
LC_ALL=C.UTF-8 add-apt-repository ppa:ondrej/php
sudo apt-get install php7.0-cli php7.0-common libapache2-mod-php php php7.0-mysql php7.0-fpm php7.0-curl php7.0-gd php7.0-mysql php7.0-bz2 php7.0-mbstring

# 三. install mysql
sudo apt-get install mysql-server-5.6
sudo apt-get install phpmyadmin

# 四. install nginx
sudo apt-get install nginx -y

# 五.配置phpmyadmin
ln -s /usr/share/phpmyadmin /home/www/phpmyadmin
server {
    listen 80;

    set $root_path '/home/www/phpmyadmin/';
    root $root_path;
    index  index.php index.html  index.htm;

    server_name phpmyadmin.js101.top;

    location ~ \.php$ {
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        root $root_path;
        fastcgi_pass unix:/var/run/php/php7.0-fpm.sock;
        fastcgi_index index.php;
        fastcgi_param  SCRIPT_FILENAME   $root_path$fastcgi_script_name;
        include fastcgi_params;
    }
}

# 六. 配置mysql的webadmin用户
mysql -u root -p
grant  on `allblue_admin`.* to webadmin@'localhost' identified by 'webadmin!@#$%^7';
flush privileges;


grant select,insert,update,delete on `allblue_admin`.* to 'webadmin'@'%' identified by 'webadmin!@#$%^7'  WITH GRANT OPTION;
flush privileges;


GRANT ALL PRIVILEGES ON *.* TO 'debuguser'@'%'IDENTIFIED BY 'debuguser!@#$%^' WITH GRANT OPTION;
FLUSH PRIVILEGES;


# 七. 拉取项目代码
sudo apt-get install git -y
git clone xxxx

# 八. 配置项目环境
sudo apt-get install python-setuptools python-dev build-essential -y
sudo apt-get install python-pip python-dev build-essential -y
pip install virtualenvwrapper

加到~/.bashrc:
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

sudo apt-get install uwsgi-plugin-python

# 九.
配置ngixn及uwsgi的配置文件　
Done~



＃　Problem:
locale: Cannot set LC_ALL to default locale: No such file or directory
fix:
1. vim /etc/enviroment
2. add this:
LC_ALL=en_US.UTF-8
LANG=en_US.UTF-8


Command "python setup.py egg_info" failed with error code 1 in /tmp/pip-build-Qwjcsm/MySQL-python/
sudo apt-get install libmysqlclient-dev -y


ImportError: no module name site
在uwsgi配置里加上执行用户　
uid=root
gid=root

OperationalError: (2005, "Unknown MySQL server host '138.128.194.193:3306' (0)")
多半是因为/etc/mysql/my.cnf里的bind_address设置原因, 注释掉就可以了