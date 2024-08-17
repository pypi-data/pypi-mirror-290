import unittest
import coverage

def run_tests():
    """Run all test cases from specified test modules."""
    # Create a test suite
    suite = unittest.TestSuite()

    # Add test modules to the suite
    suite.addTests(unittest.defaultTestLoader.loadTestsFromName('test_client'))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromName('test_lookup'))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromName('test_set_request'))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromName('test_invoke'))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromName('test_validation'))

    # Run the tests
    runner = unittest.TextTestRunner()
    runner.run(suite)

def main():
    """Main function to run tests, combine coverage, and generate the report."""
    # Initialize coverage
    cov = coverage.Coverage()
    cov.start()

    # Run tests
    run_tests()

    # Stop coverage collection
    cov.stop()
    cov.save()

    # Combine coverage data
    cov.combine()

    # Generate the HTML report
    cov.html_report(directory='coverage_html_report')
    print("Coverage report generated in 'coverage_html_report' directory.")

if __name__ == '__main__':
    main()
