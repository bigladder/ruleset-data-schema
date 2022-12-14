Ruleset Data Schema Specification
=================================

A schema to provide data related to building performance rulesets such as ASHRAE Standard 90.1 Appendix G, California Title 24 Part 6, and RESNET Standard 301.

Motivation:
-----------


1. Every software attempting to apply rulesets has to manually create their own translation from English PDF into source code. This is repetitive, and potentially error prone.
1. OpenStudio Standards ruleset data is painfully verbose, lacks a structured schema, was designed by a single organization for a single software tool.
1. ASHRAE Standard 229P provides a standardized terminology for describing ruleset models and the schema describing ruleset data should be consistent where possible.
1. ASHRAE Standard 232P provides a standard methodology for defining data schemas. ASHRAE Standard 229P uses this methodology and the ruleset data schema should also adhere to the same approach.
