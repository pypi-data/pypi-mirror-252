from robot.utils.dotdict import DotDict

# Global variables
global_var = 123

# Test case-specific test data
testcases = [
    {
        "name": "Test 1",
        "data": {
            "var": "value 1",
            "list": ["index 0.1", "index 1.1"],
            "dict": {"key1": "value1"}
        },
        "tags": ["positive-test"]
    },
    {
        "name": "Test 2",
        "data": {
            "var": "value 2",
            "list": ["index 0.2", "index 1.2"],
            "dict": {"key2": "value2"}
        },
        "tags": ["positive-test", "smoke-test"]
    }
]

# This is necessary in order to have syntax compatibility with Jinja
T_tc = DotDict(testcases[0])
