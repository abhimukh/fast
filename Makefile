MODULES := xcat docker slurm

docker: docker/build.txt docker/controller/install/custom/runme/mkfs.tgz

docker/controller/install/custom/runme/mkfs.tgz: docker/xcat/mkfs/runme
	mkdir -p docker/controller/install/custom/runme
	tar zcf docker/controller/install/custom/runme/mkfs.tgz -C docker/xcat/mkfs/ runme.sh

docker/build.txt: docker/Dockerfile docker/supervisord.conf
	docker build -t controller:5000/fast docker
	docker push controller:5000/fast
	date > docker/build.txt

