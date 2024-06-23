from dataclasses import dataclass

@dataclass
class fstab_entry:
    fs_spec:str
    fs_file:str
    fs_vfstype:str
    fs_mntops:str
    fs_freq:int
    fs_passno:int

    def __init__(self, line: str):
        self.parse(line)

    def parse(self, line: str):
        self.fs_spec = line.split()[0]
        self.fs_file = line.split()[1]
        self.fs_vfstype = line.split()[2]
        self.fs_mntops = line.split()[3]
        self.fs_freq = line.split()[4]
        self.fs_passno = line.split()[5]


@dataclass 
class OFSinfo:
    base_dir: str
    work_dir: str
    upper_dir: str
    lower_dir: list[str]  
    fstab: fstab_entry
    options: dict[str,str]


    def __init__(self):
        self.lower_dir = []
        self.options = {}



@dataclass
class OFSManager:
    info: dict[str, OFSinfo]
    
    def __init__(self):
        self.info = {}
        self._GetMountedOverlayFSInfo()

    @staticmethod
    def _parse_OFS_info(OFS_def: str) -> dict:
        """
        Parses the OFS_def containing information about the OverlayFS and returns a dictionary
        containing the base directory, lower directories, upper directory, and work directory.

        according to the wiki archlinux [https://wiki.archlinux.org/title/Overlay_filesystem] the format in fstab and concequently in /proc/mounts or /etc/mtab is:

            overlay <base_dir> overlay <options seperated by ,> 0 0
            where <options> is a list of options that can be specified in fstab. we are maintly interested in the lowerdir, upperdir, and workdir for now
            We can assume that <options> will never have spaces as they are used as delimiters. If the paths would have spaces in them, they would have been encoded with "\040"

        Args:
            OFS_def (str): The line containing OverlayFS information.

        Returns:
            dict: A dictionary containing the base directory, lower directories, upper directory, and work directory.
        """
        OFSstruct = OFSinfo()
        OFSstruct.fstab = fstab_entry(OFS_def)
        
        OFSstruct.base_dir = OFSstruct.fstab.fs_file

        # remove trailing slashes   
        OFSstruct.base_dir = OFSstruct.base_dir.rstrip("/")

        options_list = OFSstruct.fstab.fs_mntops.split(",")

        for option in options_list:
            if "=" not in option:
                OFSstruct.options[option] = "True"
            else:
                option_type = option.split("=")[0]
                option_value = option.split("=")[1]
                OFSstruct.options[option_type] = option_value

        OFSstruct.lower_dir = OFSstruct.options["lowerdir"].split(":")
        OFSstruct.upper_dir = OFSstruct.options["upperdir"]
        OFSstruct.work_dir = OFSstruct.options["workdir"]

        return OFSstruct
    

    def _GetMountedOverlayFSInfo(self):
        thisOverlayInfo:OFSinfo = OFSinfo()
        # Info from /etc/mtab because it has a more complete list of all mounted filesystems, most of the time...
        with open("/etc/mtab", 'r') as file:
            lines = file.readlines()
        overlay_lines = [line for line in lines if line.startswith("overlay")]
        for overlay_def in overlay_lines : 
            thisOverlayInfo = self._parse_OFS_info(overlay_def)
            self.info[thisOverlayInfo.base_dir] = thisOverlayInfo

