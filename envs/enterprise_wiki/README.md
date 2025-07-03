# Enterprise Wiki Database - Data Generation Complete

## Summary

Successfully created an enterprise wiki database schema and generated realistic, relationally consistent data for use with tau_bench.

## Files Created

### Schema

- `enterprise_wiki_database_schema.json` - Complete database schema in JSON format matching b2b_finance structure

### Data Files (15 tables)

All files located in `/tau_bench/envs/enterprise_wiki/data/`:

1. **users.json** - 350 realistic user accounts with various timezones, locales, and statuses
2. **groups.json** - 50 groups (system and custom) for organizing users
3. **user_groups.json** - 790 user-group relationship mappings
4. **spaces.json** - 75 wiki spaces (global, personal, private) with themes and settings
5. **permissions.json** - 18 permission types (space, page, system, user categories)
6. **page_templates.json** - 30 reusable page templates for different content types
7. **pages.json** - 1,000 wiki pages with hierarchical relationships and content
8. **page_versions.json** - 500 historical page versions with change tracking
9. **comments.json** - 800 page comments with threading support
10. **attachments.json** - 400 file attachments linked to pages and comments
11. **watchers.json** - 500 user watch subscriptions for spaces, pages, and users
12. **notifications.json** - 700 system notifications for user activities
13. **space_permissions.json** - 300 space-level permission assignments
14. **labels.json** - 100 organizational labels with colors and descriptions
15. **page_labels.json** - 600 page-label relationship mappings

## Data Characteristics

- **Total Records**: 6,408 realistic data entries
- **Referential Integrity**: All foreign keys reference valid primary keys
- **Realistic Content**: Generated using appropriate business terminology and scenarios
- **Proper Relationships**: Hierarchical pages, threaded comments, permission inheritance
- **Temporal Consistency**: Timestamps follow logical creation/update patterns
- **Format Consistency**: All files follow tau_bench's JSON structure (string-keyed objects)
