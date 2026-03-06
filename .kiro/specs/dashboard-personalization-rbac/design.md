# Design Document: Dashboard Personalization and RBAC

## Overview

This design document specifies the implementation of role-based access control (RBAC) enhancements and personalized dashboard features for the Ashoka GenAI Governance Dashboard. The system will track user feature usage, display personalized recent features, filter alerts by user context, and provide admin-specific aggregated metrics while maintaining strict access controls based on user roles (admin, creator, viewer).

### Key Features

1. **Universal Content Intelligence Access**: All user roles can access Content Intelligence features
2. **Transform Feature Access Control**: Transform features restricted to admin and creator roles with visual lock indicators for viewers
3. **Feature Usage Tracking**: Automatic tracking of feature access events for all users
4. **Personalized Recent Features**: Display of 3 most recently used features in Overview and Profile
5. **User-Specific Alert Filtering**: Alerts filtered to show only user-relevant information
6. **Admin Aggregated Metrics**: System-wide metrics and user breakdown for admin users
7. **Database Schema Extensions**: New tables for feature usage history and user preferences

### Technology Stack

- **Frontend**: NiceGUI (Python-based web framework)
- **Database**: DuckDB (for feature usage history and user preferences)
- **Authentication**: Existing auth_service with role-based permissions
- **Monitoring**: Existing monitoring_service extended with user-specific filtering

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Dashboard UI Layer                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Overview │  │ Content  │  │Transform │  │Monitoring│   │
│  │  Panel   │  │   Intel  │  │  Panel   │  │  Panel   │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
└───────┼─────────────┼─────────────┼─────────────┼──────────┘
        │             │             │             │
        ▼             ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│                   Service Layer                              │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ Access Control   │  │ Feature Usage    │                │
│  │    Manager       │  │    Tracker       │                │
│  └────────┬─────────┘  └────────┬─────────┘                │
│           │                     │                           │
│  ┌────────┴─────────┐  ┌────────┴─────────┐                │
│  │  Alert Filter    │  │ Metrics          │                │
│  │                  │  │ Aggregator       │                │
│  └──────────────────┘  └──────────────────┘                │
└─────────────────────────────────────────────────────────────┘
        │                                   │
        ▼                                   ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Layer (DuckDB)                        │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ feature_usage_   │  │ user_preferences │                │
│  │    history       │  │                  │                │
│  └──────────────────┘  └──────────────────┘                │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │ ashoka_contentint│  │ transform_history│                │
│  └──────────────────┘  └──────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```


### Data Flow

#### Feature Access Tracking Flow

```
User navigates to feature
        │
        ▼
Dashboard renders panel
        │
        ▼
Feature Usage Tracker triggered
        │
        ├─> Generate usage_id
        ├─> Capture user_id from session
        ├─> Capture feature_name
        ├─> Capture timestamp
        │
        ▼
Persist to feature_usage_history table
        │
        ▼
Update Recent Features display (if on Overview)
```

#### Alert Filtering Flow

```
User views Alerts panel
        │
        ▼
Alert Filter queries alerts
        │
        ├─> Filter by user_id
        ├─> Include Content Intelligence alerts
        ├─> Include Transform alerts
        ├─> Include Quality alerts
        ├─> Include Rate Limit alerts
        │
        ▼
Apply personalized labels
        │
        ▼
Display filtered alerts to user
```

#### Admin Metrics Aggregation Flow

```
Admin views Monitoring panel
        │
        ▼
Check user role = admin
        │
        ├─> Yes: Aggregate all users
        │   ├─> Query all ashoka_contentint records
        │   ├─> Query all transform_history records
        │   ├─> Query all feature_usage_history records
        │   ├─> Compute aggregated metrics
        │   └─> Display user breakdown table
        │
        └─> No: Filter to current user only
            └─> Display only user's metrics
```

## Components and Interfaces

### 1. Access Control Manager

**Purpose**: Enforce role-based permissions for feature access

**Location**: `src/services/access_control_service.py` (new file)

**Interface**:
```python
class AccessControlService:
    def can_access_feature(self, user_id: str, feature_name: str) -> bool
    def get_user_role(self, user_id: str) -> str
    def get_accessible_features(self, user_id: str) -> List[str]
    def is_feature_locked(self, user_id: str, feature_name: str) -> bool
```

**Key Methods**:

- `can_access_feature(user_id, feature_name)`: Returns True if user can access the feature
  - Content Intelligence: Always returns True (all roles)
  - Transform: Returns True only for admin and creator roles
  - Monitoring, Alerts, Security: Role-specific logic

- `get_user_role(user_id)`: Retrieves user role from auth_service
  - Returns: "admin", "creator", or "viewer"

- `get_accessible_features(user_id)`: Returns list of features user can access
  - Used for UI rendering decisions

- `is_feature_locked(user_id, feature_name)`: Returns True if feature should show lock icon
  - Used for Transform tab lock icon display

### 2. Feature Usage Tracker

**Purpose**: Track and record feature access events

**Location**: `src/services/feature_usage_tracker.py` (new file)

**Interface**:
```python
class FeatureUsageTracker:
    def track_feature_access(self, user_id: str, feature_name: str) -> str
    def get_recent_features(self, user_id: str, limit: int = 3) -> List[Dict]
    def get_usage_count(self, user_id: str, feature_name: str) -> int
    def get_last_accessed(self, user_id: str, feature_name: str) -> Optional[datetime]
    def should_track_event(self, user_id: str, feature_name: str) -> bool
```

**Key Methods**:

- `track_feature_access(user_id, feature_name)`: Records a feature access event
  - Generates unique usage_id
  - Stores user_id, feature_name, accessed_at timestamp
  - Returns usage_id

- `get_recent_features(user_id, limit)`: Retrieves most recent features for user
  - Queries feature_usage_history table
  - Orders by accessed_at DESC
  - Returns list with feature_name, last_accessed, usage_count

- `get_usage_count(user_id, feature_name)`: Counts total accesses for a feature
  - Aggregates from feature_usage_history table

- `should_track_event(user_id, feature_name)`: Determines if event should be tracked
  - Prevents duplicate tracking on data refresh within same feature
  - Uses session-based tracking to detect navigation vs refresh


### 3. Alert Filter

**Purpose**: Filter alerts to show only user-relevant information

**Location**: `src/services/alert_filter_service.py` (new file)

**Interface**:
```python
class AlertFilterService:
    def get_user_alerts(self, user_id: str) -> List[Dict]
    def get_personalized_labels(self, user_role: str) -> Dict[str, str]
    def filter_content_intelligence_alerts(self, user_id: str) -> List[Dict]
    def filter_transform_alerts(self, user_id: str) -> List[Dict]
    def filter_quality_alerts(self, user_id: str) -> List[Dict]
    def filter_rate_limit_alerts(self, user_id: str) -> List[Dict]
```

**Key Methods**:

- `get_user_alerts(user_id)`: Returns all alerts for a specific user
  - Combines alerts from multiple sources
  - Filters by user_id in alert metadata
  - Returns unified alert list

- `get_personalized_labels(user_role)`: Returns label mappings for UI
  - For non-admin: "Your Content Quality Score", "Your Recent Analyses"
  - For admin: "System-Wide Alerts"

- `filter_*_alerts(user_id)`: Source-specific alert filtering
  - Queries respective tables (ashoka_contentint, transform_history, etc.)
  - Filters by user_id
  - Transforms to alert format

### 4. Metrics Aggregator

**Purpose**: Compute aggregated metrics for admin users

**Location**: Extension to `src/services/monitoring_service.py`

**Interface**:
```python
class MonitoringService:
    # Existing methods...
    
    # New methods for RBAC:
    def get_aggregated_metrics(self, user_id: str) -> Dict
    def get_user_metrics_breakdown(self) -> List[Dict]
    def get_filtered_metrics(self, user_id: str, filter_user_id: Optional[str]) -> Dict
    def compute_user_statistics(self, user_id: str) -> Dict
```

**Key Methods**:

- `get_aggregated_metrics(user_id)`: Returns metrics based on user role
  - If admin: Aggregates across all users
  - If creator/viewer: Returns only user's metrics

- `get_user_metrics_breakdown()`: Returns per-user metrics table (admin only)
  - Columns: Username, Total Analyses, Total Transformations, Avg Quality Score, Last Active
  - Queries ashoka_contentint and transform_history tables
  - Joins with ashoka_users for username

- `get_filtered_metrics(user_id, filter_user_id)`: Returns metrics for specific user
  - Used when admin selects a user from dropdown
  - If filter_user_id is None: Returns aggregated metrics
  - If filter_user_id is set: Returns that user's metrics

- `compute_user_statistics(user_id)`: Computes statistics for a single user
  - Total analyses count
  - Total transformations count
  - Average quality score
  - Last active timestamp

### 5. Recent Features Panel Component

**Purpose**: Display user's 3 most recently used features

**Location**: `src/ui/dashboard.py` (modification to _create_overview_panel)

**UI Structure**:
```
┌─────────────────────────────────────────┐
│  Recent Features                        │
│  ┌─────────────────────────────────┐   │
│  │ 📊 Content Intelligence         │   │
│  │ Last used: 5 minutes ago        │   │
│  │ Usage count: 23                 │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │ 🔄 Transform                    │   │
│  │ Last used: 1 hour ago           │   │
│  │ Usage count: 12                 │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │ 📈 Monitoring                   │   │
│  │ Last used: 3 hours ago          │   │
│  │ Usage count: 8                  │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

