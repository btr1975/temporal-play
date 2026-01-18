"""
rendering utilities
"""

from jinja2 import Environment, select_autoescape, BaseLoader


def get_jinja2_environment() -> Environment:
    """Get the basic Jinja2 Rendering environment

    :rtype: Environment
    :return: The basic Jinja2 Rendering environment
    """
    render_env = Environment(
        autoescape=select_autoescape(enabled_extensions=("html", "xml", "jinja2"), default_for_string=True),
        loader=BaseLoader(),
        lstrip_blocks=True,
        trim_blocks=True,
        enable_async=True,
    )

    return render_env


async def render_jinja2_template(template: str, variable_data: dict) -> str:
    """Render a Jinja2 template with the provided variable data

    :type template: String
    :param template: The Jinja2 template in a string format
    :type variable_data: dict
    :param variable_data: The instance data

    :rtype: String
    :return: The rendered template
    """
    render_env = get_jinja2_environment().from_string(template)

    rendering = await render_env.render_async(variable_data)

    return rendering
