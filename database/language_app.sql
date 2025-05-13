-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 28, 2025 at 01:31 AM
-- Server version: 5.7.14
-- PHP Version: 5.6.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `language_app`
--

-- --------------------------------------------------------

--
-- Table structure for table `expected_texts`
--

CREATE TABLE `expected_texts` (
  `id` int(11) NOT NULL,
  `text` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `phonetic` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `difficulty` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `expected_texts`
--

INSERT INTO `expected_texts` (`id`, `text`, `phonetic`, `difficulty`) VALUES
(1, 'The quick brown fox jumps over the lazy dog', 'ðə kwɪk braʊn fɑːks ʤʌmps ˈoʊvər ðə ˈleɪzi dɔːɡ', 'medium'),
(2, 'She sells seashells by the seashore', 'ʃiː sɛlz ˈsiːʃɛlz baɪ ðə ˈsiːʃɔːr', 'medium'),
(3, 'How can a clam cram in a clean cream can?', 'haʊ kæn ə klæm kræm ɪn ə kliːn kriːm kæn', 'medium');

-- --------------------------------------------------------

--
-- Table structure for table `feedback`
--

CREATE TABLE `feedback` (
  `id` int(11) NOT NULL,
  `name` varchar(190) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `subject` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `message` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `feedback`
--

INSERT INTO `feedback` (`id`, `name`, `email`, `subject`, `message`, `created_at`) VALUES
(1, 'Abobakr', 'engabobakrh@gmail.com', 'aa', 'aa', '2025-04-13 03:04:28'),
(2, 'Abobakr', 'engabobakrh@gmail.com', 'aa', 'aa', '2025-04-13 03:37:35');

-- --------------------------------------------------------

--
-- Table structure for table `progress`
--

CREATE TABLE `progress` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `word` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `accuracy` float NOT NULL,
  `timestamp` datetime DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `email` varchar(190) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `email`, `password`, `created_at`) VALUES
(1, 'engabobakrh@gmail.com', 'scrypt:32768:8:1$49Da4YD74f1uxOeY$73d346fba693226b235dfbe89d2857c4187c83fe1a888e5d236b38256450970b7a0b818aa9f374d13428a229d4ff13300fe1090951fcb8ecf5d7c6f1f123151b', '2025-04-13 02:40:04'),
(2, 'aa@gmail.com', 'scrypt:32768:8:1$yn6iu8pR6NHS0kNL$96210d99e5b99302ffcf3a63a723d7ffcd5d2afbd1e6a0591bb984c5550d5005e86a46337193e067d9d6ac086c0eb22f9c3942dd8339935d9b857baa075f39f8', '2025-04-26 18:53:05');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `expected_texts`
--
ALTER TABLE `expected_texts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `progress`
--
ALTER TABLE `progress`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `expected_texts`
--
ALTER TABLE `expected_texts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `feedback`
--
ALTER TABLE `feedback`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `progress`
--
ALTER TABLE `progress`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
