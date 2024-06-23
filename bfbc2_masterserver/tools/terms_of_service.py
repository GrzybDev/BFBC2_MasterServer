import glob
import os
from functools import lru_cache

from bfbc2_masterserver.enumerators.client.ClientLocale import ClientLocale


@lru_cache
def getLocalizedTOS(locale: ClientLocale):
    dirname = os.path.dirname(__file__)

    # Check if locale have a TOS file
    # Example TOS is located in ./data/TOS.default.20426_17.20426_17.txt
    # The file name is in format TOS.<locale>.<version>.txt

    # Check if the file exists, any version
    filename = os.path.join(dirname, f"data/TOS.{locale.value}.*.txt")
    files = glob.glob(filename)

    if len(files) == 0:
        # If no localized TOS file found, use the default one
        filename = os.path.join(dirname, "data/TOS.default.*.txt")
        files = glob.glob(filename)

        if len(files) == 0:
            raise FileNotFoundError("No default TOS file found")

    # Select the latest one (highest version)
    files.sort()
    filename = files[-1]

    with open(filename, "r", encoding="utf-8") as f:
        return {
            "tos": f.read(),
            "version": os.path.basename(filename).split(".", 2)[2].replace(".txt", ""),
        }
