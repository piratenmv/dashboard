#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import json
import urllib.parse
import urllib.request
import time
import math
import locale
import calendar
import datetime
import timelib

def prettydate(t, fuzzy=False):
    time_word = 'vor'

    d = datetime.datetime(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
    diff = datetime.datetime.utcnow() - d

    if (diff.days < 0):
        diff = d - datetime.datetime.utcnow()
        time_word = 'in'

    s = diff.seconds

    if diff.days >= 60:
        return '{} {} Monaten'.format(time_word, round(diff.days / 30))
    if diff.days > 30 and diff.days < 60:
        return '{} 1 Monat'.format(time_word)
    if diff.days > 14:
        return '{} {} Wochen'.format(time_word, round(diff.days / 7))
#        return d.strftime('%d.%m.%Y %H:%M')
    elif diff.days == 1:
        return 'gestern'
    elif diff.days > 1:
        return '{} {} Tagen'.format(time_word, diff.days)

    if fuzzy == True:
        return "heute"
    elif s <= 1:
        return 'jetzt'
    elif s < 60:
        return '{} {} Sekunden'.format(time_word, s)
    elif s < 120:
        return '{} 1 Minute'
    elif s < 3600:
        return '{} {} Minuten'.format(time_word, round(s/60))
    elif s < 7200:
        return '{} 1 Stunde'
    else:
        return '{} {} Stunden'.format(time_word, round(s/3600))


###############
# HTML HEADER #
###############

fout = open("index.html~", mode='w')

html_header = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>PIRATEN MV Dashboard</title>
    <link rel="stylesheet" type="text/css" href="assets/reset.css">
    <link rel="stylesheet" type="text/css" href="assets/grid.css">
    <link rel="stylesheet" type="text/css" href="assets/style.css">
</head>
<body>
    <div id="wrapper" class="grid clearfix">
<!--
        <div id="main" class="grid-1">
            <div id="logo"><h1>Twitter Open Source</h1></div>
            <h1>Twitter is built on open source software.</h1>
            <p>Want to help? <a href="https://twitter.com/jobs">Join the Flock</a></p>
            <p>Visit <a href="https://dev.twitter.com/">dev.twitter.com</a></p>
            <p><a href="https://twitter.com/about/resources">Logos and other goodies</a></p>
        </div>

        <div class="grid grid-3">
            <div id="statistics" class="grid-1 alpha header">
                <h1>Statistics</h1>
                <p>
                    <a href="https://github.com/twitter/repositories"><span id="num-repos">61</span> public repos</a>
                    <br>
                    <a href="https://github.com/twitter"><span id="num-members">120</span> members</a>
                </p>
                <p class="email"><a href="mailto:opensource@twitter.com">opensource@twitter.com</a></p>
            </div>

            <div id="recently-updated" class="grid-2 omega header">
                <h1>Recently updated <a href="https://github.com/twitter/repositories">View All on GitHub</a></h1>
                <ol id="recently-updated-repos"><li><span class="name"><a href="https://github.com/twitter/bootstrap">bootstrap</a></span><span class="time"><a href="https://github.com/twitter/bootstrap/commits">Feb 19, 2012</a></span><span class="bullet">⋅</span><span class="watchers"><a href="https://github.com/twitter/bootstrap/watchers">20526 watchers</a></span><span class="bullet">⋅</span><span class="forks"><a href="https://github.com/twitter/bootstrap/network">3774 forks</a></span></li><li><span class="name"><a href="https://github.com/twitter/cloudhopper-smpp">cloudhopper-smpp</a></span><span class="time"><a href="https://github.com/twitter/cloudhopper-smpp/commits">Feb 18, 2012</a></span><span class="bullet">⋅</span><span class="watchers"><a href="https://github.com/twitter/cloudhopper-smpp/watchers">41 watchers</a></span><span class="bullet">⋅</span><span class="forks"><a href="https://github.com/twitter/cloudhopper-smpp/network">7 forks</a></span></li><li><span class="name"><a href="https://github.com/twitter/twitter-text-rb">twitter-text-rb</a></span><span class="time"><a href="https://github.com/twitter/twitter-text-rb/commits">Feb 18, 2012</a></span><span class="bullet">⋅</span><span class="watchers"><a href="https://github.com/twitter/twitter-text-rb/watchers">182 watchers</a></span><span class="bullet">⋅</span><span class="forks"><a href="https://github.com/twitter/twitter-text-rb/network">71 forks</a></span></li></ol>
            </div>
        </div>
-->
'''

fout.write(html_header)
fout.write('<ol id="repos">')




##############
# MITGLIEDER #
##############

json_object = json.loads(urllib.request.urlopen("http://opendata.piratenpartei-mv.de/mv/mitglieder").read().decode('utf8'))

fout.write('''
<li class="entry grid-1 ">
    <a href="http://wiki.piratenpartei.de/Mitgliederzahl#Mitglieder_nach_Landesverband">
        <h2>Mitglieder</h2>
        <h3>Statistik</h3>''')

fout.write('<img src="http://wiki.piratenpartei.de/wiki/images/b/b0/Mitgliederentwicklung-nach-LVs.png" />')

fout.write('<ul>')

fout.write('''<li class="supporters">''' + str(json_object['mitglieder']) + ''' Mitglieder</li>''')
fout.write('''<li class="empty">''' + str(json_object['stimmberechtigt']) + ''' stimmberechtigt (''' + str(round(((json_object['stimmberechtigt'] / json_object['mitglieder']) * 100))) +  '''%)</li>''')

fout.write('''<li class="statistics">''' + str(json_object['mitglieder_je_einwohner']) + ''' pro 1 Mio. Einwohner</li>''')
fout.write('''<li class="empty">''' + str(json_object['mitglieder_je_flaeche']) + ''' pro 1000 km<sup>2</sup></li>''')

t = time.strptime(json_object['stand'], "%d.%m.%Y")
fout.write('''<li class="created">''' + prettydate(t) + ''' aktualisiert</li>''')


fout.write('</ul>')
fout.write('''</a>
</li>''')


##############
# KONTOSTAND #
##############

json_object = json.loads(urllib.request.urlopen("http://opendata.piratenpartei-mv.de/mv/kontostand").read().decode('utf8'))

fout.write('''
<li class="entry grid-1 ">
    <a href="http://piratenpartei-mv.de/spenden">
        <h2>Kontostand</h2>
        <h3>Statistik</h3>''')

fout.write('<ul>')

kontostand = "%.2f" % json_object['kontostand']

fout.write('''<li class="money">''' + str(kontostand) + ''' Euro</li>''')

# Set locale for date parsing
locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')

t = time.strptime(json_object['datum'].replace("&auml;", "ä"), "%d. %B %Y")

fout.write('''<li class="created">''' + prettydate(t) + ''' aktualisiert</li>''')

# Reset locale back to the default setting
locale.setlocale(locale.LC_TIME, '')


fout.write('</ul>')
fout.write('''</a>
</li>''')



############
# HELPDESK #
############

json_object = json.loads(urllib.request.urlopen("http://opendata.piratenpartei-mv.de/helpdesk").read().decode('utf8'))

fout.write('''
<li class="entry grid-1 ">
    <a href="https://helpdesk.piratenpartei-mv.de/otrs/index.pl">
        <h2>Helpdesk</h2>
        <h3>Statistik der letzten 30 Tage</h3>''')

fout.write('<ul>')

fout.write('''<li class="statistics">''' + str(json_object['tickets_total']) + ''' Tickets</li>''')
fout.write('''<li class="empty">''' + str(json_object['tickets_open']) + ''' offen</li>''')
fout.write('''<li class="empty">''' + str(json_object['tickets_closed']) + ''' geschlossen</li>''')
fout.write('''<li class="empty">''' + str(json_object['tickets_pending']) + ''' wartend</li>''')

fout.write('''<li class="statistics">''' + str(json_object['articles_total']) + ''' Nachrichten</li>''')
fout.write('''<li class="empty">''' + str(json_object['articles_mail']) + ''' E-Mails</li>''')
fout.write('''<li class="empty">''' + str(json_object['articles_internal']) + ''' intern</li>''')

fout.write('''<li class="created">jetzt aktualisiert</li>''')

fout.write('</ul>')
fout.write('''</a>
</li>''')








###################
# LIQUID ACCEPTED #
###################

lqfb_status = {
  "accepted": "akzeptiert, in Diskussion",
  "frozen": "eingefroren",
  "voting": "in Abstimmung"
}

json_object = json.loads(urllib.request.urlopen("http://opendata.piratenpartei-mv.de/lqfb/mv/status/voting").read().decode('utf8'))

for issue in json_object:
    fout.write('''
    <li class="entry grid-1 python">
        <a href="''' + str(issue['url']) + '''">
            <h2>''' + issue['name'][0:50])
    if len(issue['name']) > 50:
        fout.write("...")
    fout.write('''</h2>
            <h3>LQFB-Initiative</h3>''')

    fout.write('<ul>')

    #fout.write('''<li class="supporters">''' + str(issue['satisfied_supporter_count']) + ' von ' + str(issue['supporter_count']) + ' (' + str(math.ceil((issue['policy_initiative_quorum_num'] / issue['policy_initiative_quorum_den']) * 100 )) + '''% benötigt)</li>''')

    fout.write('''<li class="status">''' + lqfb_status[issue['issue_state']] + '''</li>''')
    fout.write('''<li class="tags">''' + issue['area_name'] + '''</li>''')

    t = time.strptime(issue['current_draft_created'], "%Y-%m-%d %H:%M:%S")
    fout.write('''<li class="created">''' + prettydate(t) + ''' angelegt</li>''')

    t = time.strptime(issue['issue_fully_frozen'], "%Y-%m-%d %H:%M:%S")
    fout.write('''<li class="empty">''' + prettydate(t) + ''' in Abstimmung</li>''')

    # there can be problems with initiatives that are voted < 1 day
    try:
        s = issue['issue_fully_frozen'] + ' + ' + issue['issue_voting_time']
        t = time.strptime(str(timelib.strtodatetime(bytes(s, 'utf-8'))), "%Y-%m-%d %H:%M:%S")
        fout.write('''<li class="empty">''' + prettydate(t) + ''' geschlossen</li>''')
    except:
        s = issue['issue_fully_frozen']
        t = time.strptime(str(timelib.strtodatetime(bytes(s, 'utf-8'))), "%Y-%m-%d %H:%M:%S")
        fout.write('''<li class="empty">''' + prettydate(t) + ''' geschlossen</li>''')
    
    

    fout.write('</ul>')
    fout.write('''</a>
    </li>''')

json_object = json.loads(urllib.request.urlopen("http://opendata.piratenpartei-mv.de/lqfb/mv/status/frozen").read().decode('utf8'))

for issue in json_object:
    fout.write('''
    <li class="entry grid-1 python">
        <a href="''' + str(issue['url']) + '''">
            <h2>''' + issue['name'][0:50])
    if len(issue['name']) > 50:
        fout.write("...")
    fout.write('''</h2>
            <h3>LQFB-Initiative</h3>''')

    fout.write('<ul>')

    #fout.write('''<li class="supporters">''' + str(issue['satisfied_supporter_count']) + ' von ' + str(issue['supporter_count']) + ' (' + str(math.ceil((issue['policy_initiative_quorum_num'] / issue['policy_initiative_quorum_den']) * 100 )) + '''% benötigt)</li>''')

    fout.write('''<li class="status">''' + lqfb_status[issue['issue_state']] + '''</li>''')
    fout.write('''<li class="tags">''' + issue['area_name'] + '''</li>''')

    t = time.strptime(issue['current_draft_created'], "%Y-%m-%d %H:%M:%S")
    fout.write('''<li class="created">''' + prettydate(t) + ''' angelegt</li>''')

    t = time.strptime(issue['issue_half_frozen'], "%Y-%m-%d %H:%M:%S")
    fout.write('''<li class="empty">''' + prettydate(t) + ''' eingefroren</li>''')

    if not 'days' in issue['issue_verification_time']:
        s = issue['issue_half_frozen'] + ' + 1 days'
    else:
        s = issue['issue_half_frozen'] + ' + ' + issue['issue_verification_time']
    t = time.strptime(str(timelib.strtodatetime(bytes(s, 'utf-8'))), "%Y-%m-%d %H:%M:%S")
    fout.write('''<li class="empty">''' + prettydate(t) + ''' abzustimmen</li>''')

    fout.write('</ul>')
    fout.write('''</a>
    </li>''')


json_object = json.loads(urllib.request.urlopen("http://opendata.piratenpartei-mv.de/lqfb/mv/status/accepted").read().decode('utf8'))

for issue in json_object:
    fout.write('''
    <li class="entry grid-1 python">
        <a href="''' + str(issue['url']) + '''">
            <h2>''' + issue['name'][0:50])
    if len(issue['name']) > 50:
        fout.write("...")
    fout.write('''</h2>
            <h3>LQFB-Initiative</h3>''')

    fout.write('<ul>')

    fout.write('''<li class="supporters">''' + str(issue['satisfied_supporter_count']) + ' von ' + str(issue['supporter_count']) + ' (' + str(math.ceil((issue['policy_initiative_quorum_num'] / issue['policy_initiative_quorum_den']) * 100 )) + '''% benötigt)</li>''')

    fout.write('''<li class="status">''' + lqfb_status[issue['issue_state']] + '''</li>''')
    fout.write('''<li class="tags">''' + issue['area_name'] + '''</li>''')

    t = time.strptime(issue['current_draft_created'], "%Y-%m-%d %H:%M:%S")
    fout.write('''<li class="created">''' + prettydate(t) + ''' angelegt</li>''')

    # there can be problems with initiatives that are discussed < 1 day
    try:
        s = issue['issue_created'] + ' + ' + issue['issue_discussion_time']
        t = time.strptime(str(timelib.strtodatetime(bytes(s, 'utf-8'))), "%Y-%m-%d %H:%M:%S")
        fout.write('''<li class="empty">''' + prettydate(t) + ''' eingefroren</li>''')
    except:
        s = issue['issue_created']
        t = time.strptime(str(timelib.strtodatetime(bytes(s, 'utf-8'))), "%Y-%m-%d %H:%M:%S")
        fout.write('''<li class="empty">''' + prettydate(t) + ''' eingefroren</li>''')

#    fout.write('''<li class="created">''' + time.strftime("%d.%m.%Y %H:%M", t) + '''</li>''')

    fout.write('</ul>')
    fout.write('''</a>
    </li>''')



###########
# ANTRÄGE #
###########

json_object = json.loads(urllib.request.urlopen("http://opendata.piratenpartei-mv.de/redmine/vorstand").read().decode('utf8'))

for issue in json_object['issues']:
    fout.write('''
    <li class="entry grid-1">
        <a href="https://redmine.piratenpartei-mv.de/redmine/issues/''' + str(issue['id']) + '''">
            <h2>''' + issue['subject'] + '''</h2>
            <h3>''' + issue['category']['name'] + ''' Landesvorstand</h3>''')

    fout.write('<ul>')

    fout.write('''<li class="status">''' + issue['status']['name'] + '''</li>''')

    fout.write('''<li class="assignee">''' + issue['custom_fields'][0]['value'].split(" ")[0] + " " + issue['custom_fields'][0]['value'].split(" ")[1] + '''</li>''')

    if len(issue['tags']) > 0:
        fout.write('''<li class="tags">''')
        for tag in issue['tags']:
            fout.write(tag['id'] + " ")
        fout.write('''</li>''')

    t = time.strptime(issue['created_on'], "%Y/%m/%d %H:%M:%S %z")
    fout.write('''<li class="created">''' + prettydate(t) + ''' gestellt</li>''')

    if 'fixed_version' in issue:
        if 'id' in issue['fixed_version']:
            j = json.loads(urllib.request.urlopen("https://redmine.piratenpartei-mv.de/redmine/versions/" + str(issue['fixed_version']['id']) + ".json").read().decode('utf8'))
            t = time.strptime(j['version']['due_date'] + " " + j['version']['custom_fields'][0]['value'], "%Y/%m/%d %H:%M")
            #print(j['version']['due_date'], j['version']['custom_fields'][0]['value'])
            fout.write('''<li class="empty">''' + prettydate(t) + ''' auf Tagesordnung</li>''')

#    fout.write('''<li class="created">''' + time.strftime("%d.%m.%Y %H:%M", t) + '''</li>''')

    fout.write('</ul>')
    fout.write('''</a>
    </li>''')




#################
# REDMINE TODOS #
#################

json_object = json.loads(urllib.request.urlopen("http://opendata.piratenpartei-mv.de/redmine/arbeitsamt").read().decode('utf8'))

for issue in json_object['issues']:
    if 'assigned_to' in issue:
        continue

    fout.write('''
    <li class="entry grid-1 ruby">
        <a href="https://redmine.piratenpartei-mv.de/redmine/issues/''' + str(issue['id']) + '''">
            <h2>''' + issue['subject'] + '''</h2>
            <h3>Todo</h3>''')

    fout.write('<ul>')

    fout.write('''<li class="status">''' + issue['status']['name'] + '''</li>''')

    if 'assigned_to' in issue:
        fout.write('''<li class="assignee">''' + issue['assigned_to']['name'] + '''</li>''')

    if len(issue['tags']) > 0:
        fout.write('''<li class="tags">''')
        for tag in issue['tags']:
            fout.write(tag['id'] + " ")
        fout.write('''</li>''')

    t = time.strptime(issue['created_on'], "%Y/%m/%d %H:%M:%S %z")
    fout.write('''<li class="created">''' + prettydate(t) + ''' erstellt</li>''')
#    fout.write('''<li class="created">''' + time.strftime("%d.%m.%Y %H:%M", t) + '''</li>''')

    fout.write('</ul>')
    fout.write('''</a>
    </li>''')


############
# PAD LIST #
############

json_object = json.loads(urllib.request.urlopen("http://opendata.piratenpartei-mv.de/pads").read().decode('utf8'))

count = 0

for issue in json_object:
    if count > 10:
        break
    count = count + 1
    
    title = issue['title']
    if title.find("[") == -1 or title.find("]") == -1:
        tag = ""
    else:
        tag = title[title.find("[")+1:title.find("]")]
        title = title[title.find("]")+1:]
    
    fout.write('''
    <li class="entry grid-1 java">
        <a href="''' + str(issue['url']) + '''">
            <h2>''' + title[0:50])
    if len(title) > 50:
        fout.write("...")
    fout.write('''</h2>
            <h3>Piratenpad</h3>''')

    fout.write('<ul>')

    fout.write('''<li class="assignee">''' + str(len(issue['editors'])))
    if len(issue['editors']) > 1:
        fout.write(" Autoren")
    else:
        fout.write(" Autor")
    fout.write('''</li>''')

    if issue['protected']:
        fout.write('''<li class="unpublic">geschützt</li>''')
    else:
        fout.write('''<li class="public">öffentlich</li>''')

    fout.write('''<li class="tags">mv ''' + tag.lower() + '''</li>''')

    t = time.strptime(issue['lastUpdate'], "%Y-%m-%d")
    fout.write('''<li class="created">''' + prettydate(t, True) + ''' editiert</li>''')
#    fout.write('''<li class="created">''' + time.strftime("%d.%m.%Y", t) + '''</li>''')

    fout.write('</ul>')
    fout.write('''</a>
    </li>''')


############
# CALENDAR #
############

# json_object = json.loads(urllib.request.urlopen("http://opendata.piratenpartei-mv.de/calendar").read().decode('utf8'))
# 
# for issue in json_object:
#     fout.write('''
#     <li class="entry grid-1 python">
#         <a href="http://piratenpartei-mv.de/kalender">
#             <h2>''' + issue['summary'][0:50])
#     if len(issue['summary']) > 50:
#         fout.write("...")
#     fout.write('''</h2>
#             <h3>Termin</h3>''')
# 
#     fout.write('<ul>')
# 
#     #fout.write('''<li class="assignee">''' + issue['editor'] + '''</li>''')
# 
#     #if issue['comments'] > 0:
#     #    fout.write('''<li class="comments">''' + str(issue['comments']) + ''' Kommentare</li>''')
# 
#     t = time.strptime(issue['foo'], "%Y-%m-%dT%H:%M:%S+02:00")
#     fout.write('''<li class="created">''' + prettydate(t) + '''</li>''')
# #    fout.write('''<li class="created">''' + time.strftime("%d.%m.%Y %H:%M", t) + '''</li>''')
# 
#     fout.write('</ul>')
#     fout.write('''</a>
#     </li>''')



