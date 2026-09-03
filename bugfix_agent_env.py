import verifiers as vf
from datasets import Dataset

from docker_tool import read_file, write_file, run_tests


def load_environment(**kwargs) -> vf.Environment:
    dataset = Dataset.from_list([
        {
            "prompt": (
                "Fix the bug in the coding task.\n\n"
                "The task files are:\n"
                "- task/main.py — source code\n"
                "- task/test_main.py — tests\n"
                "- task/README.md — task description\n\n"
                "First read task/README.md and task/main.py. "
                "Identify the bug, modify the necessary code, "
                "then run the tests using run_tests. "
                "Keep fixing the code until all tests pass."
            ),
            "answer": "All tests pass",
        }
    ])

    def score_result(state, **kwargs):
        result = run_tests()

        return 1.0 if "[exit_code=0]" in result else 0.0

    rubric = vf.Rubric(
        funcs=[score_result],
        weights=[1.0],
    )

    env = vf.ToolEnv(
        tools=[
            read_file,
            write_file,
            run_tests,
        ],
        dataset=dataset,
        rubric=rubric,
        max_turns=10,
        **kwargs,
    )

    return env