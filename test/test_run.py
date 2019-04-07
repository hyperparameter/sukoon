from unittest.mock import Mock

from sukoon.kernel import SukoonKernel


def test_all():
    test_data = open("test/basic.py")

    test = ""
    for line in test_data:
        if line.startswith('## '):
            expected = line[3:]
            run_single(test, expected)
        else:
            test += line


def run_single(test, expected):
    kernel = SukoonKernel()
    send_response = Mock()
    kernel.send_response = send_response
    kernel.do_execute(test, False)

    print(send_response.call_args[0][2]['text'])
    #
    # print(test)
    # print(expected)
