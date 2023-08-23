from cook import create_task
from cook.contexts import create_group
import os
from pathlib import Path
from reference_models import COLLECTIONS


IN_CI = "CI" in os.environ


create_task("requirements", dependencies=["requirements.in", "setup.py"],
            targets=["requirements.txt"], action="pip-compile -v")


with create_group("build"):
    create_task("lint", action="flake8")
    create_task("tests", action="pytest -v --cov=reference_models --cov-report=term-missing "
                "--cov-fail-under=100")

# Generate samples for all models matching the folder structure of the models.
with create_group("samples"):
    package_path = Path("reference_models").resolve()
    for collection, experiments in COLLECTIONS.items():
        for dataset, stan_files in experiments.items():
            for stan_file in stan_files:
                path = stan_file.relative_to(package_path).with_suffix("")
                output_directory = "samples" / path
                target = output_directory / "src_info.yaml"
                action = ["python", "-m", "reference_models.sample", "--output", output_directory]
                if IN_CI:
                    action.extend(["--iter-sampling", 5, "--iter-warmup", 10, "--chains", 1])
                action.extend([collection, dataset, path.name])
                create_task(":".join(path.parts), targets=[target], dependencies=[stan_file],
                            action=action)
