#!/bin/bash
python -m cProfile -o outfile.prof -m test.app.optimizeme && gprof2dot -f pstats outfile.prof | dot -Tpng -o output.png && eog output.png
