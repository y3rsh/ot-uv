# /// script
# requires-python = "==3.10.*"
# dependencies = [
#     "opentrons==8.3.0a2",
#     "opentrons-shared-data==8.3.0a2",
# ]
# ///

from opentrons.simulate import simulate, format_runlog

def from_pypi_doc(): # https://pypi.org/project/opentrons/
    protocol_file = open("IDT_xGen_EZ_48x_v8.py")
    runlog, _bundle = simulate(protocol_file)
    print(format_runlog(runlog))

def main():
    from_pypi_doc()

if __name__ == "__main__":
    main()
