def GetOverlayStructure():
    pass

def ListOrigin(FileNames):
    OriginList = []
    for FileName in FileNames:
        OriginList.append(FileName)

    return OriginList   

if __name__ == "__main__":
    #arguments is from command line is the file name to check
    import argparse
    parser = argparse.ArgumentParser()
    parser_list = parser.add_argument_group('list')
    parser_list.add_argument('list',action='store_true',help="List all overlay filesytems")
    parser_info = parser.add_argument_group('info')
    parser_info.add_argument('info',help="List overlay structure")
    parser_show = parser.add_argument_group('show')
    parser_show.add_argument('overlay',help="List overlay directories and files in a tree")
    parser_show.add_argument('--DirOnly',action='store_true',help="Only list directories")
    parser_show.add_argument('--MaxDeep',type=int,help="Max number of layers to list")
    parser_clean = parser.add_argument_group('clean')
    parser_clean.add_argument('overlay',help="Remove version of files in lower directories")
    parser_clean.add_argument('CleanAction',choices=['All','Dir','File'],help="Remove all version for all files in lower directories")
    parser_clean.add_argument('--Dir',dest='DirName',help="Remove all version for all files in <DirName> in lower directories")
    parser_clean.add_argument('--File',dest='DirName',help="Remove all version for <FileName> in lower directories")
    parser_newlayer = parser.add_argument_group('newlayer')
    parser_newlayer.add_argument('overlay',help="Create a new uppermost directory")
    parser_newlayer.add_argument('--Run',action='store_true',help="don't ask for confirmation and run the script")
    parser_newlayer.add_argument('--Workdir',nargs=1,help="specify the working directory")
    args = parser.parse_args()

    if args.list:
        print("List all overlay filesytems")
    if args.info:
        print(f"List overlay structure {args.info}")
    if args.show:
        print("List overlay directories and files in a tree {args.overlay}")
    if args.clean:
        print("Remove version of files in lower directories {args.overlay}")
    if args.newlayer:
        print("Create a new uppermost directory {args.overlay}")

# -List : List all overlay filesytems
# -Info <OverlayFS>: List overlay structure
# -Show <OverlayFS>: List overlay directories and files in a tree
#    root = uppermost directory
#    options : --DirOnly : Only list directories
#    options : --MaxDeep : Max number of layers to list
# -Clean : 
#   --All <OverlayFS>  : Remove all version for all files in lower directories
#   --Dir <OverlayFS> <DirName>: Remove all version for all files in <DirName> in lower directories
#   --File <OverlayFS> <FileName>: Remove all version for <FileName> in lower directories
#   If there is a "rubout" file, delete it and all versions in lower directories

# -Newlayer <NewUpperDir> 
#   --Run : don't ask for confirmation and run the script
#   --Workdir <WorkDir> : specify the working directory
#    generate a command line to Create a uppermost directory and working directory with the name "."<NewUpperDir>"_work" or "<WorkDir>"
#    generate a command line to unmount the old overlayfs
#    generate a command line to delete the old working directory
#    generate a command line to rename the old upper directory to OverlayFS name with "Level_<N>" where N is the new layer number
#    generate the new mount command line with the old (renamed)upper directory as the topmost new lower directory
#    generate script to run the above commands
#    display the script and ask for confirmation to run it
#    execute the script

