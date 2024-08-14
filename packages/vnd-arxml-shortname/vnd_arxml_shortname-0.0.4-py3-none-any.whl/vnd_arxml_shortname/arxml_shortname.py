import os
from typing import List
import re

def sdb_shortname(dirpath: str, filenames):
    pattern = r'MAIN[^-]*'
    for file in filenames:
        base, ext = os.path.splitext(file)
        #xml for fibex spa3
        if ext in (".arxml", ".dbc", ".ldf", "xml"):

            name_split = base.split('_')
            name_split = [word for word in name_split if word != 'MAIN']
            name_split = [re.sub(pattern, '', part) for part in name_split]
            name_split = [re.sub(r'\dD\d.*', '', part) for part in name_split]
            # this also removes the double _ in the end of some file names
            name_split = [string for string in name_split if string]

            res_list = []
            for part in name_split:
                if part.isdigit():
                    continue
                if 'AR-' in part:
                    continue
                res_list.append(part)

            print(f'Old name: {base}, extension: {ext}')
            new_base = str("_".join(res_list))
            print(f'New name: {new_base}')
            complete_new_name = "".join([new_base, ext])
            os.rename(os.path.join(dirpath, file), os.path.join(dirpath, complete_new_name))