**Behavior**:
- Queries feature_usage_tracker.get_recent_features(user_id, limit=3)
- Displays feature icon, name, relative timestamp, usage count
- Each card is clickable and navigates to the feature
- Shows "Start using features to see your recent activity" if no usage history

### 6. Profile Settings Recent Features

**Purpose**: Display feature usage history in user profile

**Location**: `src/ui/dashboard.py` (modification to _show_profile_dialog)

**UI Structure**:
```
┌─────────────────────────────────────────┐
│  User Profile                           │
│  ┌─────────────────────────────────┐   │
│  │ Username: john_doe              │   │
│  │ Email: john@example.com         │   │
│  │ Role: Creator                   │   │
│  └─────────────────────────────────┘   │
│                                         │
│  Recent Features                        │
│  ┌─────────────────────────────────┐   │
│  │ Content Intelligence            │   │
│  │ Last used: 2024-03-15 14:30:00  │   │
│  │ Total uses: 23                  │   │
│  └─────────────────────────────────┘   │
│  ┌─────────────────────────────────┐   │
│  │ Transform                       │   │
│  │ Last used: 2024-03-15 13:15:00  │   │
│  │ Total uses: 12                  │   │
│  └─────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

**Behavior**:
- Displays absolute timestamps (not relative)
- Shows same 3 most recent features
- Non-interactive (no navigation on click)


### 7. Transform Feature Lock UI

**Purpose**: Visual indicator for viewers that Transform is restricted

**Location**: `src/ui/dashboard.py` (modification to tab creation)

**UI Structure for Viewer**:
```
┌─────────────────────────────────────────┐
│  Tabs:                                  │
│  [Overview] [Content Intelligence]      │
│  [🔒 Transform] [Monitoring] [Alerts]   │
│         ↑                               │
│    Lock icon with tooltip               │
│    Reduced opacity (0.5)                │
└─────────────────────────────────────────┘
```

**Behavior**:
- Lock icon appears only for viewers
- Tooltip displays "You don't have access" on hover (< 200ms)
- Tab has reduced opacity (0.5) to indicate disabled state
- Click shows notification: "Access denied: Transform feature requires admin or creator role"
- Navigation is prevented

**UI Structure for Admin/Creator**:
```
┌─────────────────────────────────────────┐
│  Tabs:                                  │
│  [Overview] [Content Intelligence]      │
│  [Transform] [Monitoring] [Alerts]      │
│       ↑                                 │
│  No lock icon, full opacity             │
└─────────────────────────────────────────┘
```

### 8. Admin User Metrics Breakdown

**Purpose**: Display per-user metrics table for admin users

**Location**: `src/ui/dashboard.py` (modification to _create_monitoring_panel)

**UI Structure**:
```
┌─────────────────────────────────────────────────────────────┐
│  Monitoring Panel (Admin View)                              │
│                                                              │
│  User Filter: [All Users ▼]  [Reset Filter]                │
│                                                              │
│  User Metrics Breakdown                                     │
│  ┌────────────────────────────────────────────────────────┐ │
│  │ Username ↕ │ Analyses ↕ │ Transforms ↕ │ Quality ↕ │   │ │
│  ├────────────┼────────────┼──────────────┼───────────┤   │ │
│  │ john_doe   │ 145        │ 67           │ 87.5      │   │ │
│  │ jane_smith │ 203        │ 89           │ 92.3      │   │ │
│  │ bob_wilson │ 78         │ 34           │ 85.1      │   │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
│  Aggregated Metrics                                         │
│  Total Analyses: 426  Total Transforms: 190                 │
└─────────────────────────────────────────────────────────────┘
```

**Behavior**:
- Only visible to admin users
- Table is sortable by all columns
- Clicking username filters all metrics to that user
- Reset Filter button returns to aggregated view
- User dropdown allows selecting specific user

### 9. Personalized Alert Labels

**Purpose**: Customize alert labels based on user context

**Location**: `src/ui/dashboard.py` (modification to _create_alerts_panel)

**Label Mappings**:

For Non-Admin Users:
- "Content Quality Score" → "Your Content Quality Score"
- "Recent Analyses" → "Your Recent Analyses"
- "Transformations" → "Your Transformations"
- "API Usage" → "Your API Usage"

For Admin Users:
- Panel header: "System-Wide Alerts"
- Labels remain generic when viewing aggregated data
- Labels personalize when filtering to specific user

## Data Models

### Feature Usage History Table

**Table Name**: `feature_usage_history`

**Schema**:
```sql
CREATE TABLE feature_usage_history (
    usage_id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    feature_name VARCHAR NOT NULL,
    accessed_at TIMESTAMP NOT NULL
);

CREATE INDEX idx_feature_usage_user_time 
ON feature_usage_history(user_id, accessed_at DESC);

