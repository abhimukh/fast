FROM centos:latest
MAINTAINER hans.then@clustervision.com
RUN rpm -ivh http://dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
RUN yum -y install openssh-server openssh-clients python-pip vim-minimal rsyslog mysql
RUN yum install -y http://repos.fedorapeople.org/repos/openstack/openstack-icehouse/rdo-release-icehouse-4.noarch.rpm
RUN yum install -y --enablerepo=centosplus openstack-utils openstack-selinux
RUN yum install -y openstack-keystone python-keystoneclient
RUN keystone-manage pki_setup --keystone-user keystone --keystone-group keystone
RUN chown -R keystone:keystone /etc/keystone/ssl
RUN chown -R keystone:keystone /var/log/keystone
RUN chmod -R o-rwx /etc/keystone/ssl
ADD supervisord.conf /usr/etc/supervisord.conf
# For now we just add the configuration file. We should
# change this so the config files are centrally administered
# and injected into the container.
ADD keystone.conf /etc/keystone/keystone.conf
CMD ["/usr/bin/supervisord", "-c", "/usr/etc/supervisord.conf"]
RUN pip install supervisor
