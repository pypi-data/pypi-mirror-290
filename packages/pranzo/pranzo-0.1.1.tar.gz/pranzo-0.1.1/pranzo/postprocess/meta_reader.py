import tomli

class MetaReader:

    def __init__(self, sdir, file_id):
        
        self.file_id = file_id
        self.meta_file = f"{sdir}/meta_{file_id}.toml"

    def get_meta_dict(self):
        with open(self.meta_file, 'rb') as file:
            meta_dict = tomli.load(file)
        return meta_dict
