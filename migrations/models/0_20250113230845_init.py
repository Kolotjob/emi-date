from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `users` (
    `user_id` BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `uid_code` VARCHAR(50) NOT NULL UNIQUE,
    `status_block` VARCHAR(255) NOT NULL  DEFAULT 'Active',
    `name` VARCHAR(50),
    `age` INT,
    `orientation` VARCHAR(255),
    `gender` VARCHAR(10),
    `medias` JSON,
    `about` LONGTEXT,
    `location` VARCHAR(255),
    `preferences` VARCHAR(255),
    `hobbies` JSON,
    `for_whom` VARCHAR(255),
    `subscription` VARCHAR(50) NOT NULL  DEFAULT 'Free',
    `localstatus` VARCHAR(50) NOT NULL  DEFAULT 'active',
    `subscription_start` DATETIME(6),
    `subscription_end` DATETIME(6),
    `referral_uid` VARCHAR(50)  UNIQUE,
    `balance` DECIMAL(10,2) NOT NULL  DEFAULT 0,
    `level` DECIMAL(5,2) NOT NULL  DEFAULT 0,
    `date_registered` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `lang` VARCHAR(50) NOT NULL UNIQUE DEFAULT 'nochoise'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `blocks` (
    `block_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `can_message` BOOL NOT NULL  DEFAULT 0,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `from_user_id` BIGINT NOT NULL,
    `to_user_id` BIGINT NOT NULL,
    CONSTRAINT `fk_blocks_users_f69e9486` FOREIGN KEY (`from_user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_blocks_users_041aac48` FOREIGN KEY (`to_user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `likes` (
    `like_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `is_superlike` BOOL NOT NULL  DEFAULT 0,
    `message` LONGTEXT,
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `from_user_id` BIGINT NOT NULL,
    `to_user_id` BIGINT NOT NULL,
    CONSTRAINT `fk_likes_users_0e2e7347` FOREIGN KEY (`from_user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
    CONSTRAINT `fk_likes_users_5172e914` FOREIGN KEY (`to_user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `statements` (
    `statement_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `referral_count` INT NOT NULL  DEFAULT 0,
    `subscription_level` VARCHAR(20) NOT NULL  DEFAULT 'basic',
    `price` DECIMAL(10,2) NOT NULL  DEFAULT 0,
    `referral_percentage` DECIMAL(5,2) NOT NULL  DEFAULT 0,
    `payment_method` VARCHAR(50),
    `transaction_id` VARCHAR(255),
    `status` VARCHAR(20) NOT NULL  DEFAULT 'pending',
    `created_at` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `user_id` BIGINT NOT NULL,
    CONSTRAINT `fk_statemen_users_32a21656` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
