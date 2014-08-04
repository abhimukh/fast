FROM centos:latest
MAINTAINER hans.then@clustervision.com
CMD ["/usr/bin/supervisord", "-c", "/usr/etc/supervisord.conf"]
RUN rpm -ivh http://dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
RUN yum -y install python-pip vim-minimal rsyslog mysql
RUN yum install -y http://repos.fedorapeople.org/repos/openstack/openstack-icehouse/rdo-release-icehouse-4.noarch.rpm
RUN yum install -y --enablerepo=centosplus openstack-utils openstack-selinux
RUN yum install -y openstack-glance python-glanceclient
# For now we just add the configuration file. We should
# change this so the config files are centrally administered
# and injected into the container.
RUN pip install supervisor
ADD supervisord.conf /usr/etc/supervisord.conf
ADD glance-registry.conf /etc/glance/glance-registry.conf
ADD glance-api.conf /etc/glance/glance-api.conf
VOLUME /var/lib/glance
EXPOSE 9191
EXPOSE 9292

