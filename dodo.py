"""
doit task/build automation
"""

import os

from lattice import Lattice

ruleset_schema_data_model = Lattice()

def task_validate_example_files():
  '''Validates the example files against the JSON schema (and other validation steps)'''
  return {
    'file_dep': ruleset_schema_data_model.examples + [schema.path for schema in ruleset_schema_data_model.schemas],
    'actions': [(ruleset_schema_data_model.validate_example_files,[])]
  }

def task_generate_web_docs():
  '''Generates Markdown Documentation'''
  return {
    'file_dep': [schema.path for schema in ruleset_schema_data_model.schemas] + [template.path for template in ruleset_schema_data_model.doc_templates],
    'targets': [os.path.join(ruleset_schema_data_model.web_docs_directory_path,"public")],
    'actions': [(ruleset_schema_data_model.generate_web_documentation,[])]
  }
