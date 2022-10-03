CREATE DATABASE MoniToll;
USE MoniToll;

CREATE TABLE Perfil(
idPerfil INT PRIMARY KEY,
Cargo VARCHAR(20)
);

CREATE TABLE Pedagio(
idPedagio INT PRIMARY KEY,
nomePedagio VARCHAR(40),
Localizacao VARCHAR(50)
);


CREATE TABLE Usuario(
idUsuario INT PRIMARY KEY AUTO_INCREMENT,
Nome VARCHAR(45),
CNPJ CHAR(15),
Email VARCHAR(40),
Senha VARCHAR(30),
fkPerfil INT,
fkPedagio INT,
FOREIGN KEY (fkPerfil) REFERENCES Perfil(idPerfil),
FOREIGN KEY (fkPedagio) REFERENCES Pedagio(idPedagio)
);


CREATE TABLE Maquina(
idMaquina INT PRIMARY KEY AUTO_INCREMENT,
sistemaOperacional VARCHAR(30),
fkPedagio INT,
FOREIGN KEY (fkPedagio) REFERENCES Pedagio(idPedagio)
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
foreign key (fkMaquina) references Maquina (idMaquina)
);

insert into Perfil values (1, "Usuario"),
						  (2, "Administrador"),
                          (3, "Desenvolvedor");

SELECT * FROM Perfil;
SELECT * FROM Usuario;
SELECT * FROM Pedagio;

INSERT INTO Usuario values (null, 'Mateus do Carmo', null, 'mateusMonitoll@gmail.com', '123', 3, null);