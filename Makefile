MODULES := xcat docker slurm

docker: compute/build.txt 

docker/controller/install/custom/runme/mkfs.tgz: docker/xcat/mkfs/runme
	mkdir -p docker/controller/install/custom/runme
	tar zcf docker/controller/install/custom/runme/mkfs.tgz -C docker/xcat/mkfs/ runme.sh

compute/build.txt: compute/Dockerfile compute/supervisord.conf
	docker build -t controller:5000/compute compute
	docker push controller:5000/compute
	date > compute/build.txt

compute: /install/netboot/centos6.5/x86_64/compute/rootimg compute/build.txt
	cp -r compute/controller/* /
	cp -r compute/rootimg/* /install/netboot/centos6.5/x86_64/compute/rootimg
	chroot /install/netboot/centos6.5/x86_64/compute/rootimg chkconfig ntpd on
	chroot /install/netboot/centos6.5/x86_64/compute/rootimg chkconfig rdma on
	mkdir -p /install/netboot/centos6.5/x86_64/compute/rootimg/cluster
	packimage -o centos6.5 -p compute -a x86_64

login/build.txt: login/Dockerfile login/supervisord.conf
	cp -r login/controller/* /
	docker build -t controller:5000/login login
	docker push controller:5000/login
	date > login/build.txt

/install/netboot/centos6.5/x86_64/compute/rootimg: /install/custom/netboot/centos/compute.centos6.5.pkglist
	genimage -o centos6.5 -p compute -a x86_64 -i ' '
	
test: docker image
	nodeset compute osimage=
	rpower compute reset
	mpirun -np 2 --mca btl self,openib --host c001,c002 /usr/local/sbin/IMB-MPI1 pingpong
