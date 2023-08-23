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

if IN_CI:
    iter_sampling = 5
    iter_warmup = 10
    chains = 1
else:
    iter_sampling = 100
    iter_warmup = 500
    chains = 2

# Generate samples for all models matching the folder structure of the models.
with create_group("samples"):
    package_path = Path("reference_models").resolve()
    for collection, experiments in COLLECTIONS.items():
        for dataset, stan_files in experiments.items():
            for stan_file in stan_files:
                path = stan_file.relative_to(package_path).with_suffix("")
                output_directory = "samples" / path

                # Draw posterior samples.
                sample_target = output_directory / "metadata.yaml"
                name = ":".join(path.parts)
                action = [
                    "python", "-m", "reference_models.sample", "--summary", "--output",
                    output_directory, "--seed", 2576, "--iter-sampling", iter_sampling,
                    "--iter-warmup", iter_warmup, "--chains", chains, collection, dataset, path.name
                ]
                create_task(name, targets=[sample_target], dependencies=[stan_file], action=action)
                heatmap_target = output_directory / "dependence.pdf"

                # Visualize the dependence between samples.
                action = [
                    "python", "-m", "reference_models.dependence_heatmap", "--output",
                    heatmap_target, output_directory,
                ]
                create_task(f"{name}:dependence", targets=[heatmap_target],
                            dependencies=[sample_target], action=action)
