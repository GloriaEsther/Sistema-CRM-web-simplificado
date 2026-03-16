-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: crm_proempleo
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add cliente',7,'add_cliente'),(26,'Can change cliente',7,'change_cliente'),(27,'Can delete cliente',7,'delete_cliente'),(28,'Can view cliente',7,'view_cliente'),(29,'Can add estado cliente cat',8,'add_estadoclientecat'),(30,'Can change estado cliente cat',8,'change_estadoclientecat'),(31,'Can delete estado cliente cat',8,'delete_estadoclientecat'),(32,'Can view estado cliente cat',8,'view_estadoclientecat'),(33,'Can add frecuencia cliente cat',9,'add_frecuenciaclientecat'),(34,'Can change frecuencia cliente cat',9,'change_frecuenciaclientecat'),(35,'Can delete frecuencia cliente cat',9,'delete_frecuenciaclientecat'),(36,'Can view frecuencia cliente cat',9,'view_frecuenciaclientecat'),(37,'Can add rol usuario',10,'add_rolusuario'),(38,'Can change rol usuario',10,'change_rolusuario'),(39,'Can delete rol usuario',10,'delete_rolusuario'),(40,'Can view rol usuario',10,'view_rolusuario'),(41,'Can add usuario',11,'add_usuario'),(42,'Can change usuario',11,'change_usuario'),(43,'Can delete usuario',11,'delete_usuario'),(44,'Can view usuario',11,'view_usuario'),(45,'Can add preferencia usuario',12,'add_preferenciausuario'),(46,'Can change preferencia usuario',12,'change_preferenciausuario'),(47,'Can delete preferencia usuario',12,'delete_preferenciausuario'),(48,'Can view preferencia usuario',12,'view_preferenciausuario'),(49,'Can add estatus cobros',13,'add_estatuscobros'),(50,'Can change estatus cobros',13,'change_estatuscobros'),(51,'Can delete estatus cobros',13,'delete_estatuscobros'),(52,'Can view estatus cobros',13,'view_estatuscobros'),(53,'Can add etapa ventas',14,'add_etapaventas'),(54,'Can change etapa ventas',14,'change_etapaventas'),(55,'Can delete etapa ventas',14,'delete_etapaventas'),(56,'Can view etapa ventas',14,'view_etapaventas'),(57,'Can add venta',15,'add_venta'),(58,'Can change venta',15,'change_venta'),(59,'Can delete venta',15,'delete_venta'),(60,'Can view venta',15,'view_venta'),(61,'Can add oportunidad',16,'add_oportunidad'),(62,'Can change oportunidad',16,'change_oportunidad'),(63,'Can delete oportunidad',16,'delete_oportunidad'),(64,'Can view oportunidad',16,'view_oportunidad');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `idcliente` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `apellidopaterno` varchar(45) DEFAULT NULL,
  `apellidomaterno` varchar(45) DEFAULT NULL,
  `numerotelcli` varchar(10) NOT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `rfc` varchar(13) DEFAULT NULL,
  `fecha_nacimiento` datetime DEFAULT NULL,
  `fecha_ultimocontacto` timestamp NULL DEFAULT NULL,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_modificacion` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `activo` tinyint(1) DEFAULT '1',
  `fecha_eliminacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `comentarios` text,
  `usuario_registro` int NOT NULL,
  `frecuencia_compra` int DEFAULT NULL,
  `estado_cliente` int DEFAULT NULL,
  `owner_id` int DEFAULT NULL,
  PRIMARY KEY (`idcliente`),
  KEY `fk_usuario_registro_idx` (`usuario_registro`),
  KEY `fk_frecuencia_compra_cliente_idx` (`frecuencia_compra`),
  KEY `fk_estado_cliente_idx` (`estado_cliente`),
  KEY `fk_cliente_del_negocio_idx` (`owner_id`),
  CONSTRAINT `fk_cliente_registrado_por` FOREIGN KEY (`owner_id`) REFERENCES `usuario` (`idusuario`),
  CONSTRAINT `fk_estado_cliente` FOREIGN KEY (`estado_cliente`) REFERENCES `estado_cliente_cat` (`idestado_cliente`),
  CONSTRAINT `fk_frecuencia_compra_cliente` FOREIGN KEY (`frecuencia_compra`) REFERENCES `frecuencia_cliente_cat` (`idfrecuencia_cliente`),
  CONSTRAINT `fk_usuario_registro` FOREIGN KEY (`usuario_registro`) REFERENCES `usuario` (`idusuario`)
) ENGINE=InnoDB AUTO_INCREMENT=181 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES (1,'Valeria','Molina','Castillo','2213455678','esteeselcorreodevale@gmail.com','Arco Sur, Calle Calzada del tecnologico,Col.Santa barbara no.12',NULL,NULL,NULL,'2025-12-18 06:12:48','2025-12-18 06:12:48',0,'2025-12-18 06:12:48','Le gustan las semillas de girasol, siempre compra los lunes',2,1,3,37),(2,'Maria','Lopez','Castillo','2278455678','este@gmail.com','Calle Villahermosa no.21',NULL,NULL,NULL,'2025-12-18 06:12:48','2025-12-18 06:12:48',0,'2025-12-18 06:12:48','Le gustan las semillas de girasol con chile',2,1,3,37),(3,'Miriam','Sanchez','Castillo','2278455690','miri@gmail.com','Calle Circuito uno no.14',NULL,NULL,NULL,'2025-12-18 06:12:48','2025-12-18 06:12:48',0,'2025-12-18 06:12:48','Suele comprar costales de chile guajillo',2,1,2,37),(4,'Vanessa','Lopez','Sanchez','2279555678','vane@gmail.com','Av. Xalapa',NULL,NULL,NULL,'2025-12-18 06:12:48','2025-12-18 06:12:48',0,'2025-12-18 06:12:48','Le gustan los muebles que se hacen aca',2,4,3,37),(5,'Gabriel','Martinez','Gonzales','1461588797','Gaby@gmail.com',NULL,NULL,NULL,NULL,'2025-12-11 09:10:22','2025-12-11 09:19:13',0,'2025-12-11 09:19:13','',23,1,3,23),(6,'Felipe','Carranza','Vazquez','8894864513','felipe@gmail.com',NULL,NULL,NULL,NULL,'2025-12-11 09:53:33','2025-12-15 20:48:16',1,NULL,'prueba edicion',23,NULL,4,23),(7,'Patricia','Perez','Gonzalez','1321561454',NULL,NULL,NULL,NULL,NULL,'2025-12-12 04:02:26','2025-12-15 20:44:31',0,'2025-12-15 20:44:31','',23,NULL,NULL,23),(8,'Manuel','Sanchez','Moreno','321315156',NULL,NULL,NULL,NULL,NULL,'2025-12-12 04:22:26','2025-12-16 20:47:19',0,'2025-12-16 20:47:19','',23,NULL,3,23),(9,'Perla','Martinez','Geron','3256165446',NULL,NULL,NULL,NULL,NULL,'2025-12-12 06:22:27','2025-12-12 06:22:27',1,NULL,'Esto es una prueba',23,2,3,23),(10,'Mariana','Castro','Castro','4454548781',NULL,NULL,NULL,NULL,'2025-12-01 06:00:00','2025-12-13 17:45:08','2025-12-13 17:45:08',1,NULL,'Esto es prueba',23,NULL,2,23),(11,'Pancha','Perez','Gomez','5568217189',NULL,NULL,NULL,NULL,NULL,'2025-12-13 18:12:26','2025-12-13 18:12:26',1,NULL,'',23,NULL,NULL,23),(12,'Javier','Geron','Geron','5975564566',NULL,NULL,NULL,NULL,NULL,'2025-12-13 18:24:49','2025-12-13 18:24:49',1,NULL,'',24,NULL,2,23),(13,'Gabriel','Gomez','Martinez','3545648651',NULL,NULL,NULL,NULL,NULL,'2025-12-13 19:02:10','2025-12-13 19:02:10',1,NULL,'',23,4,3,23),(14,'Gloria',NULL,NULL,'2615615959','gloriaesthermartinezmartinez@gmail.com',NULL,NULL,NULL,NULL,'2025-12-14 06:34:41','2025-12-14 06:37:32',1,NULL,'',36,NULL,NULL,36),(15,'Gloria',NULL,NULL,'2285454616',NULL,NULL,NULL,'2003-01-10 00:00:00',NULL,'2025-12-15 06:50:48','2025-12-15 06:50:48',1,NULL,'y ya :b',23,NULL,2,23),(19,'Juan','Garcia','Martinez','5512345678','juan.garcia@example.com','nan','GAMA850101H12',NULL,NULL,'2025-12-19 07:13:57','2025-12-19 07:13:57',1,NULL,'nan',23,NULL,NULL,23),(20,'Maria','Rodriguez','Lopez','5598765432','maria.rod@example.com','nan','ROLM920515J34',NULL,NULL,'2025-12-19 07:13:57','2025-12-19 07:13:57',1,NULL,'nan',23,NULL,NULL,23),(21,'Carlos','Hernandez','Perez','5544332211','c.hernandez@example.com','nan','HEPC781130K56',NULL,NULL,'2025-12-19 07:13:57','2025-12-19 07:13:57',1,NULL,'nan',23,NULL,NULL,23),(22,'Alejandro','Mendoza','Ruiz','5510293847','a.mendoza@email.com','nan','MERU850312H89','1985-03-12 00:00:00',NULL,'2025-12-19 07:13:57','2025-12-19 08:35:04',0,'2025-12-19 08:35:04','nan',23,NULL,NULL,23),(23,'Beatriz','Salinas','Vega','5599887766','beatriz.sv@servidor.mx','nan','SAVB921105J44','1992-11-05 00:00:00',NULL,'2025-12-19 07:13:57','2025-12-19 08:35:13',0,'2025-12-19 08:35:13','nan',23,NULL,NULL,23),(24,'Gerardo','Ortiz','Luna','3344556677','g.ortiz.l@webmail.com','nan','OILG780620K12','1978-06-20 00:00:00',NULL,'2025-12-19 07:13:57','2025-12-19 08:35:21',0,'2025-12-19 08:35:21','nan',23,NULL,NULL,23),(25,'Lucía','Fernández','Gómez','8112233445','lucia.fg@correo.com','nan','FEGL890115L56','1989-01-15 00:00:00',NULL,'2025-12-19 07:13:57','2025-12-19 08:35:47',0,'2025-12-19 08:35:47','nan',23,NULL,NULL,23),(26,'Alejandro','Mendoza','Ruiz','5510293847','a.mendoza@email.com',NULL,'nan','1985-03-12 00:00:00',NULL,'2025-12-19 08:36:10','2025-12-19 08:36:10',1,NULL,NULL,23,NULL,NULL,23),(27,'Marco','Garcia','Martinez','5512345678','marco@example.com',NULL,NULL,NULL,NULL,'2025-12-19 08:58:13','2025-12-19 08:58:13',1,NULL,NULL,23,NULL,NULL,23),(28,'Martha','Rodriguez','Lopez','5598765432','mar@example.com',NULL,NULL,NULL,NULL,'2025-12-19 08:58:13','2025-12-19 08:58:13',1,NULL,NULL,23,NULL,NULL,23),(29,'Carlos','Perez','Perez','5544332211','c.perez@example.com',NULL,NULL,NULL,NULL,'2025-12-19 08:58:13','2025-12-19 08:58:13',1,NULL,NULL,23,NULL,NULL,23),(30,'Alejandro','Barradas','Ruiz','5510293847','a.mendoza@email.com',NULL,NULL,'1985-03-12 00:00:00',NULL,'2025-12-19 08:58:13','2025-12-19 08:58:13',1,NULL,NULL,23,NULL,NULL,23),(31,'Beatriz','Puentes','Vega','5599887766','beatriz@servidor.mx',NULL,NULL,'1992-11-05 00:00:00',NULL,'2025-12-19 08:58:13','2025-12-19 08:58:13',1,NULL,NULL,23,NULL,NULL,23),(32,'Gabriel','Ortiz','Luna','3344556677','g.ortiz.l@webmail.com',NULL,NULL,NULL,NULL,'2025-12-19 08:58:13','2025-12-19 08:58:13',1,NULL,NULL,23,NULL,NULL,23),(33,'Marimar','Fernández','Gómez','8112233445','mari@correo.com',NULL,NULL,NULL,NULL,'2025-12-19 08:58:13','2025-12-19 08:58:13',1,NULL,NULL,23,NULL,NULL,23),(34,'Juana','Ramírez','Torres','5512345678',NULL,NULL,NULL,NULL,NULL,'2025-12-19 08:58:13','2025-12-19 08:58:13',1,NULL,NULL,23,NULL,NULL,23),(35,'Marco','Garcia','Martinez','5512345678','marco@example.com',NULL,NULL,NULL,NULL,'2025-12-19 19:09:39','2025-12-19 19:09:39',1,NULL,NULL,23,NULL,NULL,23),(36,'Martha','Rodriguez','Lopez','5598765432','mar@example.com',NULL,NULL,NULL,NULL,'2025-12-19 19:09:39','2025-12-19 19:09:39',1,NULL,NULL,23,NULL,NULL,23),(37,'Carlos','Perez','Perez','5544332211','c.perez@example.com',NULL,NULL,NULL,NULL,'2025-12-19 19:09:39','2025-12-19 19:09:39',1,NULL,NULL,23,NULL,NULL,23),(38,'Alejandro','Barradas','Ruiz','5510293847','a.mendoza@email.com',NULL,NULL,'1985-03-12 00:00:00',NULL,'2025-12-19 19:09:39','2025-12-19 19:09:39',1,NULL,NULL,23,NULL,NULL,23),(39,'Beatriz','Puentes','Vega','5599887766','beatriz@servidor.mx',NULL,NULL,'1992-11-05 00:00:00',NULL,'2025-12-19 19:09:39','2025-12-19 19:09:39',1,NULL,NULL,23,NULL,NULL,23),(40,'Gabriel','Ortiz','Luna','3344556677','g.ortiz.l@webmail.com',NULL,NULL,NULL,NULL,'2025-12-19 19:09:39','2025-12-19 19:09:39',1,NULL,NULL,23,NULL,NULL,23),(41,'Marimar','Fernández','Gómez','8112233445','mari@correo.com',NULL,NULL,NULL,NULL,'2025-12-19 19:09:39','2025-12-19 19:09:39',1,NULL,NULL,23,NULL,NULL,23),(42,'Juana','Ramírez','Torres','5512345678',NULL,NULL,NULL,NULL,NULL,'2025-12-19 19:09:39','2025-12-19 19:09:39',1,NULL,NULL,23,NULL,NULL,23),(43,'Sofia','Martinez','Sanchez','6545464848',NULL,NULL,NULL,NULL,NULL,'2025-12-21 02:35:38','2025-12-21 02:35:38',1,NULL,'',3,NULL,2,3),(44,'Maria',NULL,NULL,'2251561619',NULL,NULL,NULL,NULL,NULL,'2026-01-06 03:54:52','2026-01-06 03:54:52',1,NULL,'',3,NULL,2,3),(45,'Cecilia','Martinez',NULL,'2214165145',NULL,NULL,NULL,NULL,NULL,'2026-01-08 02:29:12','2026-01-08 02:29:29',1,NULL,'',3,NULL,NULL,3),(46,'Gloria',NULL,NULL,'2154684878',NULL,NULL,NULL,NULL,NULL,'2026-01-08 17:53:15','2026-01-16 06:27:39',1,NULL,'',38,1,3,38),(47,'Rafael','Cordoba','Alfonso','6194864126','rafa@gmail.com',NULL,NULL,NULL,NULL,'2026-01-08 18:00:25','2026-01-19 08:31:22',1,NULL,'',38,1,3,38),(48,'Adriana','Ramos','Nava','8161561789',NULL,NULL,NULL,NULL,NULL,'2026-01-08 18:00:25','2026-01-08 18:00:25',1,NULL,NULL,38,NULL,NULL,38),(49,'Carlos','Ortiz','Navarro','3344556677',NULL,NULL,NULL,NULL,NULL,'2026-01-08 18:00:25','2026-01-08 18:00:25',1,NULL,NULL,38,NULL,NULL,38),(50,'Maria Luisa','Fernández','Gómez','8112233412','marilu@correo.com',NULL,'MARKSA114R',NULL,NULL,'2026-01-08 18:00:25','2026-01-08 18:00:25',1,NULL,NULL,38,NULL,NULL,38),(51,'Chana','Ramírez','Torres','2212345678',NULL,NULL,NULL,NULL,NULL,'2026-01-08 18:00:25','2026-01-08 18:00:25',1,NULL,NULL,38,NULL,NULL,38),(52,'Abraham','Sanchez','Perez','8489562147','abraham@gmail.com',NULL,NULL,NULL,NULL,'2026-01-08 18:00:25','2026-01-15 07:05:03',0,'2026-01-15 07:05:03',NULL,38,NULL,NULL,38),(53,'Ricardo Alfredo','Galicia','Arcos','2281614866',NULL,NULL,NULL,NULL,NULL,'2026-01-08 18:23:34','2026-01-08 18:23:34',1,NULL,'',39,NULL,NULL,39),(54,'Cristina',NULL,NULL,'8719987919',NULL,NULL,NULL,NULL,NULL,'2026-01-18 20:55:05','2026-01-18 20:55:05',1,NULL,'',38,NULL,NULL,38),(55,'Marta',NULL,NULL,'6464864893',NULL,NULL,NULL,NULL,NULL,'2026-01-19 13:06:11','2026-01-19 13:26:11',0,'2026-01-19 13:26:11','',52,NULL,NULL,52),(56,'Rafael','Cordoba','Alfonso','6194864126',NULL,NULL,NULL,NULL,NULL,'2026-01-19 14:33:44','2026-01-24 06:48:30',0,'2026-01-24 06:48:30',NULL,52,NULL,NULL,52),(57,'Adriana','Ramos','Nava','8161561789',NULL,NULL,NULL,NULL,NULL,'2026-01-19 14:33:44','2026-01-28 06:26:44',0,'2026-01-28 06:26:44',NULL,52,NULL,NULL,52),(58,'Carlos','Ortiz','Navarro','3344556677',NULL,NULL,NULL,NULL,NULL,'2026-01-19 14:33:44','2026-01-30 06:09:44',1,NULL,'',52,NULL,2,52),(59,'Chana','Ramírez','Torres','2212345678',NULL,NULL,NULL,NULL,NULL,'2026-01-19 14:33:44','2026-01-24 06:52:57',0,'2026-01-24 06:52:57',NULL,52,NULL,NULL,52),(60,'Abraham','Sanchez','Perez','8489562147','abraham@gmail.com',NULL,NULL,NULL,NULL,'2026-01-19 14:33:44','2026-01-19 14:33:44',1,NULL,NULL,52,NULL,NULL,52),(85,'Marco','Garcia','Martinez','5512345678','marco@example.com',NULL,NULL,NULL,NULL,'2026-01-21 03:54:23','2026-01-21 03:54:23',1,NULL,NULL,53,NULL,NULL,53),(86,'Martha','Rodriguez','Lopez','5598765432','mar@example.com',NULL,NULL,NULL,NULL,'2026-01-21 03:54:23','2026-01-21 03:54:23',1,NULL,NULL,53,NULL,NULL,53),(87,'Carlos','Perez','Perez','5544332211','c.perez@example.com',NULL,NULL,NULL,NULL,'2026-01-21 03:54:23','2026-01-21 03:54:23',1,NULL,NULL,53,NULL,NULL,53),(88,'Alejandro','Barradas','Ruiz','5510293847','a.mendoza@email.com',NULL,NULL,'1985-03-12 00:00:00',NULL,'2026-01-21 03:54:23','2026-01-21 03:54:23',1,NULL,NULL,53,NULL,NULL,53),(89,'Beatriz','Puentes','Vega','5599887766','beatriz@servidor.mx',NULL,NULL,'1992-11-05 00:00:00',NULL,'2026-01-21 03:54:23','2026-01-21 03:54:23',1,NULL,NULL,53,NULL,NULL,53),(90,'Gabriel','Ortiz','Luna','3344556677','g.ortiz.l@webmail.com',NULL,NULL,NULL,NULL,'2026-01-21 03:54:23','2026-01-21 03:54:23',1,NULL,NULL,53,NULL,NULL,53),(91,'Marimar','Fernández','Gómez','8112233445','mari@correo.com',NULL,NULL,NULL,NULL,'2026-01-21 03:54:24','2026-01-21 03:54:24',1,NULL,NULL,53,NULL,NULL,53),(92,'Juana','Ramírez','Torres','5512345678',NULL,NULL,NULL,NULL,NULL,'2026-01-21 03:54:24','2026-01-21 03:54:24',1,NULL,NULL,53,NULL,NULL,53),(121,'Rafael','Cordoba','Alfonso','6194864126',NULL,NULL,NULL,NULL,NULL,'2026-01-21 05:43:51','2026-01-21 05:43:51',1,NULL,NULL,53,NULL,NULL,53),(122,'Adriana','Ramos','Nava','8161561789',NULL,NULL,NULL,NULL,NULL,'2026-01-21 05:43:51','2026-01-21 05:43:51',1,NULL,NULL,53,NULL,NULL,53),(123,'Carlos','Ortiz','Navarro','3344556677',NULL,NULL,NULL,NULL,NULL,'2026-01-21 05:43:51','2026-01-21 05:43:51',1,NULL,NULL,53,NULL,NULL,53),(124,'Maria Luisa','Fernández','Gómez','8112233412','marilu@correo.com',NULL,'MARKSA114R',NULL,NULL,'2026-01-21 05:43:51','2026-01-21 05:43:51',1,NULL,NULL,53,NULL,NULL,53),(125,'Chana','Ramírez','Torres','2212345678',NULL,NULL,NULL,NULL,NULL,'2026-01-21 05:43:51','2026-01-21 05:43:51',1,NULL,NULL,53,NULL,NULL,53),(126,'Abraham','Sanchez','Perez','8489562147','abraham@gmail.com',NULL,NULL,NULL,NULL,'2026-01-21 05:43:51','2026-01-21 05:43:51',1,NULL,NULL,53,NULL,NULL,53),(127,'Rafael','Cordoba','Alfonso','6194864126',NULL,NULL,NULL,NULL,NULL,'2026-01-21 05:45:37','2026-01-21 05:49:23',0,'2026-01-21 05:49:23',NULL,53,NULL,NULL,53),(128,'Adriana','Ramos','Nava','8161561789',NULL,NULL,NULL,NULL,NULL,'2026-01-21 05:45:37','2026-01-21 05:49:23',0,'2026-01-21 05:49:23',NULL,53,NULL,NULL,53),(129,'Carlos','Ortiz','Navarro','3344556677',NULL,NULL,NULL,NULL,NULL,'2026-01-21 05:45:37','2026-01-21 05:49:23',0,'2026-01-21 05:49:23',NULL,53,NULL,NULL,53),(130,'Chana','Ramírez','Torres','2212345678',NULL,NULL,NULL,NULL,NULL,'2026-01-21 05:45:37','2026-01-21 05:49:23',0,'2026-01-21 05:49:23',NULL,53,NULL,NULL,53),(131,'Abraham','Sanchez','Perez','8489562147','abraham@gmail.com',NULL,NULL,NULL,NULL,'2026-01-21 05:45:37','2026-01-21 05:49:23',0,'2026-01-21 05:49:23',NULL,53,NULL,NULL,53),(132,'Rafael','Cordoba','Alfonso','6194864126',NULL,NULL,NULL,NULL,NULL,'2026-01-21 06:15:41','2026-01-21 06:15:41',1,NULL,NULL,53,NULL,NULL,53),(133,'Adriana','Ramos','Nava','8161561789',NULL,NULL,NULL,NULL,NULL,'2026-01-21 06:15:41','2026-01-21 06:15:41',1,NULL,NULL,53,NULL,NULL,53),(134,'Carlos','Ortiz','Navarro','3344556677',NULL,NULL,NULL,NULL,NULL,'2026-01-21 06:15:41','2026-01-21 06:15:41',1,NULL,NULL,53,NULL,NULL,53),(135,'Chana','Ramírez','Torres','2212345678',NULL,NULL,NULL,NULL,NULL,'2026-01-21 06:15:41','2026-01-21 06:15:41',1,NULL,NULL,53,NULL,NULL,53),(136,'Abraham','Sanchez','Perez','8489562147','abraham@gmail.com',NULL,NULL,NULL,NULL,'2026-01-21 06:15:41','2026-01-21 06:15:41',1,NULL,NULL,53,NULL,NULL,53),(137,'Rafael','Cordoba','Alfonso','6194864126',NULL,NULL,NULL,NULL,NULL,'2026-01-24 04:44:16','2026-01-24 04:44:16',1,NULL,NULL,52,NULL,NULL,52),(138,'Mariana','Godinez',NULL,'2256487889',NULL,NULL,NULL,NULL,NULL,'2026-01-24 04:44:16','2026-01-24 04:44:16',1,NULL,NULL,52,NULL,NULL,52),(139,'Javier','Ortiz','Martinez','2245788956',NULL,NULL,NULL,NULL,NULL,'2026-01-24 04:44:16','2026-01-24 04:44:16',1,NULL,NULL,52,NULL,NULL,52),(140,'Maria Luisa','Fernández','Gómez','8112233412','marilu@correo.com',NULL,NULL,NULL,NULL,'2026-01-24 04:44:16','2026-01-24 04:44:16',1,NULL,NULL,52,NULL,NULL,52),(141,'Chana','Ramírez','Torres','2212345678',NULL,NULL,NULL,NULL,NULL,'2026-01-24 04:44:16','2026-01-24 04:44:16',1,NULL,NULL,52,NULL,NULL,52),(142,'Juana','Martinez','Torres','2245568748',NULL,NULL,NULL,NULL,NULL,'2026-01-24 06:48:06','2026-01-24 06:48:06',1,NULL,NULL,52,NULL,NULL,52),(143,'Ivan Moises','Vazquez','Morales','2245368980',NULL,NULL,NULL,NULL,NULL,'2026-01-24 07:04:04','2026-01-24 07:04:04',1,NULL,NULL,52,NULL,NULL,52),(144,'Cecilia',NULL,NULL,'2213465678',NULL,NULL,NULL,NULL,NULL,'2026-01-24 07:04:04','2026-01-24 07:04:04',1,NULL,NULL,52,NULL,NULL,52),(145,'Jorge',NULL,NULL,'2245789678',NULL,NULL,NULL,NULL,NULL,'2026-01-24 07:04:04','2026-01-24 07:04:04',1,NULL,NULL,52,NULL,NULL,52),(146,'Marco','Garcia','Martinez','5512345678','marco@example.com',NULL,NULL,NULL,NULL,'2026-01-25 00:29:11','2026-01-25 00:29:11',1,NULL,NULL,52,NULL,NULL,52),(147,'Martha','Rodriguez','Lopez','5598765432','mar@example.com',NULL,NULL,NULL,NULL,'2026-01-25 00:29:11','2026-01-25 00:29:11',1,NULL,NULL,52,NULL,NULL,52),(148,'Carlos','Perez','Perez','5544332211','c.perez@example.com',NULL,NULL,NULL,NULL,'2026-01-25 00:29:11','2026-01-25 00:29:11',1,NULL,NULL,52,NULL,NULL,52),(149,'Alejandro','Barradas','Ruiz','5510293847','a.mendoza@email.com',NULL,NULL,'1985-03-12 00:00:00',NULL,'2026-01-25 00:29:12','2026-01-25 00:29:12',1,NULL,NULL,52,NULL,NULL,52),(150,'Beatriz','Puentes','Vega','5599887766','beatriz@servidor.mx',NULL,NULL,'1992-11-05 00:00:00',NULL,'2026-01-25 00:29:12','2026-01-25 00:29:12',1,NULL,NULL,52,NULL,NULL,52),(151,'Marimar','Fernández','Gómez','8112233445','mari@correo.com',NULL,NULL,NULL,NULL,'2026-01-25 00:29:12','2026-01-25 00:29:12',1,NULL,NULL,52,NULL,NULL,52),(152,'Marco','Garcia','Martinez','5512345678','marco@example.com','nan',NULL,NULL,NULL,'2026-01-25 03:03:47','2026-01-25 03:03:47',1,NULL,'nan',51,NULL,NULL,51),(153,'Martha','Rodriguez','Lopez','5598765432','mar@example.com','nan',NULL,NULL,NULL,'2026-01-25 03:03:47','2026-01-25 03:03:47',1,NULL,'nan',51,NULL,NULL,51),(154,'Carlos','Perez','Perez','5544332211','c.perez@example.com','nan',NULL,NULL,NULL,'2026-01-25 03:03:47','2026-01-25 03:03:47',1,NULL,'nan',51,NULL,NULL,51),(155,'Alejandro','Barradas','Ruiz','5510293847','a.mendoza@email.com','nan',NULL,'1985-03-12 00:00:00',NULL,'2026-01-25 03:03:47','2026-01-25 03:03:47',1,NULL,'nan',51,NULL,NULL,51),(156,'Beatriz','Puentes','Vega','5599887766','beatriz@servidor.mx','nan',NULL,'1992-11-05 00:00:00',NULL,'2026-01-25 03:03:47','2026-01-25 03:03:47',1,NULL,'nan',51,NULL,NULL,51),(157,'Gabriel','Ortiz','Luna','3344556677','g.ortiz.l@webmail.com','nan',NULL,NULL,NULL,'2026-01-25 03:03:47','2026-01-25 03:03:47',1,NULL,'nan',51,NULL,NULL,51),(158,'Marimar','Fernández','Gómez','8112233445','mari@correo.com','nan',NULL,NULL,NULL,'2026-01-25 03:03:47','2026-01-25 03:03:47',1,NULL,'nan',51,NULL,NULL,51),(159,'Valeria',NULL,NULL,'8978451226',NULL,NULL,NULL,NULL,NULL,'2026-01-25 03:30:45','2026-01-28 06:24:12',0,'2026-01-28 06:24:12',NULL,52,NULL,NULL,52),(160,'Vanessa',NULL,NULL,'2245789789',NULL,NULL,NULL,NULL,NULL,'2026-01-25 04:23:39','2026-01-28 06:22:23',0,'2026-01-28 06:22:23',NULL,52,NULL,NULL,52),(161,'Isabela','Martinez','Torres','2245568456','isa123@gmail.com',NULL,NULL,NULL,NULL,'2026-01-25 04:23:39','2026-01-28 06:19:53',1,NULL,'',52,NULL,NULL,52),(162,'Luisa','Vazquez','Morales','2245368159','marilu@correo.com',NULL,NULL,NULL,NULL,'2026-01-25 06:59:07','2026-01-25 06:59:07',1,NULL,NULL,50,NULL,NULL,50),(163,'Vanessa',NULL,NULL,'2245789789',NULL,NULL,NULL,NULL,NULL,'2026-01-25 06:59:07','2026-01-25 06:59:07',1,NULL,NULL,50,NULL,NULL,50),(164,'Isabela','Martinez','Torres','2245568456',NULL,NULL,NULL,NULL,NULL,'2026-01-25 06:59:07','2026-01-25 06:59:07',1,NULL,NULL,50,NULL,NULL,50),(165,'Rafael','Cordoba','Alfonso','6194864126',NULL,NULL,NULL,NULL,NULL,'2026-01-25 07:03:19','2026-01-25 07:03:19',1,NULL,NULL,50,NULL,NULL,50),(166,'Adriana','Ramos','Nava','8161561789',NULL,NULL,NULL,NULL,NULL,'2026-01-25 07:03:19','2026-01-25 07:03:19',1,NULL,NULL,50,NULL,NULL,50),(167,'Carlos','Ortiz','Navarro','3344556677',NULL,NULL,NULL,NULL,NULL,'2026-01-25 07:03:19','2026-01-25 07:03:19',1,NULL,NULL,50,NULL,NULL,50),(168,'Chana','Ramírez','Torres','2212345678',NULL,NULL,NULL,NULL,NULL,'2026-01-25 07:03:19','2026-01-25 07:03:19',1,NULL,NULL,50,NULL,NULL,50),(169,'Abraham','Sanchez','Perez','8489562147','abraham@gmail.com',NULL,NULL,NULL,NULL,'2026-01-25 07:03:19','2026-01-25 07:03:19',1,NULL,NULL,50,NULL,NULL,50),(170,'Valeria',NULL,NULL,'8978451226',NULL,NULL,NULL,NULL,NULL,'2026-01-25 07:07:46','2026-01-25 07:07:46',1,NULL,NULL,50,NULL,NULL,50),(171,'Maria Luisa','Fernández','Gómez','8112233412','marialuisa@correo.com',NULL,'MARKSA114R',NULL,NULL,'2026-01-25 07:24:49','2026-01-25 07:24:49',1,NULL,NULL,50,NULL,NULL,50),(172,'Cliente nuevo',NULL,NULL,'1545648484',NULL,NULL,NULL,NULL,NULL,'2026-01-28 01:42:56','2026-01-28 01:42:56',1,NULL,'',37,NULL,NULL,NULL),(173,'Esther',NULL,NULL,'8978456145','estheeer@gmail.com',NULL,NULL,NULL,NULL,'2026-01-28 06:17:22','2026-01-28 06:19:13',1,NULL,'',37,NULL,NULL,52),(174,'Cliente de prueba...',NULL,NULL,'4564561561',NULL,NULL,NULL,NULL,NULL,'2026-01-30 07:18:38','2026-01-30 07:18:38',1,NULL,'',59,NULL,NULL,52),(175,'Cliente consultor',NULL,NULL,'2156165165',NULL,NULL,NULL,NULL,NULL,'2026-01-30 17:55:12','2026-01-30 17:55:12',1,NULL,'',59,NULL,NULL,52),(176,'Valeria',NULL,NULL,'8978451226',NULL,NULL,NULL,NULL,NULL,'2026-01-30 22:18:55','2026-01-30 22:18:55',1,NULL,NULL,35,NULL,NULL,35),(177,'Maria Luisa','Fernández','Gómez','8112233412','marialuisa@correo.com',NULL,'MARKSA114R',NULL,NULL,'2026-01-30 22:18:55','2026-01-30 22:18:55',1,NULL,NULL,35,NULL,NULL,35),(178,'Cliente prueba admin',NULL,NULL,'6548949848',NULL,NULL,NULL,NULL,NULL,'2026-01-31 05:39:34','2026-01-31 05:40:13',1,NULL,'',55,NULL,2,52),(179,'Cliente prueba vendedor',NULL,NULL,'1561564545',NULL,NULL,NULL,NULL,NULL,'2026-01-31 06:40:03','2026-01-31 06:40:03',1,NULL,'',54,NULL,NULL,52),(180,'Gabriel',NULL,NULL,'2236383947',NULL,NULL,NULL,NULL,NULL,'2026-03-16 02:24:55','2026-03-16 02:24:55',1,NULL,'',62,NULL,NULL,62);
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cobros`
--

DROP TABLE IF EXISTS `cobros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cobros` (
  `idcobros` int NOT NULL AUTO_INCREMENT,
  `monto_recibido` decimal(10,2) NOT NULL,
  `fecha_cobro` datetime NOT NULL,
  `monto_restante` decimal(10,2) DEFAULT NULL,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_modificacion` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `activo` tinyint(1) DEFAULT '1',
  `fecha_eliminacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `forma_cobro` int NOT NULL,
  `ventas_registro` int NOT NULL,
  `usuario_registro` int NOT NULL,
  PRIMARY KEY (`idcobros`),
  KEY `fk_forma_cobro_idx` (`forma_cobro`),
  KEY `fk_usuario_idx` (`usuario_registro`),
  KEY `fk_venta_cobro_idx` (`ventas_registro`),
  CONSTRAINT `fk_forma_cobro` FOREIGN KEY (`forma_cobro`) REFERENCES `forma_cobro_cat` (`idforma_cobro`),
  CONSTRAINT `fk_usuario_cobro` FOREIGN KEY (`usuario_registro`) REFERENCES `usuario` (`idusuario`),
  CONSTRAINT `fk_venta_cobro` FOREIGN KEY (`ventas_registro`) REFERENCES `ventas` (`idventa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cobros`
--

LOCK TABLES `cobros` WRITE;
/*!40000 ALTER TABLE `cobros` DISABLE KEYS */;
/*!40000 ALTER TABLE `cobros` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cotizacion`
--

