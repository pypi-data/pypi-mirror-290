import os

def validate_bds_directory(directory):
    required_dirs = ['resource_packs', 'behavior_packs', 'worlds']
    return all(os.path.exists(os.path.join(directory, d)) for d in required_dirs)
