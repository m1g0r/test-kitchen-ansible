# Testing an Ansible role using Test Kitchen
My experiment with using Test Kitchen and Kitchen Ansible extension to set up automated testing for Ansible roles in Docker.

### Requirements
* [Docker](https://www.docker.com/)
* [Ruby](https://www.ruby-lang.org/)
* [Ruby Gems](https://rubygems.org/)
* [Bundler](https://bundler.io/)

### Dependencies
* [test-kitchen](https://github.com/test-kitchen/test-kitchen)
* [kitchen-docker](https://github.com/test-kitchen/kitchen-docker)
* [kitchen-ansible](https://github.com/neillturner/kitchen-ansible)

### Available platforms:
- ubuntu-16.04
- ubuntu-18.04
- ubuntu-20.04

### Getting Started
To install all of these we use bundle install
```bash
make init
```
Check all available options:
```bash
invoke --list
```
### Start test platforms
Show a list of supported platforms
```
invoke kitchen.list
```
Manually start test one of the platform
```
invoke kitchen.create ubuntu-1604 playbook.yml
```
If error: "Message: Could not parse Docker build output for image ID"
```
export DOCKER_BUILDKIT=0
```
Then start test platforms

### Manually run Ansible playbook on the test platforms
```
invoke kitchen.converge ubuntu-1604 playbook.yml
```
### Manually delete all test platforms
```
invoke kitchen.destroy
```
### Alternately you can run the command below:
```bash
invoke kitchen.test ubuntu-1604 playbook.aml
```
It will run create, converge, verify and destroy in sequence and you can just chill, watch the logs and enjoy your fantastic Ansible Role!
