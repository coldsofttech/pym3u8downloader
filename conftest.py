def pytest_collection_modifyitems(config, items):
    """
    Custom pytest hook to modify the collection of test items.
    This function sorts test items to execute specific tests first.
    """

    def test_order(test_name):
        # Define the desired order of execution for specific test names
        order_mapping = {
            'sample': 1  # To be updated when sequential execution for unit test cases are required
        }
        return order_mapping.get(test_name, float('inf'))  # Default to infinity for tests not in the mapping

    items.sort(key=lambda item: (test_order(item.nodeid.split("::")[-1]), item.fspath, item.originalname))
