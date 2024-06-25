from dataclasses import dataclass, field
from typing import Dict, List, Tuple

@dataclass
class MountinfoEntry:
    mount_id: int
    parent_id: int
    major_minor: str
    root: str
    mount_point: str
    mount_options: Dict[str, str]
    optional_fields: Dict[str, str]
    filesystem_type: str
    mount_source: str
    super_options: Dict[str, str]

class MountInfo():
    mount_info: Dict[str, MountinfoEntry]
    @staticmethod
    def parse_options(options_str: str) -> Dict[str, str]:
        options = {}
        for opt in options_str.split(','):
            if '=' in opt:
                key, value = opt.split('=', 1)
                options[key] = value
            else:
                options[opt] = True
        return options

    @staticmethod
    def parse_mountinfo_line(line: str) -> MountinfoEntry:
        parts = line.split()
        mount_id = int(parts[0])
        parent_id = int(parts[1])
        major_minor = parts[2]
        root = parts[3]
        mount_point = parts[4]
        mount_options = MountInfo.parse_options(parts[5])
        
        # Find the position of the separator '-'
        separator_index = parts.index('-')
        
        # Extract optional fields
        optional_fields = {}
        for opt in parts[6:separator_index]:
            if ':' in opt:
                key, value = opt.split(':', 1)
                optional_fields[key] = value
            else:
                optional_fields[opt] = ""
        
        filesystem_type = parts[separator_index + 1]
        mount_source = parts[separator_index + 2]
        
        # Handle possible absence of super options
        if separator_index + 3 < len(parts):
            super_options = MountInfo.parse_options(parts[separator_index + 3])
        else:
            super_options = {}

        return MountinfoEntry(
            mount_id=mount_id,
            parent_id=parent_id,
            major_minor=major_minor,
            root=root,
            mount_point=mount_point,
            mount_options=mount_options,
            optional_fields=optional_fields,
            filesystem_type=filesystem_type,
            mount_source=mount_source,
            super_options=super_options
        )
    @staticmethod
    def get_mountinfo_from_string(mountinfo_linestr: str) -> Dict[str,MountinfoEntry]:
        lines = mountinfo_linestr.strip().split('\n')
        return MountInfo.build_mountinfo_dict(lines)
    
    @staticmethod
    def get_mountinfo_from_file(mountinfofile: str="/proc/self/mountinfo") -> Dict[str,MountinfoEntry]:
        with open(mountinfofile, 'r') as file:
            lines = file.readlines()
        return MountInfo.build_mountinfo_dict(lines)
    
    @staticmethod
    def build_mountinfo_dict(mountinfo_lines: List[str]) -> Dict[str,MountinfoEntry]:
        all_mountinfo = {}  
        for line in mountinfo_lines:
            this_mountinfo = MountInfo.parse_mountinfo_line(line)
            all_mountinfo[this_mountinfo.mount_point] = this_mountinfo

        return all_mountinfo



@dataclass 
class OFSinfo:
    base_dir: str
    work_dir: str
    upper_dir: str
    lower_dir: list[str]  # list of lower directories in the same order as they appear in fstab. The first entry is the closest to the base/upper directory
    mount_info : MountinfoEntry
    options: dict[str,str] 

    def __init__(self):
        self.lower_dir = []
        self.options = {}

    @staticmethod
    def build_OFS_info(mountinfo: MountinfoEntry) -> "OFSinfo":
        """
        get theinformation about the OverlayFS and returns a OFSinfo
        containing the base directory, list of lower directories, upper directory, and work directory.

        Args:
            OFS_def (list): The line containing OverlayFS information.

        Returns:
            dict: A dictionary containing the base directory, lower directories, upper directory, and work directory.
        """

        
        OFSstruct:OFSinfo = OFSinfo()
        OFSstruct.mount_info = mountinfo
        
              # remove trailing slashes   
        OFSstruct.base_dir = OFSstruct.mount_info.mount_point.rstrip("/")

        OFSstruct.options = OFSstruct.mount_info.mount_options|OFSstruct.mount_info.super_options

        OFSstruct.lower_dir = OFSstruct.options["lowerdir"].split(":")
        OFSstruct.upper_dir = OFSstruct.options["upperdir"]
        OFSstruct.work_dir = OFSstruct.options["workdir"]

        return OFSstruct
    

@dataclass
class OFSManager:
    info: dict[str, OFSinfo]
    
    def __init__(self, mountinfofile: str="/proc/self/mountinfo"): 
        self.info = {}
        all_mountinfo = MountInfo.get_mountinfo_from_file(mountinfofile)

        overlay_lines = [all_mountinfo[this_mountinfo_key] for this_mountinfo_key in all_mountinfo.keys() if all_mountinfo[this_mountinfo_key].filesystem_type in ["overlay", "overlayfs"] ]
        for overlay_def in overlay_lines : 
            thisOverlayInfo = OFSinfo.build_OFS_info(overlay_def)
            self.info[thisOverlayInfo.base_dir] = thisOverlayInfo

if __name__ == "__main__":
    OFS = OFSManager()
    print(OFS.info)
