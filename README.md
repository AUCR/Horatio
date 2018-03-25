# Horatio
[![Build Status](https://travis-ci.org/AUCR/Horatio.svg?branch=master)](https://travis-ci.org/AUCR/Horatio)
[![codecov](https://codecov.io/gh/AUCR/Horatio/branch/master/graph/badge.svg)](https://codecov.io/gh/AUCR/Horatio)
[![Coverage Status](https://coveralls.io/repos/github/AUCR/Horatio/badge.svg)](https://coveralls.io/github/AUCR/Horatio)

A DFIR case management system plugin for AUCR


## Organization Support Slack
[![AUCR Slack](https://slack.aucr.io/badge.svg)](https://slack.aucr.io/)

Please contact us in the organization slack and join the Horatio room to ask any questions!


## How to install

From the AUCR/app/plugins dir just git clone https://github.com/AUCR/Horatio and run the flask app.

    git clone https://github.com/AUCR/AUCR
    cd AUCR/app/plugins
    git clone https://github.com/AUCR/Horatio
    cd ../..
    EXPORT FLASK_APP=aucr.py
    flask run --host=127.0.0.1