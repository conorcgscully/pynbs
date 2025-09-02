FROM --platform=linux/amd64 mambaorg/micromamba:2.3.0

# Keep micromamba auto-activation
ARG MAMBA_DOCKERFILE_ACTIVATE=1
ENV MAMBA_DOCKERFILE_ACTIVATE=1

# # Ensure we’re root for installs and FS setup
USER root

# Create directories with proper ownership
RUN mkdir -p /workspace && \
    chown -R $MAMBA_USER:$MAMBA_USER /workspace && \
    chmod -R 755 /workspace

# Copy environment file
COPY environment.yml /tmp/environment.yml

# Create environment
RUN micromamba install -y -n nb_env -f /tmp/environment.yml && \
    micromamba clean --yes --all

# Create your env
# RUN micromamba create -y -n fepenv -c conda-forge \
#     python=3.10 \
#     requests \
#     openmm \
#     openfe \
#     openff-toolkit \
#     rdkit \
#     dask \
#     distributed \
#     pip && \
#     micromamba clean --all --yes

# Set the environment to be activated by default
ENV MAMBA_DEFAULT_ENV=nb_env

WORKDIR /workspace

# This is the key change
COPY . /workspace

# Drop privileges so writes happen as mambauser
USER $MAMBA_USER

CMD ["bash"]
