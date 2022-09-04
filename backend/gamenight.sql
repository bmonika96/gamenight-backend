-- MySQL dump 10.13  Distrib 8.0.27, for macos11 (x86_64)
--
-- Host: localhost    Database: baza
-- ------------------------------------------------------
-- Server version	8.0.27

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `dogodek`
--

DROP TABLE IF EXISTS `dogodek`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8 */;
CREATE TABLE `dogodek` (
  `id_dogodka` int NOT NULL AUTO_INCREMENT,
  `ime_skupine` varchar(30) NOT NULL,
  `datum` varchar(50) NOT NULL,
  `odigrana_igra` varchar(20) DEFAULT NULL,
  `zmagovalec` varchar(20) DEFAULT NULL,
  `uporabnisko_ime` varchar(25) NOT NULL,
  PRIMARY KEY (`id_dogodka`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dogodek`
--

LOCK TABLES `dogodek` WRITE;
/*!40000 ALTER TABLE `dogodek` DISABLE KEYS */;
INSERT INTO `dogodek` VALUES (1,'testna','2021-12-24',"Wingspan","Monika",'admin_monika'),(2,'testna2','2020-12-24',"Mysterium","Martin",'admin_monika'),(3,'testna2','2020-12-28',"Catan","Martin",'admin_monika');
/*!40000 ALTER TABLE `dogodek` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `igre`
--

DROP TABLE IF EXISTS `igre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `igre` (
  `ime_igre` varchar(50) NOT NULL,
  `min_stevilo_igralcev` int NOT NULL,
  `max_stevilo_igralcev` int NOT NULL,
  `tezavnost` varchar(50) NOT NULL,
  `dolzina_igre` varchar(50) NOT NULL,
  `ocena` varchar(50) NOT NULL,
  `slika_url` varchar(2048) DEFAULT NULL,
  `ID_igre` int NOT NULL AUTO_INCREMENT,
  `uporabnisko_ime` varchar(50) NOT NULL,
  PRIMARY KEY (`ID_igre`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `igre`
--

LOCK TABLES `igre` WRITE;
/*!40000 ALTER TABLE `igre` DISABLE KEYS */;
INSERT INTO `igre` VALUES ('Wingscape',4,6,7,"120-150",9,"https://cf.geekdo-images.com/yLZJCVLlIx4c7eJEWUNJ7w__imagepage/img/uIjeoKgHMcRtzRSR4MoUYl3nXxs=/fit-in/900x600/filters:no_upscale():strip_icc()/pic4458123.jpg",1,'admin_monika'),('Mysterium',3,6,8,100,7,"https://cf.geekdo-images.com/wfeAiLK5n5hD1omhnlYLLA__imagepage/img/FAbfi09ZD0NHVa9psSeSrBZPgms=/fit-in/900x600/filters:no_upscale():strip_icc()/pic2601683.jpg",4,'admin_martin');
/*!40000 ALTER TABLE `igre` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `odigrana_igra`
--

DROP TABLE IF EXISTS `odigrana_igra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `odigrana_igra` (
  `id_dogodka` int NOT NULL,
  `uporabnisko_ime` varchar(50) NOT NULL,
  `igra` varchar(50) NOT NULL,
  `tocke` varchar(20) NOT NULL,
  `igralec` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `odigrana_igra`
--

LOCK TABLES `odigrana_igra` WRITE;
/*!40000 ALTER TABLE `odigrana_igra` DISABLE KEYS */;
INSERT INTO `odigrana_igra` VALUES (1,'admin_monika','Wingscape',30,'Martin'),(1,'admin_monika','Wingscape',35,'Monika');
/*!40000 ALTER TABLE `odigrana_igra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `skupine`
--

DROP TABLE IF EXISTS `skupine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `skupine` (
  `uporabnisko_ime` varchar(50) NOT NULL,
  `ime_skupine` varchar(50) NOT NULL,
  `id_skupine` int NOT NULL AUTO_INCREMENT,
  `clani` text NOT NULL,
  PRIMARY KEY (`id_skupine`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `skupine`
--

LOCK TABLES `skupine` WRITE;
/*!40000 ALTER TABLE `skupine` DISABLE KEYS */;
INSERT INTO `skupine` VALUES ('admin_monika','testna',2,'martin,aljaz,jakob,marusa'),('admin_monika','testna2',3,'monika, martin');
/*!40000 ALTER TABLE `skupine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `uporabnik`
--

DROP TABLE IF EXISTS `uporabnik`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `uporabnik` (
  `uporabnisko_ime` varchar(50) NOT NULL,
  `geslo` varchar(256) DEFAULT NULL,
  `ime` varchar(25) NOT NULL,
  `priimek` varchar(50) NOT NULL,
  `email` varchar(50) NOT NULL,
  PRIMARY KEY (`uporabnisko_ime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `uporabnik`
--

LOCK TABLES `uporabnik` WRITE;
/*!40000 ALTER TABLE `uporabnik` DISABLE KEYS */;
INSERT INTO `uporabnik` VALUES ('admin_martin','pbkdf2:sha256:260000$cMoYnpl9pS1lO5yj$3cd0d1dab3c495a77009069a4832a68d8acb3ec70efede4949535ce8383c3687','Martin','Pezdir','bla@blabla.si'),('admin_monika','pbkdf2:sha256:260000$QGciVBmfIs3iZNs0$a2003a8020bb1004e9869eae31e9d537b1f510ab33312a2cdf0203790d3e088d','Monika','Bogataj','bla@blabla.si'),('nov_uporabnik','pbkdf2:sha256:260000$tTK7Bom8qCulTIhX$c06e52c4488ded9f83f44b106a110df65d0607c7f1d01157b31277819217b5b9','markod','blabla','bartin@blabla.si');
/*!40000 ALTER TABLE `uporabnik` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-08-25 20:44:07
