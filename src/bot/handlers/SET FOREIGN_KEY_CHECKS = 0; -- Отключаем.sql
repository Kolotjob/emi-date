SET FOREIGN_KEY_CHECKS = 0; -- Отключаем проверку внешних ключей

DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `likes`;
DROP TABLE IF EXISTS `blocks`;
DROP TABLE IF EXISTS `statements`;
DROP TABLE IF EXISTS `aerich`; -- Если используется Aerich

SET FOREIGN_KEY_CHECKS = 1