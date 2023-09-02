FROM python:3.10
ARG CMDSTAN_VERSION
ARG CC
ARG CXX

# Install clang.
RUN apt-get update && apt-get install -y \
  clang \
  time \
  && rm -rf /var/lib/apt/lists/*

# Export compiler configuration to the environment.
ENV CC=${CC} CXX=${CXX}
# Install all the requirements.
WORKDIR /workdir/
COPY requirements.txt setup.py /workdir/
RUN pip install --no-dependencies --no-cache-dir -r requirements.txt
RUN python -m cmdstanpy.install_cmdstan --verbose --version ${CMDSTAN_VERSION}
# Copy the source.
COPY . .
