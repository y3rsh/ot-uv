# /// script
# requires-python = "==3.10.*"
# dependencies = [
#     "opentrons @ git+https://github.com/Opentrons/opentrons.git@chore_release-8.4.0#subdirectory=api",
#     "opentrons-shared-data @ git+https://github.com/Opentrons/opentrons.git@chore_release-8.4.0#subdirectory=shared-data/python",
#     "rich",
# ]
# ///

import os
import glob
from rich.console import Console
from rich.panel import Panel
from opentrons.simulate import simulate, format_runlog

console = Console()

def simulate_protocol(file_path):
    try:
        console.print(f"[bold blue]Simulating[/bold blue]: {file_path}")

        # Create results directory if it doesn't exist
        results_dir = "./results"
        os.makedirs(results_dir, exist_ok=True)

        # Generate output file name
        base_name = os.path.basename(file_path)
        name_without_ext = os.path.splitext(base_name)[0]
        output_file = os.path.join(
            results_dir, f"{name_without_ext}_simulate_output.txt"
        )

        with open(file_path) as protocol_file:
            runlog, _bundle = simulate(protocol_file, custom_labware_paths=["./custom_labware"])
            formatted_log = format_runlog(runlog)

            # Write to output file
            with open(output_file, "w") as f:
                f.write(formatted_log)

            console.print(
                Panel(
                    f"Results saved to: {output_file}",
                    title=f"Simulated {base_name}",
                    border_style="green",
                )
            )
    except Exception as e:
        console.print(
            Panel(
                f"[bold red]Error[/bold red]: {str(e)}",
                title=f"Failed: {os.path.basename(file_path)}",
                border_style="red",
            )
        )


def simulate_all_protocols():
    protocols_dir = "./protocols"

    if not os.path.exists(protocols_dir):
        console.print(
            f"[bold red]Error[/bold red]: Directory {protocols_dir} does not exist!"
        )
        return

    # Find all .py and .json files in protocols directory
    protocol_files = glob.glob(os.path.join(protocols_dir, "*.py")) + glob.glob(
        os.path.join(protocols_dir, "*.json")
    )

    if not protocol_files:
        console.print(
            f"[bold yellow]Warning[/bold yellow]: No .py or .json files found in {protocols_dir}"
        )
        return

    console.print(
        f"[bold green]Found {len(protocol_files)} protocol files[/bold green]"
    )

    for protocol_file in protocol_files:
        simulate_protocol(protocol_file)


def main():
    console.print("[bold]Opentrons Protocol Simulator[/bold]", style="blue on white")
    simulate_all_protocols()


if __name__ == "__main__":
    main()
