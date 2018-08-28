import argparse
import configargparse
import copy
import json
import re


class Configuration:
    """Provides access to config values. These are populated from a combination of config files and command line args.
    """
    def __init__(self, config_files: list):
        parser = configargparse.ArgParser(default_config_files=config_files)
        self._setup_configuration_keys(parser)
        self._config = parser.parse_known_args()[0]  # First element in tuple is the known args

    def print_as_json(self):
        """Prints the config as json. Any keys containing password are hidden
        """
        config_dict = self.as_dict()
        for key in config_dict:
            if self._should_mask_key(key):
                config_dict[key] = '***********'
        print(json.dumps(config_dict, sort_keys=True, indent=4))

    def as_dict(self) -> dict:
        return copy.deepcopy(vars(self._config))

    def get(self, config_key):
        """Get a value from the config for a specified key. The type that is returned is unknown
        """
        return self.as_dict()[config_key]

    def add(self, config_key: str, value):
        """Allows a config value to be added.
        """
        assert isinstance(self._config, argparse.Namespace)
        vars(self._config)[config_key] = value

    @staticmethod
    def _should_mask_key(key):
        patterns_to_hide = ['.*password.*', '.*access_key.*']
        for pattern_string in patterns_to_hide:
            pattern = re.compile(pattern_string)
            if pattern.match(key):
                return True
        return False

    @staticmethod
    def _setup_configuration_keys(parser: configargparse.ArgumentParser):
        # The keys supplied in the template are for example only. Remove any that are not required in your job and add
        # Any extras
        parser.add_argument('--s3_prefix', required=True, help='s3 bucket folder prefix')
        parser.add_argument('--s3_bucket', required=True, help='s3 bucket name')

