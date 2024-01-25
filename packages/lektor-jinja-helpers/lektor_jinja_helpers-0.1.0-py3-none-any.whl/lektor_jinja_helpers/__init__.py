from __future__ import annotations

import importlib
from types import SimpleNamespace
from typing import Any

from lektor.pluginsystem import Plugin

from . import db_helpers
from . import html_helpers
from . import misc_helpers
from .ansible import import_ansible_filters_and_tests

FILTERS = {
    "adjust_heading_levels": html_helpers.adjust_heading_levels,
    "excerpt_html": html_helpers.excerpt_html,
    "lineage": db_helpers.lineage,
    "descendants": db_helpers.descendants,
    "call": misc_helpers.call,
    "flatten": misc_helpers.flatten,
}
TESTS = {
    "call": misc_helpers.call,
}
GLOBALS = {
    "import_module": importlib.import_module,
}


class JinjaHelpersPlugin(Plugin):  # type: ignore[misc]
    name = "jinja-helpers"
    description = "A collection of Jinja2 filters and globals for Lektor"

    def on_setup_env(self, **extra: Any) -> None:
        jinja_env = self.env.jinja_env
        jinja_env.filters.update({f"helpers.{name}": f for name, f in FILTERS.items()})
        jinja_env.tests.update({f"helpers.{name}": f for name, f in TESTS.items()})

        jinja_env.globals["helpers"] = helpers = SimpleNamespace()
        for name, f in GLOBALS.items():
            setattr(helpers, name, f)

        import_ansible_filters_and_tests(jinja_env)
