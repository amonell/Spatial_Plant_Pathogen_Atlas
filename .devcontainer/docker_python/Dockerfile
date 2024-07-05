# Use the official ContinuumIO Anaconda image as a base image
FROM continuumio/anaconda3:latest

# Copy the environment.yml file into the Docker image
COPY python_scripts_environment.yml /tmp/python_scripts_environment.yml

# Install the dependencies from the environment.yml file
RUN conda env create -f /tmp/python_scripts_environment.yml

# Make the new environment the default environment
RUN echo "source activate python_plant_pathogen_atlas" > ~/.bashrc
ENV PATH /opt/conda/envs/python_plant_pathogen_atlas/bin:$PATH

# Set the default command to python3
CMD ["python3"]
