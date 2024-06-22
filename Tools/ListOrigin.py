
def ExtractOverlayInfo(line):
    aaa = line.split(",")
    OFSstruct={}
    OFSstruct["BaseDir"] = aaa[0].split(" ")[1]
    OFSstruct["lowerdir"] = []
    
    
    for a in aaa :
        aType = a.split("=")[0]
        if aType=="lowerdir" :
            bbb = a.split("=")[1].split(":")
            for b in bbb :
                OFSstruct["lowerdir"].append(b)
        elif aType=="upperdir" or aType=="workdir" :
            OFSstruct[aType] = a.split("=")[1]
    return OFSstruct
    

def GetMountedOverlayFSInfo():
    overlayInfo = {}
    with open("/etc/mtab", 'r') as file:
        lines = file.readlines()
    overlay_lines = [line for line in lines if line.startswith("overlay")]
    for line in overlay_lines : 
        thisOverlayInfo = ExtractOverlayInfo(line)
        overlayInfo[thisOverlayInfo["BaseDir"]] = thisOverlayInfo
    return overlayInfo

def DisplayOverlayInfo(overlayInfo,filter="all"):
    for item in overlayInfo:
        if overlayInfo[item]['BaseDir'] == filter or filter == "all":
            print()
            print(f"{overlayInfo[item]['BaseDir']}  \t\tworkdir: {overlayInfo[item]['workdir']}")
            print(f"  ├── upperdir: {overlayInfo[item]['upperdir']}")
            for j, lowerdir in enumerate(overlayInfo[item]['lowerdir']):
                if j == len(overlayInfo[item]['lowerdir']) - 1:
                    print(f"  └── lowerdir {-(j+1)}: {lowerdir}")
                else:
                    print(f"  ├── lowerdir {-(j+1)}: {lowerdir}")




def HandleList(args):
    overlayinfo = GetMountedOverlayFSInfo()
    for item in overlayinfo.keys():
        print(item)

    

def HandleInfo(args):
    overlayinfo = GetMountedOverlayFSInfo()
    if args.overlay[0] in list(overlayinfo.keys()) or "all" in args.overlay:
        DisplayOverlayInfo(overlayinfo,args.overlay[0])
    else:
        print(f"Overlay {args.overlay} not found")  

def HandleShow(args):
    print(f"List overlay directories and files in a tree {args.overlay =}")

def HandleClean(args):
    print(f"Remove version of files in lower directories {args.overlay =}")

def HandleNewLayer(args):
    print(f"Create a new uppermost directory {args.overlay =}")


def HandleTest(args):
    print(f"{GetMountedOverlayFSInfo() =}")


# the leftmost layer of the overlay mount command is the layer nearest to the upperdir. user -> ulfs -> llfs_2 -> llfs_1




if __name__ == "__main__":
    import sys
    if  len(sys.argv) == 1:
        HandleTest(sys.argv)
        exit(0)

    
    import argparse
    parser = argparse.ArgumentParser()
    
    subparsers = parser.add_subparsers()
    parser_test = subparsers.add_parser('test')
    parser_list = subparsers.add_parser('list')
    parser_info = subparsers.add_parser('info')
    parser_show = subparsers.add_parser('show')
    parser_clean = subparsers.add_parser('clean')
    parser_newlayer = subparsers.add_parser('newlayer')

    parser_test.set_defaults(func=HandleTest)
    parser_list.set_defaults(func=HandleList)
    parser_info.set_defaults(func=HandleInfo)
    parser_clean.set_defaults(func=HandleClean)
    parser_newlayer.set_defaults(func=HandleNewLayer)
    parser_show.set_defaults(func=HandleShow)

    parser_test.add_argument('test',action='store_true',help="test",default=False)

    parser_list.add_argument('list',action='store_true',help="List all overlay filesytems",default=False)

    parser_info.add_argument('overlay',nargs=1,type=str,help="List overlay structure", default=None)

    parser_show.add_argument('overlay',nargs=1,type=str,help="List overlay directories and files in a tree", default=None)
    parser_show.add_argument('--DirOnly',action='store_true',help="Only list directories")
    parser_show.add_argument('--MaxDepth',type=int,help="Max number of layers to list")

    subparsers_clean = parser_clean.add_subparsers()
    parser_cleanAll = subparsers_clean.add_parser('All')
    parser_cleanDir = subparsers_clean.add_parser('Dir')
    parser_cleanFile = subparsers_clean.add_parser('File')

    parser_cleanAll.add_argument('overlay',help="Remove version of files in lower directories", default=None)

    parser_cleanDir.add_argument('overlay',help="Remove version of files in lower directories", default=None)
    parser_cleanDir.add_argument('--Dir',dest='DirName',help="Remove all version for all files in <DirName> in lower directories")

    parser_cleanFile.add_argument('overlay',help="Remove version of files in lower directories", default=None)
    parser_cleanFile.add_argument('--File',dest='DirName',help="Remove all version for <FileName> in lower directories")

    parser_newlayer.add_argument('overlay',help="Create a new uppermost directory", default=None)
    parser_newlayer.add_argument('newDirectory',help="Create a new uppermost directory")
    parser_newlayer.add_argument('--Run',action='store_true',help="don't ask for confirmation and run the script")
    parser_newlayer.add_argument('--Workdir',nargs=1,help="specify the working directory")


    args = parser.parse_args()
    args.func(args)


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




