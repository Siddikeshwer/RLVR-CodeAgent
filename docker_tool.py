import docker
from pathlib import Path

client = docker.from_env()

PROJECT_DIR = Path(__file__).parent.resolve()
IMAGE_NAME = "bugfix-sandbox"


def read_file(path: str) -> str:
    file_path = PROJECT_DIR / path

    if not file_path.exists():
        return f"File not found: {path}"

    return file_path.read_text(encoding="utf-8")


def write_file(path: str, content: str) -> str:
    file_path = PROJECT_DIR / path

    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")

    return f"Successfully wrote {path}"


def run_in_sandbox(command: str) -> str:
    print("\n[Docker] Starting container...")
    print(f"[Docker] Command: {command}\n")

    container = client.containers.run(
        image=IMAGE_NAME,
        command=["sh", "-c", command],
        volumes={
            str(PROJECT_DIR): {
                "bind": "/workspace",
                "mode": "rw",
            }
        },
        working_dir="/workspace",
        detach=True,
    )

    output = []

    try:
        for line in container.logs(
            stream=True,
            stdout=True,
            stderr=True,
        ):
            text = line.decode("utf-8", errors="replace")
            print(f"[Docker] {text}", end="")
            output.append(text)

        result = container.wait()
        exit_code = result["StatusCode"]

        print(
            f"\n[Docker] Container finished "
            f"with exit code {exit_code}"
        )

        return "".join(output) + f"\n[exit_code={exit_code}]"

    finally:
        container.remove(force=True)
        print("[Docker] Container removed.")


def run_tests() -> str:
    result = run_in_sandbox("python -m pytest task")
    return result