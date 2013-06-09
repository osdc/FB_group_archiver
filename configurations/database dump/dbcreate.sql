-- phpMyAdmin SQL Dump
-- version 3.3.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Sep 20, 2012 at 07:47 PM
-- Server version: 5.1.63
-- PHP Version: 5.3.5-1ubuntu7.11

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `ssngeek_cg`
--

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
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=1089 ;

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

--Functions

--To insert Links
delimiter //
create function InsertLink(url text, title text, description text, post_id varchar(100)) returns int 
begin 
	insert into links(url, title, post_id, description) values (url, title, post_id, description); return 0; 
end//
delimiter ;

--To insert posts
delimiter //
CREATE FUNCTION InsertPost(author_name VARCHAR(100), author_id TEXT, message TEXT, likes_count INT(11), comments_count INT(11), created_on TIMESTAMP ,updated_on TIMESTAMP,id VARCHAR(100)) RETURNS INT 
BEGIN 
	DECLARE affected_rows INT; 
	INSERT INTO posts (author_name, author_id, message, likes_count, comments_count, id) VALUES (author_name, author_id, message, likes_count, comments_count, id) ON DUPLICATE KEY UPDATE likes_count = likes_count, comments_count = comments_count; 
	SELECT ROW_COUNT() INTO affected_rows; 
	RETURN affected_rows; 
END//
delimiter ;
