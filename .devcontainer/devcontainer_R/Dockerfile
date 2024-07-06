# Start with R base image
FROM rocker/r-ver:4.1.2

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libfontconfig1-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libfreetype6-dev \
    libpng-dev \
    libtiff5-dev \
    libjpeg-dev \
    libhdf5-dev \
    python3 \
    python3-pip \
    python3-dev

# Install Python packages
RUN pip3 install --upgrade pip
RUN pip3 install jupyter numpy pandas matplotlib seaborn scikit-learn

RUN R -e "install.packages('devtools', repos='http://cran.rstudio.com/'); library(devtools)"
RUN R -e "install.packages('BiocManager', repos='http://cran.rstudio.com/'); library(BiocManager)"
RUN R -e "BiocManager::install(c('SingleCellExperiment', 'SummarizedExperiment')); library(SingleCellExperiment); library(SummarizedExperiment)"

# install Matrix 1.6.4
RUN R -e "install.packages('https://cran.r-project.org/src/contrib/Archive/Matrix/Matrix_1.6-4.tar.gz')"
RUN R -e "install.packages('SeuratObject', repos='http://cran.rstudio.com/'); library(SeuratObject)"
RUN R -e "install.packages('sctransform', repos='http://cran.rstudio.com/'); library(sctransform)"
RUN R -e "install.packages('Seurat', repos='http://cran.rstudio.com/'); library(Seurat)"
RUN R -e "devtools::install_github('JiekaiLab/dior'); library(dior)"
RUN R -e "devtools::install_github('dmcable/spacexr'); library(spacexr)"
RUN R -e "install.packages('ggplot2', repos='http://cran.rstudio.com/'); library(ggplot2)"
# Install R packages
#RUN R -e "install.packages(c('devtools', 'BiocManager', 'Seurat'), repos='http://cran.rstudio.com/'); library(devtools); devtools::install_github('JiekaiLab/dior'); library(BiocManager); BiocManager::install(c("SingleCellExperiment", "SummarizedExperiment"))"
# Install IRkernel (R kernel for Jupyter)
RUN R -e "install.packages('IRkernel', repos='http://cran.rstudio.com/'); IRkernel::installspec(user = FALSE)"
# Set up Python kernel for Jupyter
RUN python3 -m ipykernel install --name python3 --display-name "Python 3"
