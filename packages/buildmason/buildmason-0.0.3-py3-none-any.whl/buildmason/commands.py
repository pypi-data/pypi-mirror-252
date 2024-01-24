import click
from cookiecutter.main import cookiecutter

def generate_project(template_path, output_path, extra_context=None):
    """
    Generate a project based on the provided template.

    Parameters:
        template_path (str): Path to the cookiecutter template.
        output_path (str): Path to the output directory where the project will be generated.
        extra_context (dict): Extra context for customizing the template.

    Returns:
        None
    """
    cookiecutter(template_path, output_dir=output_path, extra_context=extra_context)

@click.command()
@click.option('--output-path', prompt='Output directory path', help='Path where the project will be generated')
def basic_project(output_path):
    click.echo("Creating a basic Flask project...")
    generate_project('gh:Worm4047/buildmason-basic-flask', output_path)


@click.command()
@click.option('--output-path', prompt='Output directory path', help='Path where the project will be generated')
def rest_api(output_path):
    click.echo("Creating a Flask RESTful API project...")
    generate_project('gh:Worm4047/buildmason-flask-rest', output_path)

@click.command()
@click.option('--output-path', prompt='Output directory path', help='Path where the project will be generated')
def blueprint(output_path):
    click.echo("Creating a Flask Blueprint project...")
    generate_project('gh:Worm4047/buildmason-flask-blueprint', output_path)

