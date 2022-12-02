#!/bin/bash

# Database credentials
user='root'
password='m1_dj4ngu1t0_db'
current_time=$(date "+%Y.%m.%d-%H.%M.%S")

sudo chown -R tecnico:www-data /var/www/sgi_django/data
sudo chmod -R 755 /var/www/sgi_django/data

###############
### MARIADB ###
###############
# Remove old backup
rm /var/www/sgi_django/data/backup/mariadb_all_dbs.OLD 2> /dev/null
# Rename actual backup to old
mv /var/www/sgi_django/data/backup/mariadb_all_dbs_* /var/www/sgi_django/data/backup/mariadb_all_dbs.OLD
# Current backup
mariadb_new_fileName=mariadb_all_dbs_$current_time
mysqldump --user=$user --password=$password -x -A > /var/www/sgi_django/data/backup/$mariadb_new_fileName

################
### POSTGRES ###
################
# Remove old backup
rm /var/www/sgi_django/data/backup/postgres_all_dbs.OLD 2> /dev/null
# Rename actual backup to old
mv /var/www/sgi_django/data/backup/postgres_all_dbs_* /var/www/sgi_django/data/backup/postgres_all_dbs.OLD
# Current backup
postgres_new_fileName=postgres_all_dbs_$current_time
pg_dump postgresql://postgres:m1_dj4ngu1t0_db@127.0.0.1:5432/sgi_django > /var/www/sgi_django/data/backup/$postgres_new_fileName


################
### GIT PUSH ###
################
cd /var/www/sgi_django
sudo git add .
git add /var/www/sgi_django/data/backup/
sudo git commit -m "backup"
sudo git push origin master

now=$(date)
echo "$now - git push origin master" >> /var/www/sgi_django/scripts/git_logs.txt
git push origin master >> /var/www/sgi_django/scripts/git_logs.txt

# Log
echo "$now - backup correcto" >> /var/www/sgi_django/scripts/backup_logs.txt
