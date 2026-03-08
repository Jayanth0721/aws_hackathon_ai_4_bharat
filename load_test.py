#!/usr/bin/env python3
"""
Ashoka Platform - Load Testing & Performance Monitoring

This script performs end-to-end load testing on a running Ashoka instance
by simulating real user interactions via HTTP requests.

Usage:
    # Start your application first
    python run_dashboard.py
    
    # Then in another terminal, run load test
    python load_test.py
    python load_test.py --url http://localhost:8080 --users 10 --duration 60
"""

import requests
import time
import json
import argparse
import statistics
from datetime import datetime
from typing import Dict, List, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import sys


class LoadTester:
    """Load testing for Ashoka platform"""
    
    def __init__(self, base_url: str = "http://localhost:8080", verbose: bool = False):
        self.base_url = base_url.rstrip('/')
        self.verbose = verbose
        self.session = requests.Session()
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'base_url': base_url,
            'tests': [],
            'summary': {}
        }
        
    def log(self, message: str):
        """Log message if verbose"""
        if self.verbose:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
    
    def test_endpoint(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Test a single endpoint and measure performance"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, timeout=30, **kwargs)
            elif method.upper() == 'POST':
                response = self.session.post(url, timeout=30, **kwargs)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            duration = (time.time() - start_time) * 1000  # Convert to ms
            
            return {
                'success': True,
                'status_code': response.status_code,
                'duration_ms': duration,
                'response_size': len(response.content),
                'error': None
            }
        except Exception as e:
            duration = (time.time() - start_time) * 1000
            return {
                'success': False,
                'status_code': 0,
                'duration_ms': duration,
                'response_size': 0,
                'error': str(e)
            }
    
    def test_homepage(self) -> Dict[str, Any]:
        """Test homepage load time"""
        self.log("Testing homepage...")
        result = self.test_endpoint('GET', '/')
        result['test_name'] = 'Homepage Load'
        return result
    
    def test_dashboard_page(self) -> Dict[str, Any]:
        """Test dashboard page (may redirect if not authenticated)"""
        self.log("Testing dashboard page...")
        result = self.test_endpoint('GET', '/dashboard')
        result['test_name'] = 'Dashboard Page'
        return result
    
    def test_static_resources(self) -> List[Dict[str, Any]]:
        """Test loading of static resources"""
        self.log("Testing static resources...")
        results = []
        
        # Test common static resources
        static_paths = [
            '/_nicegui/static/nicegui.js',
            '/_nicegui/static/nicegui.css',
        ]
        
        for path in static_paths:
            result = self.test_endpoint('GET', path)
            result['test_name'] = f'Static: {path.split("/")[-1]}'
            results.append(result)
        
        return results
    
    def simulate_user_session(self, user_id: int) -> Dict[str, Any]:
        """Simulate a complete user session"""
        self.log(f"Simulating user session {user_id}...")
        
        session_results = {
            'user_id': user_id,
            'tests': [],
            'total_duration_ms': 0,
            'success_count': 0,
            'failure_count': 0
        }
        
        start_time = time.time()
        
        # 1. Load homepage
        result = self.test_homepage()
        session_results['tests'].append(result)
        if result['success']:
            session_results['success_count'] += 1
        else:
            session_results['failure_count'] += 1
        
        # Small delay between requests (simulate human behavior)
        time.sleep(0.5)
        
        # 2. Try to access dashboard
        result = self.test_dashboard_page()
        session_results['tests'].append(result)
        if result['success']:
            session_results['success_count'] += 1
        else:
            session_results['failure_count'] += 1
        
        # 3. Load static resources
        time.sleep(0.3)
        static_results = self.test_static_resources()
        for result in static_results:
            session_results['tests'].append(result)
            if result['success']:
                session_results['success_count'] += 1
            else:
                session_results['failure_count'] += 1
        
        session_results['total_duration_ms'] = (time.time() - start_time) * 1000
        
        return session_results
    
    def run_load_test(self, num_users: int = 10, duration_seconds: int = 60):
        """Run load test with multiple concurrent users"""
        print("=" * 70)
        print("Ashoka Platform - Load Test")
        print("=" * 70)
        print(f"Target URL: {self.base_url}")
        print(f"Concurrent Users: {num_users}")
        print(f"Test Duration: {duration_seconds} seconds")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        print()
        
        # First, check if server is reachable
        print("Checking server availability...")
        try:
            response = requests.get(self.base_url, timeout=5)
            print(f"✓ Server is reachable (Status: {response.status_code})")
        except Exception as e:
            print(f"✗ Server is not reachable: {e}")
            print("\nPlease start the application first:")
            print("  python run_dashboard.py")
            return None
        
        print()
        print("Starting load test...")
        print()
        
        all_results = []
        start_time = time.time()
        request_count = 0
        
        with ThreadPoolExecutor(max_workers=num_users) as executor:
            while (time.time() - start_time) < duration_seconds:
                # Submit user sessions
                futures = []
                for user_id in range(num_users):
                    future = executor.submit(self.simulate_user_session, request_count + user_id)
                    futures.append(future)
                
                # Collect results
                for future in as_completed(futures):
                    try:
                        result = future.result()
                        all_results.append(result)
                        request_count += 1
                        
                        # Progress indicator
                        elapsed = time.time() - start_time
                        print(f"\rProgress: {elapsed:.1f}s / {duration_seconds}s | "
                              f"Sessions: {len(all_results)} | "
                              f"Requests: {sum(len(r['tests']) for r in all_results)}", 
                              end='', flush=True)
                    except Exception as e:
                        self.log(f"Error in user session: {e}")
                
                # Small delay between batches
                time.sleep(1)
        
        print("\n")
        print("Load test completed!")
        print()
        
        # Analyze results
        self.analyze_results(all_results)
        
        return all_results
    
    def analyze_results(self, results: List[Dict[str, Any]]):
        """Analyze and display load test results"""
        print("=" * 70)
        print("LOAD TEST RESULTS")
        print("=" * 70)
        
        # Aggregate all test results
        all_tests = []
        for session in results:
            all_tests.extend(session['tests'])
        
        if not all_tests:
            print("No test results to analyze")
            return
        
        # Calculate statistics
        total_requests = len(all_tests)
        successful_requests = sum(1 for t in all_tests if t['success'])
        failed_requests = total_requests - successful_requests
        
        durations = [t['duration_ms'] for t in all_tests if t['success']]
        response_sizes = [t['response_size'] for t in all_tests if t['success']]
        
        # Overall statistics
        print("\n📊 Overall Statistics")
        print("-" * 70)
        print(f"Total Requests:        {total_requests}")
        print(f"Successful:            {successful_requests} ({successful_requests/total_requests*100:.1f}%)")
        print(f"Failed:                {failed_requests} ({failed_requests/total_requests*100:.1f}%)")
        print(f"Total Sessions:        {len(results)}")
        
        if durations:
            print(f"\n⏱️  Response Time Statistics")
            print("-" * 70)
            print(f"Average:               {statistics.mean(durations):.2f} ms")
            print(f"Median:                {statistics.median(durations):.2f} ms")
            print(f"Min:                   {min(durations):.2f} ms")
            print(f"Max:                   {max(durations):.2f} ms")
            print(f"Std Dev:               {statistics.stdev(durations) if len(durations) > 1 else 0:.2f} ms")
            
            # Percentiles
            sorted_durations = sorted(durations)
            p50 = sorted_durations[int(len(sorted_durations) * 0.50)]
            p90 = sorted_durations[int(len(sorted_durations) * 0.90)]
            p95 = sorted_durations[int(len(sorted_durations) * 0.95)]
            p99 = sorted_durations[int(len(sorted_durations) * 0.99)]
            
            print(f"\n📈 Percentiles")
            print("-" * 70)
            print(f"50th percentile (P50): {p50:.2f} ms")
            print(f"90th percentile (P90): {p90:.2f} ms")
            print(f"95th percentile (P95): {p95:.2f} ms")
            print(f"99th percentile (P99): {p99:.2f} ms")
        
        if response_sizes:
            print(f"\n📦 Response Size Statistics")
            print("-" * 70)
            print(f"Average:               {statistics.mean(response_sizes):.0f} bytes")
            print(f"Total Data Transfer:   {sum(response_sizes) / 1024 / 1024:.2f} MB")
        
        # Test breakdown
        print(f"\n🔍 Test Breakdown")
        print("-" * 70)
        
        test_types = {}
        for test in all_tests:
            test_name = test.get('test_name', 'Unknown')
            if test_name not in test_types:
                test_types[test_name] = {
                    'count': 0,
                    'success': 0,
                    'durations': []
                }
            test_types[test_name]['count'] += 1
            if test['success']:
                test_types[test_name]['success'] += 1
                test_types[test_name]['durations'].append(test['duration_ms'])
        
        for test_name, stats in sorted(test_types.items()):
            success_rate = (stats['success'] / stats['count'] * 100) if stats['count'] > 0 else 0
            avg_duration = statistics.mean(stats['durations']) if stats['durations'] else 0
            print(f"{test_name:<30} {stats['count']:>5} requests | "
                  f"{success_rate:>5.1f}% success | {avg_duration:>7.2f} ms avg")
        
        # Error analysis
        errors = [t for t in all_tests if not t['success']]
        if errors:
            print(f"\n❌ Errors ({len(errors)} total)")
            print("-" * 70)
            error_types = {}
            for error in errors:
                error_msg = error.get('error', 'Unknown error')
                error_types[error_msg] = error_types.get(error_msg, 0) + 1
            
            for error_msg, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {count:>3}x {error_msg[:60]}")
        
        # Performance rating
        print(f"\n⭐ Performance Rating")
        print("-" * 70)
        if durations:
            avg_duration = statistics.mean(durations)
            if avg_duration < 100:
                rating = "Excellent"
                emoji = "🟢"
            elif avg_duration < 300:
                rating = "Good"
                emoji = "🟡"
            elif avg_duration < 1000:
                rating = "Fair"
                emoji = "🟠"
            else:
                rating = "Needs Improvement"
                emoji = "🔴"
            
            print(f"{emoji} {rating} (Average response time: {avg_duration:.2f} ms)")
        
        print("=" * 70)
    
    def save_results(self, results: List[Dict[str, Any]], filename: str = "load_test_report.json"):
        """Save results to JSON file"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'base_url': self.base_url,
            'total_sessions': len(results),
            'sessions': results
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved to: {filename}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Ashoka Platform Load Testing'
    )
    parser.add_argument(
        '--url',
        default='http://localhost:8080',
        help='Base URL of the application (default: http://localhost:8080)'
    )
    parser.add_argument(
        '--users', '-u',
        type=int,
        default=10,
        help='Number of concurrent users (default: 10)'
    )
    parser.add_argument(
        '--duration', '-d',
        type=int,
        default=60,
        help='Test duration in seconds (default: 60)'
    )
    parser.add_argument(
        '--output', '-o',
        default='load_test_report.json',
        help='Output file for JSON report (default: load_test_report.json)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Run load test
    tester = LoadTester(base_url=args.url, verbose=args.verbose)
    results = tester.run_load_test(num_users=args.users, duration_seconds=args.duration)
    
    if results:
        # Save results
        tester.save_results(results, args.output)
        
        print(f"\n✅ Load test completed successfully!")
        print(f"   Total sessions: {len(results)}")
        print(f"   Report saved to: {args.output}")
    else:
        print("\n❌ Load test failed - server not reachable")
        sys.exit(1)


if __name__ == '__main__':
    main()
