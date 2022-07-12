#!/bin/bash

APP="docker compose run --rm app"

if [ $# -ne 1 ]; then
	echo "Specify the number of rows"
	exit 2
fi

NROWS=$1

function die () {
	docker compose down
	exit 1
}

docker compose build
docker compose up -d mysql postgres

$APP init --nrows $NROWS || die
$APP exp1 --db mysql || die
$APP exp1 --db postgres || die

docker compose down

exit 0
