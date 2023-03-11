#!/bin/bash

set -x

dockerize() {
	folder="challs/$1"
	name="dctf23.azurecr.io/challs/$2:latest"
	dockerfile=${3:-Dockerfile}
	pushd $folder
	docker build --platform=linux/amd64 -t $name -f $dockerfile . &&
	docker push $name
	popd
}

# Pwn
dockerize "vun" "vun"
dockerize "casino" "casino"
dockerize "shellstraction_2" "shellstraction"
dockerize "Team_Thread_Racing" "pthread"

# Rev
dockerize "amazeing" "amazeing"

# Crypto
dockerize "singing_rsa/app" "rsa"

# Web
dockerize "timely_manner/app" "timely-manner"
dockerize "yet_another_blog/app" "yet-another-blog"
dockerize "web-101/php" "web-101"
dockerize "sanitizer_3000" "sanitizer3000" "Dockerfile.web"
dockerize "sanitizer_3000" "sanitizer3000-bot" "Dockerfile.bot"

# Misc
dockerize "xoxo" "xoxo"
