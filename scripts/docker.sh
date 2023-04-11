#!/bin/bash

set -x

dockerize() {
	folder="challs/$1"
	name="dctf23.azurecr.io/challs/$2:latest"
	pushd $folder
	docker build --platform=linux/amd64 -t $name . &&
	docker push $name
	popd
}

# Pwn
dockerize "vun" "vun"
dockerize "casino" "casino"