DROP TABLE IF EXISTS `cotizacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cotizacion` (
  `idcotizacion` int NOT NULL AUTO_INCREMENT,
  `cliente_id` int NOT NULL,
  `fecha` date NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  `usuario_registro` int NOT NULL,
  `owner_id` int NOT NULL,
  PRIMARY KEY (`idcotizacion`),
  KEY `fk_cotizacion_cliente` (`cliente_id`),
  KEY `fk_registro_cotizacion_idx` (`usuario_registro`),
  KEY `fk_cotizaciones_del_negocio_idx` (`owner_id`),
  CONSTRAINT `fk_cotizacion_cliente` FOREIGN KEY (`cliente_id`) REFERENCES `cliente` (`idcliente`) ON UPDATE CASCADE,
  CONSTRAINT `fk_cotizaciones_del_negocio` FOREIGN KEY (`owner_id`) REFERENCES `usuario` (`idusuario`),
  CONSTRAINT `fk_registro_cotizacion` FOREIGN KEY (`usuario_registro`) REFERENCES `usuario` (`idusuario`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cotizacion`
--

LOCK TABLES `cotizacion` WRITE;
/*!40000 ALTER TABLE `cotizacion` DISABLE KEYS */;
INSERT INTO `cotizacion` VALUES (1,43,'2026-01-05',300.00,1,3,3),(2,44,'2026-01-05',300.00,1,3,3),(3,44,'2026-01-06',900.00,1,3,3),(4,43,'2026-01-06',150.00,1,3,3),(5,43,'2026-01-07',600.00,1,3,3),(6,44,'2026-01-07',600.00,1,3,3),(7,45,'2026-01-07',600.00,1,3,3),(8,46,'2026-01-08',100.00,1,38,38),(9,56,'2026-01-19',1000.00,1,52,52),(10,58,'2026-01-28',1000.00,1,37,52),(11,58,'2026-01-31',500.00,1,52,52),(12,180,'2026-03-15',100.00,1,62,62);
/*!40000 ALTER TABLE `cotizacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cotizacion_detalle`
--

DROP TABLE IF EXISTS `cotizacion_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cotizacion_detalle` (
  `iddetallecotizacion` int NOT NULL AUTO_INCREMENT,
  `cotizacion_id` int NOT NULL,
  `servicio_id` int NOT NULL,
  `cantidad` int NOT NULL DEFAULT '1',
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`iddetallecotizacion`),
  KEY `fk_detalle_cotizacion` (`cotizacion_id`),
  KEY `fk_detalle_servicio` (`servicio_id`),
  CONSTRAINT `fk_detalle_cotizacion` FOREIGN KEY (`cotizacion_id`) REFERENCES `cotizacion` (`idcotizacion`) ON DELETE CASCADE,
  CONSTRAINT `fk_detalle_servicio` FOREIGN KEY (`servicio_id`) REFERENCES `servicio` (`idservicio`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cotizacion_detalle`
--

LOCK TABLES `cotizacion_detalle` WRITE;
/*!40000 ALTER TABLE `cotizacion_detalle` DISABLE KEYS */;
INSERT INTO `cotizacion_detalle` VALUES (1,1,5,2,150.00,300.00,1),(2,2,5,2,150.00,300.00,1),(3,3,6,3,300.00,900.00,1),(4,4,5,1,150.00,150.00,1),(5,5,5,4,150.00,600.00,1),(6,6,6,2,300.00,600.00,1),(7,7,6,2,300.00,600.00,1),(8,8,7,1,100.00,100.00,1),(9,9,8,2,500.00,1000.00,1),(10,10,8,2,500.00,1000.00,1),(11,11,8,1,500.00,500.00,1),(12,12,13,1,100.00,100.00,1);
/*!40000 ALTER TABLE `cotizacion_detalle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_venta`
--

DROP TABLE IF EXISTS `detalle_venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_venta` (
  `iddetalle_venta` int NOT NULL AUTO_INCREMENT,
  `cantidad` int NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `venta_id` int DEFAULT NULL,
  `inventario_id` int DEFAULT NULL,
  `servicio_id` int DEFAULT NULL,
  PRIMARY KEY (`iddetalle_venta`),
  KEY `fk_inventario_idx` (`inventario_id`),
  KEY `fk_servicio_idx` (`servicio_id`),
  KEY `fk_venta_idx` (`venta_id`),
  CONSTRAINT `fk_inventario` FOREIGN KEY (`inventario_id`) REFERENCES `inventario` (`idinventario`),
  CONSTRAINT `fk_servicio` FOREIGN KEY (`servicio_id`) REFERENCES `servicio` (`idservicio`),
  CONSTRAINT `fk_venta` FOREIGN KEY (`venta_id`) REFERENCES `ventas` (`idventa`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_venta`
--

LOCK TABLES `detalle_venta` WRITE;
/*!40000 ALTER TABLE `detalle_venta` DISABLE KEYS */;
/*!40000 ALTER TABLE `detalle_venta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(7,'cliente','cliente'),(8,'cliente','estadoclientecat'),(9,'cliente','frecuenciaclientecat'),(5,'contenttypes','contenttype'),(16,'oportunidades','oportunidad'),(6,'sessions','session'),(12,'usuario','preferenciausuario'),(10,'usuario','rolusuario'),(11,'usuario','usuario'),(13,'ventas','estatuscobros'),(14,'ventas','etapaventas'),(15,'ventas','venta');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-11-15 00:52:12.362620'),(2,'auth','0001_initial','2025-11-15 00:52:13.622961'),(3,'admin','0001_initial','2025-11-15 00:52:13.904702'),(4,'admin','0002_logentry_remove_auto_add','2025-11-15 00:52:13.929732'),(5,'admin','0003_logentry_add_action_flag_choices','2025-11-15 00:52:13.967368'),(6,'contenttypes','0002_remove_content_type_name','2025-11-15 00:52:14.183519'),(7,'auth','0002_alter_permission_name_max_length','2025-11-15 00:52:14.326108'),(8,'auth','0003_alter_user_email_max_length','2025-11-15 00:52:14.380380'),(9,'auth','0004_alter_user_username_opts','2025-11-15 00:52:14.395374'),(10,'auth','0005_alter_user_last_login_null','2025-11-15 00:52:14.520361'),(11,'auth','0006_require_contenttypes_0002','2025-11-15 00:52:14.524361'),(12,'auth','0007_alter_validators_add_error_messages','2025-11-15 00:52:14.538367'),(13,'auth','0008_alter_user_username_max_length','2025-11-15 00:52:14.721275'),(14,'auth','0009_alter_user_last_name_max_length','2025-11-15 00:52:14.871779'),(15,'auth','0010_alter_group_name_max_length','2025-11-15 00:52:14.919512'),(16,'auth','0011_update_proxy_permissions','2025-11-15 00:52:14.936719'),(17,'auth','0012_alter_user_first_name_max_length','2025-11-15 00:52:15.094725'),(18,'cliente','0001_initial','2025-11-15 00:52:15.106757'),(19,'oportunidades','0001_initial','2025-11-15 00:52:15.114781'),(20,'sessions','0001_initial','2025-11-15 00:52:15.200792'),(21,'usuario','0001_initial','2025-11-15 00:52:15.210768'),(22,'usuario','0002_preferenciausuario','2025-11-15 00:52:15.427177'),(23,'ventas','0001_initial','2025-11-15 00:52:15.427177'),(24,'ventas','0002_alter_etapaventas_options','2025-11-21 04:14:57.990639'),(25,'ventas','0003_etapaventas_orden','2025-11-21 10:31:14.820339'),(26,'usuario','0003_alter_usuario_options','2025-11-24 18:44:50.442503');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('0dbuyta2uc1d52ncswqge5rbwxr9vuh9','eyJpZHVzdWFyaW8iOjUyLCJub21icmUiOiJNYXJpYW5hIiwicm9sIjoiRHVlXHUwMGYxbyJ9:1vkub1:Bu10PEI2AWDrW3v6XI7viKq5JmQz4pOd86fqHLXNMlI','2026-02-10 19:43:51.776901'),('16hw4qadzfr7wx0coil1hedf1mxboyhj','eyJpZHVzdWFyaW8iOjMsIm5vbWJyZSI6Ikdsb3JpYSIsInJvbCI6IkR1ZVx1MDBmMW8ifQ:1vX8rC:vwWhjC7XcOHeJwcM5smD6kQ4P0mn92puRkF7pzwB7qw','2026-01-03 20:07:38.873682'),('8hmy3buztbyw0d62qep7ehq81qn4mnrq','eyJpZHVzdWFyaW8iOjUyLCJub21icmUiOiJNYXJpYW5hIiwicm9sIjoiRHVlXHUwMGYxbyJ9:1vlXpV:AsJrJ9XHhQ5AcHnDRgQne_BcXoFAUPtUC2RLCtHuGqI','2026-02-12 13:37:25.134346'),('cax4ehw3mqkaerxval7eyag1w7pay7k5','eyJpZHVzdWFyaW8iOjMsIm5vbWJyZSI6Ikdsb3JpYSIsInJvbCI6IkR1ZVx1MDBmMW8ifQ:1vKYEl:_kgeCi3xjIdQCe-0DGZ4N1KJZOKyYfWSHOPJFXY_6PI','2025-11-30 02:35:55.346613'),('cove38t0mnkehyz7ckbmhepgoxttomzk','eyJpZHVzdWFyaW8iOjIzLCJub21icmUiOiJQZXRyYSJ9:1vTrIU:fTEBhExEVyR6_-lePxLh4rVgwHlQ22WDWailpa-Zpng','2025-12-25 18:46:14.211958'),('fy04e8mb60vejsgi9mpz9wl8j3owtm1u','eyJpZHVzdWFyaW8iOjMsIm5vbWJyZSI6Ikdsb3JpYSIsInJvbCI6IkR1ZVx1MDBmMW8ifQ:1vMkxY:R5gYanVgNXDgL-RFnFyqEo-1z4TbtFtz-CsDe6vVdQU','2025-12-06 04:35:16.172744'),('g3r4l5wlos8j43digr3b9s01uxbgv84y','eyJpZHVzdWFyaW8iOjYyLCJub21icmUiOiJNYXJpYW5hIiwicm9sIjoiRHVlXHUwMGYxbyJ9:1w1xTD:e77pxtQbCbWpK_hA0I9uKkDPAD8Dq4heAiokhpm5SeE','2026-03-29 20:14:15.703020'),('hyiw7im8xpvmsqfnww9iwxtk9bgpkpx8','eyJpZHVzdWFyaW8iOjUyLCJub21icmUiOiJNYXJpYW5hIiwicm9sIjoiRHVlXHUwMGYxbyJ9:1vlGrL:VkBKAU_FxJVGIky18dqfSZ7kHSaGB-PSnOL6P2ijZ_w','2026-02-11 19:30:11.679672'),('jthj7g6kneohrx5l4rxn8m75p689pqd5','eyJpZHVzdWFyaW8iOjM4LCJub21icmUiOiJBZHJpYW5hIiwicm9sIjoiRHVlXHUwMGYxbyJ9:1vjvuW:Dz3IYK0FiWdDrsKxKJRmVg-2W9MGBIBYAxF7YufVC4U','2026-02-08 02:55:56.314395'),('lvl65b5obwue6cjphos03tux850yvvr7','eyJpZHVzdWFyaW8iOjIzLCJub21icmUiOiJQZXRyYSJ9:1vSluj:CedqTjh4_TMZ_gDAiYjAYNW-5nVni3biaQB95_WS7Xg','2025-12-22 18:49:13.432675'),('n3sv7u2o88dm0n4fgiq929tx9pbmaccp','eyJpZHVzdWFyaW8iOjM4LCJub21icmUiOiJBZHJpYW5hIiwicm9sIjoiRHVlXHUwMGYxbyJ9:1vduBG:a1QgvO2YYFN6iRwwRAF1pEv7leyc2J4Sprt7Zq3c6ko','2026-01-22 11:52:18.387026'),('ocsde8dewq0404kmw0j7btequqlmbcnq','.eJw9izEOgCAMAP_SmcnEQVY3P0HQdiCB1rTUxfh3cXG8y90NBd08axGI8xKApe1KEGHzzBBApQ5Yhc1rFx0GnViS-Ul6Fcv4jVOAJijp-LvY1el5AQ5BIV4:1vluhu:auP0lvt7za4zGUH1NBguU1tuBqAWVCITEn-31kc7U0E','2026-02-13 14:03:06.618855'),('p410yeqyoswmot0qv7exhv2shia29dxg','eyJpZHVzdWFyaW8iOjUyLCJub21icmUiOiJNYXJpYW5hIiwicm9sIjoiRHVlXHUwMGYxbyJ9:1vlcSQ:cjqEsthEciVMhARsaw4qJDs3US5wcGUzGm3zvrDTMy0','2026-02-12 18:33:54.629126'),('r7b36dlg1v5jfbf9zgmoqaxfaoy4tz9s','eyJpZHVzdWFyaW8iOjUyLCJub21icmUiOiJNYXJpYW5hIiwicm9sIjoiRHVlXHUwMGYxbyJ9:1vkzqD:qJrnkYsXu9gPiSPoIDbS_3vM3V98KXk6i_65wyoh3t0','2026-02-11 01:19:53.802776'),('veyd3t54cn0etq64dehxex1mzsthealc','eyJpZHVzdWFyaW8iOjU5LCJub21icmUiOiJKdWFuIiwicm9sIjoiQ29uc3VsdG9yIn0:1vlfYD:RAoOdPWzwczdemFYZNgqbkku9aP_LHH-NICb2NrNZag','2026-02-12 21:52:05.368232'),('y3hker95p08ozo2123ew431ahcuwckpp','eyJpZHVzdWFyaW8iOjU0LCJub21icmUiOiJHZXJhcmRvIiwicm9sIjoiVmVuZGVkb3IifQ:1vm4aY:dauOfXXC2mCYX5X8faO0_7rGvaOpSWkVlOXXcbUYE9A','2026-02-14 00:36:10.663083');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estado_cliente_cat`
--

DROP TABLE IF EXISTS `estado_cliente_cat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estado_cliente_cat` (
  `idestado_cliente` int NOT NULL AUTO_INCREMENT,
  `nombre_estado` varchar(45) NOT NULL,
  PRIMARY KEY (`idestado_cliente`),
  UNIQUE KEY `nombre_estado_UNIQUE` (`nombre_estado`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estado_cliente_cat`
--

LOCK TABLES `estado_cliente_cat` WRITE;
/*!40000 ALTER TABLE `estado_cliente_cat` DISABLE KEYS */;
INSERT INTO `estado_cliente_cat` VALUES (3,'Frecuente'),(4,'Inactivo'),(2,'Nuevo'),(6,'Perdido'),(5,'Potencial'),(1,'Prospecto');
/*!40000 ALTER TABLE `estado_cliente_cat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estatus_cobros`
--

DROP TABLE IF EXISTS `estatus_cobros`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estatus_cobros` (
  `idestatus_cobros` int NOT NULL AUTO_INCREMENT,
  `nombre_estatus_cobro` varchar(45) NOT NULL,
  PRIMARY KEY (`idestatus_cobros`),
  UNIQUE KEY `nombre_estatus_cobro_UNIQUE` (`nombre_estatus_cobro`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estatus_cobros`
--

LOCK TABLES `estatus_cobros` WRITE;
/*!40000 ALTER TABLE `estatus_cobros` DISABLE KEYS */;
INSERT INTO `estatus_cobros` VALUES (3,'Cobrado'),(2,'Cobro parcial'),(1,'Pendiente');
/*!40000 ALTER TABLE `estatus_cobros` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `etapa_ventas`
--

DROP TABLE IF EXISTS `etapa_ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `etapa_ventas` (
  `idetapa_ventas` int NOT NULL AUTO_INCREMENT,
  `nombre_etapa` varchar(45) NOT NULL,
  `orden` int unsigned NOT NULL,
  PRIMARY KEY (`idetapa_ventas`),
  UNIQUE KEY `nombre_etapa_UNIQUE` (`nombre_etapa`),
  CONSTRAINT `etapa_ventas_chk_1` CHECK ((`orden` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `etapa_ventas`
--

LOCK TABLES `etapa_ventas` WRITE;
/*!40000 ALTER TABLE `etapa_ventas` DISABLE KEYS */;
INSERT INTO `etapa_ventas` VALUES (1,'Prospecto',1),(2,'Calificación',2),(3,'Propuesta',3),(4,'Negociación',4),(5,'Cierre-Ganado',5),(6,'Cierre-Perdido',6);
/*!40000 ALTER TABLE `etapa_ventas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `forma_cobro_cat`
--

DROP TABLE IF EXISTS `forma_cobro_cat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forma_cobro_cat` (
  `idforma_cobro` int NOT NULL AUTO_INCREMENT,
  `nombre_forma_cobro` varchar(45) NOT NULL,
  PRIMARY KEY (`idforma_cobro`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forma_cobro_cat`
--

LOCK TABLES `forma_cobro_cat` WRITE;
/*!40000 ALTER TABLE `forma_cobro_cat` DISABLE KEYS */;
INSERT INTO `forma_cobro_cat` VALUES (1,'Efectivo'),(2,'Tarjeta');
/*!40000 ALTER TABLE `forma_cobro_cat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `frecuencia_cliente_cat`
--

DROP TABLE IF EXISTS `frecuencia_cliente_cat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `frecuencia_cliente_cat` (
  `idfrecuencia_cliente` int NOT NULL AUTO_INCREMENT,
  `nombre_frecuencia` varchar(45) NOT NULL,
  PRIMARY KEY (`idfrecuencia_cliente`),
  UNIQUE KEY `nombre_frecuencia_UNIQUE` (`nombre_frecuencia`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `frecuencia_cliente_cat`
--

LOCK TABLES `frecuencia_cliente_cat` WRITE;
/*!40000 ALTER TABLE `frecuencia_cliente_cat` DISABLE KEYS */;
INSERT INTO `frecuencia_cliente_cat` VALUES (4,'Anual'),(1,'Diario'),(3,'Mensual'),(2,'Semanal');
/*!40000 ALTER TABLE `frecuencia_cliente_cat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventario`
--

DROP TABLE IF EXISTS `inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventario` (
  `idinventario` int NOT NULL AUTO_INCREMENT,
  `nombrearticulo` varchar(45) DEFAULT NULL,
  `descripcion` varchar(45) DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `proveedor` int DEFAULT NULL,
  `cantidad_disponible` int DEFAULT NULL,
  `comentarios` text,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_modificacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `activo` tinyint(1) DEFAULT '1',
  `fecha_eliminacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `tipo` int DEFAULT NULL,
  `unidad` int DEFAULT NULL,
  `usuario_registro` int NOT NULL,
  `owner_id` int NOT NULL,
  PRIMARY KEY (`idinventario`),
  KEY `fk_tipo_idx` (`tipo`),
  KEY `fk_unidad_idx` (`unidad`),
  KEY `fk_proveedor_idx` (`proveedor`),
  KEY `fk_productos_del_negocio_idx` (`owner_id`),
  KEY `fk_producto_registrado_por_idx` (`usuario_registro`),
  CONSTRAINT `fk_producto_registrado_por` FOREIGN KEY (`usuario_registro`) REFERENCES `usuario` (`idusuario`),
  CONSTRAINT `fk_productos_del_negocio` FOREIGN KEY (`owner_id`) REFERENCES `usuario` (`idusuario`),
  CONSTRAINT `fk_proveedor` FOREIGN KEY (`proveedor`) REFERENCES `proveedor` (`idproveedor`),
  CONSTRAINT `fk_tipo` FOREIGN KEY (`tipo`) REFERENCES `tipo_articulo_cat` (`idtipo_articulo`),
  CONSTRAINT `fk_unidad` FOREIGN KEY (`unidad`) REFERENCES `unidad_cat` (`idunidad_cat`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventario`
--

LOCK TABLES `inventario` WRITE;
/*!40000 ALTER TABLE `inventario` DISABLE KEYS */;
INSERT INTO `inventario` VALUES (1,'Queso de rueda','Queso de rueda para la comida..',100.00,NULL,3,'y ya solo es queso','2025-12-16 05:05:28','2025-12-16 18:19:16',0,'2025-12-16 18:19:16',1,5,23,23),(2,'Tortillas',NULL,15.00,NULL,5,'','2025-12-16 05:59:30','2025-12-16 06:01:14',0,'2025-12-16 06:01:14',NULL,NULL,23,23),(3,'Manteca de cerdo','Se utiliza para las gorditas',30.00,NULL,5,'','2025-12-16 17:54:55','2025-12-16 18:21:31',0,'2025-12-16 18:21:31',1,6,23,23),(4,'Lechuga',NULL,15.00,NULL,7,'','2025-12-16 18:27:58','2025-12-16 18:28:03',0,'2025-12-16 18:28:03',NULL,1,23,23),(5,'Lechuga',NULL,15.00,NULL,8,'','2025-12-16 18:30:29','2025-12-16 19:22:24',0,'2025-12-16 19:22:24',NULL,1,23,23),(6,'Queso fresco',NULL,100.00,NULL,2,'','2025-12-16 18:32:06','2025-12-16 18:32:10',0,'2025-12-16 18:32:10',NULL,5,23,23),(7,'Papas',NULL,20.00,NULL,8,'','2025-12-16 19:10:23','2025-12-16 19:25:38',0,'2025-12-16 19:25:38',1,5,23,23),(8,'Carne de costilla',NULL,100.00,NULL,8,'','2025-12-16 19:37:29','2025-12-16 19:37:39',0,'2025-12-16 19:37:39',4,5,23,23),(9,'Cafe dolca','cafe nescafe de sobrecito',15.00,NULL,10,'','2025-12-16 20:32:08','2025-12-16 20:32:48',0,'2025-12-16 20:32:48',NULL,5,23,23),(10,'Queso manchego',NULL,50.00,1,4,'','2025-12-16 20:32:39','2025-12-18 17:39:42',1,NULL,NULL,5,23,23),(11,'Azucar',NULL,20.00,NULL,7,'','2025-12-16 20:53:09','2025-12-16 20:53:09',1,NULL,1,5,23,23),(12,'Tomates',NULL,20.00,NULL,7,'','2025-12-16 20:53:39','2025-12-16 20:53:39',1,NULL,4,5,23,23),(13,'Tortillas',NULL,15.00,NULL,7,'','2025-12-16 20:54:04','2025-12-16 20:54:14',0,'2025-12-16 20:54:14',1,5,23,23),(14,'Tortillas',NULL,15.00,NULL,8,'','2026-01-08 17:58:07','2026-01-08 17:58:23',0,'2026-01-08 17:58:23',1,5,38,38),(15,'Cafe','Cafe de olla para usar en una cafetera',50.00,NULL,12,'','2026-01-15 07:08:31','2026-01-15 07:08:31',1,NULL,NULL,5,42,38),(16,'Cables Ethernet Cat6','Son cables para ponchar',10.00,NULL,15,'Prueba','2026-01-29 01:25:25','2026-01-29 02:16:08',1,NULL,6,8,37,52),(17,'Cable Ethernet cat5','Prueba...',10.00,NULL,5,'','2026-01-29 02:01:42','2026-01-29 02:16:39',1,NULL,6,8,37,52),(18,'Memorias USB','Son de 8 GB',50.00,NULL,4,'','2026-01-31 02:29:33','2026-01-31 02:51:07',0,'2026-01-31 02:51:07',NULL,1,52,52),(19,'Cafe','es nescafe',15.00,NULL,20,'','2026-03-16 02:29:26','2026-03-16 02:29:26',1,NULL,NULL,1,62,62);
/*!40000 ALTER TABLE `inventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `oportunidades`
--

DROP TABLE IF EXISTS `oportunidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `oportunidades` (
  `idoportunidad` int NOT NULL AUTO_INCREMENT,
  `nombreoportunidad` varchar(45) NOT NULL,
  `valor_estimado` decimal(10,2) NOT NULL,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_cierre_estimada` datetime NOT NULL,
  `comentarios` text,
  `activo` tinyint(1) DEFAULT '1',
  `fecha_eliminacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `fecha_modificacion` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `cliente_oportunidad` int NOT NULL,
  `etapa_ventas` int NOT NULL,
  `usuario_responsable` int NOT NULL,
  `creado_por` int NOT NULL,
  `negocio_oportunidad` int NOT NULL,
  PRIMARY KEY (`idoportunidad`),
  KEY `fk_clientes_oportunidad_idx` (`cliente_oportunidad`),
  KEY `fk_etapa_ventas_idx` (`etapa_ventas`),
  KEY `fk_usuario_registro_op_idx` (`usuario_responsable`),
  KEY `fk_usuario_registrador_idx` (`creado_por`),
  KEY `fk_negocio_oportunidad_idx` (`negocio_oportunidad`),
  CONSTRAINT `fk_clientes_oportunidad` FOREIGN KEY (`cliente_oportunidad`) REFERENCES `cliente` (`idcliente`),
  CONSTRAINT `fk_creado_por` FOREIGN KEY (`creado_por`) REFERENCES `usuario` (`idusuario`),
  CONSTRAINT `fk_etapa_ventas` FOREIGN KEY (`etapa_ventas`) REFERENCES `etapa_ventas` (`idetapa_ventas`),
  CONSTRAINT `fk_negocio_oportunidad` FOREIGN KEY (`negocio_oportunidad`) REFERENCES `usuario` (`idusuario`),
  CONSTRAINT `fk_responsable` FOREIGN KEY (`usuario_responsable`) REFERENCES `usuario` (`idusuario`)
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `oportunidades`
--

LOCK TABLES `oportunidades` WRITE;
/*!40000 ALTER TABLE `oportunidades` DISABLE KEYS */;
INSERT INTO `oportunidades` VALUES (1,'Venta Semanal',75000.00,'2025-12-05 06:07:03','2025-12-15 00:00:00','Cliente potencial para compra recurrente. :)',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',4,4,2,3,3),(2,'Compra de Kilos de costilla',300.00,'2025-12-05 06:07:03','2025-12-15 00:00:00','Quieren costilla :) para una hacerla en salsa\r\ninviten :b',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',2,4,2,3,3),(3,'Nueva venta',100.00,'2025-12-05 06:07:03','2025-11-22 00:00:00','esto es solo una prueba',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',4,1,4,3,3),(4,'Prueba',100000.00,'2025-12-05 06:07:03','2025-11-22 00:00:00','Ay no se, funciona porfi :\') auxilio D:',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',4,4,6,3,3),(5,'Venta nueva',1000.00,'2025-12-05 06:07:03','2025-11-21 00:00:00','hola :)',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',2,5,15,3,3),(6,'prueba',100.00,'2025-12-05 06:07:03','2025-11-21 00:00:00','aaaaaaaaaaaaaaaaaaaaaa',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',2,2,6,3,3),(7,'Prueba 3',1000.00,'2025-12-05 06:07:03','2025-11-21 00:00:00','',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',2,2,9,3,3),(8,'Hola si se pudo(espero)',5000.00,'2025-12-05 06:07:03','2025-11-23 00:00:00','si se pudo gente :D',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',3,5,4,3,3),(9,'Hola si se pudo(espero)',5000.00,'2025-12-05 06:07:03','2025-11-23 00:00:00','si se pudo gente :D',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',4,3,4,3,3),(10,'Prueba de vendedor',1000.00,'2025-12-05 06:07:03','2025-11-25 00:00:00',':D',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',4,1,15,3,3),(11,'Prueba de vestido',10000.00,'2025-12-05 06:07:03','2025-11-25 00:00:00','',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',4,2,9,3,3),(12,'Zapatitos',300.50,'2025-12-05 06:07:03','2025-11-25 00:00:00','',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',2,1,5,3,3),(13,'Ropa deportiva',500.00,'2025-12-05 06:07:03','2025-12-24 00:00:00','prueba \r\nprueba',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',2,3,9,3,3),(14,'Nueva oportunidad prueba 1',50000.00,'2025-12-05 06:07:03','2025-11-26 00:00:00','',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',3,4,4,3,3),(15,'Prueba 2',1000.00,'2025-12-05 06:07:03','2025-11-26 00:00:00','jc kjd jk',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',4,4,5,3,3),(16,'Prueba de venta(editado)',412568.00,'2025-12-05 06:07:03','2025-11-28 00:00:00','ay por dios funciona plis plis plis ndjdjBDGBhjbq\r\n:)',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',4,5,5,3,3),(17,'Segunda prueba',412563.00,'2025-12-05 06:07:03','2025-12-01 00:00:00','',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',3,2,7,3,3),(18,'Tercera prueba',1000.00,'2025-12-05 06:07:03','2025-11-27 00:00:00','',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',3,5,17,3,3),(19,'Zapatitos',120000.00,'2025-12-05 06:07:03','2025-11-27 00:00:00','',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',3,4,17,3,3),(20,'Vestidos(ayuda)',1500.00,'2025-12-05 06:07:03','2025-11-27 00:00:00','',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',4,1,7,3,3),(21,'Botas de cuero',420.00,'2025-12-05 06:07:03','2025-11-25 00:00:00','',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',3,1,4,3,3),(22,'botas de gamuza',300.00,'2025-12-05 06:07:03','2025-11-26 00:00:00','ojala y funcione esta vez',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',3,1,17,3,3),(23,'Album de bts nuevecito ',1000.00,'2025-12-05 06:07:03','2025-12-24 00:00:00','Joder claro que si :D',1,'2025-12-05 06:07:03','2025-12-21 02:47:42',3,5,4,3,3),(24,'Venta de dulces',100.00,'2025-12-05 06:07:03','2025-12-08 00:00:00','',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',3,1,5,3,3),(25,'Venta de chicles motita',15.00,'2025-12-05 06:07:03','2025-12-08 00:00:00','',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',4,1,4,3,3),(26,'Botellas de brillantina',100.00,'2025-12-05 06:07:03','2025-12-03 00:00:00','',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',4,1,15,9,3),(27,'Paquete de chispitas :b',50000.00,'2025-12-05 06:07:03','2025-12-23 00:00:00','oportunidad editada (02/12/25)..',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',4,5,5,9,3),(28,'Ventas carne de res',5000000.00,'2025-12-05 06:07:03','2025-12-03 00:00:00','',1,'2025-12-05 06:07:03','2025-12-05 06:07:03',3,5,9,15,3),(29,'Ventas de bistec',100.00,'2025-12-05 06:07:03','2025-12-01 00:00:00',':b',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',3,1,15,15,3),(30,'Blusas',2200.00,'2025-12-05 06:07:03','2025-12-05 00:00:00',':)',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',3,4,3,3,3),(31,'Pantuflas de tiburoncin2',1000.00,'2025-12-05 06:07:03','2025-12-24 00:00:00',':)',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',4,2,5,3,3),(32,'prueba techita',100000.00,'2025-12-05 06:07:03','2025-12-02 00:00:00',':b prueba despues del merge: 02/12/25 -> 8:29 pm',1,'2025-12-05 06:07:03','2025-12-21 02:47:58',2,5,5,9,3),(33,'prueba merge',1000.00,'2025-12-05 06:07:03','2025-12-02 00:00:00','segunda prueba:crear oportunidad',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',4,1,13,3,3),(34,'prueba 2 despues del merge',2000.00,'2025-12-05 06:07:03','2025-12-02 00:00:00','',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',4,1,15,3,3),(35,'Chanclitas',10000.00,'2025-12-05 06:07:03','2025-12-02 00:00:00','prueba 2 rama 2',0,'2025-12-05 06:07:03','2025-12-05 06:07:03',3,3,5,3,3),(36,'Comics de marvel',10000.00,'2025-12-05 06:07:03','2025-12-24 00:00:00',':)',1,'2025-12-05 06:07:03','2025-12-21 02:48:05',4,5,15,3,3),(37,'vestidos :b',1000.00,'2025-12-05 06:07:03','2025-12-03 00:00:00','',0,'2025-12-21 02:17:54','2025-12-21 02:17:54',3,2,5,4,3),(38,'cheetos y boing de mango :b',50.00,'2025-12-05 06:07:03','2025-12-16 00:00:00','',1,'2025-12-05 06:07:03','2025-12-21 02:47:36',2,5,15,9,3),(39,'agua',10.00,'2025-12-05 06:07:03','2025-12-03 00:00:00','',0,'2025-12-26 18:17:40','2025-12-26 18:17:40',4,5,4,3,3),(40,'tomates',15.00,'2025-12-05 06:07:03','2025-12-03 00:00:00','',1,'2025-12-05 06:07:03','2025-12-21 02:47:38',4,5,4,3,3),(41,'Orden de gorditas :)',120.00,'2025-12-08 07:55:00','2025-12-08 00:00:00','',1,NULL,'2025-12-16 21:08:09',4,5,23,23,23),(42,'10 ordenes de de taquitos :)',200.00,'2025-12-10 06:00:55','2025-12-11 00:00:00','',1,NULL,'2025-12-12 17:31:47',4,5,26,23,23),(43,'Ordenes de garnachas',120.00,'2025-12-10 06:01:55','2025-12-11 00:00:00','',1,NULL,'2025-12-19 17:21:19',3,4,26,26,23),(44,'Totopos',50.00,'2025-12-10 19:46:43','2025-12-10 00:00:00','',1,NULL,'2025-12-19 17:21:16',3,5,24,23,23),(45,'Tortillas',20.00,'2025-12-13 20:50:18','2025-12-26 00:00:00','hjvhvhkvhkckc',0,'2025-12-13 20:50:49','2025-12-13 20:50:49',3,2,24,23,23),(46,'prueba 1',100.00,'2025-12-14 22:45:23','2025-12-14 00:00:00','prueba',1,NULL,'2025-12-14 22:46:25',14,4,36,36,36),(47,'Prueba 3',100.00,'2025-12-14 23:43:15','2025-12-14 00:00:00','',1,NULL,'2025-12-14 23:43:15',14,1,24,34,23),(48,'prueba 2',100.00,'2025-12-14 23:45:22','2025-12-14 00:00:00','',1,NULL,'2025-12-14 23:45:22',14,1,36,36,36),(49,'prueba 4',100.00,'2025-12-14 23:46:41','2025-12-14 00:00:00','',1,NULL,'2025-12-14 23:48:53',2,1,24,34,23),(50,'Prueba',1000.00,'2025-12-15 00:36:21','2025-12-22 00:00:00','Esto es otra prueba',0,'2025-12-15 02:57:47','2025-12-15 02:57:47',14,1,34,34,23),(51,'Prueba',200.00,'2025-12-21 02:36:42','2025-12-21 00:00:00',':)',1,NULL,'2026-01-09 00:43:12',43,4,3,3,3),(52,'prueba final1',150.00,'2026-01-08 02:26:30','2026-01-07 00:00:00','',1,NULL,'2026-01-09 00:43:04',44,4,17,3,3),(53,'Pedido de goridtas',150.00,'2026-01-08 17:54:22','2026-01-08 00:00:00','pidieron 45 gorditas..',0,'2026-01-18 22:07:29','2026-01-18 22:07:29',46,5,38,38,38),(54,'Asesoria generalista',18700.00,'2026-01-08 18:25:07','2026-01-25 00:00:00','',1,NULL,'2026-01-08 18:25:43',53,5,39,39,39),(55,'Pedido de tamales',500.00,'2026-01-09 17:51:55','2026-01-09 00:00:00','',1,NULL,'2026-01-09 17:51:55',46,5,38,38,38),(56,'Pedidos de tacos',120.00,'2026-01-09 18:13:35','2026-01-10 00:00:00','',1,NULL,'2026-01-09 18:13:35',46,5,38,38,38),(57,'prueba final',200.00,'2026-01-09 18:57:52','2026-01-09 00:00:00','ok',1,NULL,'2026-01-18 22:37:51',51,5,42,42,38),(58,'Pruebaaaaa',100.00,'2026-01-19 08:44:34','2026-01-19 00:00:00','',1,NULL,'2026-01-19 08:46:07',49,4,42,38,38),(59,'Arreglo de computadora HP',1500.00,'2026-01-19 15:07:09','2026-01-19 00:00:00','ok',0,'2026-01-19 15:31:12','2026-01-19 15:31:12',57,3,52,52,52),(60,'Cambiar pantalla de laptop',100.00,'2026-01-29 19:45:36','2026-01-29 00:00:00','prueba..',1,NULL,'2026-01-31 05:45:27',145,4,52,52,52),(61,'Prueba final',1200.00,'2026-01-29 21:42:09','2026-01-29 00:00:00','',0,'2026-01-30 01:02:41','2026-01-30 01:02:41',144,3,55,37,52),(62,'Prueba final usuario',500.00,'2026-01-30 00:34:36','2026-01-29 00:00:00','',1,NULL,'2026-01-31 06:36:31',148,3,54,52,52),(63,'prueba 0',0.00,'2026-01-30 01:36:35','2026-01-29 00:00:00','',1,NULL,'2026-01-30 01:36:46',145,6,55,52,52),(64,'prueba 3',10.00,'2026-01-30 01:44:18','2026-01-29 00:00:00','',0,'2026-01-30 01:44:45','2026-01-30 01:44:45',145,2,54,52,52),(65,'Prueba super',100.00,'2026-01-30 01:47:12','2026-01-29 00:00:00','prueba....',1,NULL,'2026-01-31 05:45:42',145,4,52,37,52),(66,'prueba',0.00,'2026-01-30 01:48:02','2026-01-29 00:00:00','',0,'2026-01-30 01:48:10','2026-01-30 01:48:10',145,1,54,37,52),(67,'Prueba consultor',2000.00,'2026-01-30 07:22:51','2026-01-30 00:00:00','',0,'2026-01-30 18:00:15','2026-01-30 18:00:15',58,2,52,59,52),(68,'Prueba 0 consultor',0.00,'2026-01-30 07:24:05','2026-01-30 00:00:00','',0,'2026-01-30 07:24:18','2026-01-30 07:24:18',58,1,54,59,52),(69,'Prueba vendedor',200.00,'2026-01-31 06:48:55','2026-01-31 00:00:00','prueba',0,'2026-01-31 07:00:57','2026-01-31 07:00:57',58,1,54,54,52),(70,'Prueba 1`',1000.00,'2026-03-16 02:28:43','2026-03-15 00:00:00','',1,NULL,'2026-03-16 02:28:49',180,2,62,62,62);
/*!40000 ALTER TABLE `oportunidades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedor`
--

DROP TABLE IF EXISTS `proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedor` (
  `idproveedor` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  `numero` varchar(10) DEFAULT NULL,
  `comentarios` text,
  `razon_social` varchar(250) NOT NULL,
  `rfc_proveedor` varchar(13) NOT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  `owner_id` int NOT NULL,
  `codigo_postal` varchar(5) NOT NULL,
  `usuario_registro` int NOT NULL,
  PRIMARY KEY (`idproveedor`),
  UNIQUE KEY `rfc_proveedor_UNIQUE` (`rfc_proveedor`),
  KEY `fk_proveedor_negocio_idx` (`owner_id`),
  KEY `fk_usuario_registro_proveedor_idx` (`usuario_registro`),
  CONSTRAINT `fk_proveedor_negocio` FOREIGN KEY (`owner_id`) REFERENCES `usuario` (`idusuario`),
  CONSTRAINT `fk_usuario_registro_proveedor` FOREIGN KEY (`usuario_registro`) REFERENCES `usuario` (`idusuario`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedor`
--

LOCK TABLES `proveedor` WRITE;
/*!40000 ALTER TABLE `proveedor` DISABLE KEYS */;
INSERT INTO `proveedor` VALUES (1,'Proveedor de pruebaok',NULL,'Este es un proveedor de prueba','Proveedor de prueba S.A. de C.V','123123Y2HENKK',1,23,'91013',23),(2,'Prueba',NULL,'','Social','2HE29JSDNJKAS',1,3,'91000',3),(3,'Don Julio','6215156415','','Don Julio S.A de C.V.','JULEIASJJ1234',1,38,'91013',42),(4,'Proveedor de prueba','666148149','','Proveedor de prueba S.A. de C.V.','PISDHIERIONQ',1,52,'91013',37),(5,'QuickFix S.A. de C.V',NULL,'Prueba','dnqwjndqjwnqiw','QODOAFM13938J',0,52,'91010',52);
/*!40000 ALTER TABLE `proveedor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rol_usuario`
--

DROP TABLE IF EXISTS `rol_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rol_usuario` (
  `id_rol` int NOT NULL AUTO_INCREMENT,
  `nombre_rol` varchar(45) NOT NULL,
  PRIMARY KEY (`id_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rol_usuario`
--

LOCK TABLES `rol_usuario` WRITE;
/*!40000 ALTER TABLE `rol_usuario` DISABLE KEYS */;
INSERT INTO `rol_usuario` VALUES (1,'Dueño'),(2,'Administrador'),(3,'Vendedor'),(4,'Superusuario'),(5,'Consultor');
/*!40000 ALTER TABLE `rol_usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicio`
--

DROP TABLE IF EXISTS `servicio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicio` (
  `idservicio` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `descripcion` text,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_modificacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `activo` tinyint(1) DEFAULT '1',
  `fecha_eliminacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `usuario_registro` int NOT NULL,
  `owner_id` int NOT NULL,
  PRIMARY KEY (`idservicio`),
  KEY `fk_usuario_registro_idx` (`usuario_registro`),
  KEY `fk_servicio_del_negocio_idx` (`owner_id`),
  CONSTRAINT `fk_servicio_del_negocio` FOREIGN KEY (`owner_id`) REFERENCES `usuario` (`idusuario`),
  CONSTRAINT `fk_servicio_registrado_por` FOREIGN KEY (`usuario_registro`) REFERENCES `usuario` (`idusuario`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicio`
--

LOCK TABLES `servicio` WRITE;
/*!40000 ALTER TABLE `servicio` DISABLE KEYS */;
INSERT INTO `servicio` VALUES (1,'Comida a domicilio',100.00,'Es entrega a domicilio el precio registrado es por entregarlo, el precio del platillo es aparte(editado)','2025-12-15 20:35:29','2025-12-15 20:38:30',0,'2025-12-15 20:38:30',23,23),(2,'Comida por eventos',1050.00,'Ejemplo','2025-12-15 20:45:57','2025-12-15 20:46:07',1,NULL,23,23),(3,'Comida a domicilio',100.00,'El precio anotado es este + el precio del platillo','2025-12-16 21:06:25','2025-12-16 21:06:25',1,NULL,23,23),(4,'Comida para llevar',10.00,'El precio total es esto + el precio del platillo que se va a pedir','2025-12-16 21:07:44','2025-12-16 21:07:54',0,'2025-12-16 21:07:54',23,23),(5,'Comida a domicilio',150.00,'este precio no toma en cuenta el costo de los platillos','2026-01-06 03:38:50','2026-01-06 03:38:50',1,NULL,3,3),(6,'Comida por pedido',300.00,'','2026-01-06 06:30:26','2026-01-06 06:30:26',1,NULL,3,3),(7,'Comida a domicilio',100.00,'prueba','2026-01-08 17:56:29','2026-01-15 07:07:31',1,NULL,38,38),(8,'Mantenimiento para laptops',500.00,'Este precio toma en cuenta: materiales, mano de obra, etc.','2026-01-19 14:52:57','2026-01-19 14:52:57',1,NULL,52,52),(9,'Cambio de pantallas de laptops',500.00,'Por el puro servicio :b','2026-01-28 21:03:31','2026-01-28 21:03:44',1,NULL,37,52),(10,'Servicio de prueba',100.00,'','2026-01-28 21:04:10','2026-01-28 21:04:14',0,'2026-01-28 21:04:14',37,52),(11,'Reparacion de consolas de videojuegos',500.00,'El precio que puse es un ejemplo','2026-01-31 01:58:19','2026-01-31 02:15:28',0,'2026-01-31 02:15:28',52,52),(12,'Prueba',20.00,'','2026-01-31 06:05:02','2026-01-31 06:05:17',1,NULL,55,52),(13,'Comida a domicilio',100.00,'','2026-03-16 02:33:09','2026-03-16 02:33:09',1,NULL,62,62);
/*!40000 ALTER TABLE `servicio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipo_articulo_cat`
--

DROP TABLE IF EXISTS `tipo_articulo_cat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipo_articulo_cat` (
  `idtipo_articulo` int NOT NULL AUTO_INCREMENT,
  `nombre_tipo` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idtipo_articulo`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipo_articulo_cat`
--

LOCK TABLES `tipo_articulo_cat` WRITE;
/*!40000 ALTER TABLE `tipo_articulo_cat` DISABLE KEYS */;
INSERT INTO `tipo_articulo_cat` VALUES (1,'Alimentos'),(2,'Bebidas'),(3,'Cosmético'),(4,'Manufacturado'),(5,'Industrial'),(6,'Electronicos'),(7,'Moda'),(8,'Abarrotes y Semillas'),(9,'Seguridad');
/*!40000 ALTER TABLE `tipo_articulo_cat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unidad_cat`
--

DROP TABLE IF EXISTS `unidad_cat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unidad_cat` (
  `idunidad_cat` int NOT NULL AUTO_INCREMENT,
  `nombre_unidad` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idunidad_cat`),
  UNIQUE KEY `nombre_unidad` (`nombre_unidad`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidad_cat`
--

LOCK TABLES `unidad_cat` WRITE;
/*!40000 ALTER TABLE `unidad_cat` DISABLE KEYS */;
INSERT INTO `unidad_cat` VALUES (12,'caja'),(9,'cm'),(3,'gr'),(13,'juego'),(5,'kg'),(7,'lbs'),(6,'ltrs'),(8,'m'),(2,'ml'),(10,'mm'),(4,'oz'),(11,'paquete'),(1,'pieza');
/*!40000 ALTER TABLE `unidad_cat` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `idusuario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `apellidopaterno` varchar(45) NOT NULL,
  `apellidomaterno` varchar(45) DEFAULT NULL,
  `numerotel` varchar(10) DEFAULT NULL,
  `correo` varchar(100) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `rfc` varchar(13) DEFAULT NULL,
  `rol` int NOT NULL DEFAULT '1',
  `local_Fijo` enum('Si','No') DEFAULT NULL,
  `nombre_negocio` varchar(100) DEFAULT NULL,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_modificacion` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `activo` tinyint(1) DEFAULT '1',
  `fecha_eliminacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `owner_id` int DEFAULT NULL,
  PRIMARY KEY (`idusuario`),
  UNIQUE KEY `correo_UNIQUE` (`correo`),
  UNIQUE KEY `rfc_UNIQUE` (`rfc`),
  KEY `fk_rol_idx` (`rol`),
  KEY `fk_registrado_por_idx` (`owner_id`),
  CONSTRAINT `fk_registrado_por` FOREIGN KEY (`owner_id`) REFERENCES `usuario` (`idusuario`),
  CONSTRAINT `fk_rol_usuario` FOREIGN KEY (`rol`) REFERENCES `rol_usuario` (`id_rol`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'Carlos','Lopez','Mora','5558881122','esteescarlos@gmail.com','pbkdf2_sha256$1000000$3TdZvJ7ZCQR4JjTEIXArWD$nF65oboxZUJqjkBJ7LYSjn+bGfy1HKYn5Gz6qhY3RdY=','LOMC880101AA2',3,NULL,NULL,'2025-12-14 06:15:24','2025-12-14 06:15:24',0,'2025-12-14 06:15:24',3),(2,'Mariana','Lopez','Mora','2245788956','carlos@gmail.com','pbkdf2_sha256$1000000$qgwLoDbUcp1i4rhhk6qMlf$vfyz33KtGxC1rpYLhlhnC3HA/ZVW9Pf/mhMk8m2WGmg=','LOMM880101AA2',2,NULL,NULL,'2025-12-14 06:15:24','2025-12-14 06:15:24',0,'2025-12-14 06:15:24',3),(3,'Gloria','Martinez','Martinez','2245788956','mimi@gmail.com','pbkdf2_sha256$1000000$KzGGVi1FKIjMWBuNXnQwPV$+2DfyHcFXx+vyTBKcsDjuQPkiQIupitPzzcyNLmlf7k=','kmdkamsdksamd',1,'Si','Code','2025-11-24 21:29:57','2025-11-24 21:29:57',1,'2025-11-24 21:29:57',3),(4,'Cecilia','Martinez','Martinez','2215478956','titi@gmail.com','pbkdf2_sha256$1000000$P0VpEu5qyba0TydmjkO9hW$pJG30Qog8JNrNbs8zCkHbe/kY/w66I8rYAfxV3f3zMU=','jdnkndokqwnfd',2,NULL,NULL,'2025-12-05 03:38:20','2025-12-05 03:38:20',1,'2025-12-05 03:38:20',4),(5,'Ian','Martinez','Martinez','2258881122','ian@example.com','pbkdf2_sha256$1000000$77pZbMpCT8vpeSNnXNkkm3$OsEr/7jRM/d/gbbAj2xxG/g0TYFji393TPzKYEFHJJs=','MAMI880101AA2',2,NULL,NULL,'2025-11-16 06:23:43','2025-11-16 06:23:43',1,NULL,3),(6,'Cristian','Aguirre','Aguirre','2245788956','cristian@gmail.com','pbkdf2_sha256$1000000$l4lsJldrxdKVRFkSnP2nzX$ss1cyx4WR2aI4r0vStZwNm7nqSsSz7cHfU/eUTevdyE=',NULL,3,NULL,NULL,'2025-11-16 07:11:38','2025-11-16 07:11:38',1,NULL,3),(7,'Saul','Martinez','Martinez','2213467989','ale@gmail.com','pbkdf2_sha256$1000000$Aah9iPq4HqiT4isnl8Li5M$yfPblTPWV3U0y/hVsk4GoRmNcjCisj6pPsSOm4dsPO8=',NULL,1,NULL,NULL,'2025-12-05 03:37:49','2025-12-05 03:37:49',1,'2025-12-05 03:37:49',7),(8,'Cristina','Martinez','Arguello','2245788956','crist@gmail.com','pbkdf2_sha256$1000000$tsd4lUFDgNEl77988VpMJG$8/ySF+5elgayKwv5JM7qhjiFnQrH/kxjJd/b8GfhPrs=',NULL,2,NULL,NULL,'2025-11-16 07:16:25','2025-11-16 07:16:25',1,NULL,7),(9,'Esther','Geron','Tejeda','2233445678','teche@gmail.com','pbkdf2_sha256$1000000$6NDwflYiavCcSoV9x37O2U$JTIlf7JKyPOEnLxaPMOxTF3p6NlN2lOoboe8M6RHs9I=',NULL,3,NULL,NULL,'2025-11-16 07:19:02','2025-11-16 07:19:02',1,NULL,3),(10,'Teresa','Geron','Tejeda','2213467989','tere@gmail.com','pbkdf2_sha256$1000000$Uc5aUnH1EgPNCLzwGJN5xc$duUPV590bt6BZBmvsvYdkeIUfMb41WulRfTVVfhdKkM=',NULL,3,NULL,NULL,'2025-11-16 07:44:20','2025-11-16 08:44:53',0,'2025-11-16 08:44:53',3),(11,'Miriam','Garcia','Padilla','2214447896','miriam@gmail.com','pbkdf2_sha256$1000000$AFXEw3iKvFIJnTo5TAyfPk$XTgAl1EfXkb4mmXjjEKBURVE/rqP93/HovFx10bdYsY=','mkwmdoanwdkne',2,NULL,NULL,'2025-11-24 21:46:34','2025-11-24 21:46:34',1,'2025-11-24 21:46:34',4),(12,'Diana','Carrasco','Lopez','2278895645','diana@gmail.com','pbkdf2_sha256$1000000$s3k4PltEU9P7Rm7G6v7XUJ$EsLoluKdwwu1m8SmnjHF857lnvxIC6IHT4FVMm6tpM4=',NULL,1,NULL,NULL,'2025-11-24 21:46:39','2025-11-24 21:46:39',1,'2025-11-24 21:46:39',4),(13,'Mariana','Padilla','Vazquez','2245788956','mariana@gmail.com','pbkdf2_sha256$1000000$oslaAqfiRaNa1h5JQaEr6I$hZRbxVJSqUK0dht3x+mmQx1skBC4HvM0zwjeslv8kco=',NULL,2,NULL,NULL,'2025-11-18 02:37:50','2025-11-18 02:37:50',1,NULL,3),(15,'Martha','Lopez','Mora','2245788963','mar@gmail.com','pbkdf2_sha256$1000000$yDNAMTyBz4IhZlytXFGKg6$Tnqfxd4RJ8/BqFB6a54shp7reiucl1ZOBU8LJpdq1K0=',NULL,3,NULL,NULL,'2025-11-18 03:55:55','2025-11-18 03:55:55',1,NULL,3),(16,'Rafael','Cordoba','Alonso','1464117846','rafa@gmail.com','pbkdf2_sha256$1000000$RIOknWrNXFvWlOUGNV99Ir$B7B3O0WvNXw1DGLHSVtNcqPMOw4h298HTW2NMVgKDN4=',NULL,2,NULL,NULL,'2025-11-24 21:50:40','2025-11-24 21:50:40',1,NULL,3),(17,'Saul','Martinez','Geron','5435168874','saul@gmail.com','pbkdf2_sha256$1000000$ydTEvuwNoy6uHaHGBFqgak$7iULNlVR7JrsJDEzVllczD8D1MXRGYa8nKWO+gf/uWQ=',NULL,2,NULL,NULL,'2025-11-25 02:38:29','2025-11-25 02:38:29',1,NULL,3),(18,'Esther','Martinez','Martinez','1415132168','esthermtz@gmail.com','pbkdf2_sha256$1000000$Z8JYD0rmEqlfBYwI1FYt1z$R4FFt+/veFB/Q7LF0vlPUdeilRSly4XiSfYPTAtdvvo=',NULL,2,NULL,NULL,'2025-12-01 08:20:01','2025-12-01 08:20:01',1,NULL,3),(19,'Sofia','Martinez','Martinez','4455154814','chofi@gmail.com','pbkdf2_sha256$1000000$0b6vfCtslqS8nknFR7DKpR$RvZYpAGUKSuYFLNK5Db+F7dFzJcY6hkJ/rzK0oRU8A4=',NULL,1,'Si',NULL,'2025-12-06 19:38:40','2025-12-06 19:38:40',1,NULL,NULL),(20,'Chana','Perez','Perez','2236588974','chanaaa@gmail.com','pbkdf2_sha256$1000000$3bOtRqr96SadMIT3Rhaote$n0eylTkU8973QE3SXx5Xyi+ZZquETmM9wr/xqCqEoPk=',NULL,1,'No',NULL,'2025-12-06 23:24:26','2025-12-06 23:24:26',1,NULL,NULL),(21,'Laura','Gutierrez','Lopez','6687514848','laura@gmail.com','pbkdf2_sha256$1000000$bA5srFqHGMwzrtcDfCdvT5$vngD9Vp/5Nr6ceionsntQp1EWGmGKWHaekMAkp2WBKo=',NULL,1,'Si',NULL,'2025-12-07 00:37:34','2025-12-07 00:37:34',1,NULL,NULL),(22,'Juana','Galvan','Sanchez','2156156416','juana@gmail.com','pbkdf2_sha256$1000000$kU1lGswh5cLGz76nwfOQVZ$93k3vqNEQYgNm+O45GKRPgsFnZKpaGfZ+M2D8PAbBwg=',NULL,1,'No',NULL,'2025-12-07 07:33:08','2025-12-07 07:33:08',1,NULL,NULL),(23,'Petra','Gutierrez','Perez','2222155648','petra@gmail.com','pbkdf2_sha256$1000000$gYp3fsmESgbkH8hunjdqZn$/j4qPKcoFezfaji94BdzJMyKAK3cbKqpgnRjRCF9lzg=',NULL,1,'Si','Antojitos :)','2025-12-10 19:15:58','2025-12-10 19:15:58',1,'2025-12-10 19:15:58',NULL),(24,'Lety','Barradas','Perez','2135156494','lety@gmail.com','pbkdf2_sha256$1000000$W3QA2QHTxnUgGqfLulZiWC$vZb3gyI4Rk5Q8g/wZVhAtkrEiXrf5iR23azS++5gCXU=',NULL,3,NULL,NULL,'2025-12-10 00:38:20','2025-12-10 00:38:20',1,NULL,23),(25,'Fabian','Geron','Gonzales','2123145646','fabian@gmail.com','pbkdf2_sha256$1000000$INUbMHE0gohl2x7V93aNfU$SzCo3Fzv4xXZglKZbbkxseiMpY5ih53aqerJ0qFu5pc=',NULL,3,NULL,NULL,'2025-12-10 00:47:42','2025-12-10 00:47:42',1,NULL,4),(26,'Oscar','Marinez','Martinez','2452151564','oooscar@gmail.com','pbkdf2_sha256$1000000$lzlBe45tZS7G6V8yDjGiNd$lWTA5TLf+FX00QhekCHbWkBNr/day1k3rodbRtHwQYQ=',NULL,3,NULL,NULL,'2025-12-10 05:54:07','2025-12-10 05:54:07',1,'2025-12-10 05:54:07',23),(27,'Pancha','Rodriguez','Barradas','2154616178','panchaa@gmail.com','pbkdf2_sha256$1000000$pDAAiRAr1nDU7CSQqEHClz$r48WeFjRtxJOAPqNV2GlInvf6KofRKbeg828bcCCiwI=',NULL,2,NULL,NULL,'2025-12-10 06:05:06','2025-12-10 06:05:06',1,NULL,23),(28,'Maria','Geron','Tejeda','2541614948','mariateje@gmail.com','pbkdf2_sha256$1000000$y8zwqunELCVXRKCtdVZhgG$24rGsl41qrjRokACKY35QiQuvnSq9K7Gscle9IJViVQ=',NULL,1,'No',NULL,'2025-12-10 07:31:02','2025-12-10 07:31:02',1,NULL,NULL),(29,'Perla','Geron','Tejeda','5146818614','perlita@gmail.com','pbkdf2_sha256$1000000$GypZyRhHkaNQ0mOHNzCAof$HyvJOMvw3B6MCS26KWe9muW9481Wci9bRg6BMmvDLmw=',NULL,1,'No',NULL,'2025-12-10 16:51:24','2025-12-10 16:51:24',1,NULL,NULL),(30,'Ivana','Godinez','Perez','1146828419','Ivana@gmail.com','pbkdf2_sha256$1000000$rM8UaHL879x4s2L84gRmgV$hf+wGR5RaHpDKBsK9ryX+BD3NRFP8LRU5IxHe9qr4Bk=',NULL,2,NULL,NULL,'2025-12-10 17:04:14','2025-12-10 17:04:14',1,NULL,29),(31,'Mariana','Godinez','Godinez','1546861484','mariana123@gmail.com','pbkdf2_sha256$1000000$mHJx9HRWn489FM9ck5h3Yg$d29g2yUnqn8PlFFn8g6cNiQLJFHsqKBobwGuRJafwvg=',NULL,3,NULL,NULL,'2025-12-10 19:36:07','2025-12-10 19:36:07',1,NULL,23),(32,'Isaias','Salcedo','Mendoza','5284611654','salcedo@gmail.com','pbkdf2_sha256$1000000$BaPZIZUJjoO420ctv0zc9o$icb7LiGek60mFf8ES6Ymn8l8MS6dO36hOQeStYJDwi4=',NULL,1,'Si','Carnotas','2025-12-13 20:08:33','2025-12-13 20:08:33',1,NULL,NULL),(33,'Iris','Salcedo','Demanos','4864866415','iris@gmail.com','pbkdf2_sha256$1000000$veOUF8Psc3ZqiQlK33oRmk$SeXgRXuCoOXEguSdrJMxsfnE57l4UNsiB6vhFaKBPqA=',NULL,2,NULL,NULL,'2025-12-13 20:21:08','2025-12-13 20:21:08',1,NULL,32),(34,'Leo','San Juan','De la Cruz','6144197498','gabygaby@gmail.com','pbkdf2_sha256$1000000$cXQJuc0E815LKqWFfStDAr$wLkR6qx5Qjy+9nd/DELEZCmpv8fSlIwNOI0jyki41es=',NULL,3,NULL,NULL,'2025-12-14 00:56:18','2025-12-14 00:56:18',1,NULL,23),(35,'Juan','Martinez',NULL,NULL,'juanito@gmail.com','pbkdf2_sha256$1000000$zrs3UWvGnMXcQiMtD6wxY1$uRTtpkjMzswElJdQbpqWMm3bkmQ2Xb94zgUjxrTNipQ=',NULL,1,'No',NULL,'2025-12-14 06:17:54','2025-12-14 06:17:54',1,NULL,NULL),(36,'Isis','Salcedo','Demanos',NULL,'isissd@gmail.com','pbkdf2_sha256$1000000$JQ4spDjdB9rOwe0pfOYSBn$3AlMcKvod2QJlyqRuyTxhhUg7crqZrG3mHwLGV7CLh4=',NULL,1,'Si','Huellitas','2025-12-14 06:19:22','2025-12-14 06:19:22',1,NULL,NULL),(37,'Gloria','Martinez','Martinez','5249894199','gloriaesthermartinezmartinez@gmail.com','pbkdf2_sha256$1000000$jjbQtJgCAcvHBTmRJLOEbn$gNeJNjmzctmbOKUcmgKDrRuwKwscz4rgHm9upSoQxsg=',NULL,4,NULL,NULL,'2025-12-18 02:42:16','2026-01-29 08:36:50',1,'2026-01-27 03:31:29',NULL),(38,'Adriana','Ramos','Nava','5484615121','adriramos@gmail.com','pbkdf2_sha256$1000000$hyLbR2fYZWl3nN6pPrIgNl$SEjy8gIBEiut3L9YwsH6VeJWdJ3W9gA9w9A0CFITt38=',NULL,1,'No',NULL,'2025-12-19 18:58:02','2026-01-11 10:12:36',1,NULL,NULL),(39,'Rafael','Córdoba','Alonso','2281773518','work.rca@hotmail.com','pbkdf2_sha256$1000000$Mx1I99fKawTiI438eNd7Gs$sO++z7b9r7hT3x8oKXaFGnHBRZbPKk8N7xsE2UeXaAk=','COAR601120',1,'Si','RcaConsultoría','2026-01-08 18:11:30','2026-01-08 18:11:30',1,NULL,NULL),(40,'Abraham','mtz','mtz','2617617919','abraham@gmail.com','pbkdf2_sha256$1000000$PrJFxRb5E6xhqAzDAkN1B4$hWMymqZcMIsLoDBgShUuvPOmqWIklK1H3fK3J3wr22c=',NULL,3,NULL,NULL,'2026-01-08 18:37:51','2026-01-08 18:37:51',1,NULL,39),(42,'Lucia','Martinez',NULL,'5415146481','lucy@gmail.com','pbkdf2_sha256$1000000$xXzewqd1LqSES3yB9l4Qea$x4+cgMmS/PBZWVjmYJItWhJo5rK++3Ap6W9kqvCmbDQ=',NULL,2,NULL,NULL,'2026-01-09 18:49:59','2026-01-15 07:03:34',1,NULL,38),(44,'Alejandro','Mtz','Mtz','5456561954','ale12@gmail.com','pbkdf2_sha256$1000000$iOwD6Ozxh3jbAnAoLKmGux$qsj3la6cRhNfmpjWY52WARIS5DWsR4Trs2IOQ4fZDpA=',NULL,3,NULL,NULL,'2026-01-10 22:12:00','2026-01-10 22:12:00',1,NULL,38),(46,'Esther','Martinez','Geron','6241817968','esther123@gmail.com','pbkdf2_sha256$1000000$wmVG0Jd8z5mmm8nmJgl3Z1$lIPez7nOu/0qNXFeX0Q83bR8fVBIytv17mYjGPLaqtk=',NULL,3,NULL,NULL,'2026-01-10 22:25:42','2026-01-10 22:25:42',1,NULL,38),(48,'Esperanza','ramirez','ramirez','4475588418','esperanza@gmail.com','pbkdf2_sha256$1000000$7wAIy0nT5oa1ORHTy480eg$uGAX9Xrlg27cd9hki0jHlLSJQC4n5j7GwBV1SgF9GpE=',NULL,3,NULL,NULL,'2026-01-10 23:00:05','2026-01-11 07:18:00',0,'2026-01-11 07:18:00',38),(49,'Maria Angelica','Martinez',NULL,NULL,'mariaaaa123@gmail.com','pbkdf2_sha256$1000000$kJSmlJAdnTZrOuFdFLCDZw$CesFl4RZdRYbx7XsgzSImT6t2uXXyb97pXGW5lRcxco=',NULL,3,NULL,NULL,'2026-01-11 09:00:32','2026-01-11 09:43:48',1,NULL,38),(50,'Esther','Martinez','Martinez',NULL,'esthermartinez@gmail.com','pbkdf2_sha256$1000000$yI7rsRsof8M5uBMQyjqVUr$zPktrZBRgqyQFXzthtf8P7D+dxrqb5lvOERg1SCdOIE=',NULL,1,'No',NULL,'2026-01-17 04:00:26','2026-01-17 04:00:26',1,NULL,NULL),(51,'Marco','Diaz',NULL,NULL,'marco@gmail.com','pbkdf2_sha256$1000000$qGNRHHttcWcgsVCg6kSsl8$em9w/lHSVF4ZvL2DEmyoAOMY5PONzUFWRJAB5LXT1T4=',NULL,1,'Si',NULL,'2026-01-17 04:02:03','2026-01-17 04:02:03',1,NULL,NULL),(52,'Mariana','Sanchez',NULL,'1461489814','Marianna@gmail.com','pbkdf2_sha256$1000000$5yidpcvVUdhfdWNsU0D1Vw$gXqzXJJ0UdryMQSe1Cb/K4XLDCAwjZ6kwuIrsSIWD80=',NULL,1,'Si',NULL,'2026-01-19 02:01:04','2026-01-29 18:51:33',1,NULL,NULL),(53,'Saul','Martinez',NULL,NULL,'Saaaul@gmail.com','pbkdf2_sha256$1000000$TkbQyEE3G7KVk18NfPvegc$w2bzfidBHWIk7iBShh5OQUk72/U+df9nVQ21IZadMVI=',NULL,1,'Si',NULL,'2026-01-21 03:52:54','2026-01-21 03:52:54',1,NULL,NULL),(54,'Gerardo','Martinez','Arguello','5146186146','gerardo@gmail.com','pbkdf2_sha256$1000000$vlamH7TANfqb3YQhYf9xVG$68+sFtGRRx5t24tC9PGFttAdXUThj/RnLQVSnRYqurY=',NULL,3,NULL,NULL,'2026-01-28 07:16:22','2026-01-28 07:16:22',1,NULL,52),(55,'Gustavo','Arguello','Perez','2245478965','gustavo@gmail.com','pbkdf2_sha256$1000000$r7fXzAxJh58ATMKZ9FB26C$NvIVntIbwk4ufq5nBf9mf7dM11LXdSQ2m1vp136GIug=',NULL,2,NULL,NULL,'2026-01-29 07:30:25','2026-01-29 07:44:55',1,'2026-01-29 07:41:13',52),(56,'Marta','Gomez','Lopez','9827984614','Martita@gmail.com','pbkdf2_sha256$1000000$ZINSshsD4i23NZxrFVZ8na$7RfNkAr+S6QWYp/fEjMwCrHKAvZAeCYXDt0GcssMvc4=',NULL,2,NULL,NULL,'2026-01-29 07:32:28','2026-01-29 07:45:34',0,'2026-01-29 07:45:34',52),(57,'Ana','Martinez','Gonzales','1561569494','Anabanana@gmail.com','pbkdf2_sha256$1000000$T6QlVdIUfNlXuEwMVnCqaN$n7YF96CqE7PxVC9yCXj7O/Or41mZGk0GNB5W7Mo7NNQ=',NULL,3,NULL,NULL,'2026-01-29 07:42:29','2026-01-29 07:45:43',0,'2026-01-29 07:45:43',52),(58,'Javier','Martinez',NULL,'2224546144','javi@gmail.com','pbkdf2_sha256$1000000$yXkBtE5y54Gb9r0rAKfdxa$PSU/848vLhNJsbN8Qo9cWGVsj/RC1cTiB/cwyAYWmGc=',NULL,1,'No',NULL,'2026-01-29 07:51:01','2026-01-29 07:51:01',1,NULL,NULL),(59,'Juan','Pérez','López','5454564646','consultor_prueba@gmail.com','pbkdf2_sha256$1000000$xLF9WWqVVjVavgIgAScaqg$pumwJVi0P+BObIQBXH+b773KXJ8suj2QnlU9MhwgZJ4=',NULL,5,NULL,NULL,'2026-01-30 03:49:52','2026-01-30 19:32:07',1,NULL,NULL),(60,'Valeria','Martinez','Perez','8848484146','Valeeee@gmail.com','pbkdf2_sha256$1000000$s5bTSkPYjajd4GHFlEYgXT$DjYXynT2AgKd+nPJc8oLUvKilh/SUOln3N1cA8HUOZM=',NULL,2,NULL,NULL,'2026-01-31 04:08:49','2026-01-31 04:46:39',0,'2026-01-31 04:46:39',52),(61,'Gloria','Martinez',NULL,NULL,'gloria@gmail.com','pbkdf2_sha256$1000000$qSEMP4CX6PQYUyOguE9EWI$wcLYNKrphwlA8zvmupW6Synw8EKpLnDrEqG8PCfISEE=',NULL,1,'No',NULL,'2026-03-16 02:10:14','2026-03-16 02:10:14',1,NULL,NULL),(62,'Mariana','Godinez',NULL,NULL,'godinez@gmail.com','pbkdf2_sha256$1000000$vf1xbvOHtxFkiDRE6CK9Cp$ffynMCp9w5D8Sw85O5DZeGxxYACr7dZqlND/5eT1zFA=',NULL,1,'Si','Antojitos','2026-03-16 02:13:54','2026-03-16 02:13:54',1,NULL,NULL);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario_preferenciausuario`
--

DROP TABLE IF EXISTS `usuario_preferenciausuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario_preferenciausuario` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `color_primario` varchar(20) NOT NULL,
  `color_secundario` varchar(20) NOT NULL,
  `color_fondo` varchar(20) NOT NULL,
  `logo` varchar(100) DEFAULT NULL,
  `usuario_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `usuario_preferenciau_usuario_id_73e428e1_fk_usuario_i` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`idusuario`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario_preferenciausuario`
--

LOCK TABLES `usuario_preferenciausuario` WRITE;
/*!40000 ALTER TABLE `usuario_preferenciausuario` DISABLE KEYS */;
INSERT INTO `usuario_preferenciausuario` VALUES (1,'#0d6efd','#6c757d','#ffffff','',4),(2,'#000000','#000000','#f5ebeb','logos/1.jpg',3),(3,'#0d6efd','#6c757d','#ffffff','logos/segunda_prueba_de_logo.png',11),(4,'#0d6efd','#6c757d','#ffffff','logos/3.jpg',23),(5,'#0d6efd','#6c757d','#ffffff','',9),(6,'#0d6efd','#6c757d','#ffffff','',32),(7,'#0d6efd','#6c757d','#ffffff','',36),(8,'#0d6efd','#6c757d','#ffffff','logos/2.jpg',38),(9,'#0d6efd','#6c757d','#ffffff','logos/1_QKCfd8x.jpg',39),(10,'#0d6efd','#6c757d','#ffffff','',42),(11,'#0d6efd','#6c757d','#ffffff','logos/1_N14bnSC.jpg',50),(12,'#0d6efd','#6c757d','#ffffff','logos/Logo_ejemplo_negocio.png',52),(13,'#0d6efd','#6c757d','#ffffff','',53),(14,'#0d6efd','#6c757d','#ffffff','',37);
/*!40000 ALTER TABLE `usuario_preferenciausuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas`
--

DROP TABLE IF EXISTS `ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas` (
  `idventa` int NOT NULL AUTO_INCREMENT,
  `nombreventa` varchar(45) NOT NULL,
  `estatus_cobro` int NOT NULL,
  `preciototal` decimal(10,2) NOT NULL,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_modificacion` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  `fecha_eliminacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `cfdi` varchar(100) DEFAULT NULL,
  `comentarios` text,
  `oportunidad_venta` int DEFAULT NULL,
  `owner_id` int NOT NULL,
  `usuario_registro` int NOT NULL,
  PRIMARY KEY (`idventa`),
  UNIQUE KEY `cfdi_UNIQUE` (`cfdi`),
  KEY `fk_estatus_cobros_idx` (`estatus_cobro`),
  KEY `fk_oportunidad_idx` (`oportunidad_venta`),
  KEY `fk_ventas_negocio_idx` (`owner_id`),
  KEY `fk_venta_usuario` (`usuario_registro`),
  CONSTRAINT `fk_estatus_cobros` FOREIGN KEY (`estatus_cobro`) REFERENCES `estatus_cobros` (`idestatus_cobros`),
  CONSTRAINT `fk_oportunidad` FOREIGN KEY (`oportunidad_venta`) REFERENCES `oportunidades` (`idoportunidad`),
  CONSTRAINT `fk_venta_usuario` FOREIGN KEY (`usuario_registro`) REFERENCES `usuario` (`idusuario`),
  CONSTRAINT `fk_ventas_del_negocio` FOREIGN KEY (`owner_id`) REFERENCES `usuario` (`idusuario`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
INSERT INTO `ventas` VALUES (1,'Compra de Kilos de costilla',3,300.00,'2026-01-09 17:33:14','2026-01-09 17:33:14',0,'2026-01-09 17:33:14',NULL,'salio bien :D',2,3,3),(2,'Venta demo',1,100.00,'2026-01-09 17:33:14','2026-01-09 17:33:14',1,'2026-01-09 17:33:14',NULL,'esto es una prueba',41,3,3),(3,'Venta demo',1,100.00,'2026-01-09 17:33:14','2026-01-09 17:33:14',1,'2026-01-09 17:33:14',NULL,'esto es una prueba',41,3,3),(4,'Prueba final',3,10000.00,'2026-01-09 17:33:14','2026-01-09 17:33:14',1,'2026-01-09 17:33:14',NULL,'esto es prueba',36,3,3),(5,'Oportunidad ganada',3,250.00,'2026-01-09 17:34:13','2026-01-09 18:14:08',0,'2026-01-09 18:14:08',NULL,'',53,38,38),(6,'primera venta',3,18700.00,'2026-01-09 17:35:57','2026-01-09 17:35:57',1,'2026-01-09 17:35:57',NULL,'ok',54,39,39),(7,'prueba',3,500000.00,'2026-01-09 17:35:57','2026-01-09 17:35:57',1,'2026-01-09 17:35:57',NULL,'',28,39,39),(8,'Prueba',3,500.00,'2026-01-09 17:52:25','2026-01-09 17:52:25',1,NULL,NULL,'',55,38,38),(9,'Prueba 2',3,120.00,'2026-01-09 18:13:57','2026-01-09 18:44:06',1,NULL,NULL,'',56,38,38),(10,'Prueba empleado',3,200.00,'2026-01-09 18:58:28','2026-01-09 18:58:28',1,NULL,NULL,'',57,38,42),(11,'Prueba',3,100.00,'2026-01-10 05:46:54','2026-01-10 05:46:54',1,NULL,NULL,'',NULL,38,38),(12,'Prueba enero',3,450.00,'2026-01-18 22:46:06','2026-01-18 22:46:06',1,NULL,NULL,'',NULL,38,38),(13,'Prueba Enero 2',3,45.00,'2026-01-18 22:46:44','2026-01-19 00:44:16',1,NULL,NULL,'jandkandkand',NULL,38,38),(14,'Cables Ethernet',3,50.00,'2026-01-19 19:13:00','2026-01-19 19:31:40',0,'2026-01-19 19:31:40',NULL,'Me pago $30',NULL,52,52),(15,'Aire comprimido',3,85.00,'2026-01-19 19:36:11','2026-01-19 19:37:08',1,NULL,NULL,'',NULL,52,52),(16,'Prueba de fuego',3,800.00,'2026-01-25 08:56:57','2026-01-26 05:30:06',1,NULL,NULL,'',NULL,38,38),(17,'Mantenimiento a laptop asus',3,1500.00,'2026-01-28 07:19:02','2026-01-28 07:19:17',1,NULL,NULL,'prueba',NULL,52,54),(18,'Paquetes de rj45',3,500.00,'2026-01-28 07:50:02','2026-01-28 07:50:02',1,NULL,NULL,'prueba..',NULL,52,37),(19,'Cable ethernet cat5',2,100.00,'2026-01-28 07:50:53','2026-01-28 07:51:19',0,'2026-01-28 07:51:19',NULL,'',NULL,52,37),(20,'Cables Ethernet cat6',1,10.00,'2026-01-28 07:54:22','2026-01-31 07:31:21',1,NULL,NULL,'ok',NULL,52,37),(21,'Cable Ethernet cat5',3,10.00,'2026-01-31 00:47:27','2026-01-31 01:05:22',1,NULL,NULL,'prueba..',NULL,52,52);
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-15 23:11:37
