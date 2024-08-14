from typing import Optional

from pydantic import BaseModel, Field


class MainConfigEntity(BaseModel):
    auth_token: Optional[str] = Field(None, alias='thestage_auth_token')
    config_local_path: Optional[str] = Field(None, alias='thestage_config_local_path')
    config_global_path: Optional[str] = Field(None, alias='thestage_config_global_path')
    config_file_name: Optional[str] = Field(None, alias='thestage_config_file_name')
    config_api_link: Optional[str] = Field(None, alias='thestage_api_url')


class DaemonConfigEntity(BaseModel):
    daemon_token: Optional[str] = Field(None, alias='daemon_token')
    backend_api_url: Optional[str] = Field(None, alias='backend_api_url')


class RuntimeConfigEntity(BaseModel):
    working_directory: Optional[str] = Field(None, alias='working_directory') # TODO move to main


class ConfigEntity(BaseModel):
    main: MainConfigEntity = Field(default_factory=MainConfigEntity, alias='main')
    runtime: RuntimeConfigEntity = Field(default_factory=RuntimeConfigEntity, alias="runtime") # TODO merge with main
    daemon: DaemonConfigEntity = Field(default_factory=DaemonConfigEntity, alias="daemon") # TODO this should not be in core package
    start_on_daemon: bool = Field(False, alias='start_on_daemon') # TODO this should not be in core package
