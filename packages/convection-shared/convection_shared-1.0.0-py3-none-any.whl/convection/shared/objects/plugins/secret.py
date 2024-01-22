# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Convection Shared Library,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###
import logging
from random import shuffle
from pathlib import Path
import threading
import typing
from cryptography.fernet import MultiFernet,Fernet

from atckit.utilfuncs import UtilFuncs
from atckit.version import version_locator

from convection.shared.config import ConvectionConfigCore
from convection.shared.exceptions import VersionCompatibilityError
from convection.shared.objects.plugin_metadata import ConvectionPluginMetadata

class ConvectionPlugin_Secret:
    """Convection Plugin base, Secrets
    Secrets Stores and Handling
    """

    _specker_root_spec:str # Specker Root Spec for Raw Config
    """Specker Root Spec for Raw Config, if not defined, defaults to 'anyitem'"""
    _raw_config:dict[str,typing.Any]
    """Raw Config, load a configuration file or pull/generate config from elsewhere, and put it here If not defined, defaults to empty dict"""

    metadata:typing.Union[ConvectionPluginMetadata,None]
    logger:logging.Logger
    tlock:threading.Lock
    _encryptor:MultiFernet
    _old_encryptor:typing.Union[MultiFernet,None]
    _tmp_encryptor:typing.Union[MultiFernet,None]
    __encryptors_all:list[Fernet]
    _store_path:Path

    _compat_checked:bool

    def __init__(self,name:str,keys:list[bytes],storage_path:Path,store_config:typing.Union[dict[str,typing.Any],None] = None) -> None:
        """Initializer
        @param str \c name Store Name
        @param list[bytes] \c keys Decryption Keys
        @param Path \c storage_path Secrets Storage Root
        @param Union[dict[str,Any],None] \c store_config Secrets Store configuration data
        If you use `self._raw_config` you should attempt to load it from file while
        here (if you saved something during `initialize()`). Fall back to sane defaults
        and use `store_config` data if it doesnt exist.
        Note that `store_config` is only provided when a Secrets Store is created. During normal loading, you should load the configuration file if you use it.
        """
        self._compat_checked = False
        if not hasattr(self,"tlock"):
            self.tlock = threading.Lock()
        if not hasattr(self,"_specker_root_spec"):
            self._specker_root_spec = "anyitem"
        if not hasattr(self,"_raw_config"):
            if store_config is None:
                self._raw_config = {}
            else:
                self._raw_config = store_config
        if not hasattr(self,"logger"):
            self.logger = UtilFuncs.create_object_logger(self)
        self.config = ConvectionConfigCore(self._specker_root_spec,self._raw_config)
        if not hasattr(self,"metadata"):
            try:
                self.metadata = ConvectionPluginMetadata(self.config.get_configuration_value("metadata"))
            except ValueError:
                self.metadata = None
                self.logger.warning(f"Secrets Plugin {name} is not a versioned object")
        if self.metadata is not None:
            self.logger.debug(f"Loading secrets.{name} ({type(self).__qualname__}), Version: {str(self.metadata.version)}, Updated: {self.metadata.updated}")
        else:
            self.logger.debug(f"Loading secrets.{name} ({type(self).__qualname__}) (Not Versioned (No Metadata))")
        self.logger = UtilFuncs.create_object_logger(self)
        if not hasattr(self,"_store_path"):
            self._store_path = storage_path.joinpath(f"{name}.store")
        shuffle(keys)
        self.__encryptors_all = [ Fernet(k) for k in keys ]
        self._encryptor = MultiFernet(self.__encryptors_all)
        self._old_encryptor = None
        self._tmp_encryptor = None

    def compat_check(self,in_metadata:ConvectionPluginMetadata) -> None:
        """Plugin Compatibility Checker
        @param ConvectionPluginMetadata \c in_metadata Incoming Metadata to check Version against loaded version compatibility string
        @retval None Nothing
        @raises SystemError No Metadata Object
        @raises VersionCompatibilityError Incoming Version is incompatible with Loaded version
        Sets `_compat_checked = True` after running, to allow developer to select whether or not to run compat again
        """
        self_name:str = type(self).__qualname__
        if self.metadata is None:
            raise SystemError(f"{self_name} did not have a Metadata object")
        compatible:bool = len(version_locator(self.metadata.compatibility,[str(in_metadata.version)])) > 0
        if not compatible:
            raise VersionCompatibilityError(f"Existing {self_name} (version {str(in_metadata.version)}) is not compatible with {str(self.metadata.version)}; Loaded Compat: {self.metadata.compatibility}")
        self.logger.debug(f"{self_name} Compatibility Check passed")
        if in_metadata.version != self.metadata.version:
            self.logger.warning(f"{self_name} Version has changed, its structure will be upgraded on the next write")
        self._compat_checked = True

    def initialize(self) -> None:
        """Creation Initializer
        Setup New Secrets Storage data for initial read (EX: create empty data, then _read() and _write())
        @retval None Nothing
        Do not add additional arguments here
        If you use `self._raw_config`, you should be sure to write the initial configuration in here
        """
        raise NotImplementedError("This function should be overwritten by the Secrets Store Object")

    def rotate(self,new_keys:list[bytes]) -> bool:
        """Encryption Key Rotation
        @param list[bytes] \c new_keys List of new Keys to be used
        @retval bool Success/Failure
        Do not add additional arguments here
        Be sure to call `_rotate_init` and `_rotate_finish`
        """
        raise NotImplementedError("This function should be overwritten by the Secrets Store Object")

    def _rotate_init(self,new_keys:list[bytes]) -> None:
        """Initiate Key Rotation Proceedures
        @param list[bytes] \c new_keys List of New Fernet Keys
        @retval None Nothing
        Creates `_old_encryptor` which is the `_encryptor` before Rotation was called
        Creates `_tmp_encryptor` which is a temporary encryptor with New Keys + Old Keys (in that order)
        Sets `_encryptor` to a new MultiFernet object containing only the New Keys
        """
        self._old_encryptor = self._encryptor
        in_keys:list[Fernet] = [ Fernet(k) for k in new_keys ]
        shuffle(in_keys)
        all_keys:list[Fernet] = in_keys + self.__encryptors_all.copy()
        self.__encryptors_all = in_keys
        self._tmp_encryptor = MultiFernet(all_keys)
        self._encryptor = MultiFernet(self.__encryptors_all)

    def _rotate_finish(self) -> None:
        """Finish Key Rotation Proceedures
        @retval None Nothing
        Removes `_old_encryptor` and `_tmp_encryptor`
        """
        self._old_encryptor = None
        self._tmp_encryptor = None

    def configure(self,**kwargs:typing.Any) -> typing.Any:
        """Secrets Store Configuration View/Set
        View or Set configuration data
        @param dict[str,Any] \c **kwargs Args
        @retval bool Success/Failure
        Additional arguments may be added here
        """
        raise NotImplementedError("This function should be overwritten by the Secrets Store Object")

    def info(self) -> dict[str,typing.Any]:
        """Secrets Store Stats and Information
        View Store Information (Like Metadata) and Stats (Accesses, Secret Count, etc)
        @param dict[str,Any] \c **kwargs Args
        @retval bool Success/Failure
        Additional arguments may be added here
        """
        raise NotImplementedError("This function should be overwritten by the Secrets Store Object")

    def marked_for_delete(self) -> None:
        """Secret Store Destruction call
        Perform Secrets Store Cleanup on Deletion
        @retval None Nothing
        """
        raise NotImplementedError("This function should be overwritten by the Secrets Store Object")

    def create(self,**kwargs:typing.Any) -> bool:
        """Secrets data create/store
        Create new secrets data
        @param dict[str,Any] \c **kwargs Args
        @retval bool Success/Failure
        Additional arguments may be added here
        """
        raise NotImplementedError("This function should be overwritten by the Secrets Store Object")

    def modify(self,**kwargs:typing.Any) -> bool:
        """Secrets data modify
        Modify existing secrets data
        @param dict[str,Any] \c **kwargs Args
        @retval bool Success/Failure
        Additional arguments may be added here
        """
        raise NotImplementedError("This function should be overwritten by the Secrets Store Object")

    def destroy(self,**kwargs:typing.Any) -> bool:
        """Secrets data destroy/remove
        Remove secrets data
        @param dict[str,Any] \c **kwargs Args
        @retval bool Success/Failure
        Additional arguments may be added here
        """
        raise NotImplementedError("This function should be overwritten by the Secrets Store Object")

    def get(self,**kwargs:typing.Any) -> typing.Any:
        """Secrets Data get
        Get an existing Secret
        @param dict[str,Any] \c **kwargs Args
        @retval Any Item Value
        Additional arguments may be added here
        """
        raise NotImplementedError("This function should be overwritten by the Secrets Store Object")

    def list(self,**kwargs:typing.Any) -> list[str]:
        """Secrets List
        Get List of Registered Secrets
        @param dict[str,Any] \c **kwargs Args
        @retval list[str] Key Names
        Additional arguments may be added here
        """
        raise NotImplementedError("This function should be overwritten by the Secrets Store Object")

    def _shuffle(self) -> None:
        """Key Shuffle. Randomize Encryption Keys, and Reload Encryptor
        Ensures that data is encrypted with random keys from the loaded KeySet, should be called before each write
        @retval None Nothing
        **DO NOT OVERWRITE THIS FUNCTION**
        """
        shuffle(self.__encryptors_all)
        self._encryptor = MultiFernet(self.__encryptors_all)

    def _read(self) -> None:
        """Load Encrypted Data for Reading/Modification
        @retval None Nothing
        Do not add additional arguments here
        """
        raise NotImplementedError("This function should be overwritten by the Secrets Store Object")

    def _write(self) -> None:
        """Encrypt and Write Loaded Data
        @retval None Nothing
        Do not add additional arguments here

        `self._shuffle()` should be called before each actual encryption write
        `self._store_path.chmod(0o600)` should be run after write, to prevent others even reading the encrypted data
        `self._close()` should be called after writing, and on exceptions, etc.
        """
        # self._shuffle() # Be sure to shuffle before each write
        raise NotImplementedError("This function should be overwritten by the Secrets Store Object")
        # self._store_path.chmod(0o600) # Be Sure to chmod 600 the secrets store to prevent reading from others after writing
        # self._close() # Be sure to close at end of write, and be sure to close on exception, etc

    def _close(self) -> None:
        """Close / Unload Data
        @retval None Nothing
        Do not add additional arguments here

        Clear any Loaded data from memory by running `.clear()` on dictionaries/lists, set objects to None, etc.
        """
        raise NotImplementedError("This function should be overwritten by the Secrets Store Object")
