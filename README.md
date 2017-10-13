 [![Build Status](https://travis-ci.org/finiteautomata/tesis.svg?branch=master)](https://travis-ci.org/geekazoid/tesis)

tesis
=====

Repo de mi tesis.




# Instalación

1. Install `python-2.7`
2. Put the corpus at `data/games-corpus`. If you already have it elsewhere, just soft-link it with `ln -s`
3. Install requirements

```
pip install -r requirements.txt
```

3. Run these commands

```
python step_0_create_instances.py run
python step_1_calculate_tama.py run tables/output.csv
python step_2_calculate_entrainment.py run tables/output.pickle tables/output.csv
```

4. Generated csv will be at `tables/output.csv`
