"""
Diagnostic utilities for troubleshooting stock API issues.
This file helps identify why stock data isn't loading.
"""
import logging
import os
import requests
import yfinance as yf
from datetime import datetime

logger = logging.getLogger(__name__)


class StockAPIDiagnostics:
    """Diagnose stock API issues."""
    
    @staticmethod
    def check_network_connectivity() -> dict:
        """Check if the app has internet connectivity."""
        try:
            response = requests.get('https://www.google.com', timeout=5)
            return {
                'status': 'OK',
                'message': 'Network connectivity is working',
                'response_time': response.elapsed.total_seconds()
            }
        except Exception as e:
            return {
                'status': 'FAIL',
                'message': f'Network connectivity issue: {str(e)}',
                'response_time': None
            }
    
    @staticmethod
    def check_yfinance_api() -> dict:
        """Check if yfinance API is accessible."""
        try:
            ticker = yf.Ticker('AAPL')
            data = ticker.history(period='1d', timeout=10)
            
            if data.empty:
                return {
                    'status': 'FAIL',
                    'message': 'yfinance returned empty data',
                    'data_length': 0
                }
            
            return {
                'status': 'OK',
                'message': f'yfinance is working (fetched {len(data)} records)',
                'data_length': len(data),
                'latest_price': float(data['Close'].iloc[-1])
            }
        except Exception as e:
            return {
                'status': 'FAIL',
                'message': f'yfinance error: {str(e)}',
                'error_type': type(e).__name__
            }
    
    @staticmethod
    def check_exchange_rate_api() -> dict:
        """Check if exchange rate API is accessible."""
        try:
            response = requests.get(
                'https://api.exchangerate-api.com/v4/latest/USD',
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                rate = data.get('rates', {}).get('INR')
                return {
                    'status': 'OK',
                    'message': f'Exchange rate API is working: 1 USD = ₹{rate:.2f}',
                    'exchange_rate': rate
                }
            else:
                return {
                    'status': 'FAIL',
                    'message': f'API returned status {response.status_code}',
                    'status_code': response.status_code
                }
        except Exception as e:
            return {
                'status': 'FAIL',
                'message': f'Exchange rate API error: {str(e)}',
                'error_type': type(e).__name__
            }
    
    @staticmethod
    def run_full_diagnostics() -> dict:
        """Run all diagnostics and return results."""
        results = {
            'timestamp': datetime.now().isoformat(),
            'environment': os.getenv('RENDER', 'Local'),
            'checks': {
                'network': StockAPIDiagnostics.check_network_connectivity(),
                'yfinance': StockAPIDiagnostics.check_yfinance_api(),
                'exchange_rate': StockAPIDiagnostics.check_exchange_rate_api()
            }
        }
        
        # Determine overall status
        all_ok = all(
            check.get('status') == 'OK' 
            for check in results['checks'].values()
        )
        results['overall_status'] = 'OK' if all_ok else 'FAILED'
        
        return results
    
    @staticmethod
    def print_diagnostics_report() -> None:
        """Print a detailed diagnostics report to console/logs."""
        diagnostics = StockAPIDiagnostics.run_full_diagnostics()
        
        print("\n" + "="*60)
        print("TRADING APP - API DIAGNOSTICS REPORT")
        print("="*60)
        print(f"Timestamp: {diagnostics['timestamp']}")
        print(f"Environment: {diagnostics['environment']}")
        print(f"Overall Status: {diagnostics['overall_status']}")
        print("-"*60)
        
        for check_name, check_result in diagnostics['checks'].items():
            status = check_result['status']
            message = check_result['message']
            print(f"\n{check_name.upper():}")
            print(f"  Status: {status}")
            print(f"  Message: {message}")
            
            # Print additional details if available
            for key, value in check_result.items():
                if key not in ['status', 'message']:
                    print(f"  {key}: {value}")
        
        print("\n" + "="*60)
        print("RECOMMENDATION:")
        if diagnostics['overall_status'] == 'OK':
            print("✅ All systems operational. Stock data should load correctly.")
        else:
            print("❌ Some systems are not responding. Check the logs above.")
            failed_checks = [
                name for name, result in diagnostics['checks'].items()
                if result['status'] == 'FAIL'
            ]
            print(f"Failed checks: {', '.join(failed_checks)}")
        print("="*60 + "\n")


if __name__ == "__main__":
    # Run diagnostics if script is executed directly
    StockAPIDiagnostics.print_diagnostics_report()
