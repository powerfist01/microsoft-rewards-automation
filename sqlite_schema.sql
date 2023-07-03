CREATE TABLE `logs` (
  `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  `email` VARCHAR(255),
  'run_date' DATE NOT NULL DEFAULT (strftime('%Y-%m-%d', 'now', 'localtime')),
  `search_count` INTEGER,
  `created_at` TIMESTAMP NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
  `updated_at` TIMESTAMP NOT NULL DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
  UNIQUE (`email`, `run_date`) ON CONFLICT REPLACE
);

CREATE TRIGGER `triggerUpdatedAt` AFTER UPDATE ON `logs`
BEGIN
   update `logs` SET `updated_at` = (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')) WHERE id = NEW.id;
END;