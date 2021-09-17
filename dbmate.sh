#!/bin/zsh

# run dbmate with default database configuration
dbmate $1
# run dbmate with test database configuration
URL=`cat tests/dsn_test.txt`
dbmate --url=$URL $1
