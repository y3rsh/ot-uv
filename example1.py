# /// script
# requires-python = "==3.10.*"
# dependencies = [
#     "opentrons==8.3.0a2",
#     "opentrons-shared-data==8.3.0a2",
# ]
# ///

from opentrons.simulate import simulate, format_runlog

def from_opentrons_doc(): # https://docs.opentrons.com/v2/new_protocol_api.html?highlight=simulate#opentrons.simulate.main
    protocol_file = open("IDT_xGen_EZ_48x_v8.py")
    runlog, _bundle = simulate(protocol_file)
    print(format_runlog(runlog))

def main():
    from_opentrons_doc()

if __name__ == "__main__":
    main()
