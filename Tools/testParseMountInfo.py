from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class MountInfo:
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

def parse_options(options_str: str) -> Dict[str, str]:
    options = {}
    for opt in options_str.split(','):
        if '=' in opt:
            key, value = opt.split('=', 1)
            options[key] = value
        else:
            options[opt] = True
    return options

def parse_mountinfo_line(line: str) -> MountInfo:
    parts = line.split()
    mount_id = int(parts[0])
    parent_id = int(parts[1])
    major_minor = parts[2]
    root = parts[3]
    mount_point = parts[4]
    mount_options = parse_options(parts[5])
    
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
        super_options = parse_options(parts[separator_index + 3])
    else:
        super_options = {}

    return MountInfo(
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

def parse_mountinfo(mountinfo: str) -> List[MountInfo]:
    lines = mountinfo.strip().split('\n')
    return [parse_mountinfo_line(line) for line in lines]

# Example usage
data = """36 3665 98:1 /mnt1 /mnt2 rw,noatime info info2:2 - ext3 none errors=continue,tt
37 3345 98:0 / /mnt5/file-rere rw,noatime - ext3 /dev/root 
38 3125 98:0 / /mnt7 rw,teer=234,noatime master:1 underdir:/mnt/dir - ext3 /dev/root rw,errors=continue,tt"""
with open("/proc/self/mountinfo", 'r') as file:
            data = file.read()

parsed_data = parse_mountinfo(data)
for entry in parsed_data:
    print(entry)
