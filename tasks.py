#!/usr/bin/env python3

import yaml
import invoke
import logging


# initialize logging
logging.basicConfig(level=logging.INFO, format=invoke.util.LOG_FORMAT)


def _gen_kitchen_options(platform, playbook):
    with open("kitchen.yml") as f:
        kitchen = yaml.load(f, Loader=yaml.FullLoader)

    if platform == "ubuntu-1604":
        kitchen["provisioner"]["require_pip"] = True
    else:
        kitchen["provisioner"]["require_pip3"] = True

    kitchen["provisioner"]["playbook"] = f"ansible/{playbook}"

    with open("kitchen.local.yml", "w") as f:
        yaml.dump(kitchen, f)


@invoke.task()
def lint(ctx):
    """run ansible/yaml linters"""
    ctx.run("ansible-lint")


@invoke.task()
def list(ctx):
    """list test platform"""
    ctx.run("bundle exec kitchen list")


@invoke.task()
def create(ctx, platform, playbook):
    """start test platform"""
    invoke.util.log.info(f"Start {platform} platform")
    _gen_kitchen_options(platform, playbook)
    ctx.run(
        f"bundle exec kitchen create {platform}",
        env={
            # Fix issue with Docker not parsing build output for image ID
            "DOCKER_BUILDKIT": "0",
        },
    )


@invoke.task()
def converge(ctx, platform, playbook):
    """start provisioning test platform"""
    invoke.util.log.info(f"Start provisioning {platform} platform")
    _gen_kitchen_options(platform, playbook)
    ctx.run(
        f"bundle exec kitchen converge {platform}",
        env={
            # Fix issue with Docker not parsing build output for image ID
            "DOCKER_BUILDKIT": "0",
        },
    )


@invoke.task()
def destroy(ctx):
    """destroy all test platform"""
    invoke.util.log.info("Destroy test platform")
    ctx.run("bundle exec kitchen destroy")


@invoke.task()
def test(ctx, platform, playbook):
    """It will run create, converge, verify and destroy in sequence and you can just chill, watch the logs and enjoy your fantastic Ansible Role!"""
    _gen_kitchen_options(platform, playbook)
    invoke.util.log.info(f"Start E2E test on {platform}")
    ctx.run(
        f"bundle exec kitchen test {platform}",
        env={
            # Fix issue with Docker not parsing build output for image ID
            "DOCKER_BUILDKIT": "0",
        },
    )


kitchen = invoke.Collection("kitchen")
kitchen.add_task(list, name="list")
kitchen.add_task(create, name="create")
kitchen.add_task(converge, name="converge")
kitchen.add_task(destroy, name="destroy")
kitchen.add_task(test, name="test")

ansible = invoke.Collection("ansible")
ansible.add_task(lint, name="lint")

ns = invoke.Collection()
ns.add_collection(kitchen)
ns.add_collection(ansible)
