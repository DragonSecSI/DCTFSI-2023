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
dockerize "shellstraction_2" "shellstraction"

# Crypto
dockerize "singing_rsa/app" "rsa"

# Web
dockerize "timely_manner/app" "timely-manner"
dockerize "yet_another_blog/app" "yet-another-blog"

# Misc
dockerize "xoxo" "xoxo"
