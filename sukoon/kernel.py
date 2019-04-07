import ast

from ipykernel.kernelbase import Kernel


class SukoonKernel(Kernel):
    implementation = 'Echo'
    implementation_version = '1.0'
    language = 'no-op'
    language_version = '0.1'
    language_info = {
        'name': 'Any text',
        'mimetype': 'text/plain',
        'file_extension': '.txt',
    }
    banner = "Echo kernel - as useful as a parrot"
    responses = [None, "1100", 3]
    index = 0

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        try:
            tree = ast.parse(code)
            lines = []
            pretty_print(tree, lines)
            result = '\n'.join(lines)
        except Exception as e:
            result = e

        if not silent:
            # stream_content = {'name': 'stdout', 'text': self.responses[self.index % len(self.responses)]}
            stream_content = {'name': 'stdout', 'text': str(result)}
            self.send_response(self.iopub_socket, 'stream', stream_content)
            self.index += 1

        return {
            'status': 'ok',
            # The base class increments the execution count
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {},
            }


def pretty_print(tree: ast.AST, result=None, depth=0):
    if result is None:
        result = []
    value = tree.__class__.__name__
    arguments = []
    for name, field in ast.iter_fields(tree):
        arguments.append(f'{name}={field}')
    argument_string = ', '.join(arguments)
    value += f'({argument_string})'

    result.append("  " * depth + value)

    for child in ast.iter_child_nodes(tree):
        pretty_print(child, result, depth + 1)


class PrintVisitor(ast.NodeVisitor):
    def __init__(self):
        self.result = ""

    def visit(self, node: ast.AST):
        self.result += str(node.__class__.__name__) + '\n'
        return super().visit(node)


if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=SukoonKernel)