####################
# WEBSITE ARTICLES #
####################

json_object = json.loads(urllib.request.urlopen("http://opendata.piratenpartei-mv.de/articles").read().decode('utf8'))

for issue in json_object:
    fout.write('''
    <li class="entry grid-1 scala">
        <a href="''' + str(issue['url']) + '''">
            <h2>''' + issue['title'][0:50])
    if len(issue['title']) > 50:
        fout.write("...")
    fout.write('''</h2>
            <h3>Webseitenartikel</h3>''')

    if 'imageurls' in issue and len(issue['imageurls']) > 0:
        fout.write('<img src="' + issue['imageurls'][0] + '" alt="' + issue['title'] + '" />')

    fout.write('<ul>')

    fout.write('''<li class="assignee">''' + issue['editor'] + '''</li>''')

    if issue['comments'] > 0:
        fout.write('''<li class="comments">''' + str(issue['comments']) + ''' Kommentare</li>''')

    t = time.strptime(issue['timestamp'], "%Y-%d-%m %H:%M")
    fout.write('''<li class="created">''' + prettydate(t) + ''' veröffentlicht</li>''')
#    fout.write('''<li class="created">''' + time.strftime("%d.%m.%Y %H:%M", t) + '''</li>''')

    fout.write('</ul>')
    fout.write('''</a>
    </li>''')



