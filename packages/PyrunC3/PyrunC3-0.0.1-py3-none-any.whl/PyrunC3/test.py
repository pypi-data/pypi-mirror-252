from mainfuncs import C3Runner
import os



output, dumps = C3Runner.RunC3File(f"{os.getcwd()}\\PyrunC3\\testfile.cs")

print(output)

C3Runner.Cleanup(dumps)