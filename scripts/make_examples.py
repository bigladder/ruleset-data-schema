import os
import csv
import lattice
from uuid import UUID
import datetime
from random import Random
import re
import koozie

SCRIPTS_PATH = os.path.dirname(__file__)
SOURCE_DATA_PATH = os.path.join(SCRIPTS_PATH,"source-data")
EXAMPLE_FILE_DIR_PATH = os.path.join(SCRIPTS_PATH,"..","examples")

for ruleset_source in os.listdir(SOURCE_DATA_PATH):
  path_name = os.path.join(SOURCE_DATA_PATH,ruleset_source)
  if not os.path.isdir(path_name):
    continue
  example_file_name = f"{lattice.file_io.get_file_basename(path_name, depth=0)}.yaml"
  rnd = Random()
  rnd.seed(example_file_name)
  timestamp = datetime.datetime.now().isoformat("T","minutes")

  standard_name = ""
  ruleset_title = ""
  standard_year = ruleset_source[-4:]
  if "ashrae-90_1-ecb" in ruleset_source:
    standard_name = "ASHRAE Standard 90.1"
    ruleset_title = "Energy Cost Budget"
    ruleset_models = ["BUDGET"]
  elif "title-24" in ruleset_source:
    standard_name = "California Title 24 Part 6"
    ruleset_title = "Performance Approach"
    ruleset_models = ["STANDARD"]
  else:
    raise Exception(f"Unknown ruleset source for {example['metadata']['description']}")

  example = {
    "metadata": {
      "data_model": "",
      "schema": "BUILDING_PERFORMANCE_RULESET_DATA",
      "schema_version": "0.1.0",
      "description": f"{standard_year} {standard_name} {ruleset_title}",
      "data_timestamp": f"{timestamp}Z",
      "id": str(UUID(int=rnd.getrandbits(128), version=4)),
      "data_version": 1
    },
    "definitions": {
      "climate_zone_definitions": {}
    },
    "model_rulesets": [
      {
        "ruleset_model_types": ruleset_models,
        "envelope_rules": {
          "opaque_envelope_rules": {
            "exterior_roofs": [],
            "semi_exterior_roofs": [],
            "exterior_walls": [],
            "semi_exterior_walls": [],
            "exterior_floors": [],
            "semi_exterior_floors": [],
            "semi_exterior_roofs": [],
            "exterior_below_grade_walls": [],
            "semi_exterior_below_grade_walls": [],
            "exterior_on_grade_floors": [],
            "semi_exterior_on_grade_floors": [],
          }
        }
      }
    ]
  }

  # Enumerations
  source_file_name = "enumerations.yaml"
  example["definitions"].update(lattice.file_io.load(os.path.join(path_name, source_file_name)))


  # Climate Zones
  source_file_name = "climate-zones.yaml"
  example["definitions"]["climate_zone_definitions"] = lattice.file_io.load(os.path.join(path_name, source_file_name))

  # Opaque Envelope
  source_file_name = "opaque-envelope.csv"

  with open(os.path.join(path_name, source_file_name)) as csv_file:
    csv_reader = csv.reader(csv_file)
    headers = []
    for i, row in enumerate(csv_reader):
      if i == 0:
        headers = row
        # TODO: Confirm header order
      else:
        surface_type = row[0]
        location = row[1]
        climate_zones = row[2].split(',')
        is_ground_adjacent = row[3] == "TRUE"
        construction_types = row[4].split(',')
        occupancy_types = row[5].split(',')
        is_heated = row[6] == "TRUE"
        u_f_c_factor = 0 if row[7] == '' else float(row[7])
        r_cavity = 0 if row[8] == '' else float(row[8])
        r_continuous = 0 if row[9] == '' else float(row[9])
        notes = row[10]

        surface_type_string = f"{surface_type.lower()}s"
        location_string = location.lower().replace('-','_')
        ground = ""
        if is_ground_adjacent:
          if surface_type == "Wall":
            ground = "Below-grade"
          elif surface_type == "Floor":
            ground = "On-grade"
          else:
            raise Exception(f"{row[0]} cannot be ground adjacent.")

        ground_string = f"{ground.lower().replace('-','_')}"

        if len(ground) > 0:
          ground_string = '_' + ground_string

        category = f"{location_string}{ground_string}_{surface_type_string}"

        rule = {
          "climate_zones": climate_zones,
          "occupancy_types": occupancy_types,
          "construction_types": construction_types,
          "has_radiant_heating": is_heated,
          "construction": {
            "id": f"{standard_year} {standard_name} {ruleset_title} {location} {ground} {surface_type}",
            "notes": notes,
            "surface_construction_input_option": "SIMPLIFIED"
          }
        }

        if is_heated:
          rule["construction"]["has_radiant_heating"] = True

        if ground == "Below-grade":
          rule["construction"]["c_factor"] = koozie.fr_u(u_f_c_factor,"Btu/(h*ft^2*°F)")
        elif ground == "On-grade":
          rule["construction"]["f_factor"] = koozie.fr_u(u_f_c_factor,"Btu/(h*ft*°F)")
        else:
          rule["construction"]["u_factor"] = koozie.fr_u(u_f_c_factor,"Btu/(h*ft^2*°F)")

        example["model_rulesets"][0]["envelope_rules"]["opaque_envelope_rules"][category].append(rule)

  lattice.file_io.dump(example, os.path.join(EXAMPLE_FILE_DIR_PATH, example_file_name))
