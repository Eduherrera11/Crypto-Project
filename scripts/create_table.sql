/*   Proyecto Crypto   */
-- Español / English
-- Script para la creación de tablas necesarias en la base de datos MySQL / Script for creating necessary tables in the MySQL database
-- Este script debe ejecutarse en un servidor MySQL para crear las tablas necesarias para el proyecto / This script needs run on a MySQL Server to create the necessary tables for the project

-- Instrucciones / Instructions:
-- 1. Abre tu cliente MySQL (como MySQL Workbench, la línea de comandos de MySQL, o cualquier otro cliente) / 1. Open your MySQL Client (like MySQL Workbench, the command line of MySQL, or whatever other cliente)
-- 2. Conéctate a tu base de datos MySQL / 2. Connect to your onw MySQL database
-- 3. Pega y ejecuta este script para crear las tablas / Paste and run this script to create the tables

-- Nota: Asegúrate de que la base de datos esté seleccionada antes de ejecutar este script / Note: Make sure the database is selected before running this script
-- Puedes seleccionar la base de datos con el comando `USE nombre_de_tu_base_de_datos;` / You can select the database with the command `USE name_of_your_database;`

-- Crear tabla para almacenar las inversiones en criptomonedas / Create tables to save all your invesment on crypto


-- Crear la base de datos y usarla / Create the database and used
create database proyecto_crypto;
use proyecto_crypto;

-- Crear la tabla usuarios / Create the table Users
create table usuarios (
	id int auto_increment primary key,
    correo varchar(255) not null unique,
    contraseña varchar(255) not  null,
    username varchar(255) not null unique,
    token_verificacion varchar(255),
    token_restauracion varchar(255),
    verificado boolean default False
);

-- Crear tabla de inversiones / Create the table invesment
create table inversiones(
	id int auto_increment primary key,
    usuario_id int,
    criptomoneda varchar(50) not null,
    cantidad decimal(18, 8) not null,
    precio_actual decimal(10,2) not null,
    precio_compra decimal(18, 2) not null,
    fecha date not null,
    foreign key (usuario_id) references usuarios(id)
);