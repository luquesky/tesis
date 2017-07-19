# Generate CSV for Argentine Spanish Corpus

1. Put the corpus at `data/games-eeg`. If you already have it elsewhere, just soft-link it with `ln -s`

2. Install requirements

```
pip install -r requirements.txt
```

3. Run these commands

```
python step_0b_create_spanish_eeg_instances.py run tables/spanish.csv
python step_1_calculate_tama.py run tables/spanish.csv
python step_2_calculate_entrainment.py run tables/spanish.pickle tables/spanish.csv
```

4. Generated csv will be at `tables/spanish.csv`