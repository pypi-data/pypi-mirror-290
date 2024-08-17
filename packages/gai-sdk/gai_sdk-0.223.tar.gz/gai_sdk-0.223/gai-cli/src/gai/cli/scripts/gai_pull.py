# requires pip install huggingface-hub
import os
from huggingface_hub import snapshot_download

from gai.lib.common.utils import get_app_path
from pathlib import Path

os.environ["HF_HUB_ENABLED_HF_TRANSFER"]="1"
import time

hf_hub = {
    "instructor-sentencepiece":{
        "repo_id":"hkunlp/instructor-large",
        "local_dir":"instructor-large",
        "revision":"54e5ffb8d484de506e59443b07dc819fb15c7233"
    },
    "exllamav2-mistral7b":{
        "repo_id":"bartowski/Mistral-7B-Instruct-v0.3-exl2",
        "local_dir":"exllamav2-mistral7b",
        "revision":"1a09a351a5fb5a356102bfca2d26507cdab11111"
    },
    "sd1.5-automatic1111":{
        "repo_id":"runwayml/stable-diffusion-v1-5",
        "local_dir":"Stable-diffusion",
        "revision":"1d0c4ebf6ff58a5caecab40fa1406526bca4b5b9"
    },
    "xttsv2-coqui":{
        "local_dir":"xttsv2-coqui",
    },
    "whisperv3-huggingface":{
        "repo_id":"openai/whisper-large-v3",
        "local_dir":"whisperv3-huggingface",
        "revision":"06f233fe06e710322aca913c1bc4249a0d71fce1"
    },
    "exllamav2-deepseek":{
        "repo_id":"bartowski/deepseek-coder-6.7b-instruct-exl2",
        "local_dir":"exllamav2-deepseek",
        "revision":"53bfa0459ca092ab4d206111be453eae148ff5a4"
    },
    "clip-openai":{
        "repo_id":"openai/clip-vit-large-patch14",
        "local_dir":"clip-vit-large-patch14",
        "revision":"32bd64288804d66eefd0ccbe215aa642df71cc41"
    },
    "llava1.5-haotian":{
        "repo_id":"liuhaotian/llava-v1.5-7b",
        "local_dir":"llava-v1.5-7b",
        "revision":"4481d270cc22fd5c4d1bb5df129622006ccd9234"
    },
    "llava1.5-hf":{
        "repo_id":"llava-hf/llava-1.5-7b-hf",
        "local_dir":"llava-1.5-7b-hf",
        "revision":"37a8553f98a8b741b2cf90c8d65753ead1d6c74a"
    },
    "llava1.6-mistral":{
        "repo_id":"liuhaotian/llava-v1.6-mistral-7b",
        "local_dir":"llava-v1.6-mistral-7b",
        "revision":"f13b6254afb9d96a82e6f568d7a01101923b3ed9"
    },
    "llava1.6-vicuna":{
        "repo_id":"liuhaotian/llava-v1.6-vicuna-7b",
        "local_dir":"llava-v1.6-vicuna-7b",
        "revision":"deae57a8c0ccb0da4c2661cc1891cc9d06503d11"
    },
    "llava1.6-mistral-hf":{
        "repo_id":"liuhaotian/llava-v1.6-mistral-7b",
        "":"llava-v1.6-mistral-7b",
        "revision":"75e686c43a9492f588490392b20fa7ac84aa57a7"
    }

}

def pull(console, model_name):
    app_dir = get_app_path()
    if not model_name:
        console.print("[red]Model name not provided[/]")
        return
    hf_model=hf_hub.get(model_name,None)

    if model_name != "xttsv2-coqui":
        if not hf_model:
            console.print(f"[red]Model {model_name} not found[/]")
            return

        start=time.time()
        console.print(f"[white]Downloading... {model_name}[/]")
        local_dir=f"{app_dir}/models/"+hf_model["local_dir"]
        snapshot_download(
            repo_id=hf_model["repo_id"],
            local_dir=local_dir,
            revision=hf_model["revision"],
            )
        end=time.time()
        duration=end-start
        download_size=Path(local_dir).stat().st_size
    else:
        start=time.time()
        console.print(f"[white]Downloading... {model_name}[/]")
        local_dir=f"{app_dir}/models/"+hf_model["local_dir"]

        import os
        os.environ["COQUI_TOS_AGREED"]="1"
        from TTS.utils.manage import ModelManager
        mm =  ModelManager(output_prefix=local_dir)
        model_name="tts_models/multilingual/multi-dataset/xtts_v2"
        mm.download_model(model_name)
        
        end=time.time()
        duration=end-start
        download_size=Path(local_dir).stat().st_size

    from rich.table import Table
    table = Table(title="Download Information")
    # Add columns
    table.add_column("Model Name", justify="left", style="bold yellow")
    table.add_column("Time Taken (s)", justify="right", style="bright_green")
    table.add_column("Size (Mb)", justify="right", style="bright_green")
    table.add_column("Location", justify="right", style="bright_green")

    # Add row with data
    table.add_row(model_name, f"{duration:4}", f"{download_size:2}", local_dir)

    # Print the table to the console
    console.print(table)  

