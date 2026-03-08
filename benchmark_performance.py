#!/usr/bin/env python3
"""
Ashoka Platform - Performance Benchmarking Script

This script benchmarks various components of the Ashoka platform and generates
a comprehensive performance report.

Usage:
    python benchmark_performance.py
    python benchmark_performance.py --output report.json
    python benchmark_performance.py --verbose
"""

import time
import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Any
import argparse

# Load environment variables from .env file BEFORE importing services
from dotenv import load_dotenv
load_dotenv()

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import Ashoka components
from src.database.duckdb_schema import db_schema
from src.services.content_analyzer import ContentAnalyzer
from src.services.content_transformer import ContentTransformer
from src.services.auth_service import auth_service
from src.services.monitoring_service import monitoring_service
from src.services.api_usage_tracker import api_usage_tracker


class PerformanceBenchmark:
    """Performance benchmarking for Ashoka platform"""
    
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'platform': 'Ashoka GenAI Governance Platform',
            'benchmarks': {},
            'summary': {}
        }
        
    def log(self, message: str):
        """Log message if verbose mode is enabled"""
        if self.verbose:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
    
    def measure_time(self, func, *args, **kwargs) -> tuple:
        """Measure execution time of a function"""
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            return (end_time - start_time) * 1000, True, result  # Convert to ms
        except Exception as e:
            end_time = time.time()
            return (end_time - start_time) * 1000, False, str(e)
    
    def benchmark_database_operations(self) -> Dict[str, Any]:
        """Benchmark database operations"""
        self.log("Benchmarking database operations...")
        
        results = {
            'name': 'Database Operations',
            'tests': []
        }
        
        # Test 1: Database connection
        duration, success, _ = self.measure_time(db_schema.connect)
        results['tests'].append({
            'name': 'Database Connection',
            'duration_ms': round(duration, 2),
            'success': success
        })
        
        # Test 2: Schema initialization
        duration, success, _ = self.measure_time(db_schema.initialize_schema)
        results['tests'].append({
            'name': 'Schema Initialization',
            'duration_ms': round(duration, 2),
            'success': success
        })
        
        # Test 3: Simple query
        def simple_query():
            return db_schema.conn.execute("SELECT 1").fetchone()
        
        duration, success, _ = self.measure_time(simple_query)
        results['tests'].append({
            'name': 'Simple Query (SELECT 1)',
            'duration_ms': round(duration, 2),
            'success': success
        })
        
        # Test 4: User table query
        def user_query():
            return db_schema.conn.execute("SELECT COUNT(*) FROM ashoka_users").fetchone()
        
        duration, success, result = self.measure_time(user_query)
        user_count = result[0] if success and result else 0
        results['tests'].append({
            'name': 'User Count Query',
            'duration_ms': round(duration, 2),
            'success': success,
            'result': f"{user_count} users"
        })
        
        # Test 5: Content analysis query
        def content_query():
            return db_schema.conn.execute(
                "SELECT COUNT(*) FROM ashoka_contentint"
            ).fetchone()
        
        duration, success, result = self.measure_time(content_query)
        content_count = result[0] if success and result else 0
        results['tests'].append({
            'name': 'Content Analysis Query',
            'duration_ms': round(duration, 2),
            'success': success,
            'result': f"{content_count} records"
        })
        
        # Calculate average
        avg_duration = sum(t['duration_ms'] for t in results['tests']) / len(results['tests'])
        results['average_duration_ms'] = round(avg_duration, 2)
        results['success_rate'] = sum(1 for t in results['tests'] if t['success']) / len(results['tests']) * 100
        
        return results
    
    def benchmark_content_analysis(self) -> Dict[str, Any]:
        """Benchmark content analysis operations"""
        self.log("Benchmarking content analysis...")
        
        results = {
            'name': 'Content Analysis',
            'tests': []
        }
        
        # Sample texts of different sizes
        test_texts = {
            'short': "This is a short test message for benchmarking.",
            'medium': "This is a medium-length test message for benchmarking. " * 10,
            'long': "This is a long test message for benchmarking purposes. " * 50
        }
        
        analyzer = ContentAnalyzer()
        
        for size, text in test_texts.items():
            self.log(f"  Testing {size} text ({len(text)} chars)...")
            
            def analyze():
                # Use analyze_content with a test version_id
                return analyzer.analyze_content(
                    version_id=f'benchmark_{size}_test',
                    content=text,
                    user_id='benchmark_user'
                )
            
            duration, success, result = self.measure_time(analyze)
            
            test_result = {
                'name': f'Analyze {size.capitalize()} Text',
                'text_length': len(text),
                'duration_ms': round(duration, 2),
                'success': success
            }
            
            # ContentAnalysis is a Pydantic model, access attributes directly
            if success and result and hasattr(result, 'summary'):
                test_result['has_summary'] = bool(result.summary)
                test_result['sentiment'] = result.sentiment.classification if hasattr(result, 'sentiment') else 'unknown'
            
            results['tests'].append(test_result)
        
        # Calculate average
        avg_duration = sum(t['duration_ms'] for t in results['tests']) / len(results['tests'])
        results['average_duration_ms'] = round(avg_duration, 2)
        results['success_rate'] = sum(1 for t in results['tests'] if t['success']) / len(results['tests']) * 100
        
        return results
    
    def benchmark_content_transformation(self) -> Dict[str, Any]:
        """Benchmark content transformation operations"""
        self.log("Benchmarking content transformation...")
        
        results = {
            'name': 'Content Transformation',
            'tests': []
        }
        
        transformer = ContentTransformer()
        test_content = "This is a test message for multi-platform transformation benchmarking."
        
        # Test different platform combinations
        platform_tests = [
            (['LinkedIn'], 'Single Platform'),
            (['LinkedIn', 'Twitter'], 'Two Platforms'),
            (['LinkedIn', 'Twitter', 'Instagram'], 'Three Platforms'),
            (['LinkedIn', 'Twitter', 'Instagram', 'Facebook'], 'Four Platforms')
        ]
        
        for platforms, test_name in platform_tests:
            self.log(f"  Testing {test_name}...")
            
            def transform():
                return transformer.transform_content(
                    content=test_content,
                    platforms=platforms,
                    tone='professional',
                    include_hashtags=True,
                    user_id='benchmark_user'
                )
            
            duration, success, result = self.measure_time(transform)
            
            test_result = {
                'name': test_name,
                'platforms': len(platforms),
                'duration_ms': round(duration, 2),
                'success': success
            }
            
            if success and isinstance(result, dict):
                test_result['platforms_generated'] = len(result.get('transformed_content', {}))
            
            results['tests'].append(test_result)
        
        # Calculate average
        avg_duration = sum(t['duration_ms'] for t in results['tests']) / len(results['tests'])
        results['average_duration_ms'] = round(avg_duration, 2)
        results['success_rate'] = sum(1 for t in results['tests'] if t['success']) / len(results['tests']) * 100
        
        return results
    
    def benchmark_authentication(self) -> Dict[str, Any]:
        """Benchmark authentication operations"""
        self.log("Benchmarking authentication...")
        
        results = {
            'name': 'Authentication',
            'tests': []
        }
        
        # Test 1: User authentication
        def authenticate():
            return auth_service.authenticate('admin', 'admin123')
        
        duration, success, result = self.measure_time(authenticate)
        results['tests'].append({
            'name': 'User Authentication',
            'duration_ms': round(duration, 2),
            'success': success
        })
        
        # Test 2: OTP generation
        if success and result and hasattr(result, 'user_id'):
            user_id = result.user_id
            
            def generate_otp():
                return auth_service.generate_otp(user_id)
            
            duration, success, otp = self.measure_time(generate_otp)
            results['tests'].append({
                'name': 'OTP Generation',
                'duration_ms': round(duration, 2),
                'success': success
            })
            
            # Test 3: OTP verification
            if success and otp:
                def verify_otp():
                    return auth_service.verify_otp(user_id, otp)
                
                duration, success, _ = self.measure_time(verify_otp)
                results['tests'].append({
                    'name': 'OTP Verification',
                    'duration_ms': round(duration, 2),
                    'success': success
                })
            
            # Test 4: Session creation
            def create_session():
                return auth_service.create_session(user_id)
            
            duration, success, _ = self.measure_time(create_session)
            results['tests'].append({
                'name': 'Session Creation',
                'duration_ms': round(duration, 2),
                'success': success
            })
        
        # Calculate average
        if results['tests']:
            avg_duration = sum(t['duration_ms'] for t in results['tests']) / len(results['tests'])
            results['average_duration_ms'] = round(avg_duration, 2)
            results['success_rate'] = sum(1 for t in results['tests'] if t['success']) / len(results['tests']) * 100
        
        return results
    
    def benchmark_monitoring(self) -> Dict[str, Any]:
        """Benchmark monitoring operations"""
        self.log("Benchmarking monitoring...")
        
        results = {
            'name': 'Monitoring',
            'tests': []
        }
        
        # Test 1: Get quality metrics
        def get_quality_metrics():
            return monitoring_service.get_quality_metrics()
        
        duration, success, _ = self.measure_time(get_quality_metrics)
        results['tests'].append({
            'name': 'Get Quality Metrics',
            'duration_ms': round(duration, 2),
            'success': success
        })
        
        # Test 2: Get performance trends
        def get_performance_trends():
            return monitoring_service.get_performance_trends()
        
        duration, success, _ = self.measure_time(get_performance_trends)
        results['tests'].append({
            'name': 'Get Performance Trends',
            'duration_ms': round(duration, 2),
            'success': success
        })
        
        # Test 3: Check system health
        def check_system_health():
            return monitoring_service.check_system_health()
        
        duration, success, _ = self.measure_time(check_system_health)
        results['tests'].append({
            'name': 'Check System Health',
            'duration_ms': round(duration, 2),
            'success': success
        })
        
        # Calculate average
        avg_duration = sum(t['duration_ms'] for t in results['tests']) / len(results['tests'])
        results['average_duration_ms'] = round(avg_duration, 2)
        results['success_rate'] = sum(1 for t in results['tests'] if t['success']) / len(results['tests']) * 100
        
        return results
    
    def benchmark_api_usage_tracking(self) -> Dict[str, Any]:
        """Benchmark API usage tracking operations"""
        self.log("Benchmarking API usage tracking...")
        
        results = {
            'name': 'API Usage Tracking',
            'tests': []
        }
        
        test_user = 'benchmark_user'
        
        # Test 1: Track request
        def track_request():
            return api_usage_tracker.track_request(
                user_id=test_user,
                engine_name='gemini',
                model_name='gemini-2.0-flash',
                success=True
            )
        
        duration, success, _ = self.measure_time(track_request)
        results['tests'].append({
            'name': 'Track API Request',
            'duration_ms': round(duration, 2),
            'success': success
        })
        
        # Test 2: Get usage today
        def get_usage():
            return api_usage_tracker.get_usage_today(test_user, 'gemini')
        
        duration, success, _ = self.measure_time(get_usage)
        results['tests'].append({
            'name': 'Get Usage Today',
            'duration_ms': round(duration, 2),
            'success': success
        })
        
        # Test 3: Get all usage
        def get_all_usage():
            return api_usage_tracker.get_all_usage_today(test_user)
        
        duration, success, _ = self.measure_time(get_all_usage)
        results['tests'].append({
            'name': 'Get All Usage Today',
            'duration_ms': round(duration, 2),
            'success': success
        })
        
        # Test 4: Can use engine
        def can_use():
            return api_usage_tracker.can_use_engine(test_user, 'gemini')
        
        duration, success, _ = self.measure_time(can_use)
        results['tests'].append({
            'name': 'Check Engine Availability',
            'duration_ms': round(duration, 2),
            'success': success
        })
        
        # Calculate average
        avg_duration = sum(t['duration_ms'] for t in results['tests']) / len(results['tests'])
        results['average_duration_ms'] = round(avg_duration, 2)
        results['success_rate'] = sum(1 for t in results['tests'] if t['success']) / len(results['tests']) * 100
        
        return results
    
    def run_all_benchmarks(self):
        """Run all benchmarks and generate report"""
        print("=" * 70)
        print("Ashoka Platform - Performance Benchmark")
        print("=" * 70)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        print()
        
        # Run benchmarks
        self.results['benchmarks']['database'] = self.benchmark_database_operations()
        self.results['benchmarks']['content_analysis'] = self.benchmark_content_analysis()
        self.results['benchmarks']['content_transformation'] = self.benchmark_content_transformation()
        self.results['benchmarks']['authentication'] = self.benchmark_authentication()
        self.results['benchmarks']['monitoring'] = self.benchmark_monitoring()
        self.results['benchmarks']['api_tracking'] = self.benchmark_api_usage_tracking()
        
        # Calculate summary
        self.calculate_summary()
        
        # Print results
        self.print_results()
        
        return self.results
    
    def calculate_summary(self):
        """Calculate overall summary statistics"""
        all_tests = []
        for benchmark in self.results['benchmarks'].values():
            all_tests.extend(benchmark['tests'])
        
        total_tests = len(all_tests)
        successful_tests = sum(1 for t in all_tests if t['success'])
        total_duration = sum(t['duration_ms'] for t in all_tests)
        avg_duration = total_duration / total_tests if total_tests > 0 else 0
        
        self.results['summary'] = {
            'total_benchmarks': len(self.results['benchmarks']),
            'total_tests': total_tests,
            'successful_tests': successful_tests,
            'failed_tests': total_tests - successful_tests,
            'success_rate': round((successful_tests / total_tests * 100) if total_tests > 0 else 0, 2),
            'total_duration_ms': round(total_duration, 2),
            'average_duration_ms': round(avg_duration, 2),
            'fastest_test_ms': round(min(t['duration_ms'] for t in all_tests), 2) if all_tests else 0,
            'slowest_test_ms': round(max(t['duration_ms'] for t in all_tests), 2) if all_tests else 0
        }
    
    def print_results(self):
        """Print benchmark results to console"""
        print("\n" + "=" * 70)
        print("BENCHMARK RESULTS")
        print("=" * 70)
        
        for name, benchmark in self.results['benchmarks'].items():
            print(f"\n{benchmark['name']}")
            print("-" * 70)
            print(f"Average Duration: {benchmark.get('average_duration_ms', 0):.2f} ms")
            print(f"Success Rate: {benchmark.get('success_rate', 0):.1f}%")
            print()
            
            for test in benchmark['tests']:
                status = "✓" if test['success'] else "✗"
                print(f"  {status} {test['name']:<40} {test['duration_ms']:>8.2f} ms")
                if 'result' in test:
                    print(f"    └─ {test['result']}")
        
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        summary = self.results['summary']
        print(f"Total Benchmarks: {summary['total_benchmarks']}")
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Successful: {summary['successful_tests']}")
        print(f"Failed: {summary['failed_tests']}")
        print(f"Success Rate: {summary['success_rate']}%")
        print(f"Total Duration: {summary['total_duration_ms']:.2f} ms")
        print(f"Average Duration: {summary['average_duration_ms']:.2f} ms")
        print(f"Fastest Test: {summary['fastest_test_ms']:.2f} ms")
        print(f"Slowest Test: {summary['slowest_test_ms']:.2f} ms")
        print("=" * 70)
    
    def save_results(self, output_file: str):
        """Save results to JSON file"""
        with open(output_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nResults saved to: {output_file}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Ashoka Platform Performance Benchmarking'
    )
    parser.add_argument(
        '--output', '-o',
        default='benchmark_report.json',
        help='Output file for JSON report (default: benchmark_report.json)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Run benchmarks
    benchmark = PerformanceBenchmark(verbose=args.verbose)
    results = benchmark.run_all_benchmarks()
    
    # Save results
    benchmark.save_results(args.output)
    
    print(f"\nBenchmark completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == '__main__':
    main()
