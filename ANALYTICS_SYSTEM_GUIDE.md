# 📊 PageForge - User Analytics & Traffic Monitoring System

## Overview
A comprehensive analytics system that tracks user accounts, password security, and website traffic - far beyond the basic customer database.

## 🆕 New Features

### 1. **User Database Analytics**
- **Total Accounts**: Track all registered users
- **Registration Trends**: Daily/weekly/monthly signup patterns
- **User Types**: Customer vs Admin distribution
- **Account Security**: Password strength analysis
- **User Activity**: Login patterns and engagement

### 2. **Password Security Monitoring**
- **Strength Analysis**: Weak/Medium/Strong password distribution
- **Security Recommendations**: Identify users with weak passwords
- **Compliance Tracking**: Monitor password policy adherence
- **Security Audits**: Regular password strength assessments

### 3. **Website Traffic Analytics**
- **Page Views**: Track all page visits with timestamps
- **Unique Visitors**: Daily/weekly/monthly visitor counts
- **Popular Pages**: Most visited sections of your site
- **Bounce Rate**: User engagement metrics
- **Session Duration**: How long users spend on site
- **Traffic Sources**: Where visitors come from

### 4. **User Activity Tracking**
- **Real-time Activity**: Who's online now
- **Action Logging**: Track user actions (login, purchases, browsing)
- **Engagement Metrics**: User interaction patterns
- **Behavior Analysis**: Understanding user preferences

## 🚀 Setup Instructions

### Step 1: Setup Analytics Database
```bash
python setup_analytics_database.py
```
This creates all necessary tables and populates them with sample data.

### Step 2: Access Analytics Dashboard
1. Start your server: `python app.py`
2. Login as admin: `admin` / `PageForge@Admin2024!`
3. Navigate to: `http://127.0.0.1:5000/admin/analytics`

### Step 3: Explore Analytics Features
- **Account Overview**: Registration trends and user distribution
- **Password Security**: Security compliance and recommendations
- **Website Traffic**: Page views and visitor analytics
- **User Activity**: Real-time activity and engagement

## 📈 Analytics Dashboard Features

### Account Overview Tab
- **Registration Chart**: Visual trend of new signups
- **User Type Distribution**: Pie chart of customers vs admins
- **Recent Registrations**: Table of newest users
- **Growth Metrics**: Month-over-month comparisons

### Password Security Tab
- **Security Distribution**: Strong/Medium/Weak password counts
- **Security Recommendations**: Action items for improving security
- **Compliance Metrics**: Percentage of secure passwords
- **Risk Assessment**: Users who need password updates

### Website Traffic Tab
- **Daily Metrics**: Unique visitors, page views, bounce rate
- **Traffic Chart**: Visual representation of site traffic over time
- **Popular Pages**: Most visited pages with view counts
- **Performance Indicators**: Session duration and engagement

### User Activity Tab
- **Online Users**: Who's currently active
- **Activity Timeline**: Recent user actions
- **Engagement Stats**: 24h/weekly/monthly active users
- **Behavior Patterns**: User interaction insights

## 🔧 Database Tables Created

### 1. `user_sessions`
Tracks user login sessions and activity periods
```sql
- session_id: Unique session identifier
- user_id: Foreign key to Users table
- ip_address: User's IP address
- start_time: When session began
- last_activity: Most recent activity
- is_active: Session status
```

### 2. `page_views`
Records every page visit for traffic analysis
```sql
- session_id: Links to user session
- page_url: URL visited
- page_title: Page title
- timestamp: When page was viewed
- load_time_ms: Page load performance
```

### 3. `user_activities`
Logs all user actions for behavior analysis
```sql
- user_id: Who performed the action
- activity_type: Type of action (login, purchase, etc.)
- activity_description: Detailed description
- timestamp: When action occurred
- metadata: Additional context (JSON)
```

### 4. `password_security_audit`
Analyzes password strength for security compliance
```sql
- user_id: User being audited
- password_strength: weak/medium/strong
- has_uppercase/lowercase/numbers/symbols: Complexity flags
- password_length: Character count
- last_updated: When audit was performed
```

### 5. `analytics_summary`
Daily rollup of key metrics for trend analysis
```sql
- date: Summary date
- unique_visitors: Daily unique visitor count
- total_page_views: Total page views
- new_registrations: New signups
- bounce_rate: Engagement metric
- avg_session_duration: Session length
```

### 6. `popular_pages`
Tracks most visited pages and content performance
```sql
- page_url: Page URL
- page_title: Page title
- view_count: Total views
- unique_visitors: Unique visitor count
- last_viewed: Most recent visit
```

## 📊 Key Metrics Tracked

### User Metrics
- Total registered accounts
- Daily/weekly/monthly new signups
- Customer vs Admin distribution
- Account creation trends
- User engagement levels

### Security Metrics
- Password strength distribution
- Security compliance percentage
- Users with weak passwords
- Security recommendation alerts
- Password policy adherence

### Traffic Metrics
- Daily unique visitors
- Total page views
- Most popular pages
- Bounce rate analysis
- Average session duration
- Traffic growth trends

### Activity Metrics
- Users currently online
- Recent user actions
- Activity timeline
- Engagement patterns
- Feature usage statistics

## 🔍 Advanced Features

### Real-time Monitoring
- Live user activity feed
- Current online user count
- Real-time page view tracking
- Instant security alerts

### Trend Analysis
- Registration growth charts
- Traffic pattern visualization
- User engagement trends
- Security compliance tracking

### Exportable Reports
- User database exports
- Analytics data downloads
- Security audit reports
- Traffic analysis summaries

### Security Insights
- Password strength recommendations
- Risk user identification
- Security policy compliance
- Vulnerability assessments

## 🎯 Business Intelligence

### User Growth
- Track registration trends
- Identify growth patterns
- Monitor user acquisition
- Analyze signup sources

### Content Performance
- Most popular pages
- Content engagement metrics
- User journey analysis
- Feature usage statistics

### Security Compliance
- Password policy adherence
- Risk user identification
- Security recommendation system
- Compliance reporting

### Traffic Analysis
- Visitor behavior patterns
- Peak usage times
- Geographic insights (if IP analysis added)
- Conversion funnel analysis

## 🛠️ Customization Options

### Adding New Metrics
- Extend user_activities table for new action types
- Add custom analytics summary fields
- Create specialized tracking tables
- Implement custom dashboard widgets

### Enhanced Security Tracking
- Add 2FA usage tracking
- Monitor failed login attempts
- Track suspicious activities
- Implement security scoring

### Advanced Traffic Analysis
- Add referrer tracking
- Implement conversion tracking
- Monitor A/B test results
- Track marketing campaign performance

---

**This analytics system provides comprehensive insights into your user base, security posture, and website performance - making it a powerful tool for business intelligence and security monitoring.**

**Developer**: Mahender Banoth (IIT Patna)  
**Project**: PageForge Digital Bookstore Analytics System
