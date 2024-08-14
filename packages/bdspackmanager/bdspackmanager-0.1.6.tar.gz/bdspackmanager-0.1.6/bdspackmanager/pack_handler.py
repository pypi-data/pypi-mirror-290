import json
import os
import zipfile
import shutil
import logging
from bdspackmanager.manifest_parser import ManifestParser
from bdspackmanager.json_updater import JSONUpdater

class PackHandler:
    def __init__(self, bds_directory):
        """
        Initializes a PackHandler object.

        Parameters:
        - bds_directory (str): The directory path of the BDS installation.

        Attributes:
        - bds_directory (str): The directory path of the BDS installation.
        - resource_packs_dir (str): The directory path of the resource packs folder.
        - behavior_packs_dir (str): The directory path of the behavior packs folder.
        - json_updater (JSONUpdater): An instance of the JSONUpdater class.
        """
        self.bds_directory = bds_directory
        self.resource_packs_dir = os.path.join(bds_directory, 'resource_packs')
        self.behavior_packs_dir = os.path.join(bds_directory, 'behavior_packs')
        self.json_updater = JSONUpdater(bds_directory)
        logging.basicConfig(level=logging.INFO)
    
    def add_pack(self, pack_path):
        """
        Adds a pack to the pack handler.
        Parameters:
        - pack_path (str): The path to the pack.
        Returns:
        - None
        Raises:
        - FileNotFoundError: If the pack path does not exist.
        - ValueError: If the pack format is invalid.
        """
        if not os.path.exists(pack_path):
            logging.error(f"Pack path does not exist: {pack_path}")
            return
        
        if pack_path.endswith('.mcaddon'):
            self._unzip_mcaddon(pack_path)
        elif pack_path.endswith('.mcpack'):
            self._unzip_pack(pack_path)
        elif os.path.isdir(pack_path):
            self._process_pack_directory(pack_path)
        else:
            logging.error(f"Invalid pack format: {pack_path}")
    
    def _unzip_mcaddon(self, addon_path):
        """
        Unzips the specified MCAddon file and processes the pack directories.
        Parameters:
        addon_path (str): The path to the MCAddon file.
        Returns:
        None
        """
        with zipfile.ZipFile(addon_path, 'r') as zip_ref:
            temp_dir = os.path.join(self.bds_directory, 'temp')
            zip_ref.extractall(temp_dir)
            
            for root, dirs, _ in os.walk(temp_dir):
                for dir_name in dirs:
                    pack_dir = os.path.join(root, dir_name)
                    self._process_pack_directory(pack_dir)
            
            shutil.rmtree(temp_dir)

    def _unzip_pack(self, zip_path):
        """
        Unzips the pack located at the given zip_path and processes its contents.

        Parameters:
        - zip_path (str): The path to the pack zip file.

        Returns:
        - None
        """
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            temp_dir = os.path.join(self.bds_directory, 'temp')
            zip_ref.extractall(temp_dir)
            for root, dirs, files in os.walk(temp_dir):
                for dir_name in dirs:
                    self._process_pack_directory(os.path.join(root, dir_name))
            shutil.rmtree(temp_dir)

    
    def _process_pack_directory(self, directory):
        manifest_path = os.path.join(directory, 'manifest.json')
        if not os.path.exists(manifest_path):
            logging.error(f"Manifest.json not found in {directory}")
            return
        
        # Parse the manifest
        with open(manifest_path, 'r') as file:
            manifest = json.load(file)
        pack_type = ManifestParser.identify_pack_type(manifest_path)
        
        if pack_type == 'resource':
            destination_dir = self.resource_packs_dir
        elif pack_type == 'behavior':
            destination_dir = self.behavior_packs_dir
        else:
            logging.error(f"Unknown pack type in {directory}")
            return
        
        pack_name = os.path.basename(directory)
        destination_path = os.path.join(destination_dir, pack_name)

        if os.path.exists(destination_path):
            confirmation = input(f"Pack {pack_name} already exists. Overwrite? (y/n): ")
            if confirmation.lower() != 'y':
                logging.info(f"Skipping {pack_name}")
                return
        
        shutil.move(directory, destination_path)
        logging.info(f"Pack {pack_name} added to {destination_dir}")
        
        # Correctly pass the manifest dictionary here
        self.json_updater.update_valid_known_packs(pack_type, manifest)
        self.json_updater.update_world_packs(pack_type, manifest)

