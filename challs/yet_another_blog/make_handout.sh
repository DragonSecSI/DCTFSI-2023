#!/bin/bash

# This script is used to generate the handout for the challenge.
# It is run from the root of the challenge directory.

FILES="app/ proxy/ docker-compose.yml .env.example"

# Create a temporary directory
TMPDIR=$(mktemp -d)
CHALLENGE_DIRNAME=$(basename $(pwd))
CPDIR=$TMPDIR/$CHALLENGE_DIRNAME
mkdir -p $CPDIR
ZIPNAME=challenge.tar.gz

security_measures() {
    # Remove the .git directory and .env file
    find $TMPDIR -name ".git" -type d -exec rm -rf {} \;
    find $TMPDIR -name ".env" -type f -exec rm -f {} \;
    echo "Removed .git and .env files" >&2
}

# Copy the files to the temporary directory
for f in $FILES; do
    cp -r $f $CPDIR
done

echo "Copied files to $TMPDIR" >&2

security_measures

# Create the handout archive
tar -czvf $ZIPNAME -C $TMPDIR $CHALLENGE_DIRNAME

echo "Created handout archive: $ZIPNAME" >&2

# Remove the temporary directory
rm -rf $TMPDIR >&2

echo "Removed temporary directory: $TMPDIR" >&2

echo $ZIPNAME
