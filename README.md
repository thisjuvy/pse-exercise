# pse-exercise long polling script
This repo contains the scripts for the Box Platform Programming Exercise v2.0

## Getting started
This repo contains two subfolders:
`node-example` and `python-example`

Simply follow along with the solution of choice by completing the corresponding sections (e.g node)

## Prerequisites

### node
- Install nodejs
- [node] https://nodejs.org/en/download/

### python
- Install python3
- [python3] https://www.python.org/downloads/

## Setup

### node
- `git clone git@github.com:juvyinparallel/pse-exercise.git`
- `cd ~/pse-exercise/node-example`
- `npm install`

### python
- `git clone git@github.com:juvyinparallel/pse-exercise.git`
- `cd ~/pse-exercise/python-example`
- `python3 -m venv pse-exercise`
- `source pse-exercise/bin/activate`
- `pip install requests`

## Run the script
Prior to running the script, you will need to provide a valid Access Token (Developer Token). The script will exit if the token referenced has expired or is invalid.

- visit https://developers.box.com/
- click "PSE-Exercise" under My Apps
- click "Configuration" on the left navigation menu
- click "Generate Developer Token"
- ensure you reference this value in the script (`ACCESS_TOKEN`)

### node
- `cd ~/pse-exercise/node-example`
- `node index`

### python
- `cd ~/pse-exercise/python-example`
- `python3 index.py`
