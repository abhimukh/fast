FROM centos:latest
MAINTAINER hans.then@clustervision.com
CMD ["/usr/bin/supervisord", "-c", "/usr/etc/supervisord.conf"]
RUN rpm -ivh http://dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
RUN yum -y install python-pip vim-minimal rsyslog mysql
RUN yum install -y http://repos.fedorapeople.org/repos/openstack/openstack-icehouse/rdo-release-icehouse-4.noarch.rpm
RUN yum install -y --enablerepo=centosplus openstack-utils openstack-selinux
RUN yum install -y openstack-nova-api openstack-nova-cert openstack-nova-conductor \
                   openstack-nova-console openstack-nova-novncproxy openstack-nova-scheduler \
                   python-novaclient python-cinderclient
RUN pip install supervisor
ADD supervisord.conf /usr/etc/supervisord.conf
EXPOSE 8773
EXPOSE 8774
EXPOSE 8775
EXPOSE 3333
EXPOSE 6080
EXPOSE 5800
EXPOSE 5900
