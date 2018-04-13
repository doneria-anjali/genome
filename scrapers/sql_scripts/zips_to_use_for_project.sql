create table zips_for_project as
select a.city, a.state_id, a.zip
from zip_lookup a 
where city in ('NEWORLEANS', 'ALBANY', 'JUNEAU', 'PASADENA', 'CARY', 'COLUMBUS', 'BOSTON', 'SACRAMENTO', 'SALTLAKECITY', 'PIERRE') and
state_id in ('LA', 'NY', 'AK', 'TX', 'NC', 'OH', 'MA', 'CA', 'UT', 'SD')
order by city;

delete from zips_for_project
where city = 'ALBANY' and state_id != 'NY';

delete from zips_for_project
where city = 'BOSTON' and state_id != 'MA';

delete from zips_for_project
where city = 'COLUMBUS' and state_id != 'OH';

delete from zips_for_project
where city = 'PASADENA' and state_id != 'TX';