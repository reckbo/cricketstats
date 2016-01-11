#!/usr/bin/env python

import yaml
import sys
import csv
from os.path import basename, splitext

EXTRATYPES = ['byes', 'legbyes', 'noballs', 'penalty', 'wides']

def flattenDelivery(delivery, matchid, team, innings):
    ballnum = delivery.keys()[0]

    result = {
            'matchid': matchid,
            'team': team,
            'ball': ballnum,
            'innings': innings
            }

    ballInfo = delivery[ballnum]

    ## Constant fields
    result['batsman']=ballInfo['batsman']
    result['bowler']=ballInfo['bowler']
    result['non_striker']=ballInfo['non_striker']
    result['runs']=ballInfo['runs']['batsman']
    result['extras']=ballInfo['runs']['extras']
    result['runs_total']=ballInfo['runs']['total']

    ## Optional fields
    # Extras
    if 'extras' in ballInfo.keys():
        for extraType in EXTRATYPES:
              result[extraType] =  ballInfo['extras'].get(extraType, 0)
    else:
        for extraType in EXTRATYPES:
            result[extraType] = 0
    # Wicket
    wicket = ballInfo.get('wicket',{})
    result['wicket'] = wicket.get('kind', None)  # e.g. caught, bowled, etc.
    result['player_out'] = wicket.get('player_out', None)

    # Fielders
    fielders = wicket.get('fielders', None)
    fielderRows = None
    if fielders is not None:
        fielderRows = [ {'matchid': matchid, 'innings': innings, 'ball': ballnum, 'fielder': fielder } for fielder in fielders]

    return (result, fielderRows)

def getDeliveries(y, matchid):
    deliveriesOut = []
    fieldersOut = []

    team = y['innings'][0]['1st innings']['team']
    deliveries = y['innings'][0]['1st innings']['deliveries']
    for d in deliveries:
        dFlat, field = flattenDelivery(d,matchid,team,1)
        deliveriesOut.append(dFlat)
        if field:
            fieldersOut.extend(field)

    team = y['innings'][1]['2nd innings']['team']
    deliveries = y['innings'][1]['2nd innings']['deliveries']
    for d in deliveries:
        dFlat, field = flattenDelivery(d,matchid,team,2)
        deliveriesOut.append(dFlat)
        if field:
            fieldersOut.extend(field)

    return (deliveriesOut, fieldersOut)

def getMatchInfo(y, matchid):
    result = { 'matchid' : matchid }

    # Constant
    info = y['info']
    result['date'] = y['info']['dates'][0]
    result['overs'] = y['info']['overs']
    result['team1'] = info['teams'][0]
    result['team2'] = info['teams'][1]
    result['venue'] = info['venue']
    result['city'] = info['city']
    result['toss_winner'] = info['toss']['winner']
    result['toss_decision'] = info['toss']['decision']
    result['umpires'] = " ".join(info['umpires'])

    # Optional
    result['player_of_match'] = info.get('player_of_match', None)
    outcome = y['info']['outcome']
    result['winner'] = outcome.get('winner',None)
    result['byruns'] = outcome.get('by', {}).get('runs', None)
    result['bywickets'] = outcome.get('by', {}).get('wickets', None)
    result['method'] = outcome.get('method', None)

    return result


def writeDeliveries(d):
    matchid = str(d[0]['matchid'])
    out = "odi/%s-deliveries.csv" % matchid
    fieldnames = [
            'matchid',
            'team',
            'innings',
            'ball',
            'batsman',
            'bowler',
            'penalty',
            'noballs',
            'wides',
            'byes',
            'legbyes',
            'non_striker',
            'runs',
            'extras',
            'runs_total',
            'wicket',
            'fielders',
            'player_out']
    with open(out, 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames)
        dict_writer.writeheader()
        dict_writer.writerows(d)

def writeFielders(d):
    print d
    out = "odi/%s-fielders.csv" % str(d[0]['matchid'])
    fieldnames = [
            'matchid',
            'innings',
            'ball',
            'fielder'
            ]
    with open(out, 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames)
        dict_writer.writeheader()
        dict_writer.writerows(d)

def writeMatchInfo(d):
    out = "odi/%s.csv" % str(d['matchid'])
    fieldnames = [
    'matchid',
    'date',
    'team1',
    'team2',
    'city',
    'venue',
    'overs',
    'toss_winner',
    'toss_decision',
    'umpires',
    'player_of_match',
    'winner',
    'byruns',
    'bywickets',
    'method']

    with open(out, 'w') as f:
        dict_writer = csv.DictWriter(f, fieldnames)
        dict_writer.writeheader()
        dict_writer.writerows([d])

def loadyaml(filepath):
    with open(filepath) as f:
        y = yaml.load(f.read())
    return y

def getMatchid(filepath):
    return splitext(basename(filepath))[0]

def main():
    y = loadyaml(sys.argv[1])
    matchid = getMatchid(sys.argv[1])

    (deliveries, fielderRows) = getDeliveries(y, matchid)
    writeDeliveries(deliveries)
    writeFielders(fielderRows)

    info = getMatchInfo(y, matchid)
    writeMatchInfo(info)



if __name__ == "__main__":
    main()
