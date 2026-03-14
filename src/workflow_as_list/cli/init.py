# src/workflow_as_list/cli/init.py
"""workflow init command - Initialize workflow-as-list integration.

REFERENCE: #42 - workflow init command for project onboarding
"""

import re
from pathlib import Path

import typer
from rich.console import Console

from ..constants import ensure_directories

console = Console()

# Templates moved to reduce file size
WORKFLOW_DOCS_SECTION = """
## Workflow Automation

This project uses workflow-as-list for process automation.

NOTE: For `.workflow.list` files, use `workflow --help` or execute:
  workflow check/run/exec <workflow-name>

Quick start:
  workflow list              # List available workflows
  workflow check <name>      # Validate workflow
  workflow run <name>        # Start execution
"""

CONFIG_TEMPLATE = """[workflow]
project_name = {project_name}
cache_dir = .imports
state_dir = .workflow-as-list/state
"""

GITIGNORE_ENTRIES = """
# workflow-as-list cache
.imports/
.workflow-as-list/
"""

WORKFLOW_README_TEMPLATE = """# Project Workflows

Workflows manage {project_name} development.

Usage:
  workflow check workflow/<name>
  workflow run workflow/<name>

NOTE: Import caching is automatic (see .imports/)
"""


def print_output(type: str, message: str):
    """Print formatted output."""
    styles = {"INFO": "blue", "SUCCESS": "green", "WARNING": "yellow", "ERROR": "red"}
    console.print(f"[{styles.get(type, 'white')}]{type}[/] {message}")


def get_project_name() -> str:
    """Get project name from pyproject.toml or directory."""
    pyproject = Path("pyproject.toml")
    if pyproject.exists():
        match = re.search(r'name\s*=\s*"([^"]+)"', pyproject.read_text())
        if match:
            return match.group(1)
    return Path.cwd().name


def find_docs_file() -> Path | None:
    """Find AGENTS.md, README.md, or CONTRIBUTING.md."""
    for name in ["AGENTS.md", "README.md", "CONTRIBUTING.md"]:
        path = Path(name)
        if path.exists():
            return path
    return None


def is_initialized() -> bool:
    """Check if already initialized."""
    docs_file = find_docs_file()
    if docs_file and "workflow-as-list" in docs_file.read_text().lower():
        return True
    return Path(".workflow-as-list/config.ini").exists()


def update_docs(force: bool = False) -> bool:
    """Add workflow-as-list section to docs."""
    docs_file = find_docs_file()
    if not docs_file:
        print_output("WARNING", "No AGENTS.md/README.md/CONTRIBUTING.md found")
        return False

    content = docs_file.read_text()
    if "workflow-as-list" in content.lower() and not force:
        print_output("INFO", f"Already initialized: {docs_file.name}")
        return False

    # Find insertion point
    insertion_point = len(content)
    for pattern, pos in [
        (r"(## Getting Started\n)", "after"),
        (r"(## Development\n)", "before"),
        (r"(## Setup\n)", "after"),
    ]:
        match = re.search(pattern, content)
        if match:
            insertion_point = match.end() if pos == "after" else match.start()
            break

    docs_file.write_text(
        content[:insertion_point] + WORKFLOW_DOCS_SECTION + content[insertion_point:]
    )
    print_output("SUCCESS", f"Updated {docs_file.name}")
    return True


def create_config(force: bool = False) -> bool:
    """Create .workflow-as-list/config.ini."""
    config_path = Path(".workflow-as-list/config.ini")
    if config_path.exists() and not force:
        print_output("INFO", f"Config exists: {config_path}")
        return False
    config_path.parent.mkdir(exist_ok=True)
    config_path.write_text(CONFIG_TEMPLATE.format(project_name=get_project_name()))
    print_output("SUCCESS", f"Created {config_path}")
    return True


def update_gitignore(force: bool = False) -> bool:
    """Add cache dirs to .gitignore."""
    gitignore_path = Path(".gitignore")
    if gitignore_path.exists():
        content = gitignore_path.read_text()
        if ".imports/" in content and ".workflow-as-list/" in content and not force:
            print_output("INFO", ".gitignore already updated")
            return False
        gitignore_path.write_text(content.rstrip() + "\n\n" + GITIGNORE_ENTRIES)
    else:
        gitignore_path.write_text(GITIGNORE_ENTRIES)
    print_output("SUCCESS", f"Updated {gitignore_path.name}")
    return True


def create_workflow_readme(force: bool = False) -> bool:
    """Create workflow/README.md if workflow/ exists."""
    workflow_dir = Path("workflow")
    if not workflow_dir.is_dir():
        return False
    readme_path = workflow_dir / "README.md"
    if readme_path.exists() and not force:
        print_output("INFO", "workflow/README.md exists")
        return False
    readme_path.write_text(
        WORKFLOW_README_TEMPLATE.format(project_name=get_project_name())
    )
    print_output("SUCCESS", "Created workflow/README.md")
    return True


def init(
    docs_only: bool = typer.Option(
        False, "--docs-only", help="Only update documentation"
    ),
    config_only: bool = typer.Option(
        False, "--config-only", help="Only create config files"
    ),
    force: bool = typer.Option(False, "--force", help="Overwrite existing files"),
):
    """Initialize workflow-as-list integration for a project.

    Adds workflow-as-list documentation to AGENTS.md or README.md,
    creates configuration files, and updates .gitignore.

    Example:
        workflow init
        workflow init --docs-only
        workflow init --force
    """
    # Ensure directories exist
    ensure_directories()

    # Check if running in a project directory
    docs_file = find_docs_file()
    if not docs_file and not (docs_only or config_only):
        print_output("ERROR", "No AGENTS.md, README.md, or CONTRIBUTING.md found")
        print_output("ERROR", "Current directory does not appear to be a project")
        print_output("INFO", "Create a README.md or AGENTS.md file first")
        raise typer.Exit(1)

    # Check if already initialized
    if is_initialized() and not force:
        print_output("WARNING", "Project already initialized with workflow-as-list")
        print_output("INFO", "Use --force to re-initialize")

    print_output("INFO", "Initializing workflow-as-list integration...")

    success = False

    if docs_only:
        success = update_docs(force)
    elif config_only:
        create_config(force)
        update_gitignore(force)
        create_workflow_readme(force)
        success = True
    else:
        # Full initialization
        success = update_docs(force)
        create_config(force)
        update_gitignore(force)
        create_workflow_readme(force)

    if success:
        print_output(
            "SUCCESS", "Project initialized. Run 'workflow list' to see workflows."
        )
    else:
        print_output("WARNING", "Initialization completed with warnings")
