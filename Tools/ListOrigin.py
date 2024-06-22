# def GetOverlayStructure():
#     pass

# def ListOrigin(FileNames):
#     OriginList = []
#     for FileName in FileNames:
#         OriginList.append(FileName)

#     return OriginList   


def HandleList(args):
    print(f"List all overlay filesytems")

def HandleInfo(args):
    print(f"List overlay structure {args.overlay =}")

def HandleShow(args):
    print(f"List overlay directories and files in a tree {args.overlay =}")

def HandleClean(args):
    print(f"Remove version of files in lower directories {args.overlay =}")

def HandleNewLayer(args):
    print(f"Create a new uppermost directory {args.overlay =}")






if __name__ == "__main__":
    #arguments is from command line is the file name to check
    import argparse
    parser = argparse.ArgumentParser()
    
    subparsers = parser.add_subparsers()
    parser_list = subparsers.add_parser('list')
    parser_info = subparsers.add_parser('info')
    parser_show = subparsers.add_parser('show')
    parser_clean = subparsers.add_parser('clean')
    parser_newlayer = subparsers.add_parser('newlayer')

    parser_list.set_defaults(func=HandleList)
    parser_info.set_defaults(func=HandleInfo)
    parser_clean.set_defaults(func=HandleClean)
    parser_newlayer.set_defaults(func=HandleNewLayer)
    parser_show.set_defaults(func=HandleShow)

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
    print(args)


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




# import argparse

# def main():
#     parser = argparse.ArgumentParser(description="Process some actions.")

#     # Create a mutually exclusive group for actions
#     action_group = parser.add_mutually_exclusive_group()
    
#     # List action
#     action_group.add_argument("list", action='store_true', help="List action (boolean).", default=False)

#     # Info action
#     action_group.add_argument("info", nargs="1", type=str, help="Info action with a directory name.",default=False)

#     # Show action with optional parameters
#     show_parser = action_group.add_argument_group("show", "Show action parameters")
#     show_parser.add_argument("show", nargs="?", type=str, help="Show action with a directory name.",default=False)
#     show_parser.add_argument("--DirOnly", action="store_true", help="Show directories only.")
#     show_parser.add_argument("--MaxDeep", type=int, help="Specify max depth for the show action.")

#     # Clean action with specific requirements
#     clean_parser = action_group.add_argument_group("clean", "Clean action parameters")
#     clean_parser.add_argument("clean", nargs="?", type=str, help="Clean action with a directory name and type.",default=False)
#     clean_parser.add_argument("clean_type", nargs="?", choices=["All", "Dir", "File"], help="Specify what to clean.")
#     clean_parser.add_argument("second_dir", nargs="?", type=str, help="Second directory name if Dir or File is selected.")

#     # Newlayer action with optional parameters
#     newlayer_parser = action_group.add_argument_group("newlayer", "Newlayer action parameters")
#     newlayer_parser.add_argument("newlayer", nargs="?", type=str, help="Newlayer action with a directory name.",default=False)
#     newlayer_parser.add_argument("--run", action="store_true", help="Run newlayer action.")
#     newlayer_parser.add_argument("--workdir", type=str, help="Specify work directory for newlayer action.")

#     args = parser.parse_args()

#     # Handle actions based on parsed arguments
#     if args.list:
#         print("List action selected.")
    
#     elif args.info:
#         print(f"Info action selected with directory: {args.info}")
    
#     elif args.show:
#         print(f"Show action selected with directory: {args.show}")
#         if args.DirOnly:
#             print("Show directories only.")
#         if args.MaxDeep:
#             print(f"Max depth: {args.MaxDeep}")
    
#     elif args.clean:
#         print(f"Clean action selected with directory: {args.clean} and type: {args.clean_type}")
#         if args.clean_type in ["Dir", "File"]:
#             print(f"Second directory: {args.second_dir}")
    
#     elif args.newlayer:
#         print(f"Newlayer action selected with directory: {args.newlayer}")
#         if args.run:
#             print("Run newlayer action.")
#         if args.workdir:
#             print(f"Work directory: {args.workdir}")

# if __name__ == "__main__":
#     main()
