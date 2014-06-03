FROM centos:latest
MAINTAINER hans.then@clustervision.com
RUN rpm -ivh http://dl.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
RUN yum -y install openssh-server python-pip vim-minimal infiniband-diags munge
RUN yum -y groupinstall "Infiniband Support"
RUN echo "root:system" | chpasswd && pip install supervisor
RUN mkdir -p /var/run/sshd ; chmod -rx /var/run/sshd
RUN sed -ri 's/^#PermitRootLogin yes/PermitRootLogin yes/g' /etc/ssh/sshd_config 
RUN sed -ri 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
RUN sed -ri 's/#UsePAM no/UsePAM no/g' /etc/ssh/sshd_config
RUN ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key
RUN ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key
ADD supervisord.conf /usr/etc/supervisord.conf
VOLUME /usr/local
EXPOSE 22 6818
CMD ["/usr/bin/supervisord"]

