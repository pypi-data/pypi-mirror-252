from octoflow.data.loader import dataloader

try:
    from pandas import read_csv
except ImportError:
    read_csv = None

__all__ = [
    "load_csv",
]


@dataloader("csv", extensions=[".csv"], wraps=read_csv, path_arg="filepath_or_buffer")
def load_csv(*args, **kwargs):
    return read_csv(*args, **kwargs)
