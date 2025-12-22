-- Postgres compatible data seeding
-- Note: DDL (Create Table) is handled by SQLAlchemy in init_db.py. We only do inserts here.

-- Insert Sample User
INSERT INTO users (username, password_hash) VALUES ('testuser', '$argon2id$v=19$m=65536,t=3,p=4$Dn9/wWl/dE7p...$hash...')
ON CONFLICT (username) DO NOTHING;

-- Clear old metrics/goals for testuser (id=1) 
-- Note: In Postgres with Serial/Identity, IDs might not match 1 if we deleted rows. 
-- Ideally we look up by username.
DELETE FROM health_metrics WHERE user_id = (SELECT id FROM users WHERE username = 'testuser');
DELETE FROM goals WHERE user_id = (SELECT id FROM users WHERE username = 'testuser');

-- Insert Sample Goal (10,000 steps daily)
INSERT INTO goals (user_id, metric_type, target_value) 
SELECT id, 'steps', 10000 FROM users WHERE username = 'testuser';

-- Insert Sample Health Records for testuser
-- We use a subquery to get the correct user_id
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-04', 5000, 1800.5, 75 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-05', 5500, 1900.0, 78 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-06', 6000, 2100.2, 80 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-07', 7000, 2200.5, 85 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-08', 4000, 1600.0, 72 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-09', 8000, 2500.0, 90 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-10', 9000, 2700.5, 95 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-11', 3000, 1500.0, 70 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-12', 5200, 1850.0, 76 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-13', 6500, 2000.0, 82 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-14', 7200, 2250.0, 86 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-15', 4500, 1700.0, 73 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-16', 8500, 2600.0, 92 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-17', 9200, 2800.0, 96 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-18', 3500, 1600.0, 71 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-19', 5800, 1950.0, 79 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-20', 6200, 2150.0, 81 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-21', 7500, 2300.0, 87 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-22', 4200, 1750.0, 74 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-23', 8200, 2550.0, 91 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-24', 9500, 2900.0, 98 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-25', 3200, 1550.0, 70 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-26', 5300, 1880.0, 77 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-27', 6800, 2100.0, 84 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-28', 7300, 2400.0, 88 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-29', 4800, 1800.0, 75 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-11-30', 8800, 2700.0, 94 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-01', 9700, 2950.0, 99 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-02', 3800, 1650.0, 72 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-03', 5900, 2000.0, 80 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-04', 6300, 2200.0, 82 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-05', 7600, 2350.0, 89 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-06', 4300, 1850.0, 74 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-07', 8300, 2600.0, 93 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-08', 9600, 3000.0, 100 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-09', 3300, 1580.0, 70 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-10', 5400, 1900.0, 78 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-11', 6900, 2180.0, 85 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-12', 7400, 2450.0, 90 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-13', 4900, 1850.0, 76 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-14', 8900, 2750.0, 95 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-15', 9800, 3050.0, 101 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-16', 3900, 1700.0, 73 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-17', 6100, 2050.0, 81 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-18', 6400, 2220.0, 83 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-19', 7700, 2380.0, 90 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-20', 4400, 1900.0, 75 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-21', 8400, 2650.0, 94 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-22', 9700, 3100.0, 102 FROM users WHERE username = 'testuser';
INSERT INTO health_metrics (user_id, date, steps, calories, heart_rate) SELECT id, '2025-12-23', 3400, 1600.0, 71 FROM users WHERE username = 'testuser';
