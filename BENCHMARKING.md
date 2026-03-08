# Ashoka Platform - Performance Benchmarking Guide

Comprehensive performance testing and benchmarking for the Ashoka GenAI Governance Platform.

## Overview

The benchmarking script (`benchmark_performance.py`) tests various components of the Ashoka platform and generates detailed performance reports including:

- Database operations
- Content analysis
- Content transformation
- Authentication
- Monitoring services
- API usage tracking

## Prerequisites

The benchmark script requires:
- Python 3.8+
- All dependencies from `requirements.txt` installed
- `.env` file with API keys configured (for AI-dependent tests)

The script automatically loads environment variables from `.env` file.

## Quick Start

### Basic Usage

```bash
python benchmark_performance.py
```

### With Custom Output File

```bash
python benchmark_performance.py --output my_report.json
```

### Verbose Mode

```bash
python benchmark_performance.py --verbose
```

## What Gets Benchmarked

### 1. Database Operations
- Database connection time
- Schema initialization
- Simple queries (SELECT 1)
- User count queries
- Content analysis queries

### 2. Content Analysis
- Short text analysis (~50 chars)
- Medium text analysis (~500 chars)
- Long text analysis (~2500 chars)
- Quality score calculation
- Sentiment detection

### 3. Content Transformation
- Single platform transformation
- Two platform transformation
- Three platform transformation
- Four platform transformation
- Hashtag generation

### 4. Authentication
- User authentication
- OTP generation
- OTP verification
- Session creation

### 5. Monitoring Services
- Quality metrics retrieval
- Performance trends calculation
- System health checks

### 6. API Usage Tracking
- Request tracking
- Usage retrieval
- Engine availability checks
- Multi-engine usage queries

## Output Format

### Console Output

```
======================================================================
Ashoka Platform - Performance Benchmark
======================================================================
Started at: 2026-03-08 15:30:00
======================================================================

======================================================================
BENCHMARK RESULTS
======================================================================

Database Operations
----------------------------------------------------------------------
Average Duration: 15.45 ms
Success Rate: 100.0%

  ✓ Database Connection                          12.34 ms
  ✓ Schema Initialization                        18.56 ms
  ✓ Simple Query (SELECT 1)                       2.15 ms
  ✓ User Count Query                              8.92 ms
    └─ 158 users
  ✓ Content Analysis Query                       15.28 ms
    └─ 45 records

...

======================================================================
SUMMARY
======================================================================
Total Benchmarks: 6
Total Tests: 24
Successful: 24
Failed: 0
Success Rate: 100.0%
Total Duration: 1234.56 ms
Average Duration: 51.44 ms
Fastest Test: 2.15 ms
Slowest Test: 245.67 ms
======================================================================
```

### JSON Output

```json
{
  "timestamp": "2026-03-08T15:30:00.123456",
  "platform": "Ashoka GenAI Governance Platform",
  "benchmarks": {
    "database": {
      "name": "Database Operations",
      "tests": [
        {
          "name": "Database Connection",
          "duration_ms": 12.34,
          "success": true
        }
      ],
      "average_duration_ms": 15.45,
      "success_rate": 100.0
    }
  },
  "summary": {
    "total_benchmarks": 6,
    "total_tests": 24,
    "successful_tests": 24,
    "failed_tests": 0,
    "success_rate": 100.0,
    "total_duration_ms": 1234.56,
    "average_duration_ms": 51.44,
    "fastest_test_ms": 2.15,
    "slowest_test_ms": 245.67
  }
}
```

## Performance Targets

### Excellent Performance
- Database queries: < 20 ms
- Content analysis: < 5000 ms (5 seconds)
- Content transformation: < 3000 ms per platform
- Authentication: < 100 ms
- Monitoring queries: < 50 ms
- API tracking: < 10 ms

### Good Performance
- Database queries: 20-50 ms
- Content analysis: 5000-10000 ms (5-10 seconds)
- Content transformation: 3000-5000 ms per platform
- Authentication: 100-200 ms
- Monitoring queries: 50-100 ms
- API tracking: 10-20 ms

### Needs Optimization
- Database queries: > 50 ms
- Content analysis: > 10000 ms (10 seconds)
- Content transformation: > 5000 ms per platform
- Authentication: > 200 ms
- Monitoring queries: > 100 ms
- API tracking: > 20 ms

## Interpreting Results

### Success Rate
- **100%**: All tests passed successfully
- **90-99%**: Minor issues, investigate failed tests
- **< 90%**: Significant issues, requires attention

### Duration Analysis
- **Fastest Test**: Best-case performance
- **Slowest Test**: Bottleneck identification
- **Average Duration**: Overall system performance

