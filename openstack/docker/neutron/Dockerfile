FROM centos:latest
MAINTAINER hans.then@clustervision.com
CMD ["/usr/bin/supervisord", "-c", "/usr/etc/supervisord.conf"]
RUN rpm -ivh http://dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
RUN yum -y install python-pip vim-minimal rsyslog mysql
RUN yum install -y http://repos.fedorapeople.org/repos/openstack/openstack-icehouse/rdo-release-icehouse-4.noarch.rpm
RUN yum install -y --enablerepo=centosplus openstack-utils openstack-selinux
RUN yum install -y openstack-neutron openstack-neutron-ml2 python-neutronclient
RUN ln -s plugins/ml2/ml2_conf.ini /etc/neutron/plugin.ini
RUN pip install supervisor
ADD supervisord.conf /usr/etc/supervisord.conf
