# Lektor-jinja-helpers

[![PyPI version](https://img.shields.io/pypi/v/lektor-jinja-helpers.svg)](https://pypi.org/project/lektor-jinja-helpers/)
[![PyPI Supported Python Versions](https://img.shields.io/pypi/pyversions/lektor-jinja-helpers.svg)](https://pypi.python.org/pypi/lektor-jinja-helpers/)
[![GitHub license](https://img.shields.io/github/license/dairiki/lektor-jinja-helpers)](https://github.com/dairiki/lektor-jinja-helpers/blob/master/LICENSE)
[![Test status badge](https://img.shields.io/github/actions/workflow/status/dairiki/lektor-jinja-helpers/ci.yml?label=tests)](https://github.com/dairiki/lektor-jinja-helpers/actions/workflows/ci.yml)

This is a [Lektor plugin] that adds an assortment of filters, tests,
and globals to Lektor’s Jinja environment.

These additions are hopefully useful in Lektor templates.

Additionally, any [Ansible] filter or test plugins that may be
installed in the Python environment will also be made available.
Ansible provides a great variety of [filters][ansible filters] and
[tests][ansible tests], some of which may be useful in Lektor
templates.

## “Namespacing”

To avoid namespace pollution, currently, all of the bits added to the
jinja environment by this plugin are added under the `helpers`
namespace. That is, all the names of these filters, tests and globals
start with `helpers.`

Any filters and tests from ansible plugins are made available under
their fully qualified names (e.g. `ansible.builtin.flatten`).

## Jinja Filters

### helpers.adjust\_heading\_levels(html\_text, demote=0, normalize=True)

This filter expects HTML text as input. It can be used both to
normalize the HTML heading hierarchy in the text, as well as to
“demote” the heading levels by a fixed amount.

This is useful when, e.g., a [markdown field] is to be included on a
page that already has some heading. E.g. the following template would
ensure that the headings with `div.markdown-body` start correctly at
`<h2>`.

```j2
<main>
  <h1>{{ this.title }}</h1>
  <div class="markdown-body">
  {{ this.body | helpers.adjust_heading_levels(demote=1) }}
  <div>
</main>
```

First (by default) it normalizes the HTML heading levels in the text, so that:

- The first heading is always `<h1>`.

- There are no "gaps" in the heading hierarchy: for every heading of
  depth greater than `<h1>` there will exist a parent heading of the
  preceding level. E.g. for every `<h3>` in the normalized text, there
  will be an extant `<h2>` parent preceding it.

This normalization may be prevented by passing `normalize=false` to
the filter.

Then, optionally, the filter *demotes* (increases the level) of each
heading by a fixed amount. The value of the `demote` argument
specifies the number of levels the headings are to be increased.

Headings are never demoted below `<h6>`. This is because `<h7>` is not
a valid HTML5 element. Instead, an [aria-level] attribute is set on
deeply demoted headings: in place of `<h7>`, an `<h6 aria-level="7">`
is used.

### helpers.excerpt\_html(html\_text, min\_words=50, cut\_mark=r"(?i)\s*more\b")

This filter expects HTML text as input and returns a possibly truncated
version of that text. It truncates the input in one of two ways:

1. This function first looks for an HTML comment whose text matches
   the regular expression **cut-mark**. (The default value matches
   comments beginning with the word “more”.) If such a comment is
   found, all text after that comment is deleted, and the result is
   returned. The truncation is done in an HTML-aware manner. The
   result will be a valid HTML fragment: it will not contain dangling
   tags, etc.

   Passing `cut_mark=none` will disable the search for a cut-mark.

2. If no cut-mark is found, then the text is truncated at the first
   block element such that there are at least ``min_words`` words in
   the preserved (preceding) text.

If no suitable truncation point can be found, the original text is returned.

This filter provides a thin wrapper around the [excerpt-html] library.


### helpers.lineage(include\_self=True)

This filter expects a Lektor DB *source object* as input, and returns
a generator generator that yields first (optionally) the input
object, then the object's parent, and so on up the tree.

The `include_self` parameter controls whether the input object is
included in the results.

As an example, this can be used to determine if any of a pages ancestors is undiscoverable:

```j2
{% if this | helpers.lineage | rejectattr('is_discoverable') | first is defined -%}
  This page or one of its ancestors is marked undiscoverable!
{% endif -%}
```

### helpers.descendants(include\_undiscoverable=False, include\_hidden=False, include\_self=True, depth\_first=False)

Iterate over descendant pages.

This Jinja filter expects a Lektor Page as input and returns a
generator which yields first (optionally) the input page, then the
page's descendants.

The `include_self` parameter controls whether the input page
is included in the results.

The `depth_first` parameter controls the traversal order.  By
default, the traversal is breadth-first.

The `include_hidden` and `include_undiscoverable` parameters control
whether hidden and undiscoverable pages are included in the result.
Note that, since hidden pages are always undiscoverable, to include hidden pages,
one must set `include_undiscoverable` as well as `include_hidden`.

As an example, here we iterate over all images contained by all discoverable
pages on the site. (This may be a slow operation if there are many pages and/or images.)

```j2
<ul>
  {% for image in site.root | helpers.descendants | map(attribute="attachments.images") | helpers.flatten -%}
    <li><img src="{{ image | url }}"></li>
  {% endfor -%}
</ul>
```

### helpers.flatten(depth=None)

Flatten a nested structure of iterables.

This filters expects an iterable as input and returns a generator.
Any iterables contained within the input will be flattened to the top level.

As an example,

    [["foo", "bar"], ["baz"]] | helpers.flatten

will return a generator that will yield ``"foo"``, ``"bar"``, ``"baz"``.

The ``depth`` parameter (if not ``None``) limits the maximum depth of
flattening performed.  If ``depth`` is less than or equal to zero, no flattening
is performed.

Strings and ``Mapping``s (though, technically, they are *iterables*)
are not flattened.

### helpers.call(function, \*args, \*\*kwargs)

This helper can be used to convert a global function to a [jinja
filter]. This is primarily useful when one would like to use a global
function in a [`map`][map filter] filter.

As a contrived example

```j2
{% for r in range(3) | map("helpers.call", range, 4) -%}
  {{ r | join(",") }}
{% endfor -%}
```

will produce

```
0,1,2,3
1,2,3
2,3
```

## Jinja Tests

### helpers.call(function, \*args, \*\*kwargs)

`Helpers.call` can also be used to convert a global function to a
Jinja test.  This is useful when one would like to use a global
function in a [`select`][select filter] filter or one of its
relatives.

Another contrived example:

```j2
{% set isupper = "".__class__.isupper -%}
{{ ["lower", "UPPER"] | select("helpers.call", isupper) | join(",") }}
```

will produce `"UPPER"`.

## Jinja Globals

### helpers.import\_module(name, package=none)

[`Importlib.import_module`][import-module] from the Python standard library is made available to Jinja templates as `helpers.import_module`. This foot-gun allows access to nearly any python value from within a template.

E.g., to access the current date

```j2
{% set date = helpers.import_module("datetime").date -%}
{{ date.today().isoformat() }}
```

## Ansible Filter and Test Plugins

If [Ansible] is installed in the Python environment, whatever ansible
[filter][ansible filters] and [test][ansible tests] plugins that can
be found will be made available to the Jinja environment.

Installing [ansible-core] (total install size ~30M) in your virtualenv
will provide access to the filters and tests from the
`ansible.builtin` module.  Installing [ansible] (total install size
~500M) will provide access to all the standard modules.

## Ideas / To Do

- Perhaps the *namespacing* of all new features under the `helpers.`
  prefix should be made configurable.

- It would be nice to avoid the weight of [BeautifulSoup4] and
  [html5lib] if possible.  (But note that [excerpt-html] currently
  uses both of those libraries.)

- Perhaps, instead of the `helpers.descandants` filter, a
  `descendants_query` global, which returns a `Query` object (with
  `.filter`, `.include_undiscoverable`, &c. methods) would present a
  more Lektor-uniform API

- Make defaults (e.g. for ``excerpt_html``) configurable via Lektor plugin config file.

## Author

Jeff Dairiki <dairiki@dairiki.org>


[Lektor]: <https://pypi.org/project/lektor/>
[Jinja]: <https://jinja.palletsprojects.com/en/3.1.x/>
[Lektor plugin]: <https://www.getlektor.com/docs/plugins/>
[markdown field]: <https://www.getlektor.com/docs/api/db/types/markdown/>
[aria-level]: <https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-level>
[html5lib]: <https://pypi.org/project/html5lib/>
[BeautifulSoup4]: <https://pypi.org/project/beautifulsoup4/>
[excerpt-html]: <https://pypi.org/project/excerpt-html/> (Excerpt-html at PyPI)
[jinja filter]: <https://jinja.palletsprojects.com/en/3.1.x/templates/#id11>
[map filter]: <https://jinja.palletsprojects.com/en/3.1.x/templates/#jinja-filters.map>
[select filter]: <https://jinja.palletsprojects.com/en/3.1.x/templates/#jinja-filters.select>
[import-module]: <https://docs.python.org/3/library/importlib.html#importlib.import_module>

[Ansible]: <https://pypi.org/project/ansible/>
[ansible-core]: <https://pypi.org/project/ansible-core/>
[ansible filters]: <https://docs.ansible.com/ansible/latest/collections/index_filter.html>
[ansible tests]: <https://docs.ansible.com/ansible/latest/collections/index_test.html>
