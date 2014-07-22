FROM centos:latest
MAINTAINER hans.then@clustervision.com
RUN yum -y install python-pip vim-minimal rsyslog mysql mysql-server MySQL-python
ADD /etc/my.cnf /etc/my.cnf
VOLUME /var/lib/mysql
RUN touch /var/lib/mysql/dodo
EXPOSE 3306
