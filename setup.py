import os
import subprocess
import sys


def is_docker_running():
    """Check if Docker is installed and running."""
    try:
        # Try to get the Docker version to confirm Docker is installed and running
        subprocess.check_call(
            ["docker", "info"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return True
    except subprocess.CalledProcessError:
        return False


def is_wsl2_running():
    """Check if WSL2 is running on Windows."""
    try:
        # Check if WSL2 is installed by running `wsl --list` and verifying Docker is installed in WSL2
        subprocess.check_call(
            ["wsl", "--list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return True
    except subprocess.CalledProcessError:
        return False


def check_docker():
    """Check if Docker is installed and running, depending on the OS."""
    if sys.platform == "win32":
        # On Windows, check if WSL2 is running and Docker is installed
        if not is_wsl2_running():
            print("WSL2 is not running. Please ensure WSL2 is installed and running.")
            sys.exit(1)

        # Check if Docker is installed and running within WSL2
        if not is_docker_running():
            print(
                "Docker is not installed or running. Please install Docker in your WSL2 environment."
            )
            sys.exit(1)
    elif sys.platform == "darwin" or sys.platform == "linux":
        # On macOS/Linux, check if Docker is installed and running
        if not is_docker_running():
            print("Docker is not installed or running. Please install Docker.")
            sys.exit(1)
    else:
        print(f"Unsupported OS: {sys.platform}")
        sys.exit(1)


def create_virtualenv():
    """Create a virtual environment."""
    print("Creating a virtual environment...")

    # Check the system type and adjust command
    if sys.platform == "win32":
        # Windows: Use `python` (ensure Python is installed and added to PATH)
        subprocess.check_call([sys.executable, "-m", "venv", ".venv"])
    elif sys.platform == "darwin" or sys.platform == "linux":
        # macOS/Linux: Use `python3` for creating the virtual environment
        subprocess.check_call(["python3", "-m", "venv", ".venv"])
    else:
        print(f"Unsupported OS: {sys.platform}")
        sys.exit(1)


def activate_virtualenv():
    """Activate the virtual environment."""
    activate_script = None
    if sys.platform == "win32":
        activate_script = os.path.join(".venv", "Scripts", "activate.bat")
    else:
        activate_script = os.path.join(".venv", "bin", "activate")

    return activate_script


def install_requirements():
    """Install the requirements from the requirements.txt file."""
    print("Installing dependencies from requirements.txt...")
    subprocess.check_call(
        [os.path.join(".venv", "bin", "pip"), "install", "-r", "requirements.txt"]
    )


def run_migrations():
    """Run Django migrations."""
    print("Running migrations...")
    subprocess.check_call(
        [os.path.join(".venv", "bin", "python"), "manage.py", "migrate"]
    )


def setup_env_file():
    """Set up the .env file from template.env or prompt the user."""
    if os.path.exists(".env"):
        print(".env file already exists. Proceeding with setup.")
    elif os.path.exists("template.env"):
        configure_env = (
            input(
                "Do you have your .env file configured? If not, do you want to use the template.env (y/n)? "
            )
            .strip()
            .lower()
        )
        if configure_env == "y":
            print("Renaming template.env to .env...")
            os.rename("template.env", ".env")  # Rename, but don't delete template.env
        else:
            print("You can manually configure your .env file later.")
    else:
        print(
            "No .env or template.env file found! Please ensure to set up your environment variables."
        )


def setup_docker():
    """Check if Docker files are present and set up Docker containers."""
    if os.path.exists("docker-compose.yml") and os.path.exists("Dockerfile"):
        print("Docker setup detected. Building Docker containers...")
        command = ["sudo", "docker", "compose", "up", "--build"]
        print(f"Running command: {' '.join(command)}")
        subprocess.check_call(command)
    else:
        print("Docker setup not found. Continuing with traditional setup.")


def create_or_switch_git_branch():
    """Ask user if they already have a branch or want to create a new one."""
    current_branch = (
        subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        .strip()
        .decode()
    )
    print(f"Current branch is: {current_branch}")

    choice = (
        input(
            "Do you already have a branch or do you want to create a new one? (existing(e)/create(c)): "
        )
        .strip()
        .lower()
    )

    if choice in ["existing", "e"]:
        branch_name = input("Enter the name of the existing branch: ").strip()
        try:
            print(f"Switching to existing branch '{branch_name}'...")
            subprocess.check_call(["git", "checkout", branch_name])
        except subprocess.CalledProcessError:
            print(f"Branch '{branch_name}' does not exist.")
    elif choice in ["create", "c"]:
        branch_name = input("Enter the name for the new Git branch: ").strip()
        if branch_name:
            print(f"Creating and switching to branch '{branch_name}'...")
            subprocess.check_call(["git", "checkout", "-b", branch_name])
        else:
            print("Branch name cannot be empty. No branch created.")
    else:
        print("Invalid choice. No branch action taken.")


def run():
    """Run the setup process."""
    print("Setting up your Django project...\n")

    # Check if Docker or WSL2 with Docker is running
    check_docker()

    # Ask the user if they want to create or switch to an existing Git branch
    create_or_switch_git_branch()

    # Option for Docker or traditional setup
    if os.path.exists("docker-compose.yml") and os.path.exists("Dockerfile"):
        use_docker = (
            input("Docker setup detected. Do you want to use Docker (y/n)? ")
            .strip()
            .lower()
        )
        if use_docker == "y":
            setup_docker()
        else:
            create_virtualenv()
            setup_env_file()
            activate_script = activate_virtualenv()
            print(f"Activate the virtual environment using: source {activate_script}")
            # Note: Activating manually via shell
            install_requirements()
            run_migrations()
    else:
        create_virtualenv()
        setup_env_file()
        activate_script = activate_virtualenv()
        print(f"Activate the virtual environment using: source {activate_script}")
        # Note: Activating manually via shell
        install_requirements()
        run_migrations()

    print(
        "\nSetup complete. Don't forget to configure your Django settings and check your .env file and activate your virtual environment."
    )


if __name__ == "__main__":
    run()
