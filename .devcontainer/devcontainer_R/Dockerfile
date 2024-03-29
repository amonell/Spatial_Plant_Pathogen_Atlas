FROM r-base:4.0.5

ARG USERNAME=vscode
ARG USER_UID=1002
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    #
    # [Optional] Add sudo support. Omit if you don't need to install software after connecting.
    && apt-get update \
    && apt-get install -y sudo python3 python3-pip ffmpeg libaec-dev libblosc-dev libgif-dev libheif-dev build-essential libcurl4-gnutls-dev libbz2-dev liblzma-dev libxml2-dev libssl-dev libfontconfig1-dev libharfbuzz-dev libfribidi-dev libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev\
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME


# installing r libraries
RUN mkdir -p /home/$USERNAME/R/x86_64-pc-linux-gnu-library/4.0 && \
    chown $USERNAME:$USERNAME /home/$USERNAME/R/x86_64-pc-linux-gnu-library/4.0 && \
    Rscript -e "install.packages('devtools', repos='http://cran.rstudio.com/', lib='/home/$USERNAME/R/x86_64-pc-linux-gnu-library/4.0')" && \
    Rscript -e "devtools::install_github('JiekaiLab/dior')" && \
    Rscript -e "install.packages('IRkernel')" && \
    Rscript -e "IRkernel::installspec()"



ENV DEVCONTAINER=true