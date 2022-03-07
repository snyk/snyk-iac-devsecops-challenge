FROM ubuntu:focal as builder

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get upgrade -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        unzip curl wget

RUN mkdir /tmp/build

RUN cd /tmp/build && \
    wget "https://releases.hashicorp.com/terraform/1.0.0/terraform_1.0.0_linux_amd64.zip" && \
    unzip "terraform_1.0.0_linux_amd64.zip" && \
    chmod +x ./terraform

FROM ubuntu:focal
RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
         git \
         python3 \
         python3-pip \
         python3.8-venv  && \
    DEBIAN_FRONTEND=noninteractive apt-get clean
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# Install terraform
COPY --from=builder /tmp/build/terraform /usr/local/bin/terraform

WORKDIR /app
COPY . .
CMD ["python", "validate.py", "."]
