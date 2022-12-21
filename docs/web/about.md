{{% blocks/cover title="About the Building Performance Ruleset Data Schema Specification" height="auto" %}}

Building performance simulation (BPS) is increasingly needed to demonstrate building designs meet criteria for energy efficiency and decarbonization. These criteria are often laid out in industry codes and standards (such as ASHRAE 90.1, and California Title 24), and require a collection of rules (i.e., a ruleset) be applied to simulation models so buildings are all compared in a consistent fashion. Generally, these rules and their associated data are described in prose and human-readable tables that must subsequently be translated into software to actually enforce the rules. This creates several potential issues:

1. Often this process involves manual, and error-prone copying of data into independent software tools.
2. There is a general lag between the publication of the human-readable ruleset description and its implementation in software, where the logic of the rules needs to be complete in its coverage of the range of building designs encountered in practice. All too often, holes in the logic are discovered during software implementation when the ruleset has already been published.

Providing ruleset data in a machine-readable format, before the ruleset is published will expedite the software implementation process, minimize translation error, and ensure greater coverage of real situations encountered in building designs across a wider range of simulation software tools.


{{% /blocks/cover %}}


{{% blocks/section  %}}
## Acknowledgements

This data model specification was developed with support from Southern California Edison.

{{% /blocks/section %}}
