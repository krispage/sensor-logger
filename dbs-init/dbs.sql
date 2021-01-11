CREATE DATABASE IF NOT EXISTS sensors DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE sensors;

CREATE TABLE `users` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `username` TEXT NOT NULL,
    `password` TEXT NOT NULL,
    PRIMARY KEY (`id`)
);

CREATE TABLE `devices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `identifier` text NOT NULL,
  `secret_key` text NOT NULL,
  PRIMARY KEY (`id`)
);

CREATE TABLE `data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `device` text DEFAULT NULL,
  `time` datetime NOT NULL,
  `data` JSON,
  PRIMARY KEY (`id`)
);
