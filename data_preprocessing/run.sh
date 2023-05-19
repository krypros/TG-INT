#!/bin/sh
python -u ea_to_kge.py
python -u train_re_triples.py
python -u train_to_vt.py
python -u ents_rels_gen.py
python -u train_add_anchor.py
