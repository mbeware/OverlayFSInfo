listOrigin.py

test : execute some tests
list : list all mounted overlayFS 
info : display a treeview of the directories used to create the overlayFS. 
      parameters : all - show for all mounted overlayFS
                   overlayFS mount point - show only for that overlayFS
show : for each files, display in a tree all versions. 
      parameters : overlayFS mount point
                    --DirOnly : show only version for directories
                    --MaxDepth : won't recurse more that this many level

clean : delete lowerversion of files 
      All <overlayFS mountpoint> : for all files
      Dir <overlayFS mountpoint> : --Dir <dirname> for all files in the specified directory. 
      File <overlayFS mountpoint> : --File <filename>  for this file. 

newlayer : Create script to add a newlayer and confirm before running it. 
  parameters : overlayFS mount point
               new directory to add as a toplayer
               --Workdir : working directory. If absent, it will be .<newDirectory>_work
               --Run : run the script without confirmation. 

The folder tests.ListOrigin contains tests. They are not up to date. 


