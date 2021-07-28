#!/usr/bin/env python3

import invoke
import logging


# initialize logging
logging.basicConfig(level=logging.INFO, format=invoke.util.LOG_FORMAT)


@invoke.task()
def lint(ctx):
    """run ansible/yaml linters"""
    ctx.run("ansible-lint")


@invoke.task()
def list(ctx):
    """list test platform"""
    ctx.run("bundle exec kitchen list")


@invoke.task()
def create(ctx, platform):
    """start test platform"""
    invoke.util.log.info(f"Start {platform} platform")
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
    if platform == "ubuntu-1604":
        require_pip = "True"
        require_pip3 = "False"
    else:
        require_pip = "False"
        require_pip3 = "True"
    ctx.run(
        f"bundle exec kitchen converge {platform}",
        env={
            # Fix issue with Docker not parsing build output for image ID
            "DOCKER_BUILDKIT": "0",
            "PLAYBOOK_NAME": playbook,
            "REQUIRE_PIP": require_pip,
            "REQUIRE_PIP3": require_pip3,
        },
    )


@invoke.task()
def destroy(ctx):
    """destroy all test platform"""
    invoke.util.log.info("Destroy test platform")
    ctx.run("bundle exec kitchen destroy")


@invoke.task()
def test(ctx, platform, playbook):
    """
    It will run create, converge, verify and destroy in sequence and you can just chill,
    watch the logs and enjoy your fantastic Ansible Role!
    """
    invoke.util.log.info(f"Start E2E test on {platform}")
    if platform == "ubuntu-1604":
        require_pip = "True"
        require_pip3 = "False"
    else:
        require_pip = "False"
        require_pip3 = "True"
    ctx.run(
        f"bundle exec kitchen test {platform}",
        env={
            # Fix issue with Docker not parsing build output for image ID
            "DOCKER_BUILDKIT": "0",
            "PLAYBOOK_NAME": playbook,
            "REQUIRE_PIP": require_pip,
            "REQUIRE_PIP3": require_pip3,
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
