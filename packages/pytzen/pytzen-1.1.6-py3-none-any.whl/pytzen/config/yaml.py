import os
import yaml

class YAML:
    """Dynamic object for storing configuration data.

    This class allows dynamic attribute assignment, where the attributes 
    are based on the provided keyword arguments. It is used to represent 
    configuration data loaded from multiple YAML files.

    Args:
        **kwargs: Arbitrary keyword arguments that will be converted to 
                  attributes of the instance.
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class Config:
    """Handles loading and management of YAML configuration files.

    This class provides methods to load and aggregate configuration data 
    from multiple YAML files located in a specified folder. The data is 
    then made available through a `YAML` object.

    Attributes:
        folder_path (str): The path to the folder containing YAML files.
    """
    def __init__(self, folder_path: str) -> None:
        """Initializes the Config object with the folder path.

        Args:
            folder_path (str): The path to the directory containing YAML 
            files.
        """
        self.folder_path = folder_path
    
    def get(self) -> YAML:
        """Returns a YAML object containing the merged configuration data.

        This method aggregates all the YAML files in the specified folder 
        and returns a `YAML` object that contains all the configurations 
        as attributes.

        Returns:
            YAML: An instance of the `YAML` class with all configurations.
        """
        return self._load_all_yaml_files()

    def _load_all_yaml_files(self) -> YAML:
        """Loads all YAML files in the specified directory.

        This method iterates over all files in the directory specified by 
        `folder_path`, loads the content of files with `.yaml` or `.yml` 
        extensions, and aggregates them into a single `YAML` object.

        Returns:
            YAML: An instance of the `YAML` class containing all loaded 
            configurations as attributes.
        """
        config_data = {}
        for filename in os.listdir(self.folder_path):
            if filename.endswith(('.yaml', '.yml')):
                attr_name, file_content = self.__load_yaml_file(filename)
                config_data[attr_name] = file_content
        
        return YAML(**config_data)

    def __load_yaml_file(self, filename: str) -> tuple:
        """Loads a single YAML file.

        This method reads the contents of a single YAML file and returns 
        a tuple containing the attribute name (derived from the filename) 
        and the file's content.

        Args:
            filename (str): The name of the YAML file to load.

        Returns:
            tuple: A tuple where the first element is the attribute name 
                   (filename without extension) and the second element is 
                   the parsed content of the YAML file.
        """
        file_path = os.path.join(self.folder_path, filename)
        with open(file_path, "r") as file:
            file_content = yaml.safe_load(file)
        attr_name = os.path.splitext(filename)[0]
        return attr_name, file_content

# Example usage:
# config = Config("path/to/config/folder")
# yaml_config = config.get()