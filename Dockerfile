# Rust crate build stage
FROM rust:latest as builder
WORKDIR /usr/src/crosswords
COPY Cargo* ./
COPY src/ ./src
RUN cargo install --path .

# Stage 1 - bundle base image + runtime
# Grab a fresh copy of the image and install GCC
FROM python:3.9-slim AS python-slim
# Install aws-lambda-cpp build dependencies
WORKDIR /home/app/
RUN apt update \
    && apt install -y \
        g++ \
        make \
        cmake \
        unzip \
        libcurl4-openssl-dev \
    && apt autoremove -y
COPY --from=builder /usr/local/cargo/bin/crossword /usr/local/bin/crossword

COPY cloud_run.py .
COPY plot/plot.py ./plot/plot.py

# Stage 2 - build function and dependencies
FROM python-slim AS build-image
COPY requirements.txt ./
COPY plot/requirements.txt ./plot/
RUN python3.9 -m pip install --no-cache-dir -r requirements.txt --target /home/app/
# Install Lambda Runtime Interface Client for Python
RUN python3.9 -m pip install awslambdaric --target /home/app/

# Stage 3 - final runtime image
# Grab a fresh copy of the Python image 
FROM python-slim
# Include global arg in this stage of the build
# Set working directory to function root directory
# Copy in the built dependencies
COPY --from=build-image /home/app/ /home/app/
# (Optional) Add Lambda Runtime Interface Emulator and use a script in the ENTRYPOINT for simpler local runs
ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
COPY entry.sh /
RUN chmod 755 /usr/bin/aws-lambda-rie /entry.sh
ENTRYPOINT [ "/entry.sh" ]
CMD [ "cloud_run.lambda_handler" ]
