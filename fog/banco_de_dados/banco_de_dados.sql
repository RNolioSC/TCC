create user '123' identified by '1234';
grant all on *.* to '123';

create database 'lrg';

create table residencia(codigo serial, descricao varchar(45)); 

create table tag(codigo varchar(8), descricao varchar(45), cod_residencia bigint unsigned, primary key (codigo), foreign key (cod_residencia) references residencia(`codigo`));

create table acesso(codigo serial, data datetime, cod_tag varchar(8) unique not null, foreign key (cod_tag) references tag(codigo));
