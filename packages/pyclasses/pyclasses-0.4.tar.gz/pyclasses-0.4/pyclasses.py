import os
import ast
import pydot
import platform

class ClassDependencyVisitor(ast.NodeVisitor):
    def __init__(self, module_name):
        self.module_name = module_name
        self.dependencies = {}
        self.abstract_classes = {}
        self.class_docstrings = {}

    def visit_ClassDef(self, node):
        class_name = f"{node.name}"
        # class_name = f"{self.module_name}.{node.name}"
        bases = [f"{base.id}" for base in node.bases if isinstance(base, ast.Name)]
        # bases = [f"{self.module_name}.{base.id}" for base in node.bases if isinstance(base, ast.Name)]
        self.dependencies[class_name] = bases

        # 提取文档字符串
        docstring = ast.get_docstring(node)
        self.class_docstrings[class_name] = docstring if docstring else "No description available."

        is_abstract = False
        abstract_methods = []

        for stmt in node.body:
            if isinstance(stmt, ast.FunctionDef):
                if any(isinstance(decorator, ast.Name) and decorator.id == 'abstractmethod' for decorator in stmt.decorator_list):
                    is_abstract = True
                    arg_list = []
                    for arg in stmt.args.args:
                        arg_list.append(arg.arg)
                    arg_str = ", ".join(arg_list)
                    method_signature = f"{stmt.name}({arg_str})"
                    abstract_methods.append(method_signature)

        if is_abstract:
            self.abstract_classes[class_name] = abstract_methods

        self.generic_visit(node)


def parse_class_dependencies(source_code, module_name):
    tree = ast.parse(source_code)
    visitor = ClassDependencyVisitor(module_name)
    visitor.visit(tree)
    return visitor.dependencies, visitor.abstract_classes, visitor.class_docstrings


def parse_directory(directory):
    exclude_dirs = {'.venv', '__pycache__'}

    all_dependencies = {}
    all_abstract_classes = {}
    all_class_docstrings = {}
    for root, dirs, files in os.walk(directory):
        # 过滤掉需要跳过的目录
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                module_name = os.path.relpath(file_path, directory).replace(os.path.sep, '.')[:-3]  # .replace()用于路径分隔符，[:-3]去掉文件扩展名
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        source_code = f.read()
                    dependencies, abstract_classes, class_docstrings = parse_class_dependencies(source_code, module_name)
                    all_dependencies.update(dependencies)
                    all_abstract_classes.update(abstract_classes)
                    all_class_docstrings.update(class_docstrings)
                except (SyntaxError, UnicodeDecodeError) as e:
                    # print(f"Error parsing {file_path}: {e}")
                    continue
    return all_dependencies, all_abstract_classes, all_class_docstrings

def draw_class_dependency_graph(dependencies, abstract_classes, class_docstrings, dot_file, output_file, focus_class=None):
    graph = pydot.Dot(graph_type='digraph', rankdir='LR')

    def add_class_with_bases(cls):
        if cls in dependencies:
            bases = dependencies[cls]
        else:
            bases = []

        cls_quoted = f'"{cls}"'
        docstring = class_docstrings.get(cls, "No description available.")

        if cls in abstract_classes:
            label = "<{cls}<BR/><FONT POINT-SIZE='10'>Abstract Methods:<BR ALIGN='LEFT'/>".format(cls=cls) + "<BR ALIGN='LEFT'/>".join(abstract_classes[cls]) + "</FONT>>"
            graph.add_node(pydot.Node(cls_quoted, style="filled", fillcolor="lightgrey", label=label, tooltip=docstring, shape="box"))
        else:
            label = f"<{cls}>"
            graph.add_node(pydot.Node(cls_quoted, shape="box", label=label, tooltip=docstring))

        for base in bases:
            base_quoted = f'"{base}"'
            if not graph.get_node(base_quoted):
                if base in dependencies:
                    add_class_with_bases(base)
                else:
                    graph.add_node(pydot.Node(base_quoted))

            graph.add_edge(pydot.Edge(base_quoted, cls_quoted))

    if focus_class:
        if focus_class not in dependencies:
            print(f"Class {focus_class} not found in the parsed classes.")
            return

        add_class_with_bases(focus_class)
        for class_name, base_names in dependencies.items():
            if focus_class in base_names:
                add_class_with_bases(class_name)
    else:
        for cls in dependencies.keys():
            add_class_with_bases(cls)

    graph.write_raw(dot_file)
    try:
        graph.write_svg(output_file)
    except Exception as e:
        # print(f"Error generating SVG file: {e}")
        with open(dot_file, 'r') as df:
            print(df.read())


def open_image_file(output_file):
    if platform.system() == 'Darwin':
        os.system(f'open {output_file}')
    elif platform.system() == 'Windows':
        os.startfile(output_file)
    else:
        os.system(f'xdg-open {output_file}')

def main():
    import sys
    if len(sys.argv) not in [3, 4]:
        print("Usage: python create_class_diagram.py <directory> <output_file> [focus_class]")
        # for example
        print("Example: python create_class_diagram.py /path/to/your/project /tmp/pyclasses.svg [MYCLASS]")
        sys.exit(1)
    else:
        directory = sys.argv[1]
        output_file = sys.argv[2]
        dot_file = '/tmp/pyclasses.dot'
        focus_class = sys.argv[3] if len(sys.argv) == 4 else None

        dependencies, abstract_classes, class_docstrings = parse_directory(directory)
        # print(f"All dependencies: {dependencies}")
        # print(f"All abstract classes: {abstract_classes}")
        draw_class_dependency_graph(dependencies, abstract_classes, class_docstrings, dot_file, output_file, focus_class)
        # print(f"Class diagram saved to {output_file}")
        open_image_file(output_file)

if __name__ == '__main__':
    main()