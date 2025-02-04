import argparse
import os


def dir_type(path):
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(f"{path} is not a valid path")

    return path
