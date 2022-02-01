import importlib.util
import os
import sys

import fire

import streamlit as st


def format_func(option: str):
    return option.split("/")[-1][:-3].replace("_", " ").title()


def main(folder=os.path.abspath(os.getcwd())):

    # Get filenames for all files in this path, excluding this script.
    this_file = os.path.abspath(__file__)
    fnames = []

    for basename in os.listdir(folder):
        fname = os.path.join(folder, basename)

        if fname.endswith(".py") and fname.split("/")[-1] != this_file.split("/")[-1]:
            fnames.append(fname)

    # Make a UI to run different files.
    fname_to_run = st.sidebar.selectbox(
        "Select an app", fnames, format_func=format_func
    )

    # Create module from filepath and put in sys.modules, so Streamlit knows
    # to watch it for changes.
    global fake_module_count
    fake_module_count = 0

    def load_module(filepath):
        global fake_module_count
        modulename = "_dont_care_%s" % fake_module_count
        spec = importlib.util.spec_from_file_location(modulename, filepath)
        module = importlib.util.module_from_spec(spec)
        sys.modules[modulename] = module

        fake_module_count += 1

    # Run the selected file.
    with open(fname_to_run) as f:
        load_module(fname_to_run)
        filebody = f.read()

    exec(filebody, {})


if __name__ == "__main__":
    fire.Fire(main)
