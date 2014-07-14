#!/bin/bash

service docker stop
umount /dev/sda1
if [ -b /dev/sda ]; then
   parted /dev/sda mklabel msdos
   sync
   blockdev --rereadpt /dev/sda 2> /dev/null
   parted -s --align cylinder /dev/sda mkpart primary ext2 0G 100%
   sleep 5
   sync
   blockdev --rereadpt /dev/sda 2> /dev/null
   mkfs.ext4 /dev/sda1
fi
