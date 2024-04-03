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
                doi = d['doi'],
                title = d['title'],
                author = d['author'],
                journal = d['journal'],
                volume = d['volume'] if 'volume' in d.keys() else None, 
                number = d['number'] if 'number' in d.keys() else None, 
                pages = d['pages'] if 'pages' in d.keys() else None, 
                year = d['year'],
                abstract = d['abstract'],
                publisher = d['publisher'],
            )

if __name__ == "__main__":
    add_data()
