
--creare tabela accounts;
create table accounts (
	id_user number(4),
	username varchar2(30) not null,
	password varchar2(30) not null,
	constraint id_user_pk primary key (id_user),
	constraint username_uk unique (username)
);
--creare tabela pentru regizori;
create table directors(
	id_director number(4),
	name varchar2(40) not null,
	constraint id_director_pk primary key (id_director)
);
--creare tabela pentru actori;
create table actors(
	id_actor number(4),
	name varchar2(40) not null,
	constraint id_actor_pk primary key (id_actor)
);


--creare tabela movies;
create table movies(
	id_film number(4),
	name varchar2(100) not null,
	debut date,
	description varchar2(250),
	gender varchar2(50),
	id_director number(4) not null,
	user_rating number(2),
	critics_rating number(2),
	constraint id_film_pk primary key (id_film),
	constraint user_rating_ck check (user_rating<=10 and user_rating>0),
	constraint critics_rating_ck check (critics_rating<=10 and critics_rating>0),
	constraint id_director_fk foreign key (id_director) references directors(id_director),
	constraint name_uk unique (name)
);

--creare tabela cast;
create table stars(
	id_film number(4),
	id_actor number(4),
	constraint cast_pk primary key (id_film, id_actor),
	constraint id_filmcast_fk foreign key (id_film) references movies(id_film),
	constraint id_actor_fk foreign key (id_actor) references actors(id_actor)
);


--creare tabela user_reviews;
create table user_reviews(
	id_user number(4),
	id_film number(4),
	note number(2),
	review varchar2(250),
	constraint review_pk primary key (id_user, id_film),
	constraint id_user_fk foreign key (id_user) references accounts(id_user),
	constraint id_film_fk foreign key (id_film) references movies(id_film)
);

create table indices(
	id number(4),
	valoare number(4)
);

