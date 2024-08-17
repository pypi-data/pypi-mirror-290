from gai.cli._gai_cli.Tools import Tools
import os
from openai import OpenAI
from rich.console import Console

os.environ["OPENAI_API_KEY"]=""
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"]=""
client=OpenAI(api_key=os.environ["OPENAI_API_KEY"])
from gai.ttt.client.completions import Completions
client=Completions.PatchOpenAI(client)

def chat(content):
    console=Console()
    with console.status("Working...",spinner="monkey") as status:
        inner_messages=[]
        inner_messages.append({"role":"user","content":content})
        inner_messages.append({"role":"assistant","content":""})
        #
        response=client.chat.completions.create(
            model="exllamav2-mistral7b",
            messages=inner_messages,
            stream=True,
            max_new_tokens=1000,
            stopping_conditions=[""]
            )
        for chunk in response:
            # Stop the spinner on the first iteration
            if 'status' in locals():
                status.stop()
                del status                
            chunk = chunk.extract()
            if chunk and isinstance(chunk, str):
                
                # Skip empty chunks
                if content is None and chunk==" ":
                    continue

                content += chunk
                console.print(f"[italic bright_white]{chunk}[/]",end="")
        print()
        inner_messages.append({"role": "assistant", "content": content})
        return inner_messages
    
