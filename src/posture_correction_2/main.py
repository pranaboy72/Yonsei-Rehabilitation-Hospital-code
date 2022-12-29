import subprocess

process1 = subprocess.Popen(["python", "posture_1.py"]) # Create and launch process pop.py using python interpreter
process2 = subprocess.Popen(["python", "posture_2.py"])
process3 = subprocess.Popen(["python", "posture_3.py"])

process1.wait() # Wait for process1 to finish (basically wait for script to finish)
process2.wait()
process3.wait()
