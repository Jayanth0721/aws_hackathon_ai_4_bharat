# Ashoka Platform - Documentation Index

## Quick Start

1. **README.md** - Project overview and quick start guide
2. **SETUP.md** - Local development setup instructions
3. **FEATURES.md** - Platform features and capabilities

## AWS Deployment

1. **AWS_DEPLOYMENT.md** - Complete AWS deployment guide
   - EC2 setup
   - S3 configuration
   - DynamoDB setup
   - Nginx and Supervisor configuration

2. **.env.production.example** - Production environment template

## Database Configuration

1. **FIXED_DYNAMODB_SCHEMA.md** - DynamoDB setup and troubleshooting
   - Schema configuration
   - Entity type prefixes (USER#, SESSION#, CONTENT#)
   - Common issues and solutions

## Security

1. **CREDENTIALS.md** - Credentials and API keys management

## Project Structure

```
ashoka-platform/
├── src/
│   ├── database/          # Database connections
│   │   ├── db_factory.py         # Database factory (DynamoDB/MockDynamoDB)
│   │   ├── dynamodb_connection.py # Real DynamoDB connection
│   │   ├── mock_storage.py       # Local DuckDB for development
│   │   └── duckdb_schema.py      # DuckDB schema
│   ├── models/            # Data models
│   ├── services/          # Business logic
│   │   ├── auth_service.py       # Authentication
│   │   ├── content_analyzer.py   # Content analysis
│   │   ├── content_ingestion.py  # Content ingestion
│   │   ├── content_transformer.py # Content transformation
│   │   ├── file_processor.py     # File processing
│   │   ├── gemini_client.py      # Google Gemini AI
│   │   ├── monitoring_service.py # Monitoring
│   │   └── security_service.py   # Security
│   ├── ui/                # User interface
│   │   ├── auth_page.py          # Login/signup page
│   │   └── dashboard.py          # Main dashboard
│   └── utils/             # Utilities
├── deployment_scripts/    # Deployment automation
├── data/                  # Local data (DuckDB)
├── .env                   # Environment variables (local)
├── .env.example           # Environment template
├── .env.production.example # Production template
└── run_dashboard.py       # Application entry point
```

## Environment Configuration

### Local Development
```bash
USE_REAL_DYNAMODB=false  # Use local DuckDB
GEMINI_API_KEY=your_key
```

### Production
```bash
USE_REAL_DYNAMODB=true   # Use AWS DynamoDB
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
DYNAMODB_TABLE=ashoka_contentint
S3_BUCKET_NAME=ashoka-ai1-s3
```

## Key Features

- **Multi-language Support**: English, Hindi, Kannada, Tamil
- **Role-based Access**: Admin, Creator, User roles
- **Content Intelligence**: AI-powered content analysis
- **Security**: OTP authentication, session management
- **Monitoring**: Real-time system health monitoring
- **AWS Integration**: S3 for storage, DynamoDB for data

## Running the Application

### Local Development
```bash
python run_dashboard.py
```

### Production Deployment
See **AWS_DEPLOYMENT.md** for complete instructions.

## Troubleshooting

See **FIXED_DYNAMODB_SCHEMA.md** for:
- DynamoDB connection issues
- Schema validation errors
- User authentication problems
- Data retrieval issues

## Support

For issues or questions, refer to the specific documentation files listed above.
