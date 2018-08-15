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
    
    
    
## Using the API
Example use case of getting the case information via the case ID using http on a terminal


    http GET httpss://aucr.io/api/case_info/1 "Authorization:Bearer IXPNMHdYkuijPeA9hUGJKv+dRHrToZQtQCiE/2ep6NMM43Q6EOrQPK6/cSlxAQfxf+OcAR7SzyYlAdtRtMAzXQ=="
    HTTP/1.1 200 OK
    Connection: keep-alive
    Content-Length: 393
    Content-Type: application/json
    Date: Wed, 15 Aug 2018 00:22:27 GMT
    
    {
        "assigned_to": 2,
        "attached_files": null,
        "case_notes": "some basic test notes",
        "case_rules": "domain:[somereallybadmalwaredomain.com]",
        "case_status": 4,
        "created_by": 1,
        "created_time_stamp": "2018-08-14T18:20:46Z",
        "description": "test description",
        "detection_method": "1",
        "group_access": 1,
        "id": 1,
        "modify_time_stamp": "2018-08-14T18:20:46Z",
        "subject": "test subject"
    }

