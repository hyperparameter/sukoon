import itertools
from unittest.mock import Mock

from sukoon.kernel import SukoonKernel


def test_all():
    test_data = open("test/basic.py")

    test = ''
    expected = ''
    for line in itertools.chain(test_data, ['']):
        if line.startswith('##'):
            expected += line[2:].lstrip()
        elif line.strip() == '' and test and expected:
            run_single(test, expected)
            test = ''
            expected = ''
        else:
            test += line


def run_single(test, expected):
    kernel = SukoonKernel()
    send_response = Mock()
    kernel.send_response = send_response
    kernel.do_execute(test, False)

    response = send_response.call_args[0][2]['text']
    assert expected == response
