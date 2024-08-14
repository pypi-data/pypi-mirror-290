import argparse
import os
from dotenv import load_dotenv
from bdspackmanager.pack_handler import PackHandler
from bdspackmanager.json_updater import JSONUpdater

def main():
    load_dotenv()

    parser = argparse.ArgumentParser(description="Minecraft Bedrock Dedicated Server Pack Manager")
    parser.add_argument('packs', nargs='+', help=".mcpack, .mcaddon, or pack directory")
    parser.add_argument('--bds-dir', help="Path to the Bedrock Dedicated Server directory")
    parser.add_argument('--validate', action='store_true', help="Validate and rescan JSON files")

    args = parser.parse_args()

    bds_directory = args.bds_dir or os.getenv("BDS_DIRECTORY")
    
    if not bds_directory or not os.path.exists(bds_directory):
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
