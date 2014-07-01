MODULES := xcat docker slurm

docker: compute/build.txt 

docker/controller/install/custom/runme/mkfs.tgz: docker/xcat/mkfs/runme
	mkdir -p docker/controller/install/custom/runme
	tar zcf docker/controller/install/custom/runme/mkfs.tgz -C docker/xcat/mkfs/ runme.sh

compute/build.txt: compute/Dockerfile compute/supervisord.conf
	docker build -t controller:5000/compute compute
	docker push controller:5000/compute
	date > compute/build.txt

image: /install/netboot/centos6.5/x86_64/compute/rootimg 
	cp -r compute/controller/* /
	cp -r compute/rootimg/* /install/netboot/centos6.5/x86_64/compute/rootimg
	packimage -o centos6.5 -p compute -a x86_64

/install/netboot/centos6.5/x86_64/compute/rootimg: /install/custom/netboot/centos/compute.centos6.5.pkglist
	genimage -o centos6.5 -p compute -a x86_64 -i ' '
	
test: docker image
	nodeset compute osimage=
	rpower compute reset
	mpirun -np 2 --mca btl self,openib --host c001,c002 /usr/local/sbin/IMB-MPI1 pingpong
