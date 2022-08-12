# Caktus Proxmox Server

## Replacing a bad hard drive

This server has 4 bays, only 3 active disks. You can use the spare to load a new drive before removing the old one.

https://blog.dalydays.com/post/2021-10-13-how-to-hot-swap-zfs-disk-in-proxmox/

1. Install the new drive.
2. SSH to the server:
   ```
   ssh root@172.20.1.40
   ```
3. To identify the new disk (e.g., `/dev/sdd`), run `dmesg` and look for the "Attached scsi generic" message.
4. Run a short smartctl test on the device:
   ```
   smartctl -t short /dev/sdd
   ```
   Look for the test results in a couple minutes with:
   ```
   smartctl -a /dev/sdd
   ```
5. Identify the disk to be replaced (e.g., from the serial number in emails from Proxmox)
6. Follow the instructions in the Proxmox Admin Guide for [Changing a failed bootable drive](https://pve.proxmox.com/pve-docs/chapter-sysadmin.html#_zfs_administration), for example:
   ```
   sgdisk /dev/sda -R /dev/sdd
   sgdisk -G /dev/sdd
   ```
7. Identify the new partition to add to the pool:
   ```
   ls -l /dev/disk/by-id/|grep sdd
   ```
8. Replace the disk:
   ```
   zpool replace -f rpool /dev/disk/by-id/ata-WDC_WD2003FYYS-02W0B0_WD-WMAY00155507-part3 /dev/disk/by-id/ata-WDC_WD30EFAX-68JH4N1_WD-WXB2DA19JT8Z-part3
   ```
9. Identify the serial number of the disk to be removed (`WMAY00155507` in the above example), and remove it from the server. Serial numbers are visible through the drive cage on the front of the server.

