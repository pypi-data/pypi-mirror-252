# Copyright 2023-2023 by AccidentallyTheCable <cableninja@cableninja.net>.
# All rights reserved.
# This file is part of Convection Secrets Store Plugin for PassDB Key-Value Store,
# and is released under "GPLv3". Please see the LICENSE
# file that should have been included as part of this package.
#### END COPYRIGHT BLOCK ###

import datetime
from pathlib import Path
import re
import secrets
import shutil
import string
import typing

from atckit.utilfuncs import UtilFuncs
from convection.shared.config import ConvectionConfigCore
from convection.shared.exceptions import PathOutsideStoragePath, StoreNotLoadedError,IncompleteError

from convection.shared.objects.plugin_metadata import ConvectionPluginMetadata
from convection.shared.objects.plugins.secret import ConvectionPlugin_Secret

class PassDB_Secret(ConvectionPlugin_Secret):
    """Plugin: Password DB (PassDB)
    Password Generator and Store
    """

    metadata:typing.Union[ConvectionPluginMetadata,None]
    __store_data:typing.Union[dict[str,typing.Any],None]
    _store_name:str
    __write_count:int
    __read_count:int

    def __init__(self, name: str, keys: list[bytes], storage_path: Path, store_config: typing.Union[dict[str, typing.Any],None] = None) -> None:
        self.logger = UtilFuncs.create_object_logger(self)
        self.__store_data = None
        if not hasattr(self,"metadata") or self.metadata is None:
            self.metadata = ConvectionPluginMetadata({
                "version": "1.0.0",
                "author": "AccidentallyTheCable <cableninja@cableninja.net>",
                "updated": int(datetime.datetime.now().strftime("%Y%m%d")),
                "compatibility": ">=:1.0,<:2.0",
                "plugin": {
                    "name": "PassDB",
                    "type": "Secret",
                    "description": "Password Generator and Store"
                }
            })
        self.__write_count = 0
        self.__read_count = 0
        if store_config is None:
            store_config = {}
        if not hasattr(self,"_raw_config"):
            self._raw_config = store_config
        if not hasattr(self,"_specker_root_spec"):
            self._specker_root_spec = "plugin.secret.passdb"
        if "/" in name:
            name = re.sub(r'^\/','',name)
        self._store_path = storage_path.joinpath("passdb/").joinpath(name).resolve()
        try:
            self._store_path.relative_to(storage_path)
        except ValueError as e:
            raise PathOutsideStoragePath(f"{name} would be written to outside of storage root, cannot proceed") from e
        storage_path_str:str = self._store_path.as_posix()
        self.logger.debug(f"PassDB Secrets Store '{name}' path: {storage_path_str}")
        if not self._store_path.parent.is_dir():
            self._store_path.parent.mkdir(parents=True)
        self._store_path.parent.chmod(0o700)
        self._store_name = name
        self.logger.info(f"Loading PassDB Secrets Store '{name}' version: {str(self.metadata.version)}")
        super().__init__("passdb", keys, storage_path, None)

    def initialize(self) -> None:
        with self.tlock:
            if self.metadata is None:
                raise AttributeError("Metadata is required for Secrets Store")
            self.__read_count += 1
            self.__store_data = {}
            self._write()
            self._close()

    def rotate(self, new_keys: list[bytes]) -> bool:
        with self.tlock:
            store_path_str:str = self._store_path.as_posix()
            self.logger.debug(f"Creating Backup of {store_path_str}")
            save_path:Path = Path(store_path_str + ".bak").resolve()
            shutil.copy2(self._store_path,save_path)
            self._rotate_init(new_keys)
            self._read()
            if self.__store_data is None:
                self.logger.error(f"{self._store_name} rotation failed. Could not read store")
                raise StoreNotLoadedError(f"{self._store_name} rotation failed. Could not read store, was not loaded")
            self._write(False)
            self.logger.info(f"Rotated Keys for Secrets Store {self._store_name}")
            self._rotate_finish()
            save_path.unlink()
        return True

    def _read(self) -> None:
        with open(self._store_path,"rb") as f:
            raw:bytes = self._encryptor.decrypt(f.read())
            rawdb:dict[str,typing.Any] = UtilFuncs.load_sstr(raw.decode("utf-8"),"toml")
            if not self._compat_checked:
                old_metadata:ConvectionPluginMetadata = ConvectionPluginMetadata(rawdb["metadata"])
                self.compat_check(old_metadata)
            self.config = ConvectionConfigCore(self._specker_root_spec,rawdb["config"])
            self.__store_data = rawdb["store"]
            if self.__read_count == 0:
                self.__read_count = rawdb["stats"]["reads"]
                self.__write_count = rawdb["stats"]["writes"]
            self.__read_count += 1

    def _write(self,shuffle:bool = True) -> None:
        if shuffle:
            self._shuffle()
        if self.__store_data is None:
            self.logger.error(f"{self._store_name} is not currently opened")
            raise StoreNotLoadedError(f"{self._store_name} is not loaded")
        self.__write_count += 1
        if self.metadata is None:
            raise SystemError(f"{self._store_name} did not have a Metadata object")
        outdb:dict[str,typing.Any] = {
            "metadata": self.metadata.get(),
            "config": self.config.get_configuration_value(None),
            "store": self.__store_data,
            "stats": {
                "reads": self.__read_count,
                "writes": self.__write_count
            }
        }
        with open(self._store_path,"wb") as f:
            raw:bytes = bytes(UtilFuncs.dump_sstr(outdb,"toml"),"utf-8")
            f.write(self._encryptor.encrypt(raw))
        self._store_path.chmod(0o600)
        self._close()

    def _close(self) -> None:
        if self.__store_data is not None:
            self.__store_data.clear()
        self.__store_data = None

    # pylint: disable=arguments-differ
    def configure(self, config_name:typing.Union[str,None] = None, config_value:typing.Union[typing.Any,None] = None) -> typing.Any:
        if config_name is None:
            return self.config.get_configuration_value(None)
        if config_name.startswith("_"):
            raise KeyError(f"Invalid Key {config_name}")
        if config_value is None:
            return self.config.get_configuration_value(config_name)
        raise IncompleteError()

    def info(self) -> dict[str,typing.Any]:
        secrets_count:int = 0
        if self.metadata is None:
            raise SystemError(f"{self._store_name} did not have a Metadata object")
        with self.tlock:
            self._read()
            if self.__store_data is None:
                self._close()
                self.logger.error(f"{self._store_name} is not currently opened")
                raise StoreNotLoadedError(f"{self._store_name} is not loaded")
            secrets_count = len(self.__store_data)
            self._close()
        output:dict[str,typing.Any] = {
            "metadata": self.metadata.get(),
            "stats": {
                "secret_count": secrets_count,
                "reads": self.__read_count,
                "writes": self.__write_count
            }
        }
        return output

    def create(self,secret_name:str,secret_value:typing.Union[str,None] = None,length:typing.Union[int,None] = None,value_type:typing.Union[str,None] = None) -> bool:
        if secret_value is None:
            secret_value = self.__generator(length,value_type)
        with self.tlock:
            self._read()
            if self.__store_data is None:
                self._close()
                self.logger.error(f"{self._store_name} is not currently opened")
                raise StoreNotLoadedError(f"{self._store_name} is not loaded")
            if secret_name in self.__store_data.keys():
                self._close()
                raise KeyError(f"Cannot Create Secret '{secret_name}', already exists. use 'modify' instead")
            self.__store_data[secret_name] = secret_value
            self.logger.info("Created new PassDB Secret")
            self._write()
            self._close()
        return True

    def list(self) -> list[str]:
        result:list[str] = []
        with self.tlock:
            self._read()
            if self.__store_data is None:
                self._close()
                self.logger.error(f"{self._store_name} is not currently opened")
                raise StoreNotLoadedError(f"{self._store_name} is not loaded")
            result = list(self.__store_data.keys())
            self._close()
        return result

    def modify(self,secret_name:str,secret_value:typing.Union[str,None] = None,length:typing.Union[int,None] = None,value_type:typing.Union[str,None] = None) -> bool:
        if secret_value is None:
            secret_value = self.__generator(length,value_type)
        with self.tlock:
            self._read()
            if self.__store_data is None:
                self._close()
                self.logger.error(f"{self._store_name} is not currently opened")
                raise StoreNotLoadedError(f"{self._store_name} is not loaded")
            if secret_name not in self.__store_data.keys():
                self._close()
                raise KeyError(f"Cannot Modify Secret '{secret_name}', does not exist. use 'create' instead")
            self.__store_data[secret_name] = secret_value
            self._write()
            self._close()
        return True

    def destroy(self,secret_name:str) -> bool:
        with self.tlock:
            self._read()
            if self.__store_data is None:
                self._close()
                self.logger.error(f"{self._store_name} is not currently opened")
                raise StoreNotLoadedError(f"{self._store_name} is not loaded")
            if secret_name not in self.__store_data.keys():
                self._close()
                raise KeyError(f"Cannot Destroy Secret '{secret_name}', does not exist")
            self.__store_data.pop(secret_name)
            self._write()
            self._close()
        return True

    def get(self,secret_name:str) -> typing.Any:
        data:typing.Any = None
        with self.tlock:
            self._read()
            if self.__store_data is None:
                self._close()
                self.logger.error(f"{self._store_name} is not currently opened")
                raise StoreNotLoadedError(f"{self._store_name} is not loaded")
            if secret_name not in self.__store_data.keys():
                self._close()
                raise KeyError(f"Cannot Get Secret '{secret_name}', does not exist")
            data = self.__store_data[secret_name]
            self._close()
        return data

    def marked_for_delete(self) -> None:
        with self.tlock:
            self._close()
            self._store_path.unlink()
    # pylint: enable=arguments-differ

    def __generator(self,length:typing.Union[int,None] = None,vtype:typing.Union[str,None] = None) -> str:
        if length is None:
            length = self.config.get_configuration_value("default.length")
        if length is None:
            length = 20
        if vtype is None:
            vtype = self.config.get_configuration_value("default.letters")
        if vtype is None:
            vtype = "printable"
        if not hasattr(string,vtype):
            raise ValueError(f"`vtype` '{vtype}' is not valid. Must be a valid property of `string`")
        alphabet:str = getattr(string,vtype)
        return ''.join(secrets.choice(alphabet) for _ in range(length))
