for db in keystone nova glance neutron cinder; do
    mysql -u root -e "CREATE database ${db}; GRANT ALL PRIVILEGES ON ${db}.* TO '${db}'@'%';"
done