#################
# WIKI ARTICLES #
#################

wiki_actions = {
    "edit": "editiert",
    "new": "angelegt",
    "log": "verschoben"
}

json_object = json.loads(urllib.request.urlopen("http://opendata.piratenpartei-mv.de/wiki").read().decode('utf8'))

for issue in json_object['query']['recentchanges']:
    fout.write('''
    <li class="entry grid-1 java">
        <a href="http://wiki.piratenpartei.de/''' + urllib.parse.quote(str(issue['title'])) + '''">
            <h2>''' + issue['title'].replace("MV:", "")[0:50])
    if len(issue['title']) > 50:
        fout.write("...")
    fout.write('''</h2>
            <h3>Wikiseite</h3>''')


    fout.write('<ul>')


    fout.write('''<li class="assignee">''' + issue['user'] + '''</li>''')
#    fout.write('''<li class="status">''' + issue['type'] + '''</li>''')

    t = time.strptime(issue['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
    fout.write('''<li class="created">''' + prettydate(t) + ' ' + wiki_actions[issue['type']] + '''</li>''')
#    fout.write('''<li class="created">''' + time.strftime("%d.%m.%Y %H:%M", t) + '''</li>''')


    fout.write('</ul>')
    fout.write('''</a>
    </li>''')


############
# FACEBOOK #
############

json_object = json.loads(urllib.request.urlopen("http://opendata.piratenpartei-mv.de/facebook/piratenmv/stream").read().decode('utf8'))

count = 0

facebook_type = {
    "link": "Link auf Facebook",
    "status": "Status auf Facebook",
    "photo": "Foto auf Facebook",
    "video": "Video auf Facebook",
    "question": "Frage auf Facebook"
}

for i in json_object:
    issue = json_object[i]
    
    if not 'link' in issue:
        continue

    if count > 10:
        break

    if 'name' in issue:
        name = issue['name']
    else:
        name = "Kein Titel"

    count = count + 1
    if 'commenturl' in issue:
      fout.write('''
    <li class="entry grid-1 ">
        <a href="''' + issue['commenturl'] + '''">
            <h2>''' + name[0:50])
    else:
      fout.write('''
    <li class="entry grid-1 ">
        <a href="">
            <h2>''' + name[0:50])
    if len(name) > 50:
        fout.write("...")
    fout.write('''</h2>
            <h3>''' + facebook_type[issue['type']] + '''</h3>''')

    if issue['type'] == 'photo':
        fout.write('<img src="' + issue['picture'] + '" alt="' + name + '" />')

    fout.write('<ul>')

    if issue['comment_count'] > 0:
        fout.write('''<li class="comments">''' + str(issue['comment_count']) + ''' Kommentare</li>''')

    if 'likes' in issue and issue['likes'] > 0:
        fout.write('''<li class="likes">''' + str(issue['likes']) + ''' Likes</li>''')


    t = time.strptime(issue['time'], "%Y-%m-%dT%H:%M:%S+0000")
    fout.write('''<li class="created">''' + prettydate(t) + ''' veröffentlicht</li>''')
#    fout.write('''<li class="created">''' + time.strftime("%d.%m.%Y %H:%M", t) + '''</li>''')

#    fout.write('''<li class="assignee">''' + issue['user']['name'] + '''</li>''')


    fout.write('</ul>')
    fout.write('''</a>
    </li>''')


###############
# HTML FOOTER #
###############

fout.write('</ol>')

fout.write('''
    </div>

</body>
</html>
''')

fout.close()
