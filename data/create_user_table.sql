create table ud
(
	id serial
		constraint ud_pk
			primary key,
	user_name varchar not null,
	first_name varchar,
	last_name varchar,
	user_role varchar not null,
	email varchar not null,
	hash_pass varchar not null,
	reg_date timestamp not null,
	avatar_pic varchar
);

comment on table ud is 'users data table';

create unique index ud_email_uindex
	on ud (email);

create unique index ud_user_name_uindex
	on ud (user_name);

