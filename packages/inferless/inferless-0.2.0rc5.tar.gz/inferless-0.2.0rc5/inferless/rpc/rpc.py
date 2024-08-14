import base64
import json
import os
import time

import dill
import requests
import rich

from . import config_yaml
from inferless.auth.token import auth_header
from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live


RUNTIME_BUILD_COMPLETED = "RUNTIME_BUILD_COMPLETED"
RUNTIME_BUILD_STARTED = "RUNTIME_BUILD_STARTED"
INFERENCE_COMPLETED = "INFERENCE_COMPLETED"
INFERENCE_STARTED = "INFERENCE_STARTED"
RUNTIME_CACHE_HIT = "RUNTIME_CACHE_HIT"


def call_rpc(func, config_path, *args, **kwargs):
    console = Console()
    spinner = Spinner("dots", "Processing...")
    live = Live(spinner, refresh_per_second=10, transient=True)
    live.start()
    payload = get_rpc_payload(func, config_path, *args, **kwargs)
    headers = get_rpc_headers()
    url = get_rpc_url()
    with requests.post(url, json=payload, stream=True, headers=headers, timeout=600) as response:
        spinner.text = "Getting Infra ready..."
        live.update(spinner)
        for line in response.iter_lines():
            if line:
                msg_type = line.decode("utf-8").split(":")[0]
                if msg_type == "event":
                    event = line.decode("utf-8")[6:]
                    if event == RUNTIME_BUILD_STARTED:
                        live.stop()
                        console.print("[green]Infra is ready \u2713[/green]")
                        spinner.text = "Building runtime..."
                        live = Live(spinner, refresh_per_second=10, transient=True)
                        live.start()
                    elif event == RUNTIME_BUILD_COMPLETED:
                        live.stop()
                        console.print("[green]Runtime is ready \u2713[/green]")
                        spinner.text = "Waiting for inference to start..."
                        live = Live(spinner, refresh_per_second=10, transient=True)
                        live.start()
                    elif event == RUNTIME_CACHE_HIT:
                        live.stop()
                        console.print("[green]Infra is ready \u2713[/green]")
                        console.print("[green]Runtime is ready \u2713[/green]")
                        spinner.text = "Waiting for inference to start..."
                        live = Live(spinner, refresh_per_second=10, transient=True)
                        live.start()
                    elif event == INFERENCE_STARTED:
                        live.stop()
                        spinner.text = "Execution started..."
                        live = Live(spinner, refresh_per_second=10, transient=True)
                        live.start()
                    elif event == INFERENCE_COMPLETED:
                        live.stop()
                        console.print("[green]Execution \u2713[/green]")
                        spinner.text = "Waiting for result..."
                        live = Live(spinner, refresh_per_second=10, transient=True)
                        live.start()
                elif msg_type == "result":
                    live.stop()
                    result = line.decode("utf-8")[7:]
                    return get_rpc_result(result)


def get_rpc_payload(func, config_path, *args, **kwargs):
    rpc_payload = {
        "func": func,
        "args": args,
        "kwargs": kwargs
    }
    print((dill.dumps(rpc_payload)))

    serialized_rpc_payload = base64.b64encode(dill.dumps(rpc_payload)).decode("utf-8")
    configuration_yaml = config_yaml.get_config_yaml(config_path)
    payload = {
        "rpc_payload": serialized_rpc_payload,
        "configuration_yaml": configuration_yaml
    }
    return payload


def get_rpc_headers():
    token_header = auth_header()
    headers = token_header.update(
        {
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
            "Transfer-Encoding": "chunked",
            "Connection": "keep-alive"
        }
    )
    return headers


def get_rpc_result(result):
    data = json.loads(result)
    request_id = data.get("request_id")
    result = data.get("result")
    try:
        output = json.loads(result)
        if output.get("error"):
            rich.print(f"\n[red]{output['error_msg']}[/red]\n")
            rich.print(f"{output['error']}")
            rich.print("\n[white].............................[/white]")
            raise SystemExit
        if output.get("logs"):
            rich.print(f"[blue]Standard Output[/blue]\n")
            rich.print(f"{output['logs']}")
            rich.print("\n[white].............................[/white]")
        if output.get("result"):
            return output.get("result")
        else:
            rich.print(f"[yellow]No result returned[/yellow]")
            return None
    except SystemExit:
        raise SystemExit
    except Exception as e:
        raise Exception(f"Internal error occurred. Request ID for reference: {request_id}, error: {e}")


def get_rpc_url():
    if os.getenv("INFERLESS_ENV") == "DEV":
        return "http://aab1b24401e6d40ee819a4a85da88501-394555867.us-east-1.elb.amazonaws.com/api/v1/rpc/start"

    return "https://serverless-region-v1.inferless.com/api/v1/rpc/start"
