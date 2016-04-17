/*
Navicat MySQL Data Transfer

Source Server         : ubuntu
Source Server Version : 50628
Source Host           : 115.159.38.166:3306
Source Database       : paper

Target Server Type    : MYSQL
Target Server Version : 50628
File Encoding         : 65001

Date: 2016-04-17 20:47:50
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for paper_authors
-- ----------------------------
DROP TABLE IF EXISTS `paper_authors`;
CREATE TABLE `paper_authors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `systemId` varchar(11) NOT NULL,
  `author` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for paper_basic_info
-- ----------------------------
DROP TABLE IF EXISTS `paper_basic_info`;
CREATE TABLE `paper_basic_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `systemId` varchar(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `publishTime` varchar(100) NOT NULL,
  `publishIn` varchar(255) NOT NULL,
  `publicationType` varchar(255) NOT NULL,
  `abstract` text NOT NULL,
  `searchKeywords` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for paper_indexes
-- ----------------------------
DROP TABLE IF EXISTS `paper_indexes`;
CREATE TABLE `paper_indexes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `systemId` varchar(11) NOT NULL,
  `indexing` varchar(255) NOT NULL,
  `type` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for paper_keywords
-- ----------------------------
DROP TABLE IF EXISTS `paper_keywords`;
CREATE TABLE `paper_keywords` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `systemId` varchar(11) NOT NULL,
  `keyword` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for paper_references
-- ----------------------------
DROP TABLE IF EXISTS `paper_references`;
CREATE TABLE `paper_references` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `systemId` varchar(11) NOT NULL,
  `reference` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
