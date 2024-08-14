import os
import json
import logging

class JSONUpdater:
    def __init__(self, bds_directory):
        """
        Initializes a JsonUpdater object.

        Parameters:
        - bds_directory (str): The path to the BDS (Bedrock Dedicated Server) directory.

        Attributes:
        - bds_directory (str): The path to the BDS (Bedrock Dedicated Server) directory.
        - world_dir (str): The path to the 'world' directory inside the BDS directory.
        """
        self.bds_directory = bds_directory
        self.world_dir = os.path.join(bds_directory, 'worlds', 'world')
        logging.basicConfig(level=logging.INFO)

    
    def update_valid_known_packs(self, pack_type, manifest):
        """
        Description:
        Update the valid_known_packs.json file with the new pack information.
        
        Parameters:
        - pack_type (str): The type of pack (e.g., 'resource', 'behavior').
        - manifest (dict): The manifest containing the pack information.
        
        Returns:
        None
        
        Raises:
        None
        """
        valid_known_packs_path = os.path.join(self.bds_directory, 'valid_known_packs.json')
        pack_path = f"{pack_type}_packs/{manifest['header']['name']}"
        
        new_entry = {
            "file_system": "RawPath",
            "path": pack_path,
            "uuid": manifest['header']['uuid'],
            "version": ".".join(map(str, manifest['header']['version']))
        }

        if os.path.exists(valid_known_packs_path):
            with open(valid_known_packs_path, 'r') as file:
                data = json.load(file)
        else:
            data = []

        # Check if the entry already exists and update it if necessary
        updated = False
        for entry in data:
            if 'uuid' not in entry:
                logging.info(f"Skipping non-pack entry: {entry}")
                continue  # Skip non-pack entries like { "file_version" : 2 }

            if entry['uuid'] == new_entry['uuid']:
                entry.update(new_entry)
                updated = True
                break

        if not updated:
            data.append(new_entry)

        with open(valid_known_packs_path, 'w') as file:
            json.dump(data, file, indent=4)
        
        logging.info(f"Updated valid_known_packs.json with pack {manifest['header']['uuid']}")

    def update_world_packs(self, pack_type, manifest):
        """
        Update or create world_resource_packs.json or world_behavior_packs.json with the new pack information.
        """
        json_file = 'world_resource_packs.json' if pack_type == 'resource' else 'world_behavior_packs.json'
        file_path = os.path.join(self.world_dir, json_file)
        pack_uuid = manifest['header']['uuid']
        pack_version = manifest['header']['version']
        
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
        else:
            data = []

        new_entry = {"pack_id": pack_uuid, "version": pack_version}

        # Check if the entry already exists and update it if necessary
        if new_entry not in data:
            data.append(new_entry)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        
        logging.info(f"Updated {json_file} with pack {pack_uuid}")

    def validate_json_files(self):
        """
        Validate the presence of packs in world_resource_packs.json or world_behavior_packs.json.
        """
        resource_json = os.path.join(self.world_dir, 'world_resource_packs.json')
        behavior_json = os.path.join(self.world_dir, 'world_behavior_packs.json')
        
        self._validate_json(resource_json, self.bds_directory + '/resource_packs')
        self._validate_json(behavior_json, self.bds_directory + '/behavior_packs')
    
    def _validate_json(self, json_file, pack_dir):
        """
        Validates the JSON file by checking if the pack IDs listed in the file exist in the specified pack directory.
        Args:
            json_file (str): The path to the JSON file to be validated.
            pack_dir (str): The path to the pack directory.
        Returns:
            None
        """
        if not os.path.exists(json_file):
            logging.warning(f"{json_file} does not exist. Skipping validation.")
            return
        
        with open(json_file, 'r') as file:
            data = json.load(file)
        
        for entry in data:
            pack_uuid = entry['pack_id']
            pack_found = any(pack_uuid in file_name for file_name in os.listdir(pack_dir))
            
            if not pack_found:
                logging.warning(f"Pack {pack_uuid} listed in {json_file} is missing in {pack_dir}.")
            else:
                logging.info(f"Pack {pack_uuid} validated successfully in {json_file}.")
