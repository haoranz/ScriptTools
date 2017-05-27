/*
Date: 2017-05-27 17:18:55
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for msmq_logs
-- ----------------------------
DROP TABLE IF EXISTS `msmq_logs`;
CREATE TABLE `msmq_logs` (
  `ms_id` int(255) NOT NULL AUTO_INCREMENT,
  `ms_time` datetime DEFAULT NULL,
  `ms_content` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ms_id`)
) ENGINE=MyISAM AUTO_INCREMENT=403 DEFAULT CHARSET=utf8;
