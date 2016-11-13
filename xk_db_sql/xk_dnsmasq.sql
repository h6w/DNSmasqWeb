-- MySQL dump 10.13  Distrib 5.5.36-34.1, for Linux (x86_64)
--
-- Host: localhost    Database: xk_dnsmasq
-- ------------------------------------------------------
-- Server version	5.5.36-34.1-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `xk_dhcp_host`
--

DROP TABLE IF EXISTS `xk_dhcp_host`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xk_dhcp_host` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(50) DEFAULT NULL,
  `mac` varchar(20) DEFAULT NULL,
  `ip` varchar(15) DEFAULT NULL,
  `comment` varchar(30) DEFAULT NULL,
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` varchar(3) NOT NULL DEFAULT 'yes',
  `action` varchar(10) NOT NULL DEFAULT 'allow',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `xk_domain`
--

DROP TABLE IF EXISTS `xk_domain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xk_domain` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(60) NOT NULL,
  `file` varchar(200) NOT NULL,
  `file_md5` varchar(64) NOT NULL,
  `create_time` datetime NOT NULL,
  `up_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `comment` varchar(200) NOT NULL,
  `status` varchar(3) NOT NULL DEFAULT 'yes',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `xk_login_logs`
--

DROP TABLE IF EXISTS `xk_login_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xk_login_logs` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `uid` int(3) NOT NULL,
  `username` varchar(30) DEFAULT NULL,
  `login_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `login_host` varchar(15) DEFAULT NULL,
  `login_location` varchar(20) DEFAULT NULL,
  `login_status` int(1) NOT NULL DEFAULT '0',
  `user_agent` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `xk_options`
--

DROP TABLE IF EXISTS `xk_options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xk_options` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(20) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `value` varchar(200) DEFAULT NULL,
  `comment` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `xk_record`
--

DROP TABLE IF EXISTS `xk_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xk_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `did` int(11) NOT NULL,
  `record` varchar(50) NOT NULL,
  `type` varchar(10) NOT NULL,
  `value` varchar(50) NOT NULL,
  `priority` int(11) DEFAULT NULL,
  `create_time` datetime NOT NULL,
  `up_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `comment` varchar(100) DEFAULT NULL,
  `status` varchar(3) NOT NULL DEFAULT 'yes',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `xk_users`
--

DROP TABLE IF EXISTS `xk_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `xk_users` (
  `id` int(3) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL,
  `name` varchar(30) NOT NULL,
  `password` varchar(64) NOT NULL,
  `mobile` varchar(15) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `cdate` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `mdate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `mask` varchar(3) NOT NULL DEFAULT '999',
  `is_admin` varchar(3) NOT NULL DEFAULT 'no',
  `status` varchar(3) NOT NULL DEFAULT 'yes',
  `comment` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `xk_users`
--

LOCK TABLES `xk_users` WRITE;
/*!40000 ALTER TABLE `xk_users` DISABLE KEYS */;
INSERT INTO `xk_users` VALUES (1,'admin','Administrator','21232f297a57a5a743894a0e4a801fc3',NULL,NULL,'2014-11-22 16:37:50','2014-11-22 08:37:50','999','yes','yes','Default');
/*!40000 ALTER TABLE `xk_users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-11-26 23:31:55
