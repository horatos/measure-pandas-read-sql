#!/bin/bash

APP="docker compose run --rm app"

if [ $# -ne 2 ]; then
	echo "Specify the number of rows and the chunksize"
	exit 2
fi

NROWS=$1
CHUNKSIZE=$2

function die () {
	docker compose down
	exit 1
}

function do_exps () {
	DB=$1
	$APP exp1 --db $DB || die
	$APP exp2 --db $DB --chunksize $CHUNKSIZE || die
	$APP exp3 --db $DB || die
	$APP exp4 --db $DB --chunksize $CHUNKSIZE || die
}

docker compose build
docker compose up -d mysql8 postgres

$APP init --nrows $NROWS || die

do_exps "mysql8"
do_exps "postgres"


docker compose down

exit 0
