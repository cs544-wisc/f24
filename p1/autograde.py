from subprocess import check_output, run, DEVNULL
import os

from tester import init, test, cleanup, tester_main

@init
def init(existing_file=None):
    os.system("docker rmi -f p1")
    os.system("docker container rm p1_tester")
    
@cleanup
def cleanup():
    run("docker rmi -f p1", shell=True, stderr=DEVNULL)
    run("docker container rm p1_tester", shell=True, stderr=DEVNULL)

@test(points = 15)
def os_test():
    with open("os.txt") as f:
        if "Ubuntu 24.04" in f.read():
            return None
    return "could not find Ubuntu 24.04 in os.txt"

@test(points = 10)
def cpu_test():
    with open("cpu.txt") as f:
        if "x86_64" in f.read():
            return None
    return "could not find x86_64 in cpu.txt"

@test(points = 15)
def docker_test():
    with open("docker.txt") as f:
        if "27.2.0" in f.read():
            return None
    return "could not find 27.2.0 in docker.txt"

@test(points = 10)
def compose_test():
    with open("compose.txt") as f:
        if "v2.29.2" in f.read():
            return None
    return "could not find v2.29.2 in compose.txt"

@test(points = 10)
def executable_test():
    if not os.path.exists("count.sh"):
        return "missing count.sh"
    if not os.access("count.sh", os.X_OK):
        return "count.sh does not have executable permissions"
    return None

@test(points = 15)
def shebang_test():
    with open("count.sh") as f:
        line = f.readline()
    if line.startswith("#!") and "bash" in line:
        return None
    return "count.sh does not appear to have a bash shebang line"

@test(points = 10, timeout = 300)
def build_test():
    os.system("docker rmi -f p1")
    _ = check_output(["docker", "build", ".", "-t", "p1"])

@test(points = 15, timeout = 300)
def run_test():
    out = check_output(["docker", "run", "--name", "p1_tester", "p1"])
    if "2493" in str(out, "utf-8"):
        return None
    return "did not find 2493 in output of Docker container"

if __name__ == "__main__":
    tester_main()
