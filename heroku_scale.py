import subprocess
import sys

# Set your Heroku app name here
HEROKU_APP_NAME = "librus-absence-extractor"

def scale_web(dynos):
    cmd = ["heroku", "ps:scale", f"web={dynos}", "--app", HEROKU_APP_NAME]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(result.returncode)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["up", "down"], help="Scale up or down")
    args = parser.parse_args()
    if args.action == "up":
        scale_web(1)  # turn ON
    else:
        scale_web(0)  # turn OFF