#!/bin/bash


if [ -b /dev/sda ]; then
   parted /dev/sda mklabel dos
   sync
   blockdev --rereadpt /dev/sda 2> /dev/null &
   wait %1
   parted -s --aling cylinder /dev/sda "mkpart logical ext2 0G 100%"
   sleep 5
   sync
   blockdev --rereadpt /dev/sda 2> /dev/null &
   wait %1
   mkfs.etx4 /dev/sda1
fi
