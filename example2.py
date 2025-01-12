# /// script
# requires-python = "==3.10.*"
# dependencies = [
#     "opentrons==8.3.0a2",
#     "opentrons-shared-data==8.3.0a2",
# ]
# ///

from opentrons.simulate import simulate

def from_pypi_doc(): # https://pypi.org/project/opentrons/
    protocol_file = open("protein_quant_and_normal.py")
    simulate(protocol_file)

def main():
    from_pypi_doc()
    for i in range(3):
        print("**************************************************")

if __name__ == "__main__":
    main()
