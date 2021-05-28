# Testing an Ansible role using Test Kitchen
My experiment with using Test Kitchen and Kitchen Ansible extension to set up automated testing for Ansible roles in Docker.

## Requirements
* [Docker](https://www.docker.com/)
* [Ruby](https://www.ruby-lang.org/)
* [Ruby Gems](https://rubygems.org/)
* [Bundler](https://bundler.io/)

## Dependencies
* [test-kitchen](https://github.com/test-kitchen/test-kitchen)
* [kitchen-docker](https://github.com/test-kitchen/kitchen-docker)
* [kitchen-ansible](https://github.com/neillturner/kitchen-ansible)

## Getting Started
To install all of these we use bundle install
```bash
bundle install --path vendor/bundle
```
## Start test platforms
```bash
bundle exec kitchen list
bundle exec kitchen create
```
If error: "Message: Could not parse Docker build output for image ID"
```bash
export DOCKER_BUILDKIT=0
```
## Run Ansible playbook on the test platforms
```bash
bundle exec kitchen converge
```
## Delete test platforms
```bash
bundle exec kitchen destroy
```
