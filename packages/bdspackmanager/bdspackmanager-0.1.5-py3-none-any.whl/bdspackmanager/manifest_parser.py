import json

import json

class ManifestParser:
    @staticmethod
    def identify_pack_type(manifest_path):
        with open(manifest_path, 'r') as file:
            manifest = json.load(file)
        
        if 'modules' not in manifest:
            raise ValueError(f"Invalid manifest: {manifest_path}")
        
        has_resource = any(module['type'] == 'resources' for module in manifest['modules'])
        has_behavior = any(module['type'] == 'data' for module in manifest['modules'])
        
        if has_resource:
            return 'resource'
        elif has_behavior:
            return 'behavior'
        else:
            raise ValueError(f"Unknown pack type in manifest: {manifest_path}")
