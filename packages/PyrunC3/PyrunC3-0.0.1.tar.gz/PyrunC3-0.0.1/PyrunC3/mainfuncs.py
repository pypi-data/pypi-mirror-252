import os
import subprocess


class C3Runner:
    def __init__(self): pass

    def RunC3Code(code: str, tempfilename: str = "tempfile") -> tuple:
        finalcode: str = ""

        finalcode = code

        with open(f"{tempfilename}.cs", "w") as f:
            f.write(finalcode)

        subprocess.run(["csc", f"{tempfilename}.cs"])
    
        Output = subprocess.run(args=[f"{tempfilename}.exe"], text=True, capture_output=True).stdout

        newdump = {}

        newdump["tempfilename"] = tempfilename

        return Output, newdump
    
    def Cleanup(dumps: dict) -> None:
        os.remove(f"{dumps['tempfilename']}.cs")
        os.remove(f"{dumps['tempfilename']}.exe")
    
    def RunC3File(path: str, tempfilename: str = "tempfile") -> tuple:
        with open(path, "r") as f:
            code = f.read()

        output, dumps = C3Runner.RunC3Code(code, tempfilename=tempfilename)

        return output, dumps