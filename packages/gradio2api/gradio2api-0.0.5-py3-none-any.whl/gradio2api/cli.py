from fastapi import FastAPI
from .clients_aggregator import Aggregator
import argparse
import uvicorn
import json

def cli_remote():
  parser = argparse.ArgumentParser(
    description="""\
    This is the command line tool for gradio2api remote server, please use `gardio2api.Aggregator` detail setting.
    Sample command:
    ```sh
    gradio2api SinDarSoup/TheWorld;/TheWorld 
    ```
    """,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
  )
  parser.add_argument("servers", nargs="*", type=str, help="""server configs, format "{uri};{router}". (e.g. "http://localhost:7860;/local", "SinDarSoup/audio_tagging_mit;") """)
  parser.add_argument("--gradio_client_config", type=str, default=None, help="The json file path of gradio_client.")
  parser.add_argument("--host", type=str, default="127.0.0.1", help="The host for uvicorn.")
  parser.add_argument("--port", type=int, default=8000, help="The port for uvicorn.")
  
  group = parser.add_mutually_exclusive_group(required=False)
  group.add_argument('--allow-error', dest='error_allowed', action='store_true', help="Allow error")
  group.add_argument('--not-allow-error', dest='error_allowed', action='store_false', help="Do not allow error")
  parser.set_defaults(error_allowed=True)

  args = parser.parse_args().__dict__

  servers = args["servers"]
  gradio_client_config_path = args["gradio_client_config"]
  host = args["host"]
  port = args["port"]
  error_allowed = args["error_allowed"]

  remote_servers_config_list = []
  for s in servers:
    ss = s.split(";")
    assert len(ss) <= 2
    if len(ss) == 2:
      uri, prefix = ss
    else:
      uri, prefix = ss[0], ""
    remote_servers_config_list.append(
      {"uri":uri, "prefix":prefix},
    )

    J = {}
    if gradio_client_config_path:
      J = json.load(open(gradio_client_config_path,"r"))

    remote_servers_config_list = [
      {
        **J,
        **orginal_config,
      }
      for orginal_config in remote_servers_config_list
    ]

  router = Aggregator(
    remote_servers_config_list,
    error_allowed=error_allowed
  )
  app = FastAPI()
  app.include_router(router)
  uvicorn.run(
    app,
    host=host,
    port=port,
  )

if __name__ == "__main__":
  cli_remote()