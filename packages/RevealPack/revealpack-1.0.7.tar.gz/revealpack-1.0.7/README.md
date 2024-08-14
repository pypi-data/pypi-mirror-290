# RevealPack

A CLI tool for managing Reveal.js presentation packages.

## Commands

- `revealpack init [--destination PATH]`: Initialize the file structure and copy `config.json` and `assets/styles` to the specified destination.
- `revealpack setup`: Setup the environment for building presentations.
- `revealpack build`: Build the presentation package.
- `revealpack serve`: Serve the presentation for live editing.
- `revealpack package`: Package the presentation as an executable.

## Usage

1. **Initialize the Project**:
    ```
    revealpack init --destination /path/to/your/project
    ```

    This command creates the necessary directory structure and copies the initial configuration and styles files to the specified destination.

2. **Setup the Environment**:
    ```
    revealpack setup
    ```

    This command sets up the environment for building Reveal.js presentations. It reads the `config.json` file, creates necessary directories, downloads and installs Reveal.js packages, checks the theme, and generates the necessary templates for the build step.

3. **Build the Presentation**:
    ```
    revealpack build
    ```

    This command builds the presentation package. It compiles the styles, processes the slide files, and generates the final HTML files in the build directory.

4. **Serve the Presentation**:
    ```
    revealpack serve
    ```

    This command starts a live server for the current presentations, allowing for real-time editing and viewing.

5. **Package the Presentation**:
    ```
    revealpack package
    ```

    This command packages the presentation as an executable for distribution.

## Configuration

The main configuration file is `config.json`. Here are some key configuration options:

- `info`: Information about the project (e.g., title, version, authors).
- `directories`: Configuration for directory structure used in the project.
- `packages`: Configuration for Reveal.js and associated plugins.
- `theme`: Path to the custom theme CSS file.
- `reveal_template`: Name of the Jinja2 template file for generating the presentation HTML.
- `toc_template`: Path to the Jinja2 template file for generating the table of contents HTML.
- `logging`: Logging level for setup and build processes.
- `highlight_theme`: Path to the highlight.js theme CSS file.
- `custom_scripts`: Array of custom JavaScript files to include in the presentation.
- `force_plugin_download`: Boolean to force re-download of plugins.
- `reveal_configurations`: Configuration options for Reveal.js.

## Dependencies

Ensure you have the necessary dependencies installed. These are listed in the `requirements.txt` file. You can install them using:

```
pip install -r requirements.txt
```

## Directory Structure

Here is an example of the directory structure after running `revealpack init` and `revealpack setup`:

```
your-project-directory/
├── config.json
├── assets/
│   └── styles/
│       ├── revealpack.scss
│       └── ... (other styles)
├── source/
│   ├── lib/
│   │   └── ... (libraries and assets)
│   ├── decks/
│   │   └── your-presentation/
│   │       ├── slide1.html
│   │       ├── slide2.html
│   │       ├── ...
│   │       └── presentation.json
│   ├── cached/
│   │   └── ... (cached packages)
│   ├── reveal_template.html
│   └── toc_template.html
└── dist/
    └── ... (build output)
```

## Documentation

For more detailed documentation on configuration options, slide options, and more, refer to `revealpack docs`.