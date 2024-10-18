# Available Objects and Variables

## Include Files

| Abbreviation | Filename |
|---|---|
| AL | docassemble.AssemblyLine:assembly_line.yml |
| BQ | basic-questions.yml |
| PBQ | docassemble.UsTxFamilyLaw:prose-basic-questions.yml |
| PFBQ | docassemble.UsTxFamilyLaw:prose-basic-family-questions.yml |
|---|---|

# Objects and Variables

| Name | Description | AL | BQ | PBQ | PFBQ |
|---|---|---|---|---|---|
| case* | Information Pertaining to a case X | X | | |
| .client (Individual) | Our client | X | X | | |
| .client.client_alignment | Petitioner/Respondent/Intervenor/Third Party | X | X | | |
| .court_number | District court number as integer (obsolete) | X | X | | |
| .county | County within case.us_state where action is pending | X | X | | |
| .id | Cause number | X | X | | |
| .is_dissolution | T/F Whether this case involves a marriage dissolution action. | X | X | | |
| .op (Individual) | Opposing party | X | X | | |
| .oc (Individual) | Opposing counsel, if any, otherwise opposing party | X | X | | |
| .child (ChildList) | List of children in this case | X | X | | |
| .petitioner (Individual) | Petitioner (points to client or op) | X | X | | |
| .respondent (Individual) | Respondent (points to client or op) | X | X | | |
| .us_state | U.S. State where case is or will be filed | X | X | | |
| district_court_name | Name of district court, if case filed in distict court | X | X | | |
| county_court_at_law_name | Name of CCL, if case is filed in CCL | X | X | | |
| justice_court_precinct | Name of precinct for JP court, if case is filed in JP court | X | X | | |
| service_efile | T/F whether document will be served via E-File | X | X | | |
| service_email | T/F whether document will be served via Email | X | X | | |
| service_first_class | T/F whether document will be served via USPS First Class Mail | X | X | | |
| service_certified | T/F whether document will be service by USPS Certified Mail | X | X | | |
| op_represented | T/F whether OP is represented by an attorney | X | X | | |
|---|---|---|---|---|---|


## Individual Properties

| Property Name | Description |
|---|---|
| name | The name object |
| .first | First name |
| .middle | Middle name |
| .last | Last name |
| .suffix | Suffix |
| .bar_no | State Bar number (if Individual is an attorney) |
| .firm_name | Attorney's firm's name |
| .phone_number | Phone number |
| .fax_number | Fax Number |
| .email | Email address |
| .address.address | Street address |
| .address.city | City |
| .address.state | U.S. State |
| .address.zip | ZIP/Postal Code 
| .address.county | County wherein address is located |
|---|---|
