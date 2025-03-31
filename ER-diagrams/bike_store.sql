-- MySQL Script generated by MySQL Workbench
-- Mon Mar 31 14:02:14 2025
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema bike_store
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `bike_store` ;

-- -----------------------------------------------------
-- Schema bike_store
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `bike_store` DEFAULT CHARACTER SET utf8 ;
USE `bike_store` ;

-- -----------------------------------------------------
-- Table `bike_store`.`customers`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bike_store`.`customers` ;

CREATE TABLE IF NOT EXISTS `bike_store`.`customers` (
  `customer_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `phone` VARCHAR(45) NULL,
  `email` VARCHAR(45) NOT NULL,
  `street` VARCHAR(45) NULL,
  `city` VARCHAR(45) NULL,
  `state` VARCHAR(2) NULL,
  `zip_code` VARCHAR(45) NULL,
  PRIMARY KEY (`customer_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bike_store`.`stores`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bike_store`.`stores` ;

CREATE TABLE IF NOT EXISTS `bike_store`.`stores` (
  `name` VARCHAR(45) NOT NULL,
  `phone` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `street` VARCHAR(45) NULL,
  `city` VARCHAR(45) NULL,
  `state` VARCHAR(3) NULL,
  `zip_code` INT NULL,
  PRIMARY KEY (`name`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bike_store`.`staffs`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bike_store`.`staffs` ;

CREATE TABLE IF NOT EXISTS `bike_store`.`staffs` (
  `staff_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NOT NULL,
  `last_name` VARCHAR(45) NOT NULL,
  `phone` VARCHAR(45) NULL,
  `active` INT NULL,
  `store_name` VARCHAR(45) NOT NULL,
  `manager_id` INT NULL,
  PRIMARY KEY (`staff_id`),
  INDEX `fk_staffs_stores1_idx` (`store_name` ASC) VISIBLE,
  INDEX `fk_staffs_staffs1_idx` (`manager_id` ASC) VISIBLE,
  CONSTRAINT `fk_staffs_stores1`
    FOREIGN KEY (`store_name`)
    REFERENCES `bike_store`.`stores` (`name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_staffs_staffs1`
    FOREIGN KEY (`manager_id`)
    REFERENCES `bike_store`.`staffs` (`staff_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bike_store`.`orders`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bike_store`.`orders` ;

CREATE TABLE IF NOT EXISTS `bike_store`.`orders` (
  `order_id` INT NOT NULL AUTO_INCREMENT,
  `customer_id` INT NOT NULL,
  `order_status` INT NULL,
  `order_date` DATE NULL,
  `required_date` DATE NULL,
  `shipped_date` DATE NULL,
  `staff_id` INT NOT NULL,
  PRIMARY KEY (`order_id`),
  INDEX `fk_orders_customers1_idx` (`customer_id` ASC) VISIBLE,
  INDEX `fk_orders_staffs1_idx` (`staff_id` ASC) VISIBLE,
  CONSTRAINT `fk_orders_customers1`
    FOREIGN KEY (`customer_id`)
    REFERENCES `bike_store`.`customers` (`customer_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_orders_staffs1`
    FOREIGN KEY (`staff_id`)
    REFERENCES `bike_store`.`staffs` (`staff_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bike_store`.`brands`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bike_store`.`brands` ;

CREATE TABLE IF NOT EXISTS `bike_store`.`brands` (
  `brand_id` INT NOT NULL AUTO_INCREMENT,
  `brand_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`brand_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bike_store`.`categories`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bike_store`.`categories` ;

CREATE TABLE IF NOT EXISTS `bike_store`.`categories` (
  `category_id` INT NOT NULL AUTO_INCREMENT,
  `category_name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`category_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bike_store`.`products`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bike_store`.`products` ;

CREATE TABLE IF NOT EXISTS `bike_store`.`products` (
  `product_id` INT NOT NULL AUTO_INCREMENT,
  `product_name` VARCHAR(45) NOT NULL,
  `brand_id` INT NOT NULL,
  `category_id` INT NOT NULL,
  `model_year` VARCHAR(45) NULL,
  `list_price` DECIMAL(2) NOT NULL,
  PRIMARY KEY (`product_id`),
  INDEX `fk_products_brands1_idx` (`brand_id` ASC) VISIBLE,
  INDEX `fk_products_categories1_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `fk_products_brands1`
    FOREIGN KEY (`brand_id`)
    REFERENCES `bike_store`.`brands` (`brand_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_products_categories1`
    FOREIGN KEY (`category_id`)
    REFERENCES `bike_store`.`categories` (`category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bike_store`.`order_items`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bike_store`.`order_items` ;

CREATE TABLE IF NOT EXISTS `bike_store`.`order_items` (
  `order_id` INT NOT NULL,
  `item_id` INT NOT NULL,
  `product_id` INT NOT NULL,
  `quantity` INT NOT NULL,
  `discount` DECIMAL(2) NULL,
  PRIMARY KEY (`order_id`, `item_id`),
  INDEX `fk_order_items_orders_idx` (`order_id` ASC) VISIBLE,
  INDEX `fk_order_items_products1_idx` (`product_id` ASC) VISIBLE,
  CONSTRAINT `fk_order_items_orders`
    FOREIGN KEY (`order_id`)
    REFERENCES `bike_store`.`orders` (`order_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_order_items_products1`
    FOREIGN KEY (`product_id`)
    REFERENCES `bike_store`.`products` (`product_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `bike_store`.`stocks`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `bike_store`.`stocks` ;

CREATE TABLE IF NOT EXISTS `bike_store`.`stocks` (
  `product_id` INT NOT NULL,
  `store_name` VARCHAR(45) NOT NULL,
  `quantity` INT NULL,
  PRIMARY KEY (`product_id`, `store_name`),
  INDEX `fk_stocks_stores1_idx` (`store_name` ASC) VISIBLE,
  CONSTRAINT `fk_stocks_products1`
    FOREIGN KEY (`product_id`)
    REFERENCES `bike_store`.`products` (`product_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_stocks_stores1`
    FOREIGN KEY (`store_name`)
    REFERENCES `bike_store`.`stores` (`name`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
