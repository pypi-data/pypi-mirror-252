"""Main module."""

from llm.mkt import bq
from importlib.resources import files
import fire
from llm import prompt_chains

def prompt_chains(filename: str,
    dataset: str = 'ds_mkt_ds-prompt-chains',
    project: str = 'ds-mkt'):
    """prompt chains."""
    print('prompt_chains')
    print(vars())
    params = {}
    package_path = files(prompt_chains)
    filename = package_path.joinpath('queries','data.sql')
    with open(filename) as f:
        sql = f.read()
    sql = sql.format(**params)
    data = bq.get_query(sql)


def main():
    """Execute main program."""
    fire.Fire(prompt_chains)
    print('\x1b[6;30;42m', 'Success!', '\x1b[0m')


if __name__ == "__main__":
    main()
