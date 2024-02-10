{% if pleading.contains_sensitive_data %}THIS DOCUMENT CONTAINS

SENSITIVE DATA{% endif %}

**CAUSE NO: <u>{{db.case.case_id}}</u>**

<table>
<colgroup>
<col style="width: 50%" />
<col style="width: 49%" />
</colgroup>
<thead>
<tr class="header">
<th><p><strong>{% if pleading.used_in_divorce %}IN THE MATTER
OF</strong></p>
<p><strong>THE MARRIAGE OF</strong></p>
<p><strong>{{ db.case.petitioner.comma_and_list() }}</strong></p>
<p><strong>AND</strong></p>
<p><strong>{{ db.case.respondent.comma_and_list() }}</strong></p>
<p><strong>{% if db.case.child.number() %}</strong></p>
<p><strong>AND{% endif %}{% endif %}</strong></p>
<p><strong>{% if db.case.child.number() %}</strong></p>
<p><strong>IN THE INTEREST OF</strong></p>
<p><strong>{{ db.case.child.comma_and_list() }},</strong></p>
<p><strong>{{ db.case.child.as_noun() }}</strong></p>
<p><strong>{% endif %}</strong></p></th>
<th><p><strong>IN THE {{ db.case.court.jurisdiction }}</strong></p>
<p><strong>{{ db.case.court.title }}</strong></p>
<p><strong>{{ db.case.court.county }} COUNTY, TEXAS</strong></p></th>
</tr>
</thead>
<tbody>
</tbody>
</table>

**CLIENT**

{{db.case.client.name}}

**PLAYERS**

**{{ db.case.petitioner.as_noun() }}**

{% for party in db.case.petitioner %}

1.  {{party.name}} {{ party.\_\_dir\_\_() }}

{% endfor %}

**{{ db.case.respondent.as_noun() }}**

{% for party in db.case.respondent %}

1.  {{party.name}} {{party.attorney.name}}

{% endfor %}

{% if db.case.intervenor %}**{{ db.case.intervenor.as_noun() }}**

{% for party in case.intervenor %}

1.  {{party.name}} {{party.\_\_dir\_\_() }}

{% endfor %}

{%p else %}

**INTERVENTORS: None**

{%p endif %}

**{% if db.case.child.number %}{{db.case.child.as_noun()}}**

{%p for child in db.case.child %}

1.  {{child.name}} {{child.birthdate}} {{child.gender}}

{%p endfor %}

{%p else %}

**CHILDREN: None**

{%p endif %}

**TEST**

DIVORCE? {{db.pleading.used_in_divorce }}

SENSITIVE? {{ db.pleading.contains_sensitive_data }}

COUNTY: {{ db.case.court.county }}

COURT NAME: {{ db.case.court.title }}

JURISDICTION: {{ db.case.court.jurisdiction }}

CAUSE NO: {{ db.case.case_id }}
