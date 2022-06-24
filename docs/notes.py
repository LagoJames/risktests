import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)

print(os.path.abspath(os.path.join(BASE_DIR, 'tests', 'synthetic_pd.xlsx')))


