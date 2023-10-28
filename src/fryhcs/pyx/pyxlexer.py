from pygments.lexer import Lexer, bygroups, default, include, inherit
from pygments.lexers.python import PythonLexer
from pygments.lexers.javascript import JavascriptLexer
from pygments.token import Token, Name, Operator, Punctuation, String, Text, Whitespace, Comment
from parsimonious import NodeVisitor, BadGrammar
from fryhcs.pyx.grammar import grammar


def merge(children):
    result = []
    for child in children:
        if isinstance(child, list):
            new = merge(child)
            if result and new and result[-1][0] == new[0][0]:
                result[-1] = (new[0][0], result[-1][1]+new[0][1])
                new = new[1:]
            result += new
        elif isinstance(child, tuple):
            if len(child[1]) == 0:
                continue
            if result and result[-1][0] == child[0]:
                result[-1] = (child[0], result[-1][1]+child[1])
            else:
                result.append(child)
        else:
            raise BadGrammar(f"invalid: |{child}|, {type(child)}")
    return result

def an(text):
    return (Name.Attribute, text)

def en(text):
    if text[0].islower():
        return (Name.HtmlElement, text)
    else:
        return (Name.ComponentElement, text)

def n(text):
    return (Name, text)

def o(text):
    return (Operator, text)

def p(text):
    return (Punctuation, text)

def ep(text):
    return (Punctuation.ElementPunctuation, text)

def sep(text):
    return (Punctuation.ServerEmbedPunctuation, text)

def cep(text):
    return (Punctuation.ClientEmbedPunctuation, text)

def s(text):
    return (String, text)

def w(text):
    return (Whitespace, text)

def t(text):
    return (Text.HtmlText, text)

def py(text):
    return ('python', text)

def js(text):
    return ('javascript', text)

def fs(text):
    return ('fstring', text)

class PyxVisitor(NodeVisitor):
    def generic_visit(self, node, children):
        return children or node.text

    def visit_pyx_script(self, node, children):
        return merge(children)

    def visit_inner_pyx_script(self, node, children):
        return children

    def visit_pyx_script_item(self, node, children):
        return children[0]

    def visit_inner_pyx_script_item(self, node, children):
        return children[0]

    def visit_py_comment(self, node, children):
        return py(node.text)

    def visit_inner_pyx_brace(self, node, children):
        _l, script, _r = children
        return [py('{'), script, py('}')]

    def visit_pyx_embed(self, node, children):
        _l, script, _r = children
        return [sep('{'), script, sep('}')]
        
    def visit_triple_single_quote(self, node, children):
        return py(node.text)

    def visit_triple_double_quote(self, node, children):
        return py(node.text)

    def visit_single_quote(self, node, children):
        return node.text

    def visit_double_quote(self, node, children):
        return node.text

    def visit_py_simple_quote(self, node, children):
        return py(children[0])

    def visit_pyx_simple_quote(self, node, children):
        return s(children[0])

    def visit_js_simple_quote(self, node, children):
        return js(children[0])

    def visit_less_than_char(self, node, children):
        return py('<')

    def visit_py_normal_code(self, node, children):
        return py(node.text)

    def visit_inner_py_normal_code(self, node, children):
        return py(node.text)

    def visit_pyx_element_with_web_script(self, node, children):
        return children

    def visit_pyx_root_element(self, node, children):
        return children[0]

    def visit_pyx_element(self, node, children):
        return children[0]

    def visit_pyx_fragment(self, node, children):
        l, chs, r = children
        return [ep(l), chs, ep(r)]

    def visit_pyx_self_closing_element(self, node, children):
        l, name, attrs, s, r = children
        return [ep(l), name, attrs, w(s), ep(r)]

    def visit_pyx_paired_element(self, node, children):
        return children

    def visit_pyx_start_tag(self, node, children):
        l, name, attrs, s, r = children
        return [ep(l), name, attrs, w(s), ep(r)]

    def visit_pyx_end_tag(self, node, children):
        l, name, s, r = children
        return [ep(l), name, w(s), ep(r)]

    def visit_pyx_element_name(self, node, children):
        return en(node.text)

    def visit_space(self, node, children):
        return node.text

    def visit_maybe_space(self, node, children):
        return node.text

    def visit_pyx_attributes(self, node, children):
        return children

    def visit_pyx_spaced_attribute(self, node, children):
        s, attr = children
        return [w(s), attr]

    def visit_pyx_attribute(self, node, children):
        return children[0]

    def visit_pyx_embed_spread_attribute(self, node, children):
        l, s1, m, s2, script, r = children
        return [sep(l), py(s1), py(m), py(s2), script, sep(r)]

    def visit_pyx_kv_attribute(self, node, children):
        name, s1, e, s2, value = children
        return [name, w(s1), o(e), w(s2), value]

    def visit_pyx_novalue_attribute(self, node, children):
        return children[0]

    def visit_pyx_attribute_name(self, node, children):
        return an(node.text)

    def visit_pyx_attribute_value(self, node, children):
        return children[0]

    def visit_pyx_children(self, node, children):
        return children

    def visit_pyx_child(self, node, children):
        return children[0]

    def visit_pyx_js_embed(self, node, children):
        pyx_embed, s, js_embed = children
        return [pyx_embed, w(s), js_embed]

    def visit_fs_js_embed(self, node, children):
        lb, fs, rb, s, js = children
        return [sep(lb), fs, sep(rb), w(s), js]
        
    def visit_f_string(self, node, children):
        return fs(node.text)

    def visit_pyx_text(self, node, children):
        return t(node.text)

    def visit_no_embed_char(self, node, children):
        return t(node.text)

    def visit_maybe_web_script(self, node, children):
        return children

    def visit_web_script(self, node, children):
        s1, comma, s2, ls, attrs, s3, r1, script, r2 = children
        return [w(s1), p(comma), w(s2), ep('<'), en('script'), attrs, w(s3), ep(r1), script, ep('</'), en('script'), ep('>')]

    def visit_html_comment(self, node, children):
        return (Comment.HtmlComment, node.text)

    def visit_js_script(self, node, children):
        return js(node.text)

    def visit_js_embed(self, node, children):
        return children[0]

    def visit_local_js_embed(self, node, children):
        l, script, r = children
        return [cep(l), script, cep(r)]

    def visit_jsop_embed(self, node, children):
        l, script, r = children
        return [cep('('), sep('{'), script, sep('}'), cep(')')]


class FStringLexer(PythonLexer):
    tokens = {
        'btdqf': [
            include('rfstringescape'),
            include('tdqf'),
        ],
        'btsqf': [
            include('rfstringescape'),
            include('tsqf'),
        ],
    }


class PyxLexer(Lexer):
    name = 'Pyx'
    aliases = ['pyx']
    filenames = ['*.pyx']
    mimetypes = ['text/pyx']

    pylexer = PythonLexer()
    fslexer = FStringLexer()
    jslexer = JavascriptLexer()
    visitor = PyxVisitor()

    def get_tokens_unprocessed(self, text):
        tree = grammar.parse(text)
        i = 0
        for t, v in self.visitor.visit(tree):
            if t in Token:
                yield i, t, v
            elif t == 'python':
                for i1, t1, v1 in self.pylexer.get_tokens_unprocessed(v):
                    yield i+i1, t1, v1
            elif t == 'fstring':
                root = 'btsqf' if '"""' in v else 'btdqf'
                for i1, t1, v1 in self.fslexer.get_tokens_unprocessed(v, stack=(root,)):
                    yield i+i1, t1, v1
            elif t == 'javascript':
                for i1, t1, v1 in self.jslexer.get_tokens_unprocessed(v):
                    yield i+i1, t1, v1
            else:
                raise ValueError(f"Invalid type '{t}': '{v}'.")
            i += len(v)


if __name__ == '__main__':
    import sys
    from pygments.formatters.terminal import TerminalFormatter
    from pygments import highlight
    lexer = PyxLexer()
    fmter = TerminalFormatter()
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            data = f.read()
        #print(highlight(data, lexer, fmter))
        for t, v in lexer.get_tokens(data):
            print(t, v)
