-- phpMyAdmin SQL Dump
-- version 3.4.10.1deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 14, 2013 at 03:47 PM
-- Server version: 5.5.29
-- PHP Version: 5.3.10-1ubuntu3.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `FB`
--

DELIMITER $$
--
-- Functions
--
CREATE DEFINER=`root`@`localhost` FUNCTION `InsertLink`(url text, title text, description text, post_id varchar(100)) RETURNS int(11)
begin 
	insert into links(url, title, post_id, description) values (url, title, post_id, description); return 0; 
end$$

CREATE DEFINER=`root`@`localhost` FUNCTION `InsertPost`(author_name VARCHAR(100), author_id TEXT, message TEXT, likes_count INT(11), comments_count INT(11), created_on TIMESTAMP ,updated_on TIMESTAMP,id VARCHAR(100)) RETURNS int(11)
BEGIN 
	DECLARE affected_rows INT; 
	INSERT INTO posts (author_name, author_id, message, likes_count, comments_count, id) VALUES (author_name, author_id, message, likes_count, comments_count, id) ON DUPLICATE KEY UPDATE likes_count = likes_count, comments_count = comments_count; 
	SELECT ROW_COUNT() INTO affected_rows; 
	RETURN affected_rows; 
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `links`
--

CREATE TABLE IF NOT EXISTS `links` (
  `url` text NOT NULL,
  `title` text NOT NULL,
  `post_id` varchar(100) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1094 ;

-- --------------------------------------------------------

--
-- Table structure for table `posts`
--

CREATE TABLE IF NOT EXISTS `posts` (
  `author_name` varchar(100) NOT NULL,
  `author_id` text NOT NULL,
  `message` text NOT NULL,
  `likes_count` int(11) DEFAULT NULL,
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `comments_count` int(11) DEFAULT NULL,
  `id` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
