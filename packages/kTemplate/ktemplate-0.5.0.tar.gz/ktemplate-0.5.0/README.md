# kTemplate

[![ci-badge]][ci-url] [![pypi-badge]][pypi-url] [![MIT-badge]][MIT-url] [![black-badge]][black-url]

> pythonic way to create HTML/XML/SVG

- create tags in pure python
- use context manager for tag hierarchy
- no external dependencies
- read the [docs]

## Quick Start

Installation: `pip install kTemplate`

```python
from kTemplate import div, img, form, label, input, del_
from kTemplate import Tag  # for creating custom element

# === html element ===
tag = div(img(src="url"), id="bar")
print(tag)  # <div id="bar"><img src="url"/></div>

# === custom element ===
my_tag = Tag("MyTag", child="foo", attr="bar")
print(my_tag)  # <MyTag attr="bar">foo</MyTag>

# == ⭐️ context manager ⭐️ ==
with form() as f:
    label("foo", for_="bar")  # python keyword 'for' -> 'for_'
    input(None, name="bar", type="checkbox", value="baz")

print(f.pretty())
# <form>
#     <label for="bar">foo</label>
#     <input name="bar" type="checkbox" value="baz"/>
# </form>

# === add content and attributes to existing tag ===
# position args -> attribute w/o value
# python keyword 'class' -> 'class_'
tag = div(class_="foo") 
# python keyword 'del' -> 'del_'
tag.add(del_("bar"), "m-2", "rounded", id="baz") 
print(tag)  
# <div m-2 rounded class="foo" id="baz"><del>bar</del></div>
```

more examples could be found on [references] and [tests]

## Limitations

- python keywords
    - tag attributes: `class` -> `class_`;  `for` -> `for_`
    - tag name: `del` -> `del_`
- `pretty()` method doesn't support attribute w/o value
    - eg. use kwargs `selected=""` instead of positional args `selected`

## Motivation

When working with HTML, instead of separating python and template files like this:

```html
<ul id="navigation">
    {% for item in navigation %}
    <li><a href="{{ item.href }}">{{ item.caption }}</a></li>
    {% endfor %}
</ul>
```

I prefer a pythonic approach like this:

```python
with ul(id="navigation") as nav:
    for item in navigation:
        li(a(item.caption, href=item.href))
```

It provides full intellisense, type checking, and all language supports from the text editor. A much better DX.

## Need Help?

[![git-logo] github issue][github issue]

[![x-logo] posts][x-post]

[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-url]: https://github.com/psf/black
[ci-badge]: https://github.com/hoishing/kTemplate/actions/workflows/ci.yml/badge.svg
[ci-url]: https://github.com/hoishing/kTemplate/actions/workflows/ci.yml
[docs]: https://hoishing.github.io/kTemplate
[git-logo]: https://api.iconify.design/bi/github.svg?color=%236FD886&width=20
[github issue]: https://github.com/hoishing/kTemplate/issues
[MIT-badge]: https://img.shields.io/github/license/hoishing/kTemplate
[MIT-url]: https://opensource.org/licenses/MIT
[pypi-badge]: https://img.shields.io/pypi/v/ktemplate
[pypi-url]: https://pypi.org/project/ktemplate/
[references]: https://github.com/hoishing/kTemplate/references
[tests]: https://github.com/hoishing/kTemplate/tree/main/tests
[x-logo]: https://api.iconify.design/ri:twitter-x-fill.svg?width=20&color=DarkGray
[x-post]: https://x.com/hoishing
