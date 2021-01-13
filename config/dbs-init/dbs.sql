CREATE DATABASE IF NOT EXISTS sensors DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE sensors;

CREATE TABLE `users` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `username` TEXT NOT NULL,
    `password` TEXT NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `devices` (
  `id` int  NOT NULL AUTO_INCREMENT,
  `identifier`  varchar(32) NOT NULL,
  `secret_key`  varchar(32)  NOT NULL,
  `data_fields` JSON,
  PRIMARY KEY (`id`)
);

CREATE TABLE `api_keys` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `api_key` varchar(32) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE `data` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device` varchar(32) NOT NULL,
  `time` datetime NOT NULL,
  `data` JSON,
  PRIMARY KEY (`id`)
);

CREATE INDEX data_index on data (
    `id`, `device`, `time`
);

CREATE TABLE `data_fields` (
  `id` int NOT NULL AUTO_INCREMENT,
  `device_id` int,
  `field` text NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (device_id) REFERENCES devices(id),
  UNIQUE(device_id, field(32))
);