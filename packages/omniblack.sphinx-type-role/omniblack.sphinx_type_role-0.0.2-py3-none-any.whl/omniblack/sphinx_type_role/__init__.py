from .resolve_type import get_namespaces, transform


def type_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    env = inliner.document.settings.env
    namespaces = get_namespaces(env)
    return transform(rawtext, text, env, namespaces), []


def setup(app):
    """Install the plugin.

    :param app: Sphinx application context.
    """
    app.add_role('type', type_role)
    return
