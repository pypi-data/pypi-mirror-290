from typing import Any
from pydantic import BaseModel, model_validator
from .gr_fastapi import RemoteGradioAppRouter
from .utils.hash import add_key_and_verify as add_prefix_and_verify
from typing_extensions import Self
from typing import Optional
from fastapi import APIRouter

class AppConfig(BaseModel):
  uri:str
  prefix: str

  # @model_validator(mode="after")
  # def check_pefix(self)->Self:
  #   add_prefix_and_verify(self.prefix)
  #   return self

class PostAppConfig(AppConfig):
  sucess:bool
  api_names: Optional[list[str]] = None
  num_of_apis:Optional[int] = None

class Info(BaseModel):
  info: list[PostAppConfig] = []

class Aggregator(APIRouter):
  config_list : list[AppConfig | dict]
  graido_app_routers: dict[str, list[RemoteGradioAppRouter]]
  error_allowed:bool
  info: Info

  def __init__(
      self,
      config_list:list[AppConfig|dict],
      error_allowed:bool=False,
      *router_args,
      **router_kwargs,
    ):
    super().__init__(*router_args, **router_kwargs)
    self.get("/info")(self.get_info)

    self.config_list = []
    self.graido_app_routers = dict()
    self.info = Info()
    self.error_allowed = error_allowed
    
    self.assign_from_config_list(config_list)


  def get_info(self)->list[PostAppConfig]:
    return [
      post_config
      for post_config in self.info.info
    ]

  @classmethod
  def _normalize_config(cls, config:list[AppConfig|dict]):
    if isinstance(config, AppConfig):
      return config
    return AppConfig(**config)
  
  def assign_from_config(self, config:AppConfig|dict):
    config = self._normalize_config(config)
    self.config_list.append(config)

    uri = config.uri
    prefix = config.prefix
    try:
      router = RemoteGradioAppRouter(
        gradio_uri=uri,
        prefix=prefix,
      )
      api_names = list(router.gradio_application.apis.keys())

      if prefix not in self.graido_app_routers:
          self.graido_app_routers[prefix] = []
      
      self.graido_app_routers[prefix].append(router)

      self.info.info.append(
        PostAppConfig(
          uri=uri,
          prefix=prefix,
          sucess=True,
          api_names=api_names,
          num_of_apis=len(api_names)
        )
      )
      self.include_router(router)

    except Exception as e:
      if self.error_allowed:
        print(f"[Get error while loading {config}]")
        print(e)
        self.info.info.append(
          PostAppConfig(
            uri=uri,
            prefix=prefix,
            sucess=False,
          )
        )
      else:
        raise e

  def assign_from_config_list(self, config_list):
    for config in config_list:
      self.assign_from_config(config)
  