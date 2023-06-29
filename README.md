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

Must be imported twice: For planning phase and integration test phase !

## OWASP MASVS (Mobile)

https://github.com/OWASP/owasp-masvs

Import from Yaml

Must be imported twice: For planning phase and integration test phase !

## OWASP ISVS (IoT)

https://github.com/OWASP/IoT-Security-Verification-Standard-ISVS/releases/tag/1.0RC

Import from Json

Must be imported twice: For planning phase and integration test phase !

## OWASP WSTG (Web)

https://github.com/OWASP/wstg

# Data layer:

Data in the DB file is layer in a complex way. This results in:

Empire -> Section (a single DB file) -> Group (Topics) -> item (control-container) -> control (this one is a checkbox)
