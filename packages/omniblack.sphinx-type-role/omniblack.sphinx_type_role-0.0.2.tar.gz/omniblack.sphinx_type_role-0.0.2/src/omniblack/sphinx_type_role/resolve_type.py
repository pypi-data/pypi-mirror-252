from importlib import import_module
from itertools import chain
from types import ModuleType
from ast import (
    Attribute,
    Name,
    NodeVisitor,
    parse,
    unparse,

    Add,
    Sub,
    Mult,
    Div,
    FloorDiv,
    Mod,
    Pow,
    LShift,
    RShift,
    BitOr,
    BitXor,
    BitAnd,
    MatMult,
)

from docutils import nodes
from sphinx import addnodes as sphinx_nodes


def get_namespaces(env):
    if doc_module_name := env.ref_context.get('py:module'):
        doc_module = import_module(doc_module_name)
        if cls_name := env.ref_context.get('py:class'):

            cls = getattr(doc_module, cls_name)

            containing_module_name = cls.__module__
            containing_module = import_module(containing_module_name)

            return (
                containing_module.__dict__,  # globals
                cls.__dict__,  # locals
            )
        else:
            return (doc_module.__dict__,)
    else:
        return tuple()


def transform(rawtext, text, env, namespaces):
    ast = parse(text)

    doc_nodes = AstToDoc(text, env, namespaces).visit(ast)

    return [nodes.literal(rawtext, '', *doc_nodes)]


class AstToDoc(NodeVisitor):
    def __init__(self, source, env, namespaces):
        self.env = env
        self.namespaces = namespaces
        self.tuple_parens = True

    def visit(self, node):
        cls_name = type(node).__name__
        handler = getattr(self, f'visit_{cls_name}', self.generic_visit)
        return handler(node)

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_Module(self, node):
        return [
            self.visit(child)
            for child in node.body
        ]

    def visit_Expression(self, node):
        return [self.visit(node)]

    def visit_Constant(self, node):
        return nodes.Text(str(node.value))

    def sep_list(self, iter, sep):
        first = True
        for item in iter:
            if not first:
                yield nodes.Text(sep)

            yield item

            first = False

    def comma_list(self, iter):
        yield from self.sep_list(iter, ', ')

    def dot_list(self, iter):
        yield from self.sep_list(iter, '.')

    def visit_Subscript(self, node):
        self.tuple_parens = False
        try:
            return nodes.inline(
                '',
                '',
                self.visit(node.value),
                nodes.inline('', '['),
                self.visit(node.slice),
                nodes.inline('', ']'),
            )
        finally:
            self.tuple_parens = True

    def visit_Tuple(self, node):
        children = []

        if self.tuple_parens:
            children.append(nodes.Text('('))

        els = (
            self.visit(el)
            for el in node.elts
        )

        children.extend(self.comma_list(els))

        if self.tuple_parens:
            children.append(nodes.Text(')'))

        return nodes.inline('', '', *children)

    def visit_Call(self, node):
        func_node = self.visit(node.func)
        args = (
            self.visit(arg)
            for arg in node.args
        )

        kwargs = (
            (nodes.Text(kwarg.arg), nodes.Text('='), self.visit(kwarg.value))
            for kwarg in node.keywords
        )

        args_iter = self.comma_list(chain(args, kwargs))

        args_list = []

        for item in args_iter:
            if isinstance(item, tuple):
                args_list.extend(item)
            else:
                args_list.append(item)

        return nodes.inline(
            '',
            '',
            func_node,
            nodes.Text('('),
            *args_list,
            nodes.Text(')'),
        )

    def generic_visit(self, node):
        cls_name = type(node).__name__
        raise NotImplementedError(
            f'{cls_name} can not be turned to doc nodes.',
        )

    def flatten_attr(self, node):
        segs = []

        while node:
            segs.append(node.attr)
            if isinstance(node.value, Attribute):
                node = node.value
            else:
                segs.append(node.value)
                node = None

        return list(reversed(segs))

    def visit_Attribute(self, node):
        attr_str = unparse(node)
        attr_segs = self.flatten_attr(node)

        if not isinstance(attr_segs[0], Name):
            return nodes.Text(attr_str)
        else:
            name_node = attr_segs[0]
            mod_name = attr_segs[0].id
            attr_segs[0] = mod_name

        # if the first part of the attr access is a module
        # assume this is external refrence
        try:
            import_module(mod_name)
        except ImportError:
            external = True
        else:
            external = False

        unresolved = sphinx_nodes.pending_xref_condition(
            '',
            '',
            self.visit(name_node),
            nodes.Text('.'),
            *self.dot_list(
                nodes.Text(seg)
                for seg in attr_segs[1:]
            ),
            condition='*',
        )

        resolved = sphinx_nodes.pending_xref_condition(
            '',
            '',
            nodes.Text(attr_segs[-1]),
            condition='resolved',
        )

        xref = sphinx_nodes.pending_xref(
            '',
            resolved,
            unresolved,
            refdomain='py',
            reftarget=attr_str,
            reftype='obj',
        )

        xref['refspecific'] = True
        if not external:
            xref['py:module'] = self.env.ref_context.get('py:module')

        return xref

    def visit_Name(self, node):
        try:
            live_value = eval(node.id, *self.namespaces)
        except NameError:
            return nodes.Text(node.id)

        name = getattr(live_value, '__qualname__', node.id)
        if isinstance(live_value, ModuleType):
            mod = live_value.__name__
        else:
            mod = getattr(live_value, '__module__')

        if not mod:
            mod = self.env.ref_context.get('py:module')

        full_name = f'{mod}.{name}'

        unqualified = name.split('.')[-1]

        resolved = sphinx_nodes.pending_xref_condition(
            '',
            '',
            nodes.Text(unqualified),
            condition='resolved',
        )

        unresolved = sphinx_nodes.pending_xref_condition(
            '',
            '',
            nodes.Text(full_name),
            condition='*',
        )
        xref = sphinx_nodes.pending_xref(
            '',
            resolved,
            unresolved,
            refdomain='py',
            reftarget=name,
            reftype='obj',
        )

        xref['refspecific'] = True
        xref['py:module'] = mod

        return xref

    def visit_BinOp(self, node):
        return nodes.inline(
            '',
            '',
            self.visit(node.left),
            nodes.Text(' '),
            nodes.Text(self.get_bin_op(node.op)),
            nodes.Text(' '),
            self.visit(node.right),
        )

    def get_bin_op(self, op):
        match op:
            case Add():
                return '+'

            case Sub():
                return '-'

            case Mult():
                return '*'

            case Div():
                return '/'

            case FloorDiv():
                return '//'

            case Mod():
                return '%'

            case Pow():
                return '**'

            case LShift():
                return '<<'

            case RShift():
                return '>>'

            case BitOr():
                return '|'

            case BitXor():
                return '^'

            case BitAnd():
                return '&'

            case MatMult():
                return '@'
