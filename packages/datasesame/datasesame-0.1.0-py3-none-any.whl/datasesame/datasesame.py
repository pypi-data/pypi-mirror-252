import typer
from typing_extensions import Annotated
import subprocess
import requests

app = typer.Typer()

@app.command()
def download(id: Annotated[str, typer.Argument()]):
    try:
        response = requests.get(f'https://idfilename.donkeys.workers.dev/?key={id}')
        subprocess.run(['curl', '-o', response.text, f'https://files.datasesa.me/{response.text}'], check=True)
        print(f"File downloaded successfully: {response.text}")
        requests.get(f'https://airtableupdate.donkeys.workers.dev/?key={id}')
    except:
        print("Unable to download dataset")
        return


def load(id):
    try:
        import pandas as pd
        response = requests.get(f'https://idfilename.donkeys.workers.dev/?key={id}')
        storage_options = {'User-Agent': 'Mozilla/5.0'}
        df = pd.read_csv(f'https://files.datasesa.me/{response.text}', storage_options=storage_options)
        requests.get(f'https://airtableupdate.donkeys.workers.dev/?key={id}')
        return df
    except:
        print("Unable to load dataset")    
        df = pd.DataFrame()
        return df 
