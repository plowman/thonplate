thonplate
=========

HTML templating using only python.

Usage Example
=============
```python
from thonplate import *

class BaseTemplate(Template):
    def __init__(self):
        super(BaseTemplate, self).__init__()

        self.add(
            doctype(html=None),
            html(lang='en').add(
                head().add(
                    title().add('Welcome to my Page'),
                    meta(charset='UTF-8'),
                    css('/static/css/common.css'),
                    js('/static/js/jquery.1.10.2.min.js'),
                    link(type='image/png', rel='icon', href='/static/img/favicon.ico'),
                ),
                body().add(
                    h1().add('This is my website. I hope you like it!')
                )
            )
        )

if __name__ == '__main__':
    print BaseTemplate().render()
```

The above would output:
```html
<!DOCTYPE html>

<html lang="en">
  <head>
    <title>Welcome to my Page</title>
    <meta charset="UTF-8"/>
    <link href="/static/css/common.css" type="text/css" rel="stylesheet"/>
    <script src="/static/js/jquery.1.10.2.min.js" charset="utf-8" type="text/javascript"></script>
    <link href="/static/img/favicon.ico" type="image/png" rel="icon"/>
  </head>
  <body>
    <h1>This is my website. I hope you like it!</h1>
  </body>
</html>
```
