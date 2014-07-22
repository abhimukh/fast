FROM centos:latest
MAINTAINER hans.then@clustervision.com
RUN rpm -ivh http://dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
RUN yum -y install openssh-server openssh-clients python-pip vim-minimal rsyslog mysql
RUN yum install -y http://repos.fedorapeople.org/repos/openstack/openstack-icehouse/rdo-release-icehouse-4.noarch.rpm
RUN yum install -y --enablerepo=centosplus openstack-utils openstack-selinux
RUN yum install -y openstack-keystone python-keystoneclient
RUN keystone-manage pki_setup --keystone-user keystone --keystone-group keystone
RUN chown -R keystone:keystone /etc/keystone/ssl
RUN chmod -R o-rwx /etc/keystone/ssl
RUN openstack-config --set /etc/keystone/keystone.conf \
   database connection mysql://keystone@controller/keystone
RUN ADMIN_TOKEN=$(openssl rand -hex 10) && \ 
   openstack-config --set /etc/keystone/keystone.conf DEFAULT admin_token $ADMIN_TOKEN 
RUN rm /var/log/keystone/keystone.log
ADD keystone.sql keystone.sql
#RUN mysql --protocol=TCP -h controller -u root < keystone.sql
#RUN su -s /bin/sh -c "keystone-manage db_sync" keystone
VOLUME /usr/local
VOLUME /root
VOLUME /home

