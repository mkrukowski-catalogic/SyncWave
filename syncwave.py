import subprocess
import argparse
import time

def execute_rsync_with_ssh_key():

    parser = argparse.ArgumentParser(description="Example script with a file name flag.")
    parser.add_argument("-s", "--sour", required=True, help="Specify a download source")
    parser.add_argument("-d", "--dest", required=True, help="Specify a destination folder")
    parser.add_argument("-l", "--logi", required=True, help="Specify a login")
    parser.add_argument("-i", "--host", required=True, help="Specify Host login and ip")
    parser.add_argument("-p", "--port", required=False, help="Specify port number")
    args = parser.parse_args()

    download_source = args.sour
    destination = args.dest
    login = args.logi
    host = args.host
    if args.port:
        port = args.port
    else:
        port = 22
    rsync_command = [
        "rsync",
        "--partial",
        "--append",
        "--progress",
        "-avze",
        f"ssh -p {port}",
        f"{login}@{host}:{download_source}",
        f"{destination}"
    ]
    max_retries = 10000
    retry_delay = 5  # seconds

    for retry_count in range(max_retries + 1):
        try:
            process = subprocess.Popen(
                rsync_command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            stdout, stderr = process.communicate()

            if process.returncode == 0:
                print("Rsync completed successfully!")
                break 
            else:
                print("Rsync failed.")
                print("stdout:", stdout)
                print("stderr:", stderr)
     
                if "write error: Broken pipe" in stderr:
                    if retry_count < max_retries:
                        print("Retrying...")
                        time.sleep(retry_delay)
                        continue  # Retry the rsync command
                    else:
                        print("Maximum retry attempts reached.")
                        break
                else:
                    print("Error message not recognized.")
                    break

        except Exception as e:
            print("An error occurred:", e)
            break

if __name__ == "__main__":
    execute_rsync_with_ssh_key()
