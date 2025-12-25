-- ============================================================================
-- JUFTBOR MATCHMAKING APP - PRODUCTION DATABASE SCHEMA
-- ============================================================================
-- This is a production-ready version with improvements:
-- 1. Proper telegram_id handling (immutable Telegram user ID)
-- 2. Essential performance indexes
-- 3. Additional validation constraints
-- 4. Better data integrity checks
-- ============================================================================

-- 1. Define Custom Types
CREATE TYPE gender_enum AS ENUM ('M', 'F');
CREATE TYPE marital_status_enum AS ENUM ('S', 'M', 'D', 'W');
CREATE TYPE contact_person_enum AS ENUM ('s', 'd', 'm', 'b', 'o');
CREATE TYPE activity_status_enum AS ENUM ('a', 'p', 'd');

-- 2. Main Users Table
CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "full_name" VARCHAR(255) NOT NULL,
  "birthdate" DATE NOT NULL, 
  "gender" gender_enum NOT NULL,
  "marital_status" marital_status_enum,
  "native_town" TEXT,
  "hometown" TEXT,
  "languages" TEXT[],
  "height" INT DEFAULT NULL,
  "weight" INT DEFAULT NULL,
  "biography" TEXT,
  "degree" SMALLINT DEFAULT NULL, -- 0-3 (0: no degree, 1: bachelor, 2: master, 3: doctorate)
  "field_of_study" TEXT DEFAULT NULL,
  "occupation" TEXT DEFAULT NULL,
  "religious_level" SMALLINT DEFAULT NULL, -- 0-3 (0: not religious, 3: very religious)
  "drinks" CHAR(1) DEFAULT NULL, -- 'n': never, 's': socially, 'y': yes
  "smokes" CHAR(1) DEFAULT NULL, -- 'n': never, 's': socially, 'y': yes
  "created_at" TIMESTAMPTZ DEFAULT NOW(),
  "reg_phone" VARCHAR(15) UNIQUE NOT NULL,
  "contact_person" contact_person_enum,
  "contact_phone" VARCHAR(15) DEFAULT NULL,
  "telegram_id" BIGINT UNIQUE DEFAULT NULL, -- Immutable Telegram user ID (from message.from_user.id)
  "telegram_username" TEXT DEFAULT NULL, -- Can change, use for display only (from message.from_user.username)
  "contact_comment" TEXT DEFAULT NULL,
  "is_active" activity_status_enum DEFAULT 'a',
  -- Ensure at least one contact method is provided
  CHECK (
    contact_phone IS NOT NULL
    OR telegram_id IS NOT NULL
  )
);

-- 3. Interactions (Interests)
CREATE TABLE "interests" (
  "id" SERIAL PRIMARY KEY,
  "sender_id" INTEGER REFERENCES "users"("id") ON DELETE CASCADE,
  "receiver_id" INTEGER REFERENCES "users"("id") ON DELETE CASCADE,
  "status" SMALLINT DEFAULT 0, -- 0: Pending, 1: Accepted, 2: Rejected
  "created_at" TIMESTAMPTZ DEFAULT NOW(),
  "responded_at" TIMESTAMPTZ,
  -- Ensure a user can't like the same person twice
  UNIQUE("sender_id", "receiver_id"),
  -- Prevent self-likes
  CHECK (sender_id != receiver_id)
);

-- 4. Metadata Table
CREATE TABLE "metadata" (
  "user_id" INTEGER PRIMARY KEY REFERENCES "users"("id") ON DELETE CASCADE,
  "registration_ip" INET, -- Postgres specific type for IP addresses
  "device" TEXT DEFAULT NULL, -- e.g., "iPhone 15 Pro"
  "bot_activated" BOOLEAN DEFAULT FALSE, -- Has user signed in via Telegram bot
  "last_active_at" TIMESTAMPTZ DEFAULT NOW(),
  "last_edited_at" TIMESTAMPTZ,
  "notify_matches" BOOLEAN DEFAULT TRUE,
  "is_banned" BOOLEAN DEFAULT FALSE,
  "ban_reason" TEXT,
  "ban_date" TIMESTAMPTZ
);

