import lattice
import os
import koozie

SCRIPTS_PATH = os.path.dirname(__file__)
EXAMPLE_FILE_DIR_PATH = os.path.join(SCRIPTS_PATH,"..","examples")

ashrae_90_1_file = os.path.join(EXAMPLE_FILE_DIR_PATH,"ashrae-90_1-ecb-2019.yaml")
title_24_file = os.path.join(EXAMPLE_FILE_DIR_PATH,"title-24-2019.yaml")

ashrae_90_1_ruleset = lattice.file_io.load(ashrae_90_1_file)
title_24_ruleset = lattice.file_io.load(title_24_file)

budget_opaque_envelope_ruleset = ashrae_90_1_ruleset["model_rulesets"][0]["envelope_rules"]["opaque_envelope_rules"]
standard_opaque_envelope_ruleset = title_24_ruleset["model_rulesets"][0]["envelope_rules"]["opaque_envelope_rules"]


# Get exterior wall U-factor for an exterior wood framed residential wall in San Francisco
occupancy_type = "RESIDENTIAL"
construction_type = "WOOD_FRAMED"
has_radiant_heating = False

climate_zone = "3C"
for rule in budget_opaque_envelope_ruleset["exterior_walls"]:
  if climate_zone in rule["climate_zones"] and occupancy_type in rule["occupancy_types"] and construction_type in rule["construction_types"] and rule["has_radiant_heating"] == has_radiant_heating:
    construction_name = rule["construction"]["id"]
    u_factor = koozie.to_u(rule["construction"]["u_factor"],"Btu/(h*ft^2*°F)")
    print(f"Found ASHRAE 90.1 match, \"{construction_name}\", with U-{u_factor:.3f}")

climate_zone = "3"
for rule in standard_opaque_envelope_ruleset["exterior_walls"]:
  if climate_zone in rule["climate_zones"] and occupancy_type in rule["occupancy_types"] and construction_type in rule["construction_types"] and rule["has_radiant_heating"] == has_radiant_heating:
    construction_name = rule["construction"]["id"]
    u_factor = koozie.to_u(rule["construction"]["u_factor"],"Btu/(h*ft^2*°F)")
    print(f"Found Title 24 match, \"{construction_name}\", with U-{u_factor:.3f}")

