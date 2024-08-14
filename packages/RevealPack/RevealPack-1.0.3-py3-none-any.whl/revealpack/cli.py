import click
import os
import subprocess
import sys
import webbrowser
import http.server
import socketserver
from revealpack import copy_config_and_assets

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """A CLI tool for managing Reveal.js presentation packages.

    Available commands:
    - init: Initialize the file structure and copy config.json and assets.
    - setup: Setup the environment for building presentations.
    - build: Build the presentation package.
    - serve: Serve the presentation for live editing.
    - package: Package the presentation into a distributable format.
    - docs: Display the documentation for revealpack.
    
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

@cli.command()
@click.option('--destination', default=None, help='Destination path to copy config.json and assets')
def init(destination):
    """Initialize the file structure and copy config.json and assets to the specified destination."""
    copy_config_and_assets(destination)

@cli.command()
@click.argument('args', nargs=-1)
@click.option('-r', '--root', default=os.getcwd(), help='Root directory for setup')
def setup(args, root):
    """Setup the environment for building presentations."""
    setup_script = os.path.join(os.path.dirname(__file__), 'setup.py')
    python_executable = sys.executable
    try:
        subprocess.run([python_executable, setup_script, '--root', root] + list(args), check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during setup: {e}")

@cli.command()
@click.argument('args', nargs=-1)
@click.option('-r', '--root', default=os.getcwd(), help='Root directory for build')
def build(args, root):
    """Build the presentation package."""
    build_script = os.path.join(os.path.dirname(__file__), 'build.py')
    python_executable = sys.executable
    try:
        subprocess.run([python_executable, build_script, '--root', root] + list(args), check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during build: {e}")

@cli.command()
@click.argument('args', nargs=-1)
@click.option('-r', '--root', default=os.getcwd(), help='Root directory for serve')
def serve(args, root):
    """Serve the presentation for live editing."""
    serve_script = os.path.join(os.path.dirname(__file__), 'serve.py')
    python_executable = sys.executable
    try:
        subprocess.run([python_executable, serve_script, '--root', root] + list(args), check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during serve: {e}")

@cli.command()
@click.argument('args', nargs=-1)
@click.option('-r','--root', default=os.getcwd(), help='Root directory for package')
@click.option('-d','--dest-dir', required=True, help='Directory to create the package')
@click.option('-n','--no-build', is_flag=True, help='Skip the build step')
def package(args, root, dest_dir, no_build):
    """Package the presentation into a distributable format."""
    package_script = os.path.join(os.path.dirname(__file__), 'package.py')
    python_executable = sys.executable
    try:
        cmd = [python_executable, package_script, '--root', root, '--dest-dir', dest_dir]
        if no_build:
            cmd.append('--no-build')
        subprocess.run(cmd + list(args), check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during packaging: {e}")

@cli.command()
def docs():
    """Display the documentation for revealpack."""
    doc_dir = os.path.join(os.path.dirname(__file__), 'site')

    if os.path.exists(doc_dir):
        port = 8000
        os.chdir(doc_dir)
        
        handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", port), handler)

        webbrowser.open(f"http://127.0.0.1:{port}")
        print(f"Serving documentation on port {port}...")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down server.")
            httpd.shutdown()
    else:
        print("Documentation not found.")

if __name__ == '__main__':
    cli()
