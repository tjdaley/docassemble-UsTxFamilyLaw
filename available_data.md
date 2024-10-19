# Available Objects and Variables

## Include Files

| Abbreviation | Filename |
|---|---|
| AL | docassemble.AssemblyLine:assembly_line.yml |
| BQ | basic-questions.yml |
| PBQ | docassemble.UsTxFamilyLaw:prose-basic-questions.yml |
| PFBQ | docassemble.UsTxFamilyLaw:prose-basic-family-questions.yml |

# Objects and Variables

| Name | Description | AL | BQ | PBQ | PFBQ |
|---|---|---|---|---|---|
| case* | Information Pertaining to a case | X | X | X | |
| .client (Individual) | Our client | X | X | X | |
| .client_alignment | Petitioner/Respondent/Intervenor/Third Party | X | X | X | |
| .court_number | District court number as integer (obsolete) | X | X | X | |
| .county | County within case.us_state where action is pending | X | X | X | |
| .id | Cause number | X | X | X | |
| .is_dissolution | T/F Whether this case involves a marriage dissolution action. | X | X | X | |
| .is_dissolution | T/F Whether this case involves a marriage dissolution action. | X | X | X | X |
| .op (Individual) | Opposing party | X | X | X | |
| .alignment | Petitioner/Respondent/Intervenor/Third | X | X | X | X |
| .oc (Individual) | Opposing counsel, if any, otherwise opposing party | X | X | X | |
| .child (ChildList) | List of children in this case | X | X | X | |
| .petitioner (Individual) | Petitioner (points to client or op) | X | X | X | |
| .respondent (Individual) | Respondent (points to client or op) | X | X | X | |
| .us_state | U.S. State where case is or will be filed | X | X | X | |
| district_court_name | Name of district court, if case filed in distict court | X | X | X | |
| county_court_at_law_name | Name of CCL, if case is filed in CCL | X | X | X | |
| justice_court_precinct | Name of precinct for JP court, if case is filed in JP court | X | X | X | |
| service_efile | T/F whether document will be served via E-File | X | X | X | |
| service_email | T/F whether document will be served via Email | X | X | X | |
| service_first_class | T/F whether document will be served via USPS First Class Mail | X | X | X | |
| service_certified | T/F whether document will be service by USPS Certified Mail | X | X | X | |
| op_represented | T/F whether OP is represented by an attorney | X | X | X | |
| clerk_info | Information about the district clerk in case.county | X | X | X | X |
| .Court | "District clerk" | X | X | X | X |
| .Court_Type | "District Clerk" | X | X | X | X |
| .Address | Street address | X | X | X | X |
| .City | City | X | X | X | X |
| .Zip_Code | ZIP Code | X | X | X | X |
| .Phone | Telephone number | X | X | X | X |
| .Email | Email address | X | X | X | X |
| .Website | District clerk's web site | X | X | X | X |
| court_info | Information about the court | X | X | X | X |
| .Court | Name of the court, suitable for case style | X | X | X | X |
| .Court_Type | District Court/Justice of the Peace/County Court at Law | X | X | X | X |
| .Address | Street address | X | X | X | X |
| .City | City | X | X | X | X |
| .Zip_Code | ZIP Code | X | X | X | X |
| .Phone | Telephone number | X | X | X | X |
| .Email | Email address | X | X | X | X |
| .Website | Court's web site | X | X | X | X |
| court_type | District Court | Justice of the Peace Court | County Court at Law

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
