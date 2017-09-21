#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import json
import os.path
import smtplib
import sys
from email.mime.text import MIMEText

def main():

    PFAD = os.path.dirname(os.path.realpath(sys.argv[0]))
    COUNTER = PFAD + '/counter.json'
    CONFIG =  PFAD + '/config.json'

    # Config laden

    with open(CONFIG, 'r') as f:
        config = json.load(f)

    # 1. Seite abrufen und in eine lokale Datei speichern

    # ### TODO: Mehrere Seiten anhand von websites.json abrufen ###

    print("Checke", config['page'], "...")

    with urllib.request.urlopen(config['page']) as f:
        data = f.read()
        current_length = len(data)

    # 2. Wenn Counterdatei existiert, Wert aus Datei lesen
    # 3. Wenn gespeicherte und aktuelle Länge nicht übereinstimmen, E-Mail senden

    if os.path.isfile(COUNTER):

        with open(COUNTER, 'r') as f:
            counter = json.load(f)

        if counter['length'] != current_length:
            print(counter['length'], current_length)
            server = smtplib.SMTP(config['server'])
            server.starttls()
            server.ehlo()
            server.login(config['from'], config['pass'])

            text = u"Hallo,\n\nauf {} hat sich etwas geändert.".format(config['page'])

            nachricht = MIMEText(text.encode('utf-8'), 'plain', 'utf-8')
            nachricht['From'] = u"Checkwebsite Service <{}>".format(config['from'])
            nachricht['To'] = u", ".join(config['to'])
            nachricht['Subject'] = u"Checkwebsite: Änderung gefunden!"

            server.sendmail(config['from'], config['to'], nachricht.as_string())
            server.quit()

            with open(COUNTER, 'w') as f:
                json.dump({'length':  len(data)}, f)

    # 4. Wenn Counter nicht existiert, in Datei schreiben

    else:
        with open(COUNTER, 'w') as f:
            json.dump({'length':  len(data)}, f)


if __name__ == '__main__':
    main()
