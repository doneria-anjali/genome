create table rules(
	id int(8) not null,
    description varchar(500),
    rrange int(8),
    unit varchar(20),
    type varchar(20),
    separation_entity varchar(50)
);

insert into rules values(1, 'limitation rule for unconventional wells', 1000, 'ft','primary','existing wells');
insert into rules values(2, 'limitation rule for unconventional wells', 300, 'ft','primary','wetlands');
