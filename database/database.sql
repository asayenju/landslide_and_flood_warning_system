CREATE DATABASE IF NOT EXISTS `landslide_flood_db`;

USE `landslide_flood_db`;

CREATE TABLE `alerts` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `sensor_id` VARCHAR(50) NOT NULL,
  `predicted_landslide_probability` DECIMAL(3,2) NOT NULL,
  `predicted_flood_probability` DECIMAL(3,2) NOT NULL,
  `timestamp` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
);

CREATE TABLE `system_metadata` (
  `key` VARCHAR(50) NOT NULL,
  `value` TEXT NOT NULL,
  PRIMARY KEY (`key`)
);