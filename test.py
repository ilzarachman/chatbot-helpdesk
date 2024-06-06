import unittest

if __name__ == "__main__":
    # Start test discovery in the 'test' folder
    loader = unittest.TestLoader()
    start_dir = 'test/'
    suite = loader.discover(start_dir, pattern='*_test.py')

    # Run the tests
    runner = unittest.TextTestRunner()
    runner.run(suite)
