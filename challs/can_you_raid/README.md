# Can you raid

1. You have 2 virtual drives, connect them to a linux machine (in my case i did it with virtualbox)
2. Add both files to your "storage" for the virtual machine and run it
   - If not using VM:
     - `sudo apt install qemu-utils -Y`
     - `sudo modprobe nbd max_part=32`
     - `qemu-nbd -c /dev/nbd0 raid_p1.vdi`
     - `qemu-nbd -c /dev/nbd1 raid_p2.vdi` 
3. Using `fdisk` on both disks you can see they have different partitions (raid, lvm, etc.)
4. Since there is a RAID array, try to mount it. Use `mdadm` - `sudo apt install mdadm`
5. Now assemble the raid array with `mdadm --assemble /dev/md0`
6. You also see there are some LVMs in the partitions, so install `lvm2` for working with them `sudo apt install lvm2`
7. Use `pvdisplay`, `vgdisplay` and `lvdisplay` to see how the drives are configured
8. Actiavte the volume group by `vgchange -a y`
9.  Now mount the final Logical Volume and look at the picture that is in the `/flag` folder, thats the flag