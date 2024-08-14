def check_et():
    print('Running easytailwind v1.1.1')

def install():
    import subprocess
    import os
    import json
    from colorama import Fore, Style, init

    # Initialize colorama
    init(autoreset=True)


    def print_header(message):
        """Print a header with color and formatting."""
        print(Fore.CYAN + Style.BRIGHT + "=" * 100)
        print(Fore.CYAN + Style.BRIGHT + f"{message}")
        print(Fore.CYAN + Style.BRIGHT + "=" * 100)


    def print_success(message):
        """Print a success message with color."""
        if message == "Tailwind CSS setup completed by EasyTailwind. They community awaits your creativity!":
            print(Fore.MAGENTA + Style.BRIGHT + f"[SUCCESS] {message}")


    def print_error(message):
        """Print an error message with color."""
        print(Fore.RED + Style.BRIGHT + f"[ERROR] {message}")


    def run_command(command, cwd=None):
        """Run a command in the specified directory and print its output."""
        try:
            result = subprocess.run(command, shell=True, cwd=cwd, text=True, capture_output=True)
            if result.returncode != 0:
                print_error(f"Error occurred while running command '{command}':")
                print(result.stderr)
            elif command != "npm init -y":
                print_success(result.stdout)
        except Exception as e:
            print_error(f"Exception occurred: {e}")


    def run_command_in_background(command, cwd=None):
        """Run a command in the background."""
        try:
            process = subprocess.Popen(command, shell=True, cwd=cwd, text=True)
            return process
        except Exception as e:
            print_error(f"Exception occurred while running command in background: {e}")


    def validate_file_extensions(file_extensions):
        """Validate file extensions against a predefined list."""
        all_file_extensions = [
            'html', 'htm', 'pug', 'ejs', 'njk', 'liquid', 'erb',
            'js', 'jsx', 'ts', 'tsx', 'mjs', 'cjs',
            'css', 'scss', 'sass', 'less', 'pcss', 'postcss',
            'vue', 'svelte', 'php', 'erb', 'njk'
        ]
        valid_extensions = []
        invalid_extensions = []

        for ext in file_extensions:
            if ext in all_file_extensions:
                valid_extensions.append(ext)
            else:
                invalid_extensions.append(ext)

        if invalid_extensions:
            print(Fore.YELLOW + Style.BRIGHT +
                f"[WARNING] Invalid or unsupported extensions: {', '.join(invalid_extensions)}. Please add them manually in tailwind.config.js")

        if not valid_extensions:
            raise ValueError("No valid file extensions provided.")

        return valid_extensions


    def validate_template_folder(folder_path):
        """Validate the template folder path to start with './'."""
        if not folder_path.startswith('./'):
            raise ValueError("Template folder path must start with './'.")

    def get_template_folder():
        """Get and validate the location of the template folder."""
        while True:
            try:
                template_folder = input(
                    Fore.BLUE + Style.BRIGHT + "Enter the location of the template folder (relative path, e.g., './src'): ")
                validate_template_folder(template_folder)
                return template_folder
            except ValueError as ve:
                print_error(ve)
            except Exception as e:
                print_error(f"Unexpected error: {e}")

    def get_file_extensions():
        """Get and validate file extensions from user input."""
        all_file_extensions = [
            'html', 'htm', 'pug', 'ejs', 'njk', 'liquid', 'erb',
            'js', 'jsx', 'ts', 'tsx', 'mjs', 'cjs',
            'css', 'scss', 'sass', 'less', 'pcss', 'postcss',
            'vue', 'svelte', 'php', 'erb', 'njk'
        ]

        while True:
            try:
                file_extensions = input(
                    "Enter the file extensions to include apart from html (comma-separated, e.g., 'html,js'): ").split(',')
                file_extensions = [ext.strip() for ext in file_extensions]
                valid_extensions = validate_file_extensions(file_extensions)
                if not valid_extensions:
                    raise ValueError("File extensions list cannot be empty.")
                return valid_extensions
            except ValueError as ve:
                print_error(ve)
            except Exception as e:
                print_error(f"Unexpected error: {e}")

    def validate_html_filename(filename):
        """Validate the HTML filename to ensure it ends with '.html'."""
        if not filename.endswith('.html'):
            raise ValueError("HTML filename must end with '.html'.")

    def get_html_filename():
        """Get and validate the HTML filename."""
        while True:
            try:
                html_filename = input(
                    "Enter the name of the HTML file to create (e.g., 'index.html'): ")
                validate_html_filename(html_filename)
                return html_filename
            except ValueError as ve:
                print_error(ve)
            except Exception as e:
                print_error(f"Unexpected error: {e}")


    def setup_tailwind():
        """Set up Tailwind CSS in the current directory."""
        print_header("Hi! I'm EasyTailwind. I'll set up Tailwind CSS for you. Sit back while I handle it!")
        print("Initializing Tailwind CSS Setup")

        # Initialize a new Node.js project
        print("Initializing your creative project...")
        run_command("npm init -y")

        # Install Tailwind CSS CLI and dependencies
        print("Installing Tailwind CSS CLI and dependencies...")
        run_command("npm install -D tailwindcss")

        # Create Tailwind configuration file
        print("Creating Tailwind configuration file...")
        run_command("npx tailwindcss init")

        # Get user input for content paths, file extensions, and template folder name
        template_folder = get_template_folder()
        file_extensions = get_file_extensions()
        html_filename = get_html_filename()

        # Create Tailwind CSS configuration with content paths
        content_paths = [f"{template_folder}/**/*.{ext}" for ext in file_extensions]
        content_paths_str = ',\n    '.join(f'"{path}"' for path in content_paths)

        print("Creating Tailwind configuration file with content paths...")
        with open('tailwind.config.js', 'w') as f:
            f.write(f"""
    /** @type {{import('tailwindcss').Config}} */
    module.exports = {{
    content: [
        "{template_folder}/**/*.html",
        {content_paths_str}
    ],
    theme: {{
        extend: {{}}  // No custom colors
    }},
    plugins: [],
    }}
            """)

        # Create Tailwind CSS file
        print("Creating Tailwind CSS file...")
        os.makedirs('src', exist_ok=True)
        with open('src/styles.css', 'w') as f:
            f.write("""
    @tailwind base;
    @tailwind components;
    @tailwind utilities;
            """)

        # Create the template folder and HTML file
        print(f"Creating template folder '{template_folder}' and HTML file...")
        os.makedirs(template_folder, exist_ok=True)
        html_file_path = os.path.join(template_folder, html_filename)
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Tailwind CSS Setup</title>
        <link href="../dist/output.css" rel="stylesheet">
    </head>
    <body class="bg-gradient-to-r from-blue-400 to-purple-500 flex flex-col items-center justify-center min-h-screen">
        <h1 class="text-5xl font-extrabold mb-4"><span class="text-gray-300">Easy</span><span class="text-blue-800">Tailwind</span> says...</h1>
        <div class="bg-white/30 backdrop-blur-lg border border-white/40 rounded-lg p-8 max-w-lg text-center shadow-lg transition-transform transform hover:scale-105">
            <h1 class="text-5xl font-extrabold text-black mb-4">🚀 Life is Colourful!</h1>
            <p class="text-xl text-black mb-4"><b>Tailwind CSS</b> is now installed and ready to use. Enjoy building your modern, responsive website!</p>
            <p class="text-sm text-gray-">
                Library developed by <a href="https://linkedin.com/in/sayedafaq" class="text-cyan-900 font-bold hover:underline" target="_blank">Sayed Afaq Ahmed</a>
            </p>
        </div>
    </body>
    </html>

            

            """)

        # Create an output directory
        print("Creating output directory...")
        os.makedirs('dist', exist_ok=True)

        # Add build and watch scripts to package.json
        print("Adding build and watch scripts to package.json...")
        package_json_path = 'package.json'
        with open(package_json_path, 'r+') as f:
            package_json = json.load(f)
            if "scripts" not in package_json:
                package_json["scripts"] = {}
            package_json["scripts"]["build:css"] = "npx tailwindcss -i src/styles.css -o dist/output.css"
            package_json["scripts"]["watch:css"] = "npx tailwindcss -i src/styles.css -o dist/output.css --watch"
            package_json["scripts"]["start"] = "http-server . -p 8080"
            f.seek(0)
            json.dump(package_json, f, indent=2)
            f.truncate()

        # Display instructions for running the Tailwind CSS watch process
        print(Fore.CYAN + Style.BRIGHT + "=" * 80)
        print('To start the Tailwind CSS watch process and run the webserver, do the following steps:')
        print(Fore.GREEN + Style.BRIGHT + "RUN : npm run watch:css")
        print(Fore.GREEN + Style.BRIGHT + f"Go to {template_folder}/{html_filename}, then click 'Go Live' and  your webpage will be displayed.")
        print(Fore.CYAN + Style.BRIGHT + "=" * 80)

        print_success("Tailwind CSS setup completed by EasyTailwind. They community awaits your creativity!")

    setup_tailwind()
