MODULES := xcat docker slurm

docker: compute/build.txt docker/controller/install/custom/runme/mkfs.tgz

docker/controller/install/custom/runme/mkfs.tgz: docker/xcat/mkfs/runme
	mkdir -p docker/controller/install/custom/runme
	tar zcf docker/controller/install/custom/runme/mkfs.tgz -C docker/xcat/mkfs/ runme.sh

compute/build.txt: compute/Dockerfile compute/supervisord.conf
	docker build -t controller:5000/compute compute
	docker push controller:5000/compute
	date > compute/build.txt