### Component-Specific Metrics

#### Database Operations
- Fast queries indicate good database performance
- Slow queries may indicate:
  - Missing indexes
  - Large dataset
  - Disk I/O issues

#### Content Analysis
- Duration scales with text length
- Longer texts take more time (expected)
- Consistent failures indicate AI API issues

#### Content Transformation
- Duration scales with number of platforms
- Each platform adds ~2-3 seconds
- Failures may indicate AI API quota exceeded

#### Authentication
- Should be consistently fast (< 100 ms)
- Slow authentication indicates:
  - Database performance issues
  - Password hashing overhead

## Troubleshooting

### High Database Query Times
```bash
# Check database size
du -h data/ashoka.duckdb

# Vacuum database
duckdb data/ashoka.duckdb "VACUUM;"

# Analyze statistics
duckdb data/ashoka.duckdb "ANALYZE;"
```

### Content Analysis Failures
- Check API keys are configured in `.env` file
- Verify Gemini API key: `GEMINI_API_KEY`
- Verify Sarvam API key: `SARVAM_API_KEY`
- Check API quota not exceeded
- Check internet connectivity
- Review error messages in verbose mode

### "API key not set" Warnings
If you see warnings about API keys not being set:
1. Verify `.env` file exists in project root
2. Check API keys are properly set (no quotes, no spaces)
3. Ensure `python-dotenv` is installed: `pip install python-dotenv`
4. The script automatically loads `.env` - no manual configuration needed

### Authentication Slow
- Check database connection
- Verify user table indexes
- Review session storage performance

## Automated Benchmarking

### Daily Benchmarks (Cron)

```bash
# Add to crontab
crontab -e

# Run daily at 2 AM
0 2 * * * cd /path/to/ashoka && python benchmark_performance.py --output reports/benchmark_$(date +\%Y\%m\%d).json
```

### CI/CD Integration

```yaml
# GitHub Actions example
name: Performance Benchmark
on:
  push:
    branches: [main]
  schedule:
    - cron: '0 2 * * *'

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run benchmarks
        run: python benchmark_performance.py --output benchmark_report.json
      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: benchmark-report
          path: benchmark_report.json
```

## Comparing Results

### Compare Two Reports

```python
import json

# Load reports
with open('benchmark_report_old.json') as f:
    old = json.load(f)
with open('benchmark_report_new.json') as f:
    new = json.load(f)

# Compare averages
old_avg = old['summary']['average_duration_ms']
new_avg = new['summary']['average_duration_ms']
improvement = ((old_avg - new_avg) / old_avg) * 100

print(f"Performance change: {improvement:+.2f}%")
```

## Best Practices

1. **Run benchmarks regularly** - Track performance over time
2. **Baseline measurements** - Establish performance baselines
3. **Before/after comparisons** - Test before and after changes
4. **Different environments** - Test on dev, staging, production
5. **Load testing** - Run benchmarks under different loads
6. **Document results** - Keep historical records

## Advanced Usage

### Custom Benchmarks

```python
from benchmark_performance import PerformanceBenchmark

# Create custom benchmark
benchmark = PerformanceBenchmark(verbose=True)

# Add custom test
def my_custom_test():
    # Your test code here
    pass

duration, success, result = benchmark.measure_time(my_custom_test)
print(f"Duration: {duration:.2f} ms, Success: {success}")
```

### Programmatic Access

```python
from benchmark_performance import PerformanceBenchmark

# Run benchmarks
benchmark = PerformanceBenchmark()
results = benchmark.run_all_benchmarks()

# Access results
print(f"Success rate: {results['summary']['success_rate']}%")
print(f"Average duration: {results['summary']['average_duration_ms']} ms")

# Save to custom location
benchmark.save_results('custom_report.json')
```

## Performance Optimization Tips

### Database
- Add indexes on frequently queried columns
- Vacuum database regularly
- Use prepared statements
- Limit result sets

### Content Analysis
- Cache analysis results
- Batch process multiple texts
- Use appropriate text sizes
- Implement rate limiting

### Content Transformation
- Cache platform-specific templates
- Parallel platform processing
- Reuse AI responses when possible

### Authentication
- Cache session data
- Use connection pooling
- Optimize password hashing rounds

## Support

For performance issues or questions:
1. Run benchmarks with `--verbose` flag
2. Check system resources (CPU, memory, disk)
3. Review application logs
4. Compare with baseline measurements
5. Check AWS service health (if using cloud)

---

**Last Updated**: March 8, 2026
**Version**: 1.0.0
