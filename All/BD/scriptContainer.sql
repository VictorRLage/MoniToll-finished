create database MoniToll;
use MoniToll;
create table Leitura (
idLeitura int primary key auto_increment, 
dataHora datetime,
cpuPercent varchar(45),
ramTotal varchar(45), 
ramUso varchar(45), 
ramUsoPercent varchar(45), 
discoTotal varchar(45), 
discoUso varchar(45), 
discoLivre varchar(45),
discoPercent varchar(45), 
pacoEnv varchar(45), 
pacoRec varchar(45),
pacoPerd varchar(45)
);

select * from leitura;