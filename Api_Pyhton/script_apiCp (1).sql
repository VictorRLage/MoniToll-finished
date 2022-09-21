create database apiCp;
use apiCp;

create table maquina (
id int primary key,
sistemaOperacional varchar(40)
localizacao varchar (40)
);

create table dadosMedidas (
idMedidas int primary key auto_increment,
freqCpu decimal (7,2),
cpuPercent decimal(5,2),
ramPercent decimal(5,2),
ramEmusoGB decimal (5,2),
diskPercent decimal(5,2),
diskEmUsoGB decimal (5,2),
dataHora datetime, 
fkMaquina int,
foreign key (fkMaquina) references maquina (id)
) auto_increment = 1;

insert into maquina values 
(100, 'Windows','Campinas'),
(101, 'Windows', 'Jundiaí'),
(102, 'Linux', 'Santos');


select dadosMedidas.ramPercent, dadosMedidas.diskPercent, dadosMedidas.dataHora, dadosMedidas.fkMaquina, 
 maquina.NumeroSerie, maquina.Localizacao, dadosMedidas.cpuPercent 
 from maquina, dadosMedidas where fkMaquina = idMedidas; 

truncate dadosMedidas;
select * from dadosMedidas;