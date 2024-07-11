import django
import os
import json
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Phage_api.settings")

django.setup()


def add_data():
    from Phage_api import settings_local as local_settings
    from publication.models import publication

    with open(local_settings.CRUSTDB_DATABASE + 'main/datasets.json') as f:
        data = json.load(f)
        for d in data:
            publication.objects.create(
                doi=d['doi'],
                title=d['title'] if 'title' in d.keys() else None,
                author=d['author'] if 'author' in d.keys() else None,
                journal=d['journal'] if 'journal' in d.keys() else None,
                volume=d['volume'] if 'volume' in d.keys() else None,
                number=d['number'] if 'number' in d.keys() else None,
                pages=d['pages'] if 'pages' in d.keys() else None,
                year=d['year'] if 'year' in d.keys() else None,
                abstract=d['abstract'] if 'abstract' in d.keys() else None,
                link=d['link'] if 'link' in d.keys() else None,
                publisher=d['publisher'] if 'publisher' in d.keys() else None,
            )


if __name__ == "__main__":
    add_data()
