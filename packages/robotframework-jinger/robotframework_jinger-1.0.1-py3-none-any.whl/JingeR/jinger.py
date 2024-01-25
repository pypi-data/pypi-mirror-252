import click
from jinja2 import Template, DebugUndefined

import importlib.util
import os
import re
import shutil
import sys
from pathlib import Path
from types import ModuleType


jinger_package_path = Path(os.path.abspath(__file__)).parent


class CustomUndefined(DebugUndefined):
    __slots__ = ()

    def _fail_with_undefined_error(self, *args, **kwargs):
        return f"Undefined variable: {self._undefined_name!r}"

    def __str__(self) -> str:
        return f"Undefined variable: {self._undefined_name!r}"


def import_module_from_path(module_path: Path):
    spec = importlib.util.spec_from_file_location("custom_module", module_path)
    custom_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(custom_module)
    return custom_module


@click.group()
@click.version_option(package_name="robotframework_jinger", prog_name='jinger')
def cli():
    """
    jinger generates data-driven test cases using Jinja templates
    """
    pass


@cli.command('init', short_help='Create the initial template and testdata file')
def init():
    jinga_template_path = os.path.abspath(jinger_package_path / "templates/testcase.jinja.robot")
    testdata_path = os.path.abspath(jinger_package_path / "templates/testdata.py")
    shutil.copy(jinga_template_path, os.getcwd())
    shutil.copy(testdata_path, os.getcwd())


@cli.command('run', short_help='Generate a testsuite from a template and a testdata file')
@click.option('--debug', is_flag=True, help='Print the placeholders in the generated testsuite')
@click.argument('jinja_template')
@click.argument('test_data')
@click.argument('testsuite')
def run(debug, jinja_template: str, test_data: str, testsuite: str):
    """
    Given a Jinja template and a testdata file generate a testsuite.
    
    Example: jinger run template.jinja.robot testdata.py testsuite.robot
    """

    try:
        test_data_module = import_module_from_path(Path(test_data))
    except ImportError:
        print(f"Error: The module {test_data} could not be imported")
        sys.exit(1)

    var_names = {var for var in dir(test_data_module) if not var.startswith("__")}
    variables = {
        name: value
        for name, value in vars(test_data_module).items()
        if name in var_names and not isinstance(value, ModuleType)
    }

    with open(jinja_template, encoding="utf-8") as file:
        robot_template_lines = []
        JINJA_PLACEHOLDER_REGEX = r"\${T_([\w\.]+)}"
        INDEX_REGEX = r"\[\d+\]"

        for line in file:
            jinja_line = line.removeprefix("#").removesuffix("\n")

            if re.findall(INDEX_REGEX, jinja_line):
                replace_jinja = re.sub(INDEX_REGEX, "[{{loop.index0}}]", jinja_line)
            else:
                replace_jinja = re.sub(JINJA_PLACEHOLDER_REGEX, "{{\\1}}", jinja_line)
            
            jinja_placeholders = re.findall(JINJA_PLACEHOLDER_REGEX, jinja_line)

            if jinja_placeholders and debug:
                robot_template_lines.append(replace_jinja + 4*" " + "# " + ", ".join(jinja_placeholders))
            else:
                robot_template_lines.append(replace_jinja)

        robot_template = "\n".join(robot_template_lines)

    template = Template(robot_template, undefined=CustomUndefined)
    robot_tests = template.render(variables)

    with open(testsuite, "w+", encoding="utf-8") as file:
        file.write(robot_tests)
    
    return f"Generated {testsuite}"
