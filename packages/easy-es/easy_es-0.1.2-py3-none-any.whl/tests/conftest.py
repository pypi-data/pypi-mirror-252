def pytest_addoption(parser):
    parser.addoption("--max_diff", action="store", default=0.1,
                     help="Maximum difference to consider valid")
    parser.addoption("--test_result_data_path", action="store", default=None,
                     help="Path to the file with test icp results")

