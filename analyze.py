# /// script
# requires-python = "==3.10.*"
# dependencies = [
#     "opentrons==8.3.0",
#     "opentrons-shared-data==8.3.0",
#     "rich",
# ]
# ///


from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum, auto
import json
from pathlib import Path
import time
from typing import Dict, List, Optional, Any
from rich.console import Console
from rich.traceback import install
import subprocess

install(show_locals=True)
console = Console()


class ProtocolType(Enum):
    PROTOCOL_DESIGNER = auto()
    PYTHON = auto()


@dataclass
class TargetProtocol:
    protocol_file: Path
    analysis_file: Path
    custom_labware_paths: List[str]
    analysis_execution_time: Optional[float] = None
    command_exit_code: Optional[int] = None
    command_output: Optional[str] = None
    analysis: Optional[Dict[str, Any]] = None

    @property
    def analysis_file_exists(self) -> bool:
        return self.analysis_file.exists()

    def create_failed_analysis(self) -> Dict[str, Any]:
        created_at = datetime.now(timezone.utc).isoformat()

        return {
            "createdAt": created_at,
            "errors": [
                {
                    "analysis_execution_time": self.analysis_execution_time,
                    "command_output": self.command_output,
                    "command_exit_code": self.command_exit_code,
                },
            ],
            "files": [],
            "metadata": [],
            "commands": [],
            "labware": [],
            "pipettes": [],
            "modules": [],
            "liquids": [],
            "config": {},
            "runTimeParameters": [],
        }

    def write_failed_analysis(self) -> None:
        self.analysis = self.create_failed_analysis()
        with open(self.analysis_file, "w") as file:
            json.dump(self.analysis, file, indent=4)

    def set_analysis(self) -> None:
        if self.analysis_file_exists:
            with open(self.analysis_file, "r") as file:
                self.analysis = json.load(file)
        else:
            self.write_failed_analysis()

    @property
    def protocol_file_name(self) -> str:
        return self.protocol_file.name

    @property
    def protocol_type(self) -> str:
        return (
            ProtocolType.PYTHON
            if self.protocol_file.suffix == ".py"
            else ProtocolType.PROTOCOL_DESIGNER
        ).name.title()

    def set_analysis_execution_time(self, analysis_execution_time: float) -> None:
        self.analysis_execution_time = analysis_execution_time


def analyze(protocol: TargetProtocol) -> TargetProtocol:
    command = [
        "uv",
        "run",
        "python",
        "-I",
        "-m",
        "opentrons.cli",
        "analyze",
        "--json-output",
        str(protocol.analysis_file),
        str(protocol.protocol_file),
    ]

    # Add custom labware paths if any
    for labware_path in protocol.custom_labware_paths:
        command.append(labware_path)

    start_time = time.time()
    exit_code = None
    console.print(f"Beginning analysis of {protocol.protocol_file.name}")

    try:
        process = subprocess.run(command, capture_output=True, text=True, check=False)

        exit_code = process.returncode
        protocol.command_output = process.stdout + process.stderr
        protocol.command_exit_code = exit_code
        protocol.set_analysis()
    except Exception as e:
        console.print(f"An unexpected error occurred: {e}")
        protocol.command_output = str(e)
        protocol.command_exit_code = exit_code if exit_code is not None else -1
        protocol.set_analysis()
    finally:
        protocol.set_analysis_execution_time(time.time() - start_time)
        console.print(
            f"Analysis of {protocol.protocol_file.name} completed in {protocol.analysis_execution_time:.2f} seconds."
        )
    return protocol


def main():
    console.print("[bold green]Starting protocol analysis process...[/bold green]")

    # Get all protocol files (.py and .json) from protocols directory
    protocol_dir = Path("./protocols")
    if not protocol_dir.exists():
        console.print(
            f"[bold red]Error: {protocol_dir} directory not found![/bold red]"
        )
        return

    protocol_files = list(protocol_dir.glob("*.py")) + list(protocol_dir.glob("*.json"))
    console.print(f"[blue]Found {len(protocol_files)} protocol files to analyze[/blue]")

    # Get all custom labware files
    custom_labware_dir = Path("./custom_labware")
    custom_labware_paths = []

    if custom_labware_dir.exists():
        custom_labware_files = list(custom_labware_dir.glob("*.json"))
        custom_labware_paths = [str(path) for path in custom_labware_files]
        console.print(
            f"[blue]Found {len(custom_labware_paths)} custom labware definitions[/blue]"
        )
    else:
        console.print(
            "[yellow]No custom_labware directory found, proceeding without custom labware[/yellow]"
        )

    # Process each protocol
    for i, protocol_file in enumerate(protocol_files, 1):
        console.print(
            f"[bold cyan]Processing protocol {i}/{len(protocol_files)}: {protocol_file.name}[/bold cyan]"
        )

        analysis_file = Path(f"results/{protocol_file.name}_analysis.json")

        protocol = TargetProtocol(
            protocol_file=protocol_file,
            analysis_file=analysis_file,
            custom_labware_paths=custom_labware_paths,
        )

        analyze(protocol)
        status = (
            "[green]has no errors.[/green]"
            if protocol.analysis["errors"] == []
            else "[red]has errors.[/red]"
        )
        console.print(f"Analysis of {protocol_file.name} {status}")

    console.print("[bold green]Done analyzing protocols![/bold green]")


if __name__ == "__main__":
    main()
