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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.namespace = {}
        self.locals = {}

    def do_execute(self, code, silent, store_history=True, user_expressions=None,
                   allow_stdin=False):
        tree = ast.parse(code)
        # debug_print(tree)
        transform(tree)
        try:
            exec(compile(tree, filename="<ast>", mode='exec'), self.namespace, self.locals)
        except Exception as e:
            result = e
        else:
            result = ''
            assign_ids = get_assign_ids(tree)
            for name in assign_ids:
                value = self.locals[name]
                result += f'{name} = {value}\n'


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


def transform(tree):
    if isinstance(tree, ast.Module):
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                args = [arg.arg for arg in node.args.args]
                assign = get_function_call(node)
                tree.body.append(assign)
    ast.fix_missing_locations(tree)


def get_function_call(function_node: ast.FunctionDef):
    function_name = function_node.name
    variable_name = None
    for child in function_node.body:
        if isinstance(child, ast.Return):
            if isinstance(child.value, ast.Name):
                variable_name = child.value.id
    if variable_name is None:
        variable_name = get_new_variable_name()
    return ast.Assign(targets=[ast.Name(id=variable_name, ctx=ast.Store())],
                      value=ast.Call(func=ast.Name(id=function_name, ctx=ast.Load()),
                                     args=[],
                                     keywords=[]))


_variable_count = 0


def get_new_variable_name():
    global _variable_count
    _variable_count += 1
    return f'_{_variable_count}'




def get_assign_ids(tree):
    ids = []
    if isinstance(tree, ast.Module):
        for node in tree.body:
            if isinstance(node, ast.Assign):
                target = node.targets[0]
                if isinstance(target, ast.Name):
                    ids.append(target.id)
                elif isinstance(target, ast.Tuple):
                    for child in target.elts:
                        if isinstance(child, ast.Name):
                            ids.append(child.id)

    return ids


def debug_print(tree):
    lines = []
    pretty_print(tree, lines)
    print('\n' + '\n'.join(lines))


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
