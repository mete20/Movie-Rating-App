"""Populate movie data from CSV

Revision ID: 7965efeb8446
Revises: 6f0f19c6d605
Create Date: 2023-08-08 00:16:10.904081

"""
from typing import Sequence, Union
from alembic import op
from sqlalchemy import insert, delete
from app.models.model_movie import Movie
import csv

# revision identifiers, used by Alembic.
revision: str = '7965efeb8446'
down_revision: Union[str, None] = '6f0f19c6d605'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """This method reads the movies.csv file and fills the movie table.
    In the Revenue column, null tuples are denoted as N so the upgrade handles null values.
    """
    with open('app/db/movies.csv', 'r') as csv_file:
        conn = op.get_bind()

        csv_reader = csv.DictReader(csv_file)

        values_list = []
        for row in csv_reader:
            if row['Revenue'] == r'\N':
                row['Revenue'] = None
            else:
                row['Revenue'] = float(row['Revenue'])
            values_list.append(row)

        conn.execute(insert(Movie), values_list)
    # ### end Alembic commands ###


def downgrade() -> None:
    """ This method deletes all the data taken from the movies.csv file.
    """
    conn = op.get_bind()

    with open('db/movies.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        for row in csv_reader:
            stmt = delete(Movie).where(Movie.MovieID == int(row['MovieID']))
            conn.execute(stmt)
    # ### end Alembic commands ###