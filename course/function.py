# -*- coding: utf-8 -*-
__author__ = 'xiaohuanshu'
import re

weekstring = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']


def getweek(str):
    gweek = re.findall(u"(?<=\{第).*?(?=周[\}\|])", str, re.DOTALL)[0]
    week2 = gweek.split('-')
    we = []
    issingle = u'|单周' in str
    isdouble = u'|双周' in str
    for i in range(int(week2[0]), int(week2[1]) + 1):
        if issingle and i % 2 == 0:
            continue
        if isdouble and i % 2 == 1:
            continue
        we.append(i)
    return we


def gettime(str):
    week = re.findall(u"(?<=第).*?(?=节)", str, re.DOTALL)[0]
    week2 = week.split(',')
    we = []
    for i in week2:
        we.append(int(i))
    return we


def getday(str):
    if u"周一" in str:
        return 1
    elif u"周二" in str:
        return 2
    elif u"周三" in str:
        return 3
    elif u"周四" in str:
        return 4
    elif u"周五" in str:
        return 5
    elif u"周六" in str:
        return 6
    elif u"周日" in str:
        return 0


def t(ele1, ele2):
    if ele1['week'] > ele2['week']:
        return 1
    elif ele1['week'] < ele2['week']:
        return -1
    elif ele1['week'] == ele2['week']:
        if ele1['day'] > ele2['day']:
            return 1
        elif ele1['day'] < ele2['day']:
            return -1
        elif ele1['day'] == ele2['day']:
            if ele1['time'] > ele2['time']:
                return 1
            elif ele1['time'] < ele2['time']:
                return -1
            elif ele1['time'] == ele2['time']:
                return 0


def splitlesson(timestr, classroomstr):
    Sroom = classroomstr.split(';')
    i = -1
    data = []
    for Sweek in timestr.split(';'):
        i = i + 1
        for week in getweek(Sweek):
            for time in gettime(Sweek):
                data.append({'week': week, 'day': getday(Sweek), 'time': time, 'length': 1, 'location': Sroom[i]})
    data.sort(cmp=t)
    i = 0
    while i <= len(data) - 2:
        while (data[i]['week'] == data[i + 1]['week']) and (data[i]['day'] == data[i + 1]['day']) and (
                    data[i]['time'] == (data[i + 1]['time'] - data[i]['length'])) and (
                    data[i]['location'] == data[i + 1]['location']):
            data[i].update({'length': data[i]['length'] + 1})
            del data[i + 1]
            if i == len(data) - 1:
                break
        i = i + 1
    return data


def simplifytime(timestr, classroomstr):
    data = splitlesson(timestr, classroomstr)
    simplifydata = []

    for d in data:
        addflag = False
        for s in simplifydata:
            # print simplifydata
            if s['day'] == d['day'] and s['location'] == s['location'] and s['time'] == d['time'] and s['length'] == d[
                'length'] and s['weeklength'] + s['week'] == d['week'] and 'interval' not in s:
                s['weeklength'] += 1
                addflag = True
                break
            elif s['day'] == d['day'] and s['location'] == s['location'] and s['time'] == d['time'] and s['length'] == \
                    d['length'] and s['weeklength'] + s['week'] + 1 == d['week'] and (
                            'interval' in s or s['weeklength'] == 1):
                s['weeklength'] += 2
                s['interval'] = True
                addflag = True
                break
        if not addflag:
            d.update({'weeklength': 1})
            simplifydata.append(d)
    newtimestr = ';'.join(["%s第%s节{第%d-%d周%s}" % (
        weekstring[s['day']],
        ','.join([str(e) for e in range(s['time'], s['time'] + s['length'])]),
        s['week'], s['week'] + s['weeklength'] - 1,
        (('interval' in s and s['interval']) and '|' + (s['week'] % 2 == 0 and '双周' or '单周') or '')) for s in
                           simplifydata])
    newclassroomstr = ';'.join(s['location'] for s in simplifydata)
    return newtimestr, newclassroomstr