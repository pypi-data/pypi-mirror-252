This is the loader module and CLI tool for [DataSesame](https://datasesa.me). DataSesame is the easiest way to find open tabular datasets for all your data science projects.

You can find ready-to-go CSV datasets in the DataSesame database [here](https://airtable.com/appZkpJOcJeDAEreY/shrBAUpOzi3mOBxGg). All datasets can be downloaded in your browser using the download link. 

Alternatively, you can:
1. Download a dataset into your terminal's current working directory 
2. Directly load a dataset into your scripts/notebooks (as a Pandas DataFrame)

Install from PyPi:

```shell
$ pip install datasesame
```

A. Download a dataset by its [ID](https://airtable.com/appZkpJOcJeDAEreY/shrBAUpOzi3mOBxGg) into your CWD using the CLI interface, e.g.:

```shell
$ datasesame 42
```

B. Load a dataset as a Pandas DataFrames in Python, e.g.:

```python
import datasesame as ds
df = ds.load(42)
# returns a Pandas DataFrame
print(df.head(5))
```

Sadly this dataset does not reveal the meaning of life, but it might make for interesting data science / ML...