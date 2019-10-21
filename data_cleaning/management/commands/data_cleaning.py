import os

from django.core.management.base import BaseCommand
import pandas

from data_cleaning.models import Song, Contributor


DATA_PATH = "/code/raw_data/"


class Command(BaseCommand):

    help = 'Read csv input, "clean" and store'

    def handle(self, *args, **kwargs):
        """
        data_cleaning command entry point. This will read all the csv files on raw_data directory and try to reconcile
        them. Then store them.

        """
        files = self._get_files()

        for csv_file in files:
            self.stdout.write('Reading file: "%s"' % csv_file)
            self._evaluate_records_with_iswc(csv_file)
            # self._evaluate_records_without_iswc(csv_file)

    def _evaluate_records_with_iswc(self, filename):
        """
        This method groups by ISWC (ignoring the works without one) and merge the contributors (It also assumes that
        there cannot be the same code to different titles)

        Args:
            filename:
        """
        data_frame = pandas.read_csv(filename)
        data_frame = data_frame.groupby("iswc").agg({"title": "first", "contributors": "|".join}).reset_index()
        data_frame["contributors"].update(data_frame["contributors"].str.split("|"))
        self._create_items(data_frame.to_dict(orient="records"))

    def _evaluate_records_without_iswc(self, filename):
        """
        This method should take care of the records without ISWC, doing an union of songs with same name only if one of
        the contributors matches.

        Args:
            filename:
        """
        raise NotImplementedError()

    def _create_items(self, records: list):
        """
        Create or update the records read from csv files. The contributors records may have duplicated info due to the
        concatenation of the previous step, we do a set to remove duplications.

        Args:
            records: list of dictionaries with keys {
                iswc: string
                title: string
                contributors: list of strings
            }

        """

        for record in records:
            self.stdout.write('Evaluating record: "%s"' % record)
            song_item, song_check = Song.objects.get_or_create(iswc=record["iswc"], title=record["title"])
            contributors_set = set(record["contributors"])

            for contributor in contributors_set:
                contributor_created, contributor_check = Contributor.objects.get_or_create(name=contributor)
                song_item.contributors.add(contributor_created)

    @staticmethod
    def _get_files() -> list:
        """
        Get all the csv files of the raw_data folder

        Returns:
            List with file names

        """
        result = list()

        for r, d, files in os.walk(DATA_PATH):

            for file in files:

                if file.endswith(".csv"):
                    result.append(os.path.join(r, file))

        return result
