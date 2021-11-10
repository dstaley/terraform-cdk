#!/usr/bin/python3 -tt
from constructs import Construct
from cdktf import App, TerraformStack, Testing, TerraformOutput
from imports.docker import Image, Container, DockerProvider

class References(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        DockerProvider(self, "provider")

        docker_image = Image(self, 'nginxImage', name='nginx:latest', keep_locally=False)

        # Simple References
        container = Container(self, 'nginxContainer', name='nginx-python-cdktf',
                  image=docker_image.repo_digest, ports=[
                      {
                          'internal': 80,
                          'external': 8000
                      }], privileged=False)
        # Single-item References
        TerraformOutput(self, "containerCapAdd", value=container.capabilities.add)

        # Direct Mutation
        docker_image.keep_locally = True

        # Reference Mutation
        container.privileged = docker_image.keep_locally



app = Testing.stub_version(App(stack_traces=False))
References(app, "references")

app.synth()
