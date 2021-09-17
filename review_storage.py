import csv
import hashlib
import os

import click
import psycopg2

from db import DB, DatabaseStringBuilder
from location import Location
from hotel_orm import HotelOrm
from review_orm import ReviewOrm
from reviewer_orm import ReviewerOrm
from errors import NotFoundException


def get_log_file_name(file_name):
    return hashlib.md5(file_name.encode()).hexdigest()


def find_or_create_hotel(db, row, location):
    """ Look for the hotel using name and address, create if none exists"""
    try:
        hotel = HotelOrm(db, by_fields={
            'hotel_name': row['Hotel'],
            'address': row['Address'],
        })
    except NotFoundException:
        hotel = HotelOrm(db, data={
            "hotel_name": row["Hotel"],
            "address": row['Address'],
            "location_id": location.id
        })
    hotel.save()
    return hotel


def parse_row(db, row):
    location = Location.new_location(db, row['Address'], 'Mexico')
    if not location.id:
        location.save()
    hotel = find_or_create_hotel(db, row, location)
    reviewer_location = Location.new_location(db, row['Reviewer Address'], 'DefaultLocation')
    # save reviewer location
    reviewer_location.save()
    # save reviewer
    reviewer = ReviewerOrm(db, data={
        "name": row['Reviewer'],
        'address': row['Address'],
        'location_id': location.id
    })
    reviewer.save()
    # set review properties
    review = ReviewOrm(db, data={
        'title': row['Review Title'],
        'rating': row['Review Star'],
        'full_review': row['Full Review'],
        'review_date': row['Date'],
        'word_count': len(row['Full Review'].split()),
        'reviewer_id': reviewer.id,
        'hotel_id': hotel.id
    })
    review.save()
    return [hotel.id, location.id, reviewer_location.id, review.id, reviewer.id]


@click.group()
def cli():
    pass


@click.command()
@click.option('--csv-file', help='path to csv file')
@click.option('--db', help='Database name')
@click.option('--db-user', help='Database user')
@click.option('--db-pass', help='Database password', default=None)
@click.option('--db-host', help='Database host', default=None)
@click.option('--db-port', help='Database port', default=None)
def parse_csv(**kwargs):
    """
    parses the CSV file and stores in database

    """
    csv_file = kwargs['csv_file']
    log_file = f"log/{get_log_file_name(csv_file)}"
    error_log_file = f"log/errors_{get_log_file_name(csv_file)}"
    i = 0
    total = 0
    start_from = 0
    errors = 0
    if os.path.exists(log_file):
        with open(log_file, 'r') as fp:
            progress = fp.readline()
            start_from = int(progress)
            print(f"Will skip {start_from} rows, delete {log_file} to start from beginning")
    db = get_db(kwargs)
    progress = ['|', '/', '‒', '\\', '|', '/', '‒', '\\']
    with open(csv_file) as fp:
        reader = csv.DictReader(fp)
        if start_from > total:
            for row in reader:
                total = total + 1
                if total > start_from:
                    break
        for row in reader:
            total = total + 1
            with open(log_file, "w") as lf:
                lf.write(f"{total}")
            print(f'\r{progress[i]} {total} row(s) / {errors} errors', end='')
            i = i + 1
            if i >= len(progress):
                i = 0
            try:
                parse_row(db, row)
            except psycopg2.Error as e:
                errors = errors + 1
                with open(error_log_file, "w+") as lf:
                    lf.write(f"{e}: {row}")
                continue


@click.command()
@click.option('--db', help='Database name')
@click.option('--db-user', help='Database user')
@click.option('--db-pass', help='Database password', default=None)
@click.option('--db-host', help='Database host', default=None)
@click.option('--db-port', help='Database port', default=None)
def count_avg_words(**kwargs):
    """ response with avg words in all reviews"""
    db = get_db(kwargs)
    q = "select avg(word_count) from reviews"
    r = db.query_get(q, ())
    print(f"Average words count is: {r[0][0]}")


def get_db(kwargs):
    # are we providing database information
    keys = {'db_pass': 'password', 'host': 'db_host', 'db_port': 'port'}
    db_builder = DatabaseStringBuilder(kwargs['db'], kwargs['db_user'])
    for k in keys:
        if k not in kwargs:
            continue
        db_builder.set_key(k, keys[k])
    dsn = db_builder.get_connection_string()
    return DB(dsn)


if __name__ == '__main__':
    cli.add_command(parse_csv)
    cli.add_command(count_avg_words)
    cli()
