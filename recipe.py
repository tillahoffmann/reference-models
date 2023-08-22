from cook import create_task


create_task("requirements", dependencies=["requirements.in", "setup.py"],
            targets=["requirements.txt"], action="pip-compile -v")
create_task("tests", action="pytest -v --cov=reference_models --cov-report=term-missing "
            "--cov-fail-under=100")