-- 5. Preferences Table
CREATE TABLE "preferences" (
  "user_id" INTEGER PRIMARY KEY REFERENCES "users"("id") ON DELETE CASCADE,
  "age_range" INT4RANGE DEFAULT '[18, 60]',
  "height_range" INT4RANGE DEFAULT '[140, 200]',
  "marital_status" marital_status_enum[] DEFAULT NULL, -- Users can pick multiple (e.g., S and D)
  "preferred_towns" TEXT[] DEFAULT NULL, -- Array of cities/regions
  "preferred_languages" TEXT[] DEFAULT NULL,
  "occupation_blacklist" TEXT[] DEFAULT NULL, -- Array of occupations to avoid
  "religious_level" SMALLINT[] DEFAULT NULL, -- Array of levels (0-3)
  "preferred_degree" SMALLINT[] DEFAULT NULL, -- Array of degrees (0-3)
  "updated_at" TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Reports Table
CREATE TABLE "reports" (
  "id" SERIAL PRIMARY KEY,
  "reporter_id" INTEGER REFERENCES "users"("id") ON DELETE SET NULL,
  "reported_id" INTEGER REFERENCES "users"("id") ON DELETE CASCADE,
  "category" VARCHAR(50) NOT NULL, -- e.g., 'scam', 'harassment', 'fake_profile'
  "description" TEXT,
  "status" activity_status_enum DEFAULT 'p', -- a: active, p: pending, d: dismissed
  "admin_notes" TEXT, -- For internal use only
  "created_at" TIMESTAMPTZ DEFAULT NOW(),
  "resolved_at" TIMESTAMPTZ
);

-- 7. Matches Table (when both users accept interest)
CREATE TABLE "matches" (
  "id" SERIAL PRIMARY KEY,
  "user1_id" INTEGER REFERENCES "users"("id") ON DELETE CASCADE,
  "user2_id" INTEGER REFERENCES "users"("id") ON DELETE CASCADE,
  "matched_at" TIMESTAMPTZ DEFAULT NOW(),
  "is_active" BOOLEAN DEFAULT TRUE, -- Can be set to false if users unmatch
  UNIQUE("user1_id", "user2_id"),
  -- Ensure consistent ordering (lower ID always first)
  CHECK (user1_id < user2_id)
);

-- 8. Photos Table
CREATE TABLE "photos" (
  "id" SERIAL PRIMARY KEY,
  "user_id" INTEGER REFERENCES "users"("id") ON DELETE CASCADE,
  "url" TEXT NOT NULL,
  "is_primary" BOOLEAN DEFAULT FALSE,
  "uploaded_at" TIMESTAMPTZ DEFAULT NOW(),
  "order" SMALLINT DEFAULT 0 -- For ordering multiple photos
);

-- ============================================================================
-- CONSTRAINTS
-- ============================================================================

-- Users table constraints
ALTER TABLE "users" 
ADD CONSTRAINT check_smokes_value 
CHECK (smokes IN ('n', 's', 'y'));

ALTER TABLE "users" 
ADD CONSTRAINT check_drinks_value 
CHECK (drinks IN ('n', 's', 'y'));

ALTER TABLE "users"
ADD CONSTRAINT check_degree_range 
CHECK (degree BETWEEN 0 AND 3);

ALTER TABLE "users"
ADD CONSTRAINT check_religious_level_range 
CHECK (religious_level BETWEEN 0 AND 3);

ALTER TABLE "users"
ADD CONSTRAINT check_height_reasonable 
CHECK (height IS NULL OR (height BETWEEN 100 AND 250));

ALTER TABLE "users"
ADD CONSTRAINT check_weight_reasonable 
CHECK (weight IS NULL OR (weight BETWEEN 30 AND 300));

-- Ensure birthdate is reasonable (18+ years old, not before 1940)
ALTER TABLE "users"
ADD CONSTRAINT check_birthdate_valid 
CHECK (
  birthdate >= '1940-01-01' 
  AND birthdate <= CURRENT_DATE - INTERVAL '18 years'
);

-- Preferences table constraints
ALTER TABLE "preferences"
ADD CONSTRAINT check_age_range_valid 
CHECK (lower(age_range) >= 18 AND upper(age_range) <= 100);

ALTER TABLE "preferences"
ADD CONSTRAINT check_height_range_valid 
CHECK (lower(height_range) >= 100 AND upper(height_range) <= 250);

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

-- Users table indexes (for matchmaking queries)
-- CREATE INDEX idx_users_gender ON "users"("gender");
-- CREATE INDEX idx_users_is_active ON "users"("is_active");
-- CREATE INDEX idx_users_gender_active ON "users"("gender", "is_active");
-- CREATE INDEX idx_users_birthdate ON "users"("birthdate"); -- For age-based filtering
-- CREATE INDEX idx_users_telegram_id ON "users"("telegram_id"); -- For bot authentication

-- -- Interests table indexes (for showing sent/received interests)
-- CREATE INDEX idx_interests_receiver_status ON "interests"("receiver_id", "status");
-- CREATE INDEX idx_interests_sender_status ON "interests"("sender_id", "status");
-- CREATE INDEX idx_interests_created_at ON "interests"("created_at"); -- For sorting by date

-- -- Metadata table indexes
-- CREATE INDEX idx_metadata_bot_activated ON "metadata"("bot_activated");
-- CREATE INDEX idx_metadata_last_active ON "metadata"("last_active_at");

-- -- Matches table indexes
-- CREATE INDEX idx_matches_user1_active ON "matches"("user1_id", "is_active");
-- CREATE INDEX idx_matches_user2_active ON "matches"("user2_id", "is_active");

-- -- Photos table indexes
-- CREATE INDEX idx_photos_user_id ON "photos"("user_id");
-- CREATE INDEX idx_photos_user_primary ON "photos"("user_id", "is_primary");

-- -- Reports table indexes
-- CREATE INDEX idx_reports_reported_id ON "reports"("reported_id");
-- CREATE INDEX idx_reports_status ON "reports"("status");

-- ============================================================================
-- HELPER FUNCTIONS (Optional but useful)
-- ============================================================================

-- Function to calculate age from birthdate
CREATE OR REPLACE FUNCTION calculate_age(birthdate DATE) 
RETURNS INTEGER AS $$
BEGIN
  RETURN EXTRACT(YEAR FROM AGE(birthdate));
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function to check if two users match each other (both expressed interest)
CREATE OR REPLACE FUNCTION check_mutual_interest(user1_id INTEGER, user2_id INTEGER)
RETURNS BOOLEAN AS $$
DECLARE
  interest1 INTEGER;
  interest2 INTEGER;
BEGIN
  -- Check if user1 accepted interest from user2
  SELECT status INTO interest1 
  FROM interests 
  WHERE sender_id = user2_id AND receiver_id = user1_id AND status = 1;
  
  -- Check if user2 accepted interest from user1
  SELECT status INTO interest2 
  FROM interests 
  WHERE sender_id = user1_id AND receiver_id = user2_id AND status = 1;
  
  RETURN (interest1 IS NOT NULL AND interest2 IS NOT NULL);
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- VIEWS FOR COMMON QUERIES (Optional but recommended)
-- ============================================================================

-- View for active users with their age
CREATE VIEW active_users_with_age AS
SELECT 
  u.*,
  calculate_age(u.birthdate) as age,
  m.bot_activated,
  m.last_active_at
FROM users u
LEFT JOIN metadata m ON u.id = m.user_id
WHERE u.is_active = 'a' AND (m.is_banned IS NULL OR m.is_banned = FALSE);

-- View for pending interests (useful for notifications)
CREATE VIEW pending_interests AS
SELECT 
  i.*,
  sender.full_name as sender_name,
  receiver.full_name as receiver_name
FROM interests i
JOIN users sender ON i.sender_id = sender.id
JOIN users receiver ON i.receiver_id = receiver.id
WHERE i.status = 0;

-- ============================================================================
-- COMMENTS FOR DOCUMENTATION
-- ============================================================================

COMMENT ON TABLE users IS 'Main user profiles with personal and professional information';
COMMENT ON TABLE interests IS 'Tracks when users express interest in each other';
COMMENT ON TABLE matches IS 'Created when both users accept each other (mutual interest)';
COMMENT ON TABLE metadata IS 'User metadata including bot activation, IP, device, and ban status';
COMMENT ON TABLE preferences IS 'User matchmaking preferences';
COMMENT ON TABLE reports IS 'User reports for moderation';
COMMENT ON TABLE photos IS 'User profile photos';

COMMENT ON COLUMN users.telegram_id IS 'Immutable Telegram user ID from message.from_user.id';
COMMENT ON COLUMN users.telegram_username IS 'Display only - can change. From message.from_user.username';
COMMENT ON COLUMN users.is_active IS 'a: active, p: paused, d: deactivated';
COMMENT ON COLUMN interests.status IS '0: Pending, 1: Accepted, 2: Rejected';
