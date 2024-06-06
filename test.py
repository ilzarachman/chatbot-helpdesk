import argparse
import os
import unittest

def get_test_cases(folder: str = '') -> unittest.TestSuite:
    test_loader = unittest.TestLoader()
    root_test_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test')
    test_suite = test_loader.discover(folder, pattern='*_test.py', top_level_dir=root_test_folder)
    return test_suite

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run tests from a specific folder')
    parser.add_argument('--folder', '-f', type=str, help='Path to the folder containing the tests')
    parser.add_argument('--verbose', "-v", action='store_true', help='Enable verbose output')
    args = parser.parse_args()

    only_folders: list = args.folder.split(",") if args.folder else []

    if only_folders:
        test_suite = unittest.TestSuite()

        for folder in only_folders:
            test_suite.addTest(get_test_cases(folder))
    else:
        test_suite = get_test_cases("test/")
    
    if args.verbose:
        # Enable verbose output
        unittest.TextTestRunner(verbosity=2).run(test_suite)
    else:
        # Disable verbose output
        unittest.TextTestRunner().run(test_suite)