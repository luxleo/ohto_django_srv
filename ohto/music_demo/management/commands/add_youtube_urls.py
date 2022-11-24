from django.core.management.base import BaseCommand
import pandas as pd
import os
from pathlib import Path

class Command(BaseCommand):
    def handle(self,*args,**kwargs):

        BASE_PATH = Path(__file__).parent.parent.parent
        DATA_PATH = os.path.join(BASE_PATH,'data','test.json')
        df = pd.read_json(DATA_PATH)
        print(df.head(10))