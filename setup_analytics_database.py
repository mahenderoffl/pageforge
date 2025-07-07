#!/usr/bin/env python3
"""
PageForge - Database Analytics Setup
Creates tables for tracking user analytics and website traffic
"""

from app import get_connection
import mysql.connector

def create_analytics_tables():
    """Create tables for user analytics and traffic tracking"""
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        print("📊 Creating Analytics Database Tables...")
        
        # 1. User Sessions Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_sessions (
                session_id VARCHAR(255) PRIMARY KEY,
                user_id INT,
                ip_address VARCHAR(45),
                user_agent TEXT,
                start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                INDEX(user_id),
                INDEX(start_time),
                FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE SET NULL
            )
        """)
        print("✅ Created user_sessions table")
        
        # 2. Page Views Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS page_views (
                id INT AUTO_INCREMENT PRIMARY KEY,
                session_id VARCHAR(255),
                user_id INT,
                page_url VARCHAR(500),
                page_title VARCHAR(255),
                referrer VARCHAR(500),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                load_time_ms INT,
                INDEX(session_id),
                INDEX(user_id),
                INDEX(page_url),
                INDEX(timestamp),
                FOREIGN KEY (session_id) REFERENCES user_sessions(session_id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE SET NULL
            )
        """)
        print("✅ Created page_views table")
        
        # 3. User Activities Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_activities (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                activity_type VARCHAR(100),
                activity_description TEXT,
                metadata JSON,
                ip_address VARCHAR(45),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX(user_id),
                INDEX(activity_type),
                INDEX(timestamp),
                FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
            )
        """)
        print("✅ Created user_activities table")
        
        # 4. Password Security Audit Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS password_security_audit (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT UNIQUE,
                password_strength ENUM('weak', 'medium', 'strong') DEFAULT 'medium',
                has_uppercase BOOLEAN DEFAULT FALSE,
                has_lowercase BOOLEAN DEFAULT FALSE,
                has_numbers BOOLEAN DEFAULT FALSE,
                has_symbols BOOLEAN DEFAULT FALSE,
                password_length INT DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX(user_id),
                INDEX(password_strength),
                FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
            )
        """)
        print("✅ Created password_security_audit table")
        
        # 5. Website Analytics Summary Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analytics_summary (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date DATE UNIQUE,
                unique_visitors INT DEFAULT 0,
                total_page_views INT DEFAULT 0,
                new_registrations INT DEFAULT 0,
                new_orders INT DEFAULT 0,
                bounce_rate DECIMAL(5,2) DEFAULT 0,
                avg_session_duration INT DEFAULT 0,
                top_page VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX(date)
            )
        """)
        print("✅ Created analytics_summary table")
        
        # 6. Popular Pages Tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS popular_pages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                page_url VARCHAR(500),
                page_title VARCHAR(255),
                view_count INT DEFAULT 1,
                unique_visitors INT DEFAULT 1,
                last_viewed TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                UNIQUE KEY unique_page (page_url),
                INDEX(view_count),
                INDEX(last_viewed)
            )
        """)
        print("✅ Created popular_pages table")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n🎉 Analytics database setup completed successfully!")
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Error creating analytics tables: {e}")
        return False

def populate_sample_analytics_data():
    """Populate tables with sample analytics data"""
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        print("\n📈 Populating Sample Analytics Data...")
        
        # Get existing users
        cursor.execute("SELECT id, username FROM Users LIMIT 5")
        users = cursor.fetchall()
        
        if not users:
            print("⚠️  No users found. Please run database_setup.py first.")
            return False
        
        # Sample password security data
        from datetime import datetime, timedelta
        import random
        
        for user in users:
            user_id = user[0]
            
            # Random password strength
            strength = random.choice(['weak', 'medium', 'strong'])
            has_upper = strength != 'weak'
            has_lower = True
            has_numbers = strength in ['medium', 'strong']
            has_symbols = strength == 'strong'
            length = random.randint(6, 16) if strength == 'weak' else random.randint(8, 20)
            
            cursor.execute("""
                INSERT INTO password_security_audit 
                (user_id, password_strength, has_uppercase, has_lowercase, has_numbers, has_symbols, password_length)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                password_strength = VALUES(password_strength),
                has_uppercase = VALUES(has_uppercase),
                has_lowercase = VALUES(has_lowercase),
                has_numbers = VALUES(has_numbers),
                has_symbols = VALUES(has_symbols),
                password_length = VALUES(password_length)
            """, (user_id, strength, has_upper, has_lower, has_numbers, has_symbols, length))
        
        print("✅ Added password security audit data")
        
        # Sample popular pages
        popular_pages_data = [
            ('/', 'Home - PageForge Digital Bookstore', 1250, 890),
            ('/browse', 'Browse All Books', 890, 650),
            ('/login', 'Login - PageForge', 650, 420),
            ('/register', 'Register - PageForge', 420, 380),
            ('/cart', 'Shopping Cart', 350, 280),
            ('/browse/Fiction', 'Fiction Books', 300, 220),
            ('/browse/Science Fiction', 'Science Fiction Books', 280, 200),
            ('/bestsellers', 'Bestselling Books', 220, 180),
            ('/new-arrivals', 'New Arrivals', 200, 160),
            ('/free-books', 'Free Books', 150, 120),
        ]
        
        for page_data in popular_pages_data:
            cursor.execute("""
                INSERT INTO popular_pages (page_url, page_title, view_count, unique_visitors)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                view_count = VALUES(view_count),
                unique_visitors = VALUES(unique_visitors)
            """, page_data)
        
        print("✅ Added popular pages data")
        
        # Sample analytics summary for last 30 days
        for i in range(30):
            date = (datetime.now() - timedelta(days=i)).date()
            unique_visitors = random.randint(50, 200)
            page_views = random.randint(unique_visitors, unique_visitors * 4)
            new_registrations = random.randint(0, 8)
            new_orders = random.randint(0, 15)
            bounce_rate = round(random.uniform(20.0, 60.0), 2)
            avg_session = random.randint(120, 600)  # seconds
            
            cursor.execute("""
                INSERT INTO analytics_summary 
                (date, unique_visitors, total_page_views, new_registrations, new_orders, bounce_rate, avg_session_duration, top_page)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                unique_visitors = VALUES(unique_visitors),
                total_page_views = VALUES(total_page_views),
                new_registrations = VALUES(new_registrations),
                new_orders = VALUES(new_orders),
                bounce_rate = VALUES(bounce_rate),
                avg_session_duration = VALUES(avg_session_duration)
            """, (date, unique_visitors, page_views, new_registrations, new_orders, bounce_rate, avg_session, '/'))
        
        print("✅ Added 30 days of analytics summary data")
        
        # Sample user activities
        activities = [
            ('login', 'User logged in'),
            ('logout', 'User logged out'),
            ('book_view', 'Viewed book details'),
            ('cart_add', 'Added book to cart'),
            ('cart_remove', 'Removed book from cart'),
            ('order_place', 'Placed an order'),
            ('profile_update', 'Updated profile information'),
            ('password_change', 'Changed password'),
            ('browse_category', 'Browsed book category'),
            ('search', 'Searched for books'),
        ]
        
        for user in users:
            user_id = user[0]
            # Add 5-15 random activities per user
            for _ in range(random.randint(5, 15)):
                activity = random.choice(activities)
                timestamp = datetime.now() - timedelta(
                    days=random.randint(0, 7),
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59)
                )
                
                cursor.execute("""
                    INSERT INTO user_activities 
                    (user_id, activity_type, activity_description, ip_address, timestamp)
                    VALUES (%s, %s, %s, %s, %s)
                """, (user_id, activity[0], activity[1], '127.0.0.1', timestamp))
        
        print("✅ Added user activity data")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n🎉 Sample analytics data populated successfully!")
        return True
        
    except mysql.connector.Error as e:
        print(f"❌ Error populating sample data: {e}")
        return False

def show_analytics_summary():
    """Display a summary of the analytics data"""
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        print("\n📊 ANALYTICS DATABASE SUMMARY")
        print("="*50)
        
        # User statistics
        cursor.execute("SELECT COUNT(*) as total FROM Users")
        total_users = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as count FROM password_security_audit WHERE password_strength = 'strong'")
        strong_passwords = cursor.fetchone()['count']
        
        cursor.execute("SELECT COUNT(*) as count FROM password_security_audit WHERE password_strength = 'weak'")
        weak_passwords = cursor.fetchone()['count']
        
        print(f"👥 Total Users: {total_users}")
        print(f"🔒 Strong Passwords: {strong_passwords}")
        print(f"⚠️  Weak Passwords: {weak_passwords}")
        
        # Popular pages
        cursor.execute("SELECT * FROM popular_pages ORDER BY view_count DESC LIMIT 5")
        popular = cursor.fetchall()
        
        print("\n🔥 Top 5 Popular Pages:")
        for i, page in enumerate(popular, 1):
            print(f"   {i}. {page['page_title']}: {page['view_count']} views")
        
        # Recent activity
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM user_activities 
            WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
        """)
        recent_activities = cursor.fetchone()['count']
        
        print(f"\n⚡ Activities (Last 24h): {recent_activities}")
        
        # Analytics summary
        cursor.execute("""
            SELECT SUM(unique_visitors) as total_visitors, 
                   SUM(total_page_views) as total_views,
                   SUM(new_registrations) as total_registrations
            FROM analytics_summary 
            WHERE date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
        """)
        weekly_stats = cursor.fetchone()
        
        print("\n📈 Last 7 Days:")
        print(f"   Unique Visitors: {weekly_stats['total_visitors'] or 0}")
        print(f"   Page Views: {weekly_stats['total_views'] or 0}")
        print(f"   New Registrations: {weekly_stats['total_registrations'] or 0}")
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*50)
        print("🌐 Access analytics at: http://127.0.0.1:5000/admin/analytics")
        
    except mysql.connector.Error as e:
        print(f"❌ Error showing summary: {e}")

if __name__ == "__main__":
    print("🚀 PageForge Analytics Database Setup")
    print("="*50)
    
    # Create tables
    if create_analytics_tables():
        # Populate with sample data
        if populate_sample_analytics_data():
            # Show summary
            show_analytics_summary()
        else:
            print("❌ Failed to populate sample data")
    else:
        print("❌ Failed to create analytics tables")
