import argparse
import os
from dotenv import load_dotenv
from bdspackmanager.pack_handler import PackHandler
from bdspackmanager.json_updater import JSONUpdater
from bdspackmanager.utils import validate_bds_directory

def main():
    """
    Minecraft Bedrock Dedicated Server Pack Manager.
    Args:
        packs (list): List of pack files or directories.
        bds-dir (str, optional): Path to the Bedrock Dedicated Server directory. Defaults to None.
        validate (bool, optional): Flag to validate and rescan JSON files. Defaults to False.
    """
    load_dotenv()

    parser = argparse.ArgumentParser(description="Minecraft Bedrock Dedicated Server Pack Manager")
    parser.add_argument('packs', nargs='+', help=".mcpack, .mcaddon, or pack directory")
    parser.add_argument('--bds-dir', help="Path to the Bedrock Dedicated Server directory")
    parser.add_argument('--validate', action='store_true', help="Validate and rescan JSON files")

    args = parser.parse_args()

    bds_directory = args.bds_dir or os.getenv("BDS_DIRECTORY")
    
    if not bds_directory or not validate_bds_directory(bds_directory):
        print("Invalid or missing BDS directory. Use --bds-dir or set BDS_DIRECTORY in your .env file.")
        return
    
    pack_handler = PackHandler(bds_directory)
    json_updater = JSONUpdater(bds_directory)
    
    if args.validate:
        json_updater.validate_json_files()
    else:
        for pack in args.packs:
            pack_handler.add_pack(pack)

if __name__ == "__main__":
    main()
