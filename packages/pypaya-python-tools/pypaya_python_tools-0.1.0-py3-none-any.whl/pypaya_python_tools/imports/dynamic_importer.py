import importlib
import importlib.util
import os
import sys
import logging
from types import ModuleType
from typing import Any, Callable, Dict, List, Optional, Union, Tuple


class ImportLevel:
    PACKAGE = "package"
    MODULE = "module"
    OBJECT = "object"


class SecurityError(Exception):
    """Exception raised for security violations in the DynamicImporter."""
    pass


class DynamicImporter:
    """
    A flexible and powerful class for dynamically importing packages, modules, and objects.

    This class provides methods to import from installed packages, project packages,
    and arbitrary .py files, with consistent handling across different sources.
    """

    def __init__(self, add_to_sys_modules: bool = True, debug: bool = False,
                 allowed_paths: Optional[List[str]] = None,
                 disallowed_modules: Optional[List[str]] = None):
        self._loaded_modules: Dict[str, ModuleType] = {}
        self._module_paths: Dict[str, str] = {}
        self._add_to_sys_modules = add_to_sys_modules
        self._debug = debug

        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self.set_allowed_paths(allowed_paths or [])
        self.set_disallowed_modules(disallowed_modules or [])

    def import_object(self,
                      import_path: str,
                      level: str = ImportLevel.OBJECT,
                      base_path: Optional[str] = None,
                      object_name: Optional[str] = None) -> Any:
        """
        Import a package, module, or object based on the provided path and level.

        Args:
            import_path (str): The path to the object to import. Can be a dot-separated
                               path or a file system path.
            level (str): The import level (PACKAGE, MODULE, or OBJECT).
            base_path (Optional[str]): Base path for relative imports.
            object_name (Optional[str]): Name of the specific object to import from the module.
                                         If not provided, the last part of the import_path is used.

        Returns:
            Any: The imported package, module, or object.

        Raises:
            ImportError: If the import fails.
            SecurityError: If the import is not allowed due to security restrictions.
        """
        try:
            self._check_security(import_path, base_path)
            if os.path.isfile(import_path) or (base_path and os.path.isfile(os.path.join(base_path, import_path))):
                return self._import_from_file(import_path, level, base_path, object_name)
            else:
                return self._import_from_package(import_path, level, object_name)
        except Exception as e:
            self.logger.error(f"Import failed: {str(e)}", exc_info=self._debug)
            raise ImportError(f"Failed to import {import_path}: {str(e)}")

    def _check_security(self, import_path: str, base_path: Optional[str] = None) -> None:
        """
        Check if the import is allowed based on security settings.

        Args:
            import_path (str): The path to the object to import.
            base_path (Optional[str]): Base path for relative imports.

        Raises:
            SecurityError: If the import is not allowed due to security restrictions.
        """
        full_path = os.path.join(base_path, import_path) if base_path else import_path

        # If no allowed paths are set, allow all imports. Otherwise, check if the import path is allowed.
        if self._allowed_paths and not any(full_path.startswith(path) for path in self._allowed_paths):
            raise SecurityError(f"Import from {full_path} is not allowed")

        # Check if the module is in disallowed modules
        module_name = import_path.split('.')[0]
        if module_name in self._disallowed_modules:
            raise SecurityError(f"Import of module {module_name} is not allowed")

    def _import_from_file(self,
                          file_path: str,
                          level: str,
                          base_path: Optional[str] = None,
                          object_name: Optional[str] = None) -> Any:
        """
        Import from a file.

        Args:
            file_path (str): The path to the file to import.
            level (str): The import level (PACKAGE, MODULE, or OBJECT).
            base_path (Optional[str]): Base path for relative imports.
            object_name (Optional[str]): Name of the specific object to import from the module.

        Returns:
            Any: The imported package, module, or object.

        Raises:
            ImportError: If the import fails.
        """
        full_path = os.path.join(base_path, file_path) if base_path else file_path
        module_name = os.path.splitext(os.path.basename(full_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, full_path)
        if spec is None:
            raise ImportError(f"Failed to create spec for {full_path}")
        module = importlib.util.module_from_spec(spec)
        self._loaded_modules[module_name] = module
        self._module_paths[module_name] = full_path
        if self._add_to_sys_modules:
            sys.modules[module_name] = module
        spec.loader.exec_module(module)
        self.logger.info(f"Successfully imported module {module_name} from file {full_path}")
        return self._get_object_by_level(module, level, module_name, object_name)

    def _import_from_package(self, import_path: str, level: str, object_name: Optional[str] = None) -> Any:
        """
        Import from a package, including nested subpackages.

        Args:
            import_path (str): The dot-separated path to the object to import.
            level (str): The import level (PACKAGE, MODULE, or OBJECT).
            object_name (Optional[str]): Name of the specific object to import from the module.

        Returns:
            Any: The imported package, module, or object.

        Raises:
            ImportError: If the import fails.
        """
        try:
            if level == ImportLevel.PACKAGE:
                module = importlib.import_module(import_path)
                self.logger.info(f"Successfully imported package {import_path}")
                return module
            elif level == ImportLevel.MODULE:
                module = importlib.import_module(import_path)
                self.logger.info(f"Successfully imported module {import_path}")
                return module
            else:  # ImportLevel.OBJECT
                if object_name:
                    module_path = import_path
                else:
                    module_path, object_name = import_path.rsplit('.', 1)
                module = importlib.import_module(module_path)
                obj = self._get_object_by_level(module, level, object_name, object_name)
                self.logger.info(f"Successfully imported object {object_name} from module {module_path}")
                return obj
        except (ImportError, AttributeError) as e:
            self.logger.error(f"Failed to import {import_path}: {str(e)}", exc_info=self._debug)
            raise ImportError(f"Failed to import {import_path}: {str(e)}")

    def _get_object_by_level(self,
                             module: ModuleType,
                             level: str,
                             default_name: str,
                             object_name: Optional[str] = None) -> Any:
        """
        Get the appropriate object based on the import level.

        Args:
            module (ModuleType): The imported module.
            level (str): The import level (PACKAGE, MODULE, or OBJECT).
            default_name (str): The default name to use if object_name is not provided.
            object_name (Optional[str]): Name of the specific object to import from the module.

        Returns:
            Any: The imported package, module, or object.

        Raises:
            ValueError: If an invalid import level is provided.
            AttributeError: If the specified object is not found in the module.
        """
        if level == ImportLevel.PACKAGE or level == ImportLevel.MODULE:
            return module
        elif level == ImportLevel.OBJECT:
            name_to_use = object_name or default_name
            if hasattr(module, name_to_use):
                return getattr(module, name_to_use)
            else:
                raise AttributeError(f"Object '{name_to_use}' not found in module {module.__name__}")
        else:
            raise ValueError(f"Invalid import level: {level}")

    def safe_import(self,
                    import_path: str,
                    level: str = ImportLevel.OBJECT,
                    base_path: Optional[str] = None) -> Optional[Any]:
        """
        Safely import an object, returning None if import fails.

        Args:
            import_path (str): The path to the object to import.
            level (str): The import level (PACKAGE, MODULE, or OBJECT).
            base_path (Optional[str]): Base path for relative imports.

        Returns:
            Optional[Any]: The imported object, or None if import fails.
        """
        try:
            return self.import_object(import_path, level, base_path)
        except (ImportError, SecurityError):
            self.logger.warning(f"Safe import failed for {import_path}", exc_info=self._debug)
            return None

    def load_plugins(self, plugin_dir: str, base_class: Optional[type] = None) -> List[Any]:
        """
        Load all plugins from a directory.

        Args:
            plugin_dir (str): The directory containing plugin files.
            base_class (Optional[type]): If provided, only load classes that inherit from this base class.

        Returns:
            List[Any]: A list of loaded plugin classes or objects.
        """
        plugins = []
        for filename in os.listdir(plugin_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                try:
                    module = self.import_object(os.path.join(plugin_dir, filename), ImportLevel.MODULE)
                    for attribute_name in dir(module):
                        attribute = getattr(module, attribute_name)
                        if isinstance(attribute, type):
                            if base_class is None or issubclass(attribute, base_class):
                                plugins.append(attribute)
                                self.logger.info(f"Loaded plugin {attribute.__name__} from {filename}")
                except (ImportError, SecurityError) as e:
                    self.logger.error(f"Error loading plugin {filename}: {str(e)}", exc_info=self._debug)
        return plugins

    def call_function(self, func: Union[Callable, str], *args: Any, **kwargs: Any) -> Any:
        """
        Call a function, whether it's already imported or needs to be imported.

        Args:
            func (Union[Callable, str]): The function to call, or a string path to the function.
            *args: Positional arguments to pass to the function.
            **kwargs: Keyword arguments to pass to the function.

        Returns:
            Any: The result of the function call.

        Raises:
            ImportError: If the function cannot be imported.
            TypeError: If the imported object is not callable.
        """
        if isinstance(func, str):
            func = self.import_object(func, ImportLevel.OBJECT)

        if not callable(func):
            raise TypeError(f"Object {func} is not callable")

        return func(*args, **kwargs)

    def reload_module(self, module_name: str) -> None:
        """
        Reload a previously imported module.

        Args:
            module_name (str): The name of the module to reload.

        Raises:
            ImportError: If the module has not been previously imported by this importer.
        """
        if module_name not in self._loaded_modules:
            raise ImportError(f"Module {module_name} has not been imported by this DynamicImporter")

        module_path = self._module_paths[module_name]
        reloaded_module = self.import_object(module_path, ImportLevel.MODULE)
        self._loaded_modules[module_name] = reloaded_module
        if self._add_to_sys_modules:
            sys.modules[module_name] = reloaded_module

        self.logger.info(f"Successfully reloaded module {module_name}")

    @staticmethod
    def add_to_path(directory: str) -> None:
        """
        Add a directory to the Python path.

        Args:
            directory (str): The directory to add to the Python path.
        """
        abs_path = os.path.abspath(directory)
        if abs_path not in sys.path:
            sys.path.append(abs_path)
            logging.info(f"Added {abs_path} to Python path")

    def set_debug(self, debug: bool) -> None:
        """
        Set the debug mode.

        Args:
            debug (bool): Whether to enable debug mode.
        """
        self._debug = debug
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)
        self.logger.info(f"Debug mode set to {debug}")

    def set_add_to_sys_modules(self, add_to_sys_modules: bool) -> None:
        """
        Set whether to add imported modules to sys.modules.

        Args:
            add_to_sys_modules (bool): Whether to add imported modules to sys.modules.
        """
        self._add_to_sys_modules = add_to_sys_modules
        self.logger.info(f"Add to sys.modules set to {add_to_sys_modules}")

    def set_allowed_paths(self, allowed_paths: List[str]) -> None:
        """
        Set the list of allowed import paths.

        Args:
            allowed_paths (List[str]): List of allowed import paths.
        """
        self._allowed_paths = [os.path.abspath(path) for path in allowed_paths]
        self.logger.info(f"Allowed paths set to {self._allowed_paths}")

    def set_disallowed_modules(self, disallowed_modules: List[str]) -> None:
        """
        Set the list of disallowed modules.

        Args:
            disallowed_modules (List[str]): List of disallowed module names.
        """
        self._disallowed_modules = disallowed_modules
        self.logger.info(f"Disallowed modules set to {self._disallowed_modules}")
