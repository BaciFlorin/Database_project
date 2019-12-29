--inserare user;
insert into accounts values(2, 'test', 'test');
insert into accounts values(1, 'admin', 'admin');


--inserare regizori;
insert into directors values(1, 'Frank Darabont');
insert into directors values(2, 'Cristopher Nolan');
insert into directors values(3, 'Quentin Tarantino');
insert into directors values(4, 'Todd Phillips');
insert into directors values(5, 'Ridley Scott');
insert into directors values(6, 'Damien Chazelle');


--inserare film;
insert into movies values(1,'The Shawshank Redemption', '14-OCT-1994', 
					'Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.',
					'Drama', 1, 1, 8);
insert into movies values(2,'Inception', '16-JUL-2010', 
					'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.',
					'Action, Adventure', 2, 1, 7);
insert into movies values(3,'Once Upon a Time... in Hollywood', '26-JUL-2019', 
					'A faded television actor and his stunt double strive to achieve fame and success in the film industry during the final years of Hollywood s Golden Age in 1969 Los Angeles.',
					'Comedy, Drama', 3, 1, 8);
insert into movies values(4,'Inglourious Basterds', '21-AUG-2009', 
					'In Nazi-occupied France during World War II, a plan to assassinate Nazi leaders by a group of Jewish U.S. soldiers coincides with a theatre owner s vengeful plans for the same.',
					'Adventure, Drama', 3, 1, 7);
insert into movies values(5,'Joker', '4-OCT-2019', 
					'In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society. He then embarks on a downward spiral of revolution and bloody crime. This path brings him face-to-face with his alter-ego: the Joker.',
					'Thriller, Drama', 4, 1, 6);
insert into movies values(6,'Gladiator', '5-MAY-2000', 
					'A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.',
					'Action, Drama', 5, 1, 7);
insert into movies values(7,'La La Land', '25-DEC-2016', 
					'While navigating their careers in Los Angeles, a pianist and an actress fall in love while attempting to reconcile their aspirations for the future.',
					'Comedy, Drama', 6, 1, 9);


--inserare actori;
insert into actors values(1, 'Tim Robbins');
insert into actors values(2, 'Morgan Freeman');
insert into actors values(3, 'Leonardo DiCaprio');
insert into actors values(4, 'Joseph Gordon-Levitt');
insert into actors values(5, 'Brad Pitt');
insert into actors values(6, 'Margot Robbie');
insert into actors values(7, 'Melanie Laurent');
insert into actors values(8, 'Christoph Waltz');
insert into actors values(9, 'Joaquin Phoenix');
insert into actors values(10, 'Robert De Niro');
insert into actors values(11, 'Russell Crowe');
insert into actors values(12, 'Ryan Gosling');
insert into actors values(13, 'Emma Stone');


--inserare cast;
insert into stars values(1, 1);
insert into stars values(1, 2);
insert into stars values(2, 3);
insert into stars values(2, 4);
insert into stars values(3, 3);
insert into stars values(3, 5);
insert into stars values(3, 6);
insert into stars values(4, 5);
insert into stars values(4, 7);
insert into stars values(4, 8);
insert into stars values(5, 9);
insert into stars values(5, 10);
insert into stars values(6, 11);
insert into stars values(6, 9);
insert into stars values(7, 12);
insert into stars values(7, 13);

--inserare indici;
insert into indices values(1,8);
insert into indices values(2,3);
insert into indices values(3,7);
insert into indices values(4,14);