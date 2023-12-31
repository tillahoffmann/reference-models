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
                "--cov-fail-under=100 -m 'not compile_only'")
    create_task("docs", action="rm -rf docs/_build && sphinx-build -naW . docs/_build")

if IN_CI:
    iter_sampling = 5
    iter_warmup = 10
    chains = 1
else:
    iter_sampling = 500
    iter_warmup = 1000
    chains = 4

# Generate samples for all models matching the folder structure of the models.
with create_group("samples"):
    package_path = Path("reference_models").resolve()
    for collection, experiments in COLLECTIONS.items():
        for name, experiment in experiments.items():
            stan_file = experiment.stan_file
            path = stan_file.relative_to(package_path).parent / name
            output_directory = "samples" / path

            # Draw posterior samples.
            sample_target = output_directory / "metadata.yaml"
            task_name = ":".join(path.parts)
            action = [
                "python", "-m", "reference_models.sample", "--summary", "--output",
                output_directory, "--seed", 2576, "--iter-sampling", iter_sampling,
                "--iter-warmup", iter_warmup, "--chains", chains, collection, name
            ]
            create_task(task_name, targets=[sample_target], dependencies=[stan_file], action=action)
            heatmap_target = output_directory / "dependence.pdf"

            # Visualize the dependence between samples.
            action = [
                "python", "-m", "reference_models.dependence_heatmap", "--output",
                heatmap_target, output_directory,
            ]
            create_task(f"{task_name}:dependence", targets=[heatmap_target],
                        dependencies=[sample_target], action=action)


configs = [
    ("2.32.2", "clang", "clang++"),
    ("2.32.2", "gcc", "g++"),
    ("2.33.0-rc1", "clang", "clang++"),
    ("2.33.0-rc1", "gcc", "g++"),
]
for cmdstan_version, cc, cxx in configs:
    tag = f"{cmdstan_version}-{cc}"
    action = [
        "docker", "build", "-t", tag, "--build-arg", f"CMDSTAN_VERSION={cmdstan_version}",
        "--build-arg", f"CC={cc}", "--build-arg", f"CXX={cxx}", "--progress=plain", ".",
    ]
    docker_image = create_task(f"docker-image:{tag}", action=action)
    action = f"docker run --rm -it -v `pwd`/docker-samples/{tag}:/workdir/samples " \
        f"-e CMDSTAN_COMPILE=force {tag} time cook exec samples"
    create_task(f"docker-samples:{tag}", action=action, task_dependencies=[docker_image])
