import pandas as pd
from .models import *
from django.conf import settings
"""
This script is meant to be used with this specific dataset
https://drive.google.com/file/d/0B0810KzsNR3mUDkzdERQNmc3U00/view?usp=sharing
"""

dframe = pd.read_csv('/data/SoHAffordabilityDatabyNeighborhoodUpload.csv')

ry,_ = ReportYear.objects.get_or_create(year=2016)
ry.save()

for neighborhood in dframe.Neighborhood.unique():
    Neighborhood(name=neighborhood, report_year=ry)

for index, row in dframe.iterrows():
    d, _ = Demographic.objects.get_or_create(name=row['Demographic'])
    h, _ = HousingSize.objects.get_or_create(household_type=row['Unit_Size'])
    n, _ = Neighborhood.objects.get_or_create(name=row['Neighborhood'],report_year=ry)
    d.save()
    h.save()
    n.save()
    if row['Affordable_ind'] == 'Y':
        aff = True
    elif row['Affordable_ind'] == 'N':
        aff = False
        a = Affordable(
            affordable=aff,
            demographic=d,
            housing_size=h,
            neighborhood=n,
        )
        a.save()