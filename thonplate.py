class BaseTag(object):
    children = None
    parent = None
    name = None
    indent_string = '  '

    def __init__(self):
        self.children = []
        self.parent = None

    def __str__(self):
        return self.render()

    def add(self, *args):
        for child in args:
            if isinstance(child, (str, unicode, long, int, float)):
                self.children.append(StringTag(child))
            elif isinstance(child, BaseTag):
                self.children.append(child)
            elif child is None:
                # default args are None, so ignoring them is probably the best thing to do
                pass
            elif isinstance(child, (list, tuple)) or child.__class__.__name__ == 'generator':
                for grandchild in child:
                    self.children.append(grandchild)
            else:
                raise Exception("Cannot add item to %s of type %s" % (self.name, child.__class__))
        return self

    def add_if(self, condition, *args):
        if condition:
            return self.add(*args)
        else:
            return self

    def render(self, depth=0):
        return ''

    def _get_indent(self, depth):
        return self.indent_string * depth


class Template(BaseTag):
    template = None
    head_tags = None

    def __init__(self):
        super(Template, self).__init__()
        self.title = None
        self.head_tags = []

    def render(self, depth=-1):
        str = ''
        for child in self.children:
            str += child.render(depth + 1)

        return str

    def get_head_tags(self):
        return self.head_tags

    def add_head_tag(self, tag):
        self.head_tags.append(tag)

    def add_head_tags(self, *tags):
        for tag in tags:
            self.head_tags.append(tag)

    def get_title(self):
        return self.title


class Tag(BaseTag):
    name = None
    attrs = None

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__()
        self.attrs = {}
        for arg in args:
            if isinstance(arg, dict):
                for key, value in arg.iteritems():
                    self.attrs[key] = value
            else:
                raise Exception('Do not recognize arg of type %s' % arg.__class__)

        for key, value in kwargs.iteritems():
            if key == 'cls':
                key = 'class'
            if value is None:
                value = ''
            self.attrs[key] = value

    def get_attr_string(self):
        attr_string = ''
        for key, value in self.attrs.iteritems():
            attr_string += ' %s="%s"' % (key, value)
        return attr_string

    def get_open_tag(self):
        attr_string = self.get_attr_string()
        return '<%s%s>' % (self.name, attr_string)

    def get_self_closing_tag(self):
        attr_string = self.get_attr_string()
        return '<%s%s/>' % (self.name, attr_string)

    def get_close_tag(self):
        return '</%s>' % self.name

    def render(self, depth=0):
        indent = self._get_indent(depth)
        if len(self.children) == 0:
            str = indent + self.get_self_closing_tag() + '\n'
        else:
            str = indent + self.get_open_tag() + '\n'
            for child in self.children:
                str += child.render(depth + 1)
            str += indent + self.get_close_tag() + '\n'
        return str


class StringTag(Tag):
    value = None
    name = 'string_tag'

    def __init__(self, value):
        self.value = unicode(value)
        super(StringTag, self).__init__()

    def render(self, depth=0):
        return self.value


class CloseTagRequired(Tag):
    def render(self, depth=0):
        indent = self._get_indent(depth)
        result = indent + self.get_open_tag()
        if len(self.children) == 1 and isinstance(self.children[0], StringTag):
            # if there is only one child and it's a string, do not pad it with whitespace
            for child in self.children:
                result += child.render(depth + 1)
            result += self.get_close_tag() + '\n'
        elif len(self.children) > 0:
            result += '\n'
            for child in self.children:
                result += child.render(depth + 1)
            result += indent + self.get_close_tag() + '\n'
        else:
            result += self.get_close_tag() + '\n'

        return result


class a(CloseTagRequired):
    name = 'a'


class b(CloseTagRequired):
    name = 'b'


class button(CloseTagRequired):
    name = 'button'


class body(Tag):
    name = 'body'


class em(CloseTagRequired):
    name = 'em'


class div(CloseTagRequired):
    name = 'div'


class form(Tag):
    name = 'form'


class h1(CloseTagRequired):
    name = 'h1'


class h2(CloseTagRequired):
    name = 'h2'


class h3(CloseTagRequired):
    name = 'h3'


class h4(CloseTagRequired):
    name = 'h4'


class h5(CloseTagRequired):
    name = 'h5'


class h6(CloseTagRequired):
    name = 'h6'


class hr(Tag):
    name = 'hr'


class head(Tag):
    name = 'head'


class html(Tag):
    name = 'html'


class i(CloseTagRequired):
    name = 'i'


class label(CloseTagRequired):
    name = 'label'


class li(Tag):
    name = 'li'


class link(Tag):
    name = 'link'


class meta(Tag):
    name = 'meta'


class nav(Tag):
    name = 'nav'


class ol(CloseTagRequired):
    name = 'ol'


class p(CloseTagRequired):
    name = 'p'


class pre(CloseTagRequired):
    name = 'pre'


class strong(CloseTagRequired):
    name = 'strong'


class script(CloseTagRequired):
    name = 'script'


class span(CloseTagRequired):
    name = 'span'


class textarea(CloseTagRequired):
    name = 'textarea'


class title(CloseTagRequired):
    name = 'title'


class ul(Tag):
    name = 'ul'


class input(Tag):
    name = 'input'


class css(link):
    def __init__(self, url, *args):
        super(css, self).__init__(*args)
        self.attrs['href'] = url
        self.attrs['type'] = 'text/css'
        self.attrs['rel'] = 'stylesheet'


class js(script):
    def __init__(self, url, *args, **kwargs):
        super(js, self).__init__(*args, **kwargs)
        self.attrs['src'] = url
        self.attrs['type'] = 'text/javascript'
        self.attrs['charset'] = 'utf-8'


class doctype(Tag):
    name = '!DOCTYPE'

    def render(self, depth=0):
        attr_string = ''
        for key, value in self.attrs.iteritems():
            if value is None or value == '':
                attr_string += ' %s' % key
            else:
                attr_string += ' %s="%s"' % (key, value)
        indent = depth * Tag.indent_string

        return '%s<!DOCTYPE%s>\n\n' % (indent, attr_string)
