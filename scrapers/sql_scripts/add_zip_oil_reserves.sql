insert into oil_reserve
(state, year11, year12, year13, year14, year15, year16)
values
( 'Alabama', 8.555, 7.704, 6.795, 7.280, 6.206, 5.722);

insert into oil_reserve
(state, year11, year12, year13, year14, year15, year16)
values
( 'Louisiana', 8.555, 7.704, 6.795, 7.280, 6.206, 5.722);

create table oil_reserve_final as
select b.zip, a.*
from dddm.oil_reserve a
	inner join dddm.zip_lookup b
		on a.state = b.state_name;