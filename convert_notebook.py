"""
convert_notebook.py  –  Convert notebooks/eda_analysis.py → eda_analysis.ipynb

Uses nbformat to build a proper Jupyter notebook from the
# %% cell markers in the .py file.

Usage:
    python convert_notebook.py
"""

import os
import re
import sys
import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell


def py_to_notebook(py_path: str, ipynb_path: str):
    with open(py_path) as f:
        source = f.read()

    # Split on # %% markers
    cell_pattern = re.compile(r"^# %%(.*)$", re.MULTILINE)
    splits       = cell_pattern.split(source)

    # splits[0] = text before first marker (discard if empty)
    # splits[1::2] = cell headers (" [markdown]" or "")
    # splits[2::2] = cell bodies

    cells = []
    parts = list(zip(splits[1::2], splits[2::2]))

    for header, body in parts:
        body = body.strip()
        if not body:
            continue
        if "[markdown]" in header:
            # Strip leading # from docstring lines
            md_lines = []
            for line in body.splitlines():
                if line.startswith("# "):
                    md_lines.append(line[2:])
                elif line == "#":
                    md_lines.append("")
                else:
                    md_lines.append(line)
            cells.append(new_markdown_cell("\n".join(md_lines)))
        else:
            cells.append(new_code_cell(body))

    nb = new_notebook(cells=cells)
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language":     "python",
        "name":         "python3",
    }
    nb.metadata["language_info"] = {
        "name":    "python",
        "version": "3.11.0",
    }

    with open(ipynb_path, "w") as f:
        nbformat.write(nb, f)

    print(f"Notebook written: {ipynb_path}")
    print(f"  {len(cells)} cells ({sum(1 for c in cells if c['cell_type']=='code')} code, "
          f"{sum(1 for c in cells if c['cell_type']=='markdown')} markdown)")


if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    src  = os.path.join(root, "notebooks", "eda_analysis.py")
    dst  = os.path.join(root, "notebooks", "eda_analysis.ipynb")

    if not os.path.exists(src):
        print(f"Source not found: {src}")
        sys.exit(1)

    py_to_notebook(src, dst)
    print("\nTo open in Jupyter:")
    print("  jupyter notebook notebooks/eda_analysis.ipynb")
