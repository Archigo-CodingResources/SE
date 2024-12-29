-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-12-29 05:08:52
-- 伺服器版本： 10.4.32-MariaDB
-- PHP 版本： 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `final_se`
--

-- --------------------------------------------------------

--
-- 資料表結構 `account`
--

CREATE TABLE `account` (
  `id` int(255) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `pwd` varchar(100) NOT NULL,
  `address` varchar(20) NOT NULL,
  `summary` int(11) NOT NULL DEFAULT 0,
  `role` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `account`
--

INSERT INTO `account` (`id`, `name`, `email`, `pwd`, `address`, `summary`, `role`) VALUES
(12, 'admin', 'admin@admin', 'admin', 'admin', 0, -1),
(13, '客戶1', 'c1@c1', '123', 'c1', 105, 2),
(14, '吃雞雞餐廳', 'r1@r1', '123', 'r1', 105, 0),
(15, '外送1', 'de@de', '123', 'de', 1, 1),
(17, 'ccc', 'ccc@ccc', '123', 'ccc', 0, 2),
(18, 'ccccc', 'ccccc@ccccc', '123', '123', 0, 0);

-- --------------------------------------------------------

--
-- 資料表結構 `cart`
--

CREATE TABLE `cart` (
  `id` int(11) NOT NULL,
  `food_id` int(11) NOT NULL,
  `cid` int(11) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `comment`
--

CREATE TABLE `comment` (
  `com_id` int(11) NOT NULL,
  `rating` int(10) NOT NULL,
  `content` varchar(100) NOT NULL,
  `rid` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `comment`
--

INSERT INTO `comment` (`com_id`, `rating`, `content`, `rid`) VALUES
(27, 5, '雞雞好好吃', 14),
(28, 4, '123', 14);

-- --------------------------------------------------------

--
-- 資料表結構 `food`
--

CREATE TABLE `food` (
  `food_id` int(255) NOT NULL,
  `name` varchar(100) NOT NULL,
  `price` int(255) NOT NULL,
  `description` varchar(100) NOT NULL,
  `rid` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `food`
--

INSERT INTO `food` (`food_id`, `name`, `price`, `description`, `rid`) VALUES
(29, 'a雞雞', 10, 'a腿', 14),
(30, 'b機', 15, '2313', 14);

-- --------------------------------------------------------

--
-- 資料表結構 `the_order`
--

CREATE TABLE `the_order` (
  `oid` int(11) NOT NULL,
  `rid` int(11) NOT NULL,
  `food_id` int(11) NOT NULL,
  `cid` int(11) NOT NULL,
  `did` int(11) DEFAULT NULL,
  `quantity` int(11) NOT NULL,
  `address` varchar(20) NOT NULL,
  `time` datetime DEFAULT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- 傾印資料表的資料 `the_order`
--

INSERT INTO `the_order` (`oid`, `rid`, `food_id`, `cid`, `did`, `quantity`, `address`, `time`, `status`) VALUES
(39, 14, 29, 13, 15, 3, 'c1', '2024-12-27 21:00:02', 3),
(40, 14, 30, 13, 15, 5, 'c1', '2024-12-27 21:00:02', 3);

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `account`
--
ALTER TABLE `account`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `comment`
--
ALTER TABLE `comment`
  ADD PRIMARY KEY (`com_id`);

--
-- 資料表索引 `food`
--
ALTER TABLE `food`
  ADD PRIMARY KEY (`food_id`);

--
-- 資料表索引 `the_order`
--
ALTER TABLE `the_order`
  ADD PRIMARY KEY (`oid`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `account`
--
ALTER TABLE `account`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `cart`
--
ALTER TABLE `cart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `comment`
--
ALTER TABLE `comment`
  MODIFY `com_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `food`
--
ALTER TABLE `food`
  MODIFY `food_id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `the_order`
--
ALTER TABLE `the_order`
  MODIFY `oid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
