#!/usr/bin/env python3

import nbformat
import sys

def remove_skip_execution_tags(notebook_path):
   # Load the Jupyter Notebook
   notebook = nbformat.read(notebook_path, as_version=4)

   # Check and remove "skip execution" tags from each cell
   for cell in notebook.cells:
      if 'metadata' in cell and 'tags' in cell.metadata:
         if 'skip-execution' in cell.metadata.tags:
               if "from friendly.jupyter import *" in cell.source:
                  pass
               else:
                  cell.metadata.tags.remove('skip-execution')

   # Save the modified notebook
   nbformat.write(notebook, notebook_path)
   return notebook_path

if __name__ == "__main__":
   if len(sys.argv) != 2:
      print("Usage: python script_name.py <notebook_path>")
      sys.exit(1)

   input_notebook_path = sys.argv[1]
   output_notebook_path = remove_skip_execution_tags(input_notebook_path)
