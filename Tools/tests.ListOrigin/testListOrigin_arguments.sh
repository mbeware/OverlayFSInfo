create_testfoldersAndFiles() {
sudo mkdir /tmp/tstofs
sudo chown $(whoami) /tmp/tstofs

mkdir /tmp/tstofs/tstofs
mkdir /tmp/tstofs/llfs_1
mkdir /tmp/tstofs/llfs_1/subdir1

mkdir /tmp/tstofs/llfs_2

mkdir /tmp/tstofs/llfs_2/subdir1
mkdir /tmp/tstofs/ulfs

mkdir /tmp/tstofs/ulfs/subdir1

mkdir /tmp/tstofs/workfs
mkdir /tmp/tstofs/nlfs


echo "Content for file 1 on level 1" > /tmp/tstofs/llfs_1/file1_l2
echo "Content for file 2 on level 1" > /tmp/tstofs/llfs_1/file2_l2
echo "Content for file 3 on level 1" > /tmp/tstofs/llfs_1/file3_l1
#file4 only on llfs_2
echo "Content for file 5 on level 1" > /tmp/tstofs/llfs_1/file5_ul
echo "Content for file 6 on level 1" > /tmp/tstofs/llfs_1/file6_deleted
echo "Content for file 7 on level 1" > /tmp/tstofs/llfs_1/file7_deleted

echo "Content for file 1 on level 1" > /tmp/tstofs/llfs_1/subdir1/subdir1_file1_l2
echo "Content for file 2 on level 1" > /tmp/tstofs/llfs_1/subdir1/subdir1_file2_l2
echo "Content for file 3 on level 1" > /tmp/tstofs/llfs_1/subdir1/subdir1_file3_l1
#file4 only on llfs_2
echo "Content for file 5 on level 1" > /tmp/tstofs/llfs_1/subdir1/subdir1_file5_ul
echo "Content for file 6 on level 1" > /tmp/tstofs/llfs_1/subdir1/subdir1_file6_deleted
echo "Content for file 7 on level 1" > /tmp/tstofs/llfs_1/subdir1/subdir1_file7_deleted

echo "Content for file 1 on level 2" > /tmp/tstofs/llfs_2/file1_l2
echo "Content for file 2 on level 2" > /tmp/tstofs/llfs_2/file2_l2
#file3 only on llfs_1
echo "Content for file 4 on level 2" > /tmp/tstofs/llfs_2/file4_l2
echo "Content for file 5 on level 2" > /tmp/tstofs/llfs_2/file5_ul
echo "Content for file 6 on level 2" > /tmp/tstofs/llfs_2/file6_deleted
echo "Content for file 7 on level 2" > /tmp/tstofs/llfs_2/file7_deleted
#file8 only on ulfs

echo "Content for file 1 on level 2" > /tmp/tstofs/llfs_2/subdir1/subdir1_file1_l2
echo "Content for file 2 on level 2" > /tmp/tstofs/llfs_2/subdir1/subdir1_file2_l2
#file3 only on llfs_1
echo "Content for file 4 on level 2" > /tmp/tstofs/llfs_2/subdir1/subdir1_file4_l2
echo "Content for file 5 on level 2" > /tmp/tstofs/llfs_2/subdir1/subdir1_file5_ul
echo "Content for file 6 on level 2" > /tmp/tstofs/llfs_2/subdir1/subdir1_file6_deleted
echo "Content for file 7 on level 2" > /tmp/tstofs/llfs_2/subdir1/subdir1_file7_deleted
#file8 only on ulfs



echo "Content for file 5 on level ulfs" > /tmp/tstofs/ulfs/file5_ul
echo "Content for file 6 on level ulfs" > /tmp/tstofs/ulfs/file6_deleted
echo "Content for file 8 on level ulfs" > /tmp/tstofs/ulfs/file8_ul
echo "Content for file 9 on level ulfs" > /tmp/tstofs/ulfs/file9_deleted


echo "Content for file 5 on level ulfs" > /tmp/tstofs/ulfs/subdir1/subdir1_file5_ul
echo "Content for file 6 on level ulfs" > /tmp/tstofs/ulfs/subdir1/subdir1_file6_deleted
echo "Content for file 8 on level ulfs" > /tmp/tstofs/ulfs/subdir1/subdir1_file8_ul
echo "Content for file 9 on level ulfs" > /tmp/tstofs/ulfs/subdir1/subdir1_file9_deleted


}

Clean_testfoldersAndFiles() {
sudo rm -rf /tmp/tstofs
}

if [ $1 = "Create" ] 
    then
    create_testfoldersAndFiles
elif [ $1 = "Clean" ] 
    then
    Clean_testfoldersAndFiles

else
    create_testfoldersAndFiles
    sudo mount overlay -t overlay -o lowerdir=/tmp/tstofs/llfs_1:/tmp/tstofs/llfs_2,upperdir=/tmp/tstofs/ulfs,workdir=/tmp/tstofs/workfs,redirect_dir=on,index=on,xino=on /tmp/tstofs/tstofs 
                                                          
    rm /tmp/tstofs/tstofs/file7_deleted
    rm /tmp/tstofs/tstofs/file6_deleted
    rm /tmp/tstofs/tstofs/file9_deleted

    rm /tmp/tstofs//tstofs/subdir1/subdir1_file7_deleted
    rm /tmp/tstofs/tstofs/subdir1/subdir1_file6_deleted
    rm /tmp/tstofs/tstofs/subdir1/subdir1_file9_deleted


    ls -lR /tmp/tstofs/
    echo "==list=========================================================="
    python3 ./ListOrigin.py list 
    echo "==info=========================================================="
    python3 ./ListOrigin.py info /tmp/tstofs/tstofs
    echo "==show=========================================================="
    python3 ./ListOrigin.py show /tmp/tstofs/tstofs --DirOnly --MaxDepth 2
    echo "==clean 1 ======================================================"
    python3 ./ListOrigin.py clean All /tmp/tstofs/tstofs
    echo "==clean 2======================================================="
    python3 ./ListOrigin.py clean Dir /tmp/tstofs/tstofs  --Dir /tmp/tstofs/tstofs/subdir1
    echo "==clean 3======================================================="
    python3 ./ListOrigin.py clean File /tmp/tstofs/tstofs --File /tmp/tstofs/tstofs/file5_ul
    echo "==newlayer======================================================"
    python3 ./ListOrigin.py newlayer /tmp/tstofs/tstofs /tmp/tstofs/nlfs
    echo "================================================================"
    sudo umount /tmp/tstofs/tstofs

    Clean_testfoldersAndFiles
fi
