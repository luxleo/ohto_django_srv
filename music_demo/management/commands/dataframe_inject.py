from django.core.management.base import BaseCommand
import pandas as pd
from pathlib import Path
import os

from music_demo.models import Song

class Command(BaseCommand):
    def handle(self,*args,**options):
        base_path= Path(__file__).resolve().parent.parent.parent
        dataframe_path = os.path.join(base_path,'Dataframe_csv','for_django.csv')
        df = pd.read_csv(dataframe_path)
        for idx,row in df.iterrows():
            Song.objects.create(artist=row.artist,title=row.song,energy=row.e_label,valence=row.v_label)