CREATE INDEX idx_feature_usage_feature_time 
ON feature_usage_history(feature_name, accessed_at DESC);
```

**Columns**:
- `usage_id`: Unique identifier for each access event (UUID format)
- `user_id`: Foreign key to ashoka_users.user_id
- `feature_name`: Name of the accessed feature (e.g., "Content Intelligence", "Transform")
- `accessed_at`: Timestamp when feature was accessed

**Indexes**:
- `(user_id, accessed_at)`: Optimizes queries for user's recent features
- `(feature_name, accessed_at)`: Optimizes analytics queries by feature

**Sample Data**:
```
usage_id                              | user_id        | feature_name           | accessed_at
--------------------------------------|----------------|------------------------|-------------------
550e8400-e29b-41d4-a716-446655440000 | user_john_doe  | Content Intelligence   | 2024-03-15 14:30:00
550e8400-e29b-41d4-a716-446655440001 | user_john_doe  | Transform              | 2024-03-15 13:15:00
550e8400-e29b-41d4-a716-446655440002 | user_jane_smith| Monitoring             | 2024-03-15 12:45:00
```

### User Preferences Table

**Table Name**: `user_preferences`

**Schema**:
```sql
CREATE TABLE user_preferences (
    user_id VARCHAR PRIMARY KEY,
    preferences_json JSON NOT NULL,
    updated_at TIMESTAMP NOT NULL
);
```

**Columns**:
- `user_id`: Foreign key to ashoka_users.user_id (primary key)
- `preferences_json`: JSON object storing flexible preference data
- `updated_at`: Timestamp of last preference update

**Preferences JSON Structure**:
```json
{
    "theme": "light",
    "language": "English",
    "notifications": true,
    "auto_save": true,
    "email_alerts": false,
    "session_timeout": 30,
    "dashboard_layout": {
        "overview_widgets": ["recent_features", "system_health", "recent_activity"]
    }
}
```

**Default Preferences** (initialized on user creation):
```json
{
    "theme": "light",
    "language": "English",
    "notifications": true,
    "auto_save": true,
    "email_alerts": false,
    "session_timeout": 30
}
```


### Extended Alert Metadata

**Modification to Alert Generation**:

All alerts generated by the system must include `user_id` in their metadata for filtering purposes.

**Alert Sources and User Association**:

1. **Content Intelligence Alerts**:
   - Source: `ashoka_contentint` table
   - User ID: From `ashoka_contentint.user_id`
   - Alert types: Quality issues, sentiment warnings, policy violations

2. **Transform Alerts**:
   - Source: `transform_history` table
   - User ID: From `transform_history.user_id`
   - Alert types: Transformation failures, format issues

3. **Quality Alerts**:
   - Source: `quality_metrics` table (joined with `ashoka_contentint`)
   - User ID: From content owner's `user_id`
   - Alert types: Readability below threshold, tone inconsistency

4. **Rate Limit Alerts**:
   - Source: `youtube_rate_limits` table
   - User ID: From `youtube_rate_limits.user_id`
   - Alert types: API quota warnings, rate limit exceeded

**Alert Metadata Structure**:
```python
{
    "alert_id": "alert_uuid",
    "user_id": "user_john_doe",  # Required for filtering
    "alert_type": "quality_warning",
    "source": "content_intelligence",
    "source_id": "content_uuid",
    "severity": "medium",
    "message": "Content quality score below threshold",
    "timestamp": "2024-03-15T14:30:00Z",
    "metadata": {
        "quality_score": 65.5,
        "threshold": 70.0
    }
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property Reflection

After analyzing all acceptance criteria, I identified the following areas of potential redundancy:

1. **Feature Access Event Properties (3.1-3.5)**: These can be combined into a single comprehensive property about event structure
2. **Recent Features Display Properties (4.5-4.8, 5.4-5.6)**: Similar display requirements can be consolidated
3. **Alert Filtering Properties (6.2-6.5)**: Multiple source-specific filters can be combined into one comprehensive property
4. **Metrics Aggregation Properties (7.3-7.6)**: Can be combined into a single property about aggregation completeness
5. **Schema Properties (8.1-8.6, 9.1-9.3)**: These are examples, not properties, and will be tested as unit tests

After reflection, I've consolidated redundant properties and ensured each property provides unique validation value.

### Property 1: Universal Content Intelligence Access

*For any* user regardless of role (admin, creator, or viewer), the access control manager should grant access to the Content Intelligence feature.

**Validates: Requirements 1.1**

### Property 2: Transform Access Control by Role

*For any* user, the access control manager should grant access to the Transform feature if and only if the user's role is "admin" or "creator".

**Validates: Requirements 2.1**

### Property 3: Feature Access Event Structure

*For any* feature access event recorded by the feature usage tracker, the event should contain a valid usage_id, user_id, feature_name, and accessed_at timestamp, and should be persisted to the feature_usage_history table.

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5**

### Property 4: Recent Features Ordering and Limiting

*For any* user with feature access history, querying recent features should return at most 3 features ordered by accessed_at timestamp in descending order.

**Validates: Requirements 4.2, 5.3**

### Property 5: Recent Features Display Completeness

*For any* feature displayed in the recent features panel, the display should include the feature name, feature icon, last used timestamp, and usage count.

**Validates: Requirements 4.5, 4.6, 4.7, 4.8, 5.4, 5.5, 5.6**

### Property 6: User-Specific Alert Filtering

*For any* user viewing the alerts panel, all displayed alerts should have a user_id in their metadata that matches the current user's user_id, and no alerts from other users should be displayed.

**Validates: Requirements 6.1, 6.6**

### Property 7: Alert Source Inclusion

*For any* user, the alert filter should include alerts from all relevant sources (Content Intelligence, Transform, Quality, Rate Limits) where the user_id matches the current user.

**Validates: Requirements 6.2, 6.3, 6.4, 6.5**

### Property 8: Admin Metrics Aggregation Completeness

*For any* admin user viewing the monitoring panel, the aggregated metrics should include data from all users in the system, including the admin's own data.

**Validates: Requirements 7.1, 7.2, 7.3, 7.4, 7.5, 7.6**

### Property 9: Non-Admin Metrics Isolation

*For any* user with role "creator" or "viewer", the monitoring panel should display only metrics where the user_id matches the current user's user_id.

**Validates: Requirements 7.10**

### Property 10: Admin User Filter Behavior

*For any* admin user who selects a specific user from the filter dropdown, all displayed metrics should be filtered to show only that selected user's data.

**Validates: Requirements 7.8**

### Property 11: Default Preferences Initialization

*For any* newly created user account, the system should automatically create a user_preferences record with default preference values.

**Validates: Requirements 9.4**

### Property 12: Feature Access Event Deduplication

*For any* user refreshing data within the same feature (without navigating away), the feature usage tracker should not generate a duplicate feature access event.

**Validates: Requirements 10.6, 10.7**

### Property 13: Usage Count Accuracy

*For any* user and feature combination, the displayed usage count should equal the total number of feature access events in the feature_usage_history table for that user_id and feature_name.

**Validates: Requirements 14.1, 14.3**

### Property 14: Usage Count Real-Time Update

*For any* user, when a new feature access event is recorded, the usage count displayed in the UI should update to reflect the new count immediately.

**Validates: Requirements 14.2**

### Property 15: Alert User Association

*For any* alert generated by the system, the alert should have a user_id in its metadata that corresponds to the user_id from the source table (ashoka_contentint, transform_history, quality_metrics, or youtube_rate_limits).

**Validates: Requirements 15.1, 15.2, 15.3, 15.4, 15.5**


## Error Handling

### Access Control Errors

**Scenario**: User attempts to access restricted feature
- **Detection**: Access control manager checks user role before rendering
- **Response**: Display lock icon and tooltip for viewers
- **User Feedback**: Notification message "Access denied: Transform feature requires admin or creator role"
- **Logging**: Log access attempt with user_id, feature_name, and denial reason

**Scenario**: User role cannot be determined
- **Detection**: auth_service.get_user_role() returns None
- **Response**: Default to most restrictive role (viewer)
- **User Feedback**: Display warning "Unable to verify permissions, limited access granted"
- **Logging**: Log error with user_id and session details

### Feature Usage Tracking Errors

**Scenario**: Database write failure when recording feature access
- **Detection**: Exception during feature_usage_tracker.track_feature_access()
- **Response**: Log error but allow user to continue using feature
- **User Feedback**: No user-facing error (silent failure for non-critical feature)
- **Logging**: Log error with user_id, feature_name, and exception details
- **Recovery**: Retry on next feature access

**Scenario**: Duplicate event detection fails
- **Detection**: Multiple events recorded for same feature access
- **Response**: Cleanup duplicate events in background task
- **User Feedback**: None (handled transparently)
- **Logging**: Log duplicate detection and cleanup

### Alert Filtering Errors

**Scenario**: Alert metadata missing user_id
- **Detection**: Alert object lacks user_id field
- **Response**: Exclude alert from user-specific views, include in admin aggregated view
- **User Feedback**: None (alert simply not displayed)
- **Logging**: Log warning with alert_id and source

**Scenario**: Database query failure when fetching alerts
- **Detection**: Exception during alert_filter_service.get_user_alerts()
- **Response**: Display cached alerts if available, otherwise show empty state
- **User Feedback**: "Unable to load alerts. Please refresh the page."
- **Logging**: Log error with user_id and exception details

### Metrics Aggregation Errors

**Scenario**: Incomplete data for user metrics breakdown
- **Detection**: User exists but has no activity records
- **Response**: Display user in table with zero values
- **User Feedback**: None (zeros are valid)
- **Logging**: None (expected scenario)

**Scenario**: Database query timeout for large aggregations
- **Detection**: Query exceeds timeout threshold (30 seconds)
- **Response**: Display partial results with warning
- **User Feedback**: "Metrics may be incomplete due to high system load"
- **Logging**: Log timeout with query details
- **Recovery**: Implement query pagination or caching

### UI Rendering Errors

**Scenario**: Recent features panel fails to render
- **Detection**: Exception during panel creation
- **Response**: Display error message in panel area
- **User Feedback**: "Unable to load recent features. Please try again later."
- **Logging**: Log error with user_id and exception details
- **Recovery**: Provide refresh button

**Scenario**: Lock icon fails to display for viewer
- **Detection**: Icon resource not found or CSS not applied
- **Response**: Display text-based indicator "[LOCKED]"
- **User Feedback**: Tooltip still shows "You don't have access"
- **Logging**: Log UI rendering error

### Data Consistency Errors

**Scenario**: User preferences not found for existing user
- **Detection**: Query returns None for user_id
- **Response**: Create default preferences immediately
- **User Feedback**: None (handled transparently)
- **Logging**: Log preference initialization

**Scenario**: Feature usage count mismatch
- **Detection**: Displayed count doesn't match database count
- **Response**: Recalculate count from database
- **User Feedback**: None (corrected automatically)
- **Logging**: Log mismatch with user_id, feature_name, displayed count, actual count

## Testing Strategy

### Dual Testing Approach

This feature requires both unit tests and property-based tests for comprehensive coverage:

- **Unit Tests**: Verify specific examples, edge cases, UI components, and database schema
- **Property Tests**: Verify universal properties across all inputs using randomized testing

Both testing approaches are complementary and necessary. Unit tests catch concrete bugs in specific scenarios, while property tests verify general correctness across a wide range of inputs.

### Property-Based Testing

**Framework**: Use `hypothesis` library for Python property-based testing

**Configuration**:
- Minimum 100 iterations per property test (due to randomization)
- Each property test must reference its design document property
- Tag format: `# Feature: dashboard-personalization-rbac, Property {number}: {property_text}`

**Property Test Examples**:

```python
from hypothesis import given, strategies as st
import hypothesis

# Property 1: Universal Content Intelligence Access
@given(user_role=st.sampled_from(['admin', 'creator', 'viewer']))
def test_property_1_universal_content_intelligence_access(user_role):
    """
    Feature: dashboard-personalization-rbac
    Property 1: For any user regardless of role, access control should grant 
    access to Content Intelligence
    """
    access_control = AccessControlService()
    user_id = f"user_test_{user_role}"
    
    # Create test user with role
    create_test_user(user_id, user_role)
    
    # Verify access is granted
    assert access_control.can_access_feature(user_id, "Content Intelligence") == True

# Property 2: Transform Access Control by Role
@given(user_role=st.sampled_from(['admin', 'creator', 'viewer']))
def test_property_2_transform_access_by_role(user_role):
    """
    Feature: dashboard-personalization-rbac
    Property 2: For any user, Transform access should be granted if and only if 
    role is admin or creator
    """
    access_control = AccessControlService()
    user_id = f"user_test_{user_role}"
    
    create_test_user(user_id, user_role)
    
    can_access = access_control.can_access_feature(user_id, "Transform")
    expected = user_role in ['admin', 'creator']
    
    assert can_access == expected

# Property 3: Feature Access Event Structure
@given(
    user_id=st.text(min_size=5, max_size=20),
    feature_name=st.sampled_from(['Content Intelligence', 'Transform', 'Monitoring', 'Alerts', 'Security'])
)
def test_property_3_feature_access_event_structure(user_id, feature_name):
    """
    Feature: dashboard-personalization-rbac
    Property 3: For any feature access event, it should contain valid usage_id, 
    user_id, feature_name, and timestamp
    """
    tracker = FeatureUsageTracker()
    
    usage_id = tracker.track_feature_access(user_id, feature_name)
    
    # Verify event was persisted
    event = get_feature_access_event(usage_id)
    
    assert event is not None
    assert event['usage_id'] == usage_id
    assert event['user_id'] == user_id
    assert event['feature_name'] == feature_name
    assert event['accessed_at'] is not None
    assert isinstance(event['accessed_at'], datetime)

# Property 6: User-Specific Alert Filtering
@given(
    user_id=st.text(min_size=5, max_size=20),
    num_user_alerts=st.integers(min_value=0, max_value=10),
    num_other_alerts=st.integers(min_value=0, max_value=10)
)
def test_property_6_user_specific_alert_filtering(user_id, num_user_alerts, num_other_alerts):
    """
    Feature: dashboard-personalization-rbac
    Property 6: For any user, all displayed alerts should match the user's user_id
    """
    alert_filter = AlertFilterService()
    
    # Create alerts for user
    for i in range(num_user_alerts):
        create_test_alert(user_id, f"alert_{i}")
    
    # Create alerts for other users
    for i in range(num_other_alerts):
        create_test_alert(f"other_user_{i}", f"other_alert_{i}")
    
    # Get filtered alerts
    alerts = alert_filter.get_user_alerts(user_id)
    
    # Verify all alerts belong to user
    assert len(alerts) == num_user_alerts
    for alert in alerts:
        assert alert['user_id'] == user_id

# Property 13: Usage Count Accuracy
@given(
    user_id=st.text(min_size=5, max_size=20),
    feature_name=st.sampled_from(['Content Intelligence', 'Transform', 'Monitoring']),
    num_accesses=st.integers(min_value=0, max_value=50)
)
def test_property_13_usage_count_accuracy(user_id, feature_name, num_accesses):
    """
    Feature: dashboard-personalization-rbac
    Property 13: For any user and feature, usage count should equal number of 
    access events in database
    """
    tracker = FeatureUsageTracker()
    
    # Record multiple accesses
    for _ in range(num_accesses):
        tracker.track_feature_access(user_id, feature_name)
    
    # Get usage count
    count = tracker.get_usage_count(user_id, feature_name)
    
    # Verify count matches
    assert count == num_accesses
```


### Unit Testing

**Focus Areas**:
- Specific UI components and interactions
- Database schema validation
- Edge cases (empty states, zero counts)
- Error handling scenarios
- Integration between components

**Unit Test Examples**:

```python
import pytest
from datetime import datetime

class TestAccessControl:
    """Unit tests for access control functionality"""
    
    def test_viewer_sees_lock_icon_on_transform_tab(self):
        """Requirement 2.3: Viewer should see lock icon on Transform tab"""
        dashboard = create_test_dashboard(user_role='viewer')
        transform_tab = dashboard.get_tab('Transform')
        
        assert transform_tab.has_lock_icon() == True
        assert transform_tab.get_tooltip() == "You don't have access"
    
    def test_admin_no_lock_icon_on_transform_tab(self):
        """Requirement 2.6: Admin should not see lock icon"""
        dashboard = create_test_dashboard(user_role='admin')
        transform_tab = dashboard.get_tab('Transform')
        
        assert transform_tab.has_lock_icon() == False
    
    def test_viewer_transform_click_shows_notification(self):
        """Requirement 2.4: Clicking Transform shows access denied message"""
        dashboard = create_test_dashboard(user_role='viewer')
        transform_tab = dashboard.get_tab('Transform')
        
        transform_tab.click()
        
        notification = dashboard.get_last_notification()
        assert notification == "Access denied: Transform feature requires admin or creator role"

class TestFeatureUsageTracking:
    """Unit tests for feature usage tracking"""
    
    def test_track_content_intelligence_access(self):
        """Requirement 10.1: Content Intelligence access generates event"""
        tracker = FeatureUsageTracker()
        user_id = "test_user"
        
        usage_id = tracker.track_feature_access(user_id, "Content Intelligence")
        
        assert usage_id is not None
        event = get_feature_access_event(usage_id)
        assert event['feature_name'] == "Content Intelligence"
    
    def test_no_duplicate_on_refresh(self):
        """Requirement 10.6: No duplicate events on data refresh"""
        tracker = FeatureUsageTracker()
        user_id = "test_user"
        feature = "Monitoring"
        
        # First access
        usage_id_1 = tracker.track_feature_access(user_id, feature)
        
        # Simulate refresh (same session, same feature)
        tracker.set_current_feature(user_id, feature)
        usage_id_2 = tracker.track_feature_access(user_id, feature)
        
        # Should not create new event
        assert usage_id_2 is None
        
        # Verify only one event exists
        count = tracker.get_usage_count(user_id, feature)
        assert count == 1

class TestRecentFeaturesPanel:
    """Unit tests for recent features display"""
    
    def test_empty_state_message(self):
        """Requirement 4.4: Show message when no features accessed"""
        panel = RecentFeaturesPanel(user_id="new_user")
        
        content = panel.render()
        
        assert "Start using features to see your recent activity" in content
    
    def test_display_fewer_than_three_features(self):
        """Requirement 4.3: Display only accessed features if < 3"""
        tracker = FeatureUsageTracker()
        user_id = "test_user"
        
        # Access only 2 features
        tracker.track_feature_access(user_id, "Content Intelligence")
        tracker.track_feature_access(user_id, "Monitoring")
        
        panel = RecentFeaturesPanel(user_id=user_id)
        features = panel.get_features()
        
        assert len(features) == 2
    
    def test_feature_card_click_navigates(self):
        """Requirement 4.9: Clicking feature card navigates to feature"""
        tracker = FeatureUsageTracker()
        user_id = "test_user"
        tracker.track_feature_access(user_id, "Transform")
        
        panel = RecentFeaturesPanel(user_id=user_id)
        feature_card = panel.get_feature_card("Transform")
        
        feature_card.click()
        
        assert panel.dashboard.current_tab == "Transform"

class TestAlertFiltering:
    """Unit tests for alert filtering"""
    
    def test_personalized_labels_for_non_admin(self):
        """Requirement 11.1-11.4: Personalized labels for users"""
        alert_filter = AlertFilterService()
        labels = alert_filter.get_personalized_labels(user_role='creator')
        
        assert labels['quality_score'] == "Your Content Quality Score"
        assert labels['analyses'] == "Your Recent Analyses"
        assert labels['transformations'] == "Your Transformations"
        assert labels['api_usage'] == "Your API Usage"
    
    def test_system_wide_label_for_admin(self):
        """Requirement 11.5: System-wide label for admin"""
        alert_filter = AlertFilterService()
        labels = alert_filter.get_personalized_labels(user_role='admin')
        
        assert labels['panel_header'] == "System-Wide Alerts"
    
    def test_empty_alerts_message(self):
        """Requirement 6.9: Show message when no alerts"""
        alert_filter = AlertFilterService()
        user_id = "test_user"
        
        alerts = alert_filter.get_user_alerts(user_id)
        
        if len(alerts) == 0:
            message = alert_filter.get_empty_state_message()
            assert message == "No alerts for your account"

class TestDatabaseSchema:
    """Unit tests for database schema"""
    
    def test_feature_usage_history_table_structure(self):
        """Requirements 8.1-8.4: Verify table structure"""
        conn = db_schema.get_connection()
        
        # Check table exists
        tables = conn.execute("SHOW TABLES").fetchall()
        assert ('feature_usage_history',) in tables
        
        # Check columns
        columns = conn.execute("DESCRIBE feature_usage_history").fetchall()
        column_names = [col[0] for col in columns]
        
        assert 'usage_id' in column_names
        assert 'user_id' in column_names
        assert 'feature_name' in column_names
        assert 'accessed_at' in column_names
    
    def test_feature_usage_history_indexes(self):
        """Requirements 8.5-8.6: Verify indexes exist"""
        conn = db_schema.get_connection()
        
        indexes = conn.execute("""
            SELECT index_name FROM duckdb_indexes() 
            WHERE table_name = 'feature_usage_history'
        """).fetchall()
        
        index_names = [idx[0] for idx in indexes]
        
        assert 'idx_feature_usage_user_time' in index_names
        assert 'idx_feature_usage_feature_time' in index_names
    
    def test_user_preferences_table_structure(self):
        """Requirements 9.1-9.3: Verify preferences table"""
        conn = db_schema.get_connection()
        
        columns = conn.execute("DESCRIBE user_preferences").fetchall()
        column_names = [col[0] for col in columns]
        
        assert 'user_id' in column_names
        assert 'preferences_json' in column_names
        assert 'updated_at' in column_names

class TestAdminMetrics:
    """Unit tests for admin metrics functionality"""
    
    def test_user_metrics_breakdown_table_columns(self):
        """Requirement 12.2: Verify breakdown table columns"""
        monitoring = MonitoringService()
        breakdown = monitoring.get_user_metrics_breakdown()
        
        if len(breakdown) > 0:
            first_row = breakdown[0]
            assert 'username' in first_row
            assert 'total_analyses' in first_row
            assert 'total_transformations' in first_row
            assert 'avg_quality_score' in first_row
            assert 'last_active' in first_row
    
    def test_admin_sees_all_users_in_breakdown(self):
        """Requirement 12.3: All users included in breakdown"""
        # Create test users
        create_test_user("user_1", "creator")
        create_test_user("user_2", "viewer")
        create_test_user("user_3", "admin")
        
        monitoring = MonitoringService()
        breakdown = monitoring.get_user_metrics_breakdown()
        
        usernames = [row['username'] for row in breakdown]
        assert "user_1" in usernames
        assert "user_2" in usernames
        assert "user_3" in usernames
    
    def test_non_admin_sees_only_own_metrics(self):
        """Requirement 7.10: Creator/Viewer see only own metrics"""
        monitoring = MonitoringService()
        user_id = "user_creator"
        
        metrics = monitoring.get_aggregated_metrics(user_id)
        
        # Verify metrics are filtered to user
        assert metrics['user_id'] == user_id
        assert 'all_users' not in metrics

class TestLockIconDisplay:
    """Unit tests for Transform lock icon"""
    
    def test_lock_icon_tooltip_timing(self):
        """Requirement 13.3: Tooltip appears within 200ms"""
        dashboard = create_test_dashboard(user_role='viewer')
        transform_tab = dashboard.get_tab('Transform')
        
        start_time = time.time()
        transform_tab.hover()
        tooltip_visible = transform_tab.is_tooltip_visible()
        end_time = time.time()
        
        assert tooltip_visible == True
        assert (end_time - start_time) < 0.2  # 200ms
    
    def test_transform_tab_reduced_opacity(self):
        """Requirement 13.5: Transform tab has reduced opacity for viewers"""
        dashboard = create_test_dashboard(user_role='viewer')
        transform_tab = dashboard.get_tab('Transform')
        
        opacity = transform_tab.get_opacity()
        assert opacity == 0.5

class TestUsageCount:
    """Unit tests for usage count calculation"""
    
    def test_zero_usage_count_for_never_accessed(self):
        """Requirement 14.4: Display 0 for never accessed features"""
        tracker = FeatureUsageTracker()
        user_id = "new_user"
        
        count = tracker.get_usage_count(user_id, "Transform")
        
        assert count == 0
    
    def test_usage_count_is_integer(self):
        """Requirement 14.3: Usage count is integer"""
        tracker = FeatureUsageTracker()
        user_id = "test_user"
        
        tracker.track_feature_access(user_id, "Monitoring")
        count = tracker.get_usage_count(user_id, "Monitoring")
        
        assert isinstance(count, int)
```

### Integration Testing

**Test Scenarios**:

1. **End-to-End Feature Access Flow**:
   - User logs in → navigates to feature → event tracked → recent features updated → usage count incremented

2. **Role-Based Access Flow**:
   - Viewer logs in → attempts Transform access → sees lock icon → clicks tab → receives denial notification

3. **Admin Metrics Flow**:
   - Admin logs in → views monitoring → sees all users → selects specific user → metrics filtered → resets filter → sees aggregated view

4. **Alert Filtering Flow**:
   - User performs analysis → alert generated with user_id → user views alerts → sees only own alerts → labels personalized

### Performance Testing

**Metrics to Monitor**:

1. **Feature Usage Tracking**:
   - Event recording latency: < 50ms
   - Database write time: < 100ms

2. **Recent Features Query**:
   - Query execution time: < 200ms
   - UI rendering time: < 100ms

3. **Alert Filtering**:
   - Filter query time: < 500ms (for 1000+ alerts)
   - UI update time: < 200ms

4. **Admin Metrics Aggregation**:
   - Aggregation query time: < 2 seconds (for 100+ users)
   - Breakdown table rendering: < 500ms

**Load Testing**:
- Simulate 50 concurrent users accessing features
- Verify no database deadlocks
- Verify UI remains responsive


## Implementation Details

### Service Layer Changes

#### 1. Access Control Service (New File)

**File**: `src/services/access_control_service.py`

**Key Implementation Details**:

```python
class AccessControlService:
    """Manages role-based access control for dashboard features"""
    
    FEATURE_PERMISSIONS = {
        'Content Intelligence': ['admin', 'creator', 'viewer'],
        'Transform': ['admin', 'creator'],
        'Monitoring': ['admin', 'creator', 'viewer'],
        'Alerts': ['admin', 'creator', 'viewer'],
        'Security': ['admin']
    }
    
    def __init__(self):
        self.auth_service = auth_service
    
    def can_access_feature(self, user_id: str, feature_name: str) -> bool:
        """Check if user can access feature based on role"""
        user_role = self.auth_service.get_user_role(user_id)
        
        if not user_role:
            logger.warning(f"Unable to determine role for user {user_id}")
            return False
        
        allowed_roles = self.FEATURE_PERMISSIONS.get(feature_name, [])
        return user_role in allowed_roles
    
    def is_feature_locked(self, user_id: str, feature_name: str) -> bool:
        """Check if feature should display lock icon"""
        return not self.can_access_feature(user_id, feature_name)
```

#### 2. Feature Usage Tracker (New File)

**File**: `src/services/feature_usage_tracker.py`

**Key Implementation Details**:

```python
class FeatureUsageTracker:
    """Tracks user feature access for personalization"""
    
    def __init__(self):
        self.db = db_schema.get_connection()
        self.current_sessions = {}  # user_id -> current_feature
    
    def track_feature_access(self, user_id: str, feature_name: str) -> Optional[str]:
        """Record feature access event"""
        # Check if should track (prevent duplicates on refresh)
        if not self.should_track_event(user_id, feature_name):
            return None
        
        usage_id = str(uuid.uuid4())
        accessed_at = datetime.now()
        
        self.db.execute("""
            INSERT INTO feature_usage_history 
            (usage_id, user_id, feature_name, accessed_at)
            VALUES (?, ?, ?, ?)
        """, [usage_id, user_id, feature_name, accessed_at])
        
        # Update current session
        self.current_sessions[user_id] = feature_name
        
        logger.info(f"Tracked feature access: {user_id} -> {feature_name}")
        return usage_id
    
    def should_track_event(self, user_id: str, feature_name: str) -> bool:
        """Determine if event should be tracked"""
        current_feature = self.current_sessions.get(user_id)
        
        # Track if navigating to different feature or first access
        return current_feature != feature_name
    
    def get_recent_features(self, user_id: str, limit: int = 3) -> List[Dict]:
        """Get user's most recently accessed features"""
        result = self.db.execute("""
            SELECT 
                feature_name,
                MAX(accessed_at) as last_accessed,
                COUNT(*) as usage_count
            FROM feature_usage_history
            WHERE user_id = ?
            GROUP BY feature_name
            ORDER BY last_accessed DESC
            LIMIT ?
        """, [user_id, limit]).fetchall()
        
        features = []
        for row in result:
            features.append({
                'feature_name': row[0],
                'last_accessed': row[1],
                'usage_count': row[2]
            })
        
        return features
    
    def get_usage_count(self, user_id: str, feature_name: str) -> int:
        """Get total usage count for a feature"""
        result = self.db.execute("""
            SELECT COUNT(*) 
            FROM feature_usage_history
            WHERE user_id = ? AND feature_name = ?
        """, [user_id, feature_name]).fetchone()
        
        return result[0] if result else 0
```

#### 3. Alert Filter Service (New File)

**File**: `src/services/alert_filter_service.py`

**Key Implementation Details**:

```python
class AlertFilterService:
    """Filters alerts to show user-specific information"""
    
    def __init__(self):
        self.db = db_schema.get_connection()
    
    def get_user_alerts(self, user_id: str) -> List[Dict]:
        """Get all alerts for a specific user"""
        alerts = []
        
        # Content Intelligence alerts
        alerts.extend(self.filter_content_intelligence_alerts(user_id))
        
        # Transform alerts
        alerts.extend(self.filter_transform_alerts(user_id))
        
        # Quality alerts
        alerts.extend(self.filter_quality_alerts(user_id))
        
        # Rate limit alerts
        alerts.extend(self.filter_rate_limit_alerts(user_id))
        
        # Sort by timestamp descending
        alerts.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return alerts
    
    def filter_content_intelligence_alerts(self, user_id: str) -> List[Dict]:
        """Get Content Intelligence alerts for user"""
        result = self.db.execute("""
            SELECT 
                ci.id,
                ci.content_type,
                ci.sentiment,
                ci.quality_score,
                ci.analyzed_at
            FROM ashoka_contentint ci
            WHERE ci.user_id = ?
            AND ci.quality_score < 70.0
            ORDER BY ci.analyzed_at DESC
            LIMIT 10
        """, [user_id]).fetchall()
        
        alerts = []
        for row in result:
            alerts.append({
                'alert_id': f"quality_{row[0]}",
                'user_id': user_id,
                'type': 'quality_warning',
                'source': 'content_intelligence',
                'message': f"Content quality score {row[3]:.1f} below threshold",
                'timestamp': row[4],
                'severity': 'medium'
            })
        
        return alerts
    
    def get_personalized_labels(self, user_role: str) -> Dict[str, str]:
        """Get personalized label mappings"""
        if user_role == 'admin':
            return {
                'panel_header': 'System-Wide Alerts',
                'quality_score': 'Content Quality Score',
                'analyses': 'Recent Analyses',
                'transformations': 'Transformations',
                'api_usage': 'API Usage'
            }
        else:
            return {
                'panel_header': 'Your Alerts',
                'quality_score': 'Your Content Quality Score',
                'analyses': 'Your Recent Analyses',
                'transformations': 'Your Transformations',
                'api_usage': 'Your API Usage'
            }
```

#### 4. Monitoring Service Extensions

**File**: `src/services/monitoring_service.py` (modifications)

**New Methods**:

```python
class MonitoringService:
    # ... existing methods ...
    
    def get_aggregated_metrics(self, user_id: str) -> Dict:
        """Get metrics based on user role"""
        user_role = auth_service.get_user_role(user_id)
        
        if user_role == 'admin':
            return self._get_all_users_metrics()
        else:
            return self._get_user_specific_metrics(user_id)
    
    def _get_all_users_metrics(self) -> Dict:
        """Get aggregated metrics across all users"""
        conn = db_schema.get_connection()
        
        # Total analyses
        total_analyses = conn.execute("""
            SELECT COUNT(*) FROM ashoka_contentint
        """).fetchone()[0]
        
        # Total transformations
        total_transforms = conn.execute("""
            SELECT COUNT(*) FROM transform_history
        """).fetchone()[0]
        
        # Average quality score
        avg_quality = conn.execute("""
            SELECT AVG(quality_score) FROM ashoka_contentint
            WHERE quality_score IS NOT NULL
        """).fetchone()[0]
        
        return {
            'total_analyses': total_analyses,
            'total_transformations': total_transforms,
            'avg_quality_score': avg_quality or 0.0,
            'view_type': 'aggregated'
        }
    
    def _get_user_specific_metrics(self, user_id: str) -> Dict:
        """Get metrics for specific user"""
        conn = db_schema.get_connection()
        
        # User analyses
        user_analyses = conn.execute("""
            SELECT COUNT(*) FROM ashoka_contentint
            WHERE user_id = ?
        """, [user_id]).fetchone()[0]
        
        # User transformations
        user_transforms = conn.execute("""
            SELECT COUNT(*) FROM transform_history
            WHERE user_id = ?
        """, [user_id]).fetchone()[0]
        
        # User quality score
        user_quality = conn.execute("""
            SELECT AVG(quality_score) FROM ashoka_contentint
            WHERE user_id = ? AND quality_score IS NOT NULL
        """, [user_id]).fetchone()[0]
        
        return {
            'user_id': user_id,
            'total_analyses': user_analyses,
            'total_transformations': user_transforms,
            'avg_quality_score': user_quality or 0.0,
            'view_type': 'user_specific'
        }
    
    def get_user_metrics_breakdown(self) -> List[Dict]:
        """Get per-user metrics breakdown (admin only)"""
        conn = db_schema.get_connection()
        
        result = conn.execute("""
            SELECT 
                u.username,
                COUNT(DISTINCT ci.id) as total_analyses,
                COUNT(DISTINCT th.id) as total_transformations,
                AVG(ci.quality_score) as avg_quality_score,
                MAX(GREATEST(
                    COALESCE(ci.analyzed_at, '1970-01-01'),
                    COALESCE(th.created_at, '1970-01-01')
                )) as last_active
            FROM ashoka_users u
            LEFT JOIN ashoka_contentint ci ON u.user_id = ci.user_id
            LEFT JOIN transform_history th ON u.user_id = th.user_id
            GROUP BY u.username
            ORDER BY last_active DESC
        """).fetchall()
        
        breakdown = []
        for row in result:
            breakdown.append({
                'username': row[0],
                'total_analyses': row[1],
                'total_transformations': row[2],
                'avg_quality_score': row[3] or 0.0,
                'last_active': row[4]
            })
        
        return breakdown
```


### UI Layer Changes

#### 1. Dashboard Tab Creation with Access Control

**File**: `src/ui/dashboard.py`

**Modifications to `create_dashboard()` method**:

```python
def create_dashboard(self):
    """Create the main dashboard UI with RBAC"""
    
    # Get current user info
    user_id = app.storage.general.get('user_id', '')
    username = app.storage.general.get('username', '')
    
    # Initialize services
    self.access_control = AccessControlService()
    self.feature_tracker = FeatureUsageTracker()
    self.alert_filter = AlertFilterService()
    
    # ... existing header code ...
    
    # Main content with tabs
    with ui.tabs().classes('w-full justify-center') as tabs:
        self.overview_tab = ui.tab('Overview', icon='dashboard')
        self.content_tab = ui.tab('Content Intelligence', icon='psychology')
        
        # Transform tab with conditional lock icon
        if self.access_control.is_feature_locked(user_id, 'Transform'):
            # Viewer sees locked tab
            with ui.tab('Transform', icon='transform').classes('opacity-50') as self.transform_tab:
                ui.icon('lock').classes('ml-1').tooltip('You don\'t have access')
        else:
            # Admin/Creator sees normal tab
            self.transform_tab = ui.tab('Transform', icon='transform')
        
        self.monitor_tab = ui.tab('Monitoring', icon='bar_chart')
        self.alerts_tab = ui.tab('Alerts', icon='notifications')
        
        # Security tab - only for admin
        if self.access_control.can_access_feature(user_id, 'Security'):
            self.security_tab = ui.tab('Security', icon='security')
    
    with ui.tab_panels(tabs, value=self.overview_tab).classes('w-full'):
        # Overview Panel
        with ui.tab_panel(self.overview_tab):
            self._track_feature_access('Overview')
            self._create_overview_panel()
        
        # Content Intelligence Panel
        with ui.tab_panel(self.content_tab):
            self._track_feature_access('Content Intelligence')
            self._create_content_intelligence_panel()
        
        # Transform Panel
        with ui.tab_panel(self.transform_tab):
            if self.access_control.can_access_feature(user_id, 'Transform'):
                self._track_feature_access('Transform')
                self._create_transform_panel()
            else:
                # Show access denied message
                ui.notify('Access denied: Transform feature requires admin or creator role', 
                         type='warning')
                ui.label('You do not have permission to access this feature').classes('text-xl text-center mt-8')
        
        # ... other panels ...

def _track_feature_access(self, feature_name: str):
    """Track feature access event"""
    user_id = app.storage.general.get('user_id', '')
    if user_id:
        self.feature_tracker.track_feature_access(user_id, feature_name)
```

#### 2. Recent Features Panel in Overview

**Modifications to `_create_overview_panel()` method**:

```python
def _create_overview_panel(self):
    """Create overview dashboard panel with recent features"""
    
    user_id = app.storage.general.get('user_id', '')
    
    # ... existing overview content ...
    
    # Recent Features Section
    with ui.card().classes('w-full mt-4'):
        ui.label('Recent Features').classes('text-2xl font-bold mb-4')
        
        recent_features = self.feature_tracker.get_recent_features(user_id, limit=3)
        
        if not recent_features:
            ui.label('Start using features to see your recent activity').classes('text-gray-500 text-center py-8')
        else:
            with ui.column().classes('w-full gap-2'):
                for feature in recent_features:
                    self._create_feature_card(feature)

def _create_feature_card(self, feature: Dict):
    """Create a clickable feature card"""
    feature_name = feature['feature_name']
    last_accessed = feature['last_accessed']
    usage_count = feature['usage_count']
    
    # Get feature icon
    icon_map = {
        'Content Intelligence': 'psychology',
        'Transform': 'transform',
        'Monitoring': 'bar_chart',
        'Alerts': 'notifications',
        'Security': 'security'
    }
    icon = icon_map.get(feature_name, 'star')
    
    # Format relative time
    relative_time = self._format_relative_time(last_accessed)
    
    with ui.card().classes('w-full cursor-pointer hover:shadow-lg transition-shadow').on('click', 
                                                                                         lambda: self._navigate_to_feature(feature_name)):
        with ui.row().classes('w-full items-center'):
            ui.icon(icon, size='lg').classes('text-blue-500')
            with ui.column().classes('flex-grow'):
                ui.label(feature_name).classes('text-lg font-semibold')
                ui.label(f'Last used: {relative_time}').classes('text-sm text-gray-600')
                ui.label(f'Usage count: {usage_count}').classes('text-sm text-gray-500')

def _format_relative_time(self, timestamp: datetime) -> str:
    """Format timestamp as relative time"""
    now = datetime.now()
    diff = now - timestamp
    
    if diff.total_seconds() < 60:
        return 'just now'
    elif diff.total_seconds() < 3600:
        minutes = int(diff.total_seconds() / 60)
        return f'{minutes} minute{"s" if minutes > 1 else ""} ago'
    elif diff.total_seconds() < 86400:
        hours = int(diff.total_seconds() / 3600)
        return f'{hours} hour{"s" if hours > 1 else ""} ago'
    else:
        days = int(diff.total_seconds() / 86400)
        return f'{days} day{"s" if days > 1 else ""} ago'

def _navigate_to_feature(self, feature_name: str):
    """Navigate to a specific feature"""
    tab_map = {
        'Content Intelligence': self.content_tab,
        'Transform': self.transform_tab,
        'Monitoring': self.monitor_tab,
        'Alerts': self.alerts_tab,
        'Security': self.security_tab
    }
    
    target_tab = tab_map.get(feature_name)
    if target_tab:
        # Trigger tab change
        target_tab.value = target_tab
```

#### 3. Profile Settings with Recent Features

**Modifications to `_show_profile_dialog()` method**:

```python
def _show_profile_dialog(self):
    """Show user profile dialog with recent features"""
    user_id = app.storage.general.get('user_id', '')
    username = app.storage.general.get('username', '')
    
    with ui.dialog() as profile_dialog, ui.card().classes('w-96'):
        ui.label('User Profile').classes('text-2xl font-bold mb-4')
        
        # User info
        with ui.column().classes('w-full gap-2 mb-4'):
            ui.label(f'Username: {username}').classes('text-lg')
            
            # Get user details
            user = auth_service.get_user_by_id(user_id)
            if user:
                ui.label(f'Email: {user.email}').classes('text-lg')
                ui.label(f'Role: {user.role.capitalize()}').classes('text-lg')
                ui.label(f'Member since: {user.created_at.strftime("%Y-%m-%d")}').classes('text-lg')
        
        ui.separator()
        
        # Recent Features Section
        ui.label('Recent Features').classes('text-xl font-bold mt-4 mb-2')
        
        recent_features = self.feature_tracker.get_recent_features(user_id, limit=3)
        
        if not recent_features:
            ui.label('No feature usage recorded yet').classes('text-gray-500 text-center py-4')
        else:
            with ui.column().classes('w-full gap-2'):
                for feature in recent_features:
                    feature_name = feature['feature_name']
                    last_accessed = feature['last_accessed']
                    usage_count = feature['usage_count']
                    
                    with ui.card().classes('w-full'):
                        ui.label(feature_name).classes('font-semibold')
                        ui.label(f'Last used: {last_accessed.strftime("%Y-%m-%d %H:%M:%S")}').classes('text-sm text-gray-600')
                        ui.label(f'Total uses: {usage_count}').classes('text-sm text-gray-500')
        
        ui.button('Close', on_click=profile_dialog.close).classes('mt-4')
    
    profile_dialog.open()
```

#### 4. Alerts Panel with User Filtering

**Modifications to `_create_alerts_panel()` method**:

```python
def _create_alerts_panel(self):
    """Create alerts panel with user-specific filtering"""
    
    user_id = app.storage.general.get('user_id', '')
    user_role = auth_service.get_user_role(user_id)
    
    # Get personalized labels
    labels = self.alert_filter.get_personalized_labels(user_role)
    
    # Panel header
    ui.label(labels['panel_header']).classes('text-3xl font-bold mb-4')
    
    # Get user-specific alerts
    alerts = self.alert_filter.get_user_alerts(user_id)
    
    if not alerts:
        ui.label('No alerts for your account').classes('text-gray-500 text-center py-8')
        return
    
    # Alert metrics with personalized labels
    with ui.row().classes('w-full gap-4 mb-6'):
        # Quality score metric
        quality_alerts = [a for a in alerts if a['type'] == 'quality_warning']
        with ui.card().classes('flex-1'):
            ui.label(labels['quality_score']).classes('text-lg font-semibold')
            ui.label(str(len(quality_alerts))).classes('text-3xl font-bold text-orange-500')
        
        # Analyses metric
        analysis_alerts = [a for a in alerts if a['source'] == 'content_intelligence']
        with ui.card().classes('flex-1'):
            ui.label(labels['analyses']).classes('text-lg font-semibold')
            ui.label(str(len(analysis_alerts))).classes('text-3xl font-bold text-blue-500')
        
        # Transformations metric
        transform_alerts = [a for a in alerts if a['source'] == 'transform']
        with ui.card().classes('flex-1'):
            ui.label(labels['transformations']).classes('text-lg font-semibold')
            ui.label(str(len(transform_alerts))).classes('text-3xl font-bold text-green-500')
    
    # Alert list
    with ui.column().classes('w-full gap-2'):
        for alert in alerts[:10]:  # Show top 10
            self._create_alert_card(alert)

def _create_alert_card(self, alert: Dict):
    """Create an alert card"""
    severity_colors = {
        'critical': 'red',
        'high': 'orange',
        'medium': 'yellow',
        'low': 'blue'
    }
    
    color = severity_colors.get(alert.get('severity', 'low'), 'gray')
    
    with ui.card().classes(f'w-full border-l-4 border-{color}-500'):
        with ui.row().classes('w-full items-center'):
            ui.icon('warning', size='md').classes(f'text-{color}-500')
            with ui.column().classes('flex-grow'):
                ui.label(alert['message']).classes('font-semibold')
                ui.label(self._format_relative_time(alert['timestamp'])).classes('text-sm text-gray-600')
```


#### 5. Monitoring Panel with Admin Breakdown

**Modifications to `_create_monitoring_panel()` method**:

```python
def _create_monitoring_panel(self):
    """Create monitoring panel with role-based metrics"""
    
    user_id = app.storage.general.get('user_id', '')
    user_role = auth_service.get_user_role(user_id)
    
    ui.label('Monitoring & Analytics').classes('text-3xl font-bold mb-4')
    
    # Admin-specific: User filter dropdown
    if user_role == 'admin':
        with ui.row().classes('w-full items-center gap-4 mb-4'):
            ui.label('User Filter:').classes('text-lg')
            
            # Get all users for dropdown
            all_users = self._get_all_usernames()
            user_options = ['All Users'] + all_users
            
            self.user_filter_select = ui.select(
                user_options,
                value='All Users',
                on_change=lambda e: self._on_user_filter_change(e.value)
            ).classes('w-64')
            
            ui.button('Reset Filter', on_click=self._reset_user_filter).classes('ml-2')
    
    # Metrics display container
    self.metrics_container = ui.column().classes('w-full')
    
    # Initial metrics load
    self._load_metrics(user_id, filter_user_id=None)
    
    # Admin-specific: User Metrics Breakdown
    if user_role == 'admin':
        ui.separator().classes('my-6')
        ui.label('User Metrics Breakdown').classes('text-2xl font-bold mb-4')
        
        self.breakdown_container = ui.column().classes('w-full')
        self._load_user_breakdown()

def _load_metrics(self, user_id: str, filter_user_id: Optional[str] = None):
    """Load metrics based on user role and filter"""
    self.metrics_container.clear()
    
    with self.metrics_container:
        if filter_user_id:
            # Show specific user's metrics
            metrics = monitoring_service.get_filtered_metrics(user_id, filter_user_id)
            ui.label(f'Metrics for: {filter_user_id}').classes('text-xl mb-4')
        else:
            # Show aggregated or user-specific based on role
            metrics = monitoring_service.get_aggregated_metrics(user_id)
        
        # Display metrics
        with ui.row().classes('w-full gap-4'):
            with ui.card().classes('flex-1'):
                ui.label('Total Analyses').classes('text-lg font-semibold')
                ui.label(str(metrics['total_analyses'])).classes('text-3xl font-bold text-blue-500')
            
            with ui.card().classes('flex-1'):
                ui.label('Total Transformations').classes('text-lg font-semibold')
                ui.label(str(metrics['total_transformations'])).classes('text-3xl font-bold text-green-500')
            
            with ui.card().classes('flex-1'):
                ui.label('Avg Quality Score').classes('text-lg font-semibold')
                ui.label(f"{metrics['avg_quality_score']:.1f}").classes('text-3xl font-bold text-purple-500')

def _load_user_breakdown(self):
    """Load user metrics breakdown table (admin only)"""
    self.breakdown_container.clear()
    
    breakdown = monitoring_service.get_user_metrics_breakdown()
    
    with self.breakdown_container:
        # Create sortable table
        columns = [
            {'name': 'username', 'label': 'Username', 'field': 'username', 'sortable': True, 'align': 'left'},
            {'name': 'analyses', 'label': 'Total Analyses', 'field': 'total_analyses', 'sortable': True, 'align': 'right'},
            {'name': 'transforms', 'label': 'Total Transformations', 'field': 'total_transformations', 'sortable': True, 'align': 'right'},
            {'name': 'quality', 'label': 'Avg Quality Score', 'field': 'avg_quality_score', 'sortable': True, 'align': 'right'},
            {'name': 'last_active', 'label': 'Last Active', 'field': 'last_active', 'sortable': True, 'align': 'left'}
        ]
        
        rows = []
        for user_data in breakdown:
            rows.append({
                'username': user_data['username'],
                'total_analyses': user_data['total_analyses'],
                'total_transformations': user_data['total_transformations'],
                'avg_quality_score': f"{user_data['avg_quality_score']:.1f}",
                'last_active': user_data['last_active'].strftime('%Y-%m-%d %H:%M') if user_data['last_active'] else 'Never'
            })
        
        table = ui.table(columns=columns, rows=rows, row_key='username').classes('w-full')
        
        # Make username clickable
        table.on('row-click', lambda e: self._on_username_click(e.args[1]['username']))

def _on_user_filter_change(self, selected_user: str):
    """Handle user filter dropdown change"""
    user_id = app.storage.general.get('user_id', '')
    
    if selected_user == 'All Users':
        self._load_metrics(user_id, filter_user_id=None)
    else:
        # Get user_id from username
        filter_user_id = f"user_{selected_user}"
        self._load_metrics(user_id, filter_user_id=filter_user_id)

def _on_username_click(self, username: str):
    """Handle username click in breakdown table"""
    # Update filter dropdown
    self.user_filter_select.value = username
    
    # Load filtered metrics
    user_id = app.storage.general.get('user_id', '')
    filter_user_id = f"user_{username}"
    self._load_metrics(user_id, filter_user_id=filter_user_id)

def _reset_user_filter(self):
    """Reset user filter to show all users"""
    self.user_filter_select.value = 'All Users'
    user_id = app.storage.general.get('user_id', '')
    self._load_metrics(user_id, filter_user_id=None)

def _get_all_usernames(self) -> List[str]:
    """Get list of all usernames"""
    conn = db_schema.get_connection()
    result = conn.execute("SELECT username FROM ashoka_users ORDER BY username").fetchall()
    return [row[0] for row in result]
```

### Database Layer Changes

#### 1. Schema Initialization

**File**: `src/database/duckdb_schema.py`

**Add to `initialize_schema()` method**:

```python
def initialize_schema(self):
    """Create all tables and indexes"""
    # ... existing tables ...
    
    # Feature Usage History Table
    self.conn.execute("""
        CREATE TABLE IF NOT EXISTS feature_usage_history (
            usage_id VARCHAR PRIMARY KEY,
            user_id VARCHAR NOT NULL,
            feature_name VARCHAR NOT NULL,
            accessed_at TIMESTAMP NOT NULL
        )
    """)
    
    # User Preferences Table
    self.conn.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            user_id VARCHAR PRIMARY KEY,
            preferences_json JSON NOT NULL,
            updated_at TIMESTAMP NOT NULL
        )
    """)
    
    # Create indexes
    self._create_rbac_indexes()

def _create_rbac_indexes(self):
    """Create indexes for RBAC feature"""
    # Feature usage indexes
    self.conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_feature_usage_user_time 
        ON feature_usage_history(user_id, accessed_at DESC)
    """)
    
    self.conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_feature_usage_feature_time 
        ON feature_usage_history(feature_name, accessed_at DESC)
    """)
```

#### 2. User Preferences Initialization

**File**: `src/services/auth_service.py`

**Modify `signup()` method**:

```python
def signup(self, username: str, email: str, password: str, role: str = "user") -> Tuple[bool, str]:
    """Register new user"""
    # ... existing user creation code ...
    
    # Initialize default preferences
    self._initialize_user_preferences(user_id)
    
    logger.info(f"User registered: {username} with role: {role}")
    return True, "Registration successful"

def _initialize_user_preferences(self, user_id: str):
    """Initialize default preferences for new user"""
    default_preferences = {
        "theme": "light",
        "language": "English",
        "notifications": True,
        "auto_save": True,
        "email_alerts": False,
        "session_timeout": 30
    }
    
    conn = db_schema.get_connection()
    conn.execute("""
        INSERT INTO user_preferences (user_id, preferences_json, updated_at)
        VALUES (?, ?, ?)
    """, [user_id, json.dumps(default_preferences), datetime.now()])
    
    logger.info(f"Initialized preferences for user {user_id}")
```

### API/Service Integration

#### Alert Generation with User Association

**Modify alert generation in various services**:

**Content Intelligence Service** (`src/services/content_analyzer.py`):

```python
def generate_quality_alert(self, content_id: str, quality_score: float):
    """Generate quality alert with user association"""
    # Get user_id from content
    conn = db_schema.get_connection()
    result = conn.execute("""
        SELECT user_id FROM ashoka_contentint WHERE id = ?
    """, [content_id]).fetchone()
    
    if not result:
        return
    
    user_id = result[0]
    
    alert = {
        'alert_id': str(uuid.uuid4()),
        'user_id': user_id,  # Associate with user
        'type': 'quality_warning',
        'source': 'content_intelligence',
        'source_id': content_id,
        'severity': 'medium',
        'message': f'Content quality score {quality_score:.1f} below threshold',
        'timestamp': datetime.now(),
        'metadata': {
            'quality_score': quality_score,
            'threshold': 70.0
        }
    }
    
    # Store alert (implementation depends on alert storage mechanism)
    self._store_alert(alert)
```

**Transform Service** (`src/services/content_transformer.py`):

```python
def generate_transform_alert(self, transform_id: str, error_message: str):
    """Generate transform alert with user association"""
    # Get user_id from transform history
    conn = db_schema.get_connection()
    result = conn.execute("""
        SELECT user_id FROM transform_history WHERE id = ?
    """, [transform_id]).fetchone()
    
    if not result:
        return
    
    user_id = result[0]
    
    alert = {
        'alert_id': str(uuid.uuid4()),
        'user_id': user_id,  # Associate with user
        'type': 'transform_error',
        'source': 'transform',
        'source_id': transform_id,
        'severity': 'high',
        'message': f'Transformation failed: {error_message}',
        'timestamp': datetime.now()
    }
    
    self._store_alert(alert)
```

## Deployment Considerations

### Database Migration

**Migration Script**: `migrations/add_rbac_tables.py`

```python
"""
Migration: Add RBAC tables
Date: 2024-03-15
"""

def upgrade(conn):
    """Add feature_usage_history and user_preferences tables"""
    
    # Create feature_usage_history table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS feature_usage_history (
            usage_id VARCHAR PRIMARY KEY,
            user_id VARCHAR NOT NULL,
            feature_name VARCHAR NOT NULL,
            accessed_at TIMESTAMP NOT NULL
        )
    """)
    
    # Create indexes
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_feature_usage_user_time 
        ON feature_usage_history(user_id, accessed_at DESC)
    """)
    
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_feature_usage_feature_time 
        ON feature_usage_history(feature_name, accessed_at DESC)
    """)
    
    # Create user_preferences table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            user_id VARCHAR PRIMARY KEY,
            preferences_json JSON NOT NULL,
            updated_at TIMESTAMP NOT NULL
        )
    """)
    
    # Initialize preferences for existing users
    existing_users = conn.execute("SELECT user_id FROM ashoka_users").fetchall()
    
    default_prefs = json.dumps({
        "theme": "light",
        "language": "English",
        "notifications": True,
        "auto_save": True,
        "email_alerts": False,
        "session_timeout": 30
    })
    
    for user in existing_users:
        user_id = user[0]
        conn.execute("""
            INSERT INTO user_preferences (user_id, preferences_json, updated_at)
            VALUES (?, ?, ?)
        """, [user_id, default_prefs, datetime.now()])
    
    print(f"Initialized preferences for {len(existing_users)} existing users")

def downgrade(conn):
    """Remove RBAC tables"""
    conn.execute("DROP TABLE IF EXISTS feature_usage_history")
    conn.execute("DROP TABLE IF EXISTS user_preferences")
```

### Performance Optimization

1. **Index Usage**:
   - Ensure queries use indexes for user_id and accessed_at
   - Monitor query performance with EXPLAIN ANALYZE

2. **Caching**:
   - Cache recent features for 5 minutes to reduce database queries
   - Cache user role lookups for session duration

3. **Query Optimization**:
   - Use LIMIT clauses for recent features queries
   - Batch alert queries instead of individual lookups

4. **Background Tasks**:
   - Cleanup old feature usage events (> 90 days) in background task
   - Aggregate metrics computation can be cached and refreshed periodically

### Security Considerations

1. **Access Control Enforcement**:
   - Always check permissions server-side, not just in UI
   - Validate user_id from session, never from client input

2. **Data Isolation**:
   - Ensure queries always filter by user_id for non-admin users
   - Prevent SQL injection with parameterized queries

3. **Audit Logging**:
   - Log all access control decisions
   - Log feature access events for audit trail

4. **Session Management**:
   - Validate session before tracking feature access
   - Clear feature tracking state on logout

## Summary

This design provides a comprehensive implementation plan for dashboard personalization and RBAC features. Key highlights:

- **Access Control**: Role-based permissions with visual indicators (lock icons) for restricted features
- **Feature Tracking**: Automatic tracking of feature usage with deduplication logic
- **Personalization**: Recent features display in Overview and Profile with usage statistics
- **Alert Filtering**: User-specific alerts with personalized labels
- **Admin Capabilities**: Aggregated metrics, user breakdown table, and filtering options
- **Database Schema**: New tables for feature usage history and user preferences
- **Testing Strategy**: Comprehensive property-based and unit testing approach

The implementation follows the existing codebase patterns and integrates seamlessly with current services (auth_service, monitoring_service, db_schema).

