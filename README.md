# checkbox_empire

For compliance reasons we will have to X checkboxes in documents.
Like everyone else. But we are smart and lazy.

Those documents will be generated automatically and the automatic test tools will report the checkboxes to be filled.

# Tasks it will do

## Create the TODO checkbox table

Read different sources and combine them to a internal checkbox landscape

## Export CSV files

From this landscape it will export CSV files that will have to be filled out and returned.
Those CSV files can be managed in Git

## Read CSV files

Integrate the checkboxes for the different tasks from the CSV files into the data landscape

## Export as human readable

Use templates to export the data as a human readable format. Include percent achieved by section

## Bonus: integrate tools

Add the ability for build-tools to directly and automatically report their success/fails

## Bonus: Export for machines

# Sources for Checkboxes

## Microsoft SDL

Manual, is not that much

## OWASP ASVS (Generic)

https://github.com/OWASP/ASVS/releases/tag/v4.0.3_release

import from json

MD5SUM: 3780058aabbb2c855b0e159032125b36

## OWASP MASVS (Mobile)

https://github.com/OWASP/owasp-masvs
https://github.com/OWASP/owasp-masvs/releases  Version 2.0.0

Import from Yaml

MD5SUM: d7d8bafa734d51738c7bed41b7d48aab

## OWASP ISVS (IoT)

https://github.com/OWASP/IoT-Security-Verification-Standard-ISVS/releases/tag/1.0RC

Import from Json

MD5SUM: 3730500305762843f71dda011c3c5604

## OWASP WSTG (Web)

https://github.com/OWASP/wstg

https://github.com/OWASP/wstg/blob/master/checklists/checklist.json

(curl the raw version, comment on the checklist used "wstgbot Publish Latest checklists 2023-06-16 (#1068)")

MD5SUM: 98eeb5ad65c0cc5c63ba326973c93ebe

# Data layer:

Data in the DB file is layer in a complex way. This results in:

Empire -> Section (a single DB file) -> Group (Topics) -> item (control-container) -> control (this one is a checkbox)
