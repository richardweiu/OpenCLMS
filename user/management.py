# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, RequestContext, redirect
from rbac.auth import resourcejurisdiction_view_auth, is_user_has_resourcejurisdiction
from user.models import User
from django.http import HttpResponse
import json

@resourcejurisdiction_view_auth(jurisdiction='view_userlist')
def userlist(request):
    return render_to_response('user.html', {}, context_instance=RequestContext(request))


@resourcejurisdiction_view_auth(jurisdiction='view_userlist')
def userdata(request):
    limit = int(request.GET['limit'])
    offset = int(request.GET['offset'])
    userdata = User.objects.order_by('id')
    search = request.GET.get('search', '')
    if not search == '':
        count = userdata.filter(username__icontains=search).count()
        userdata = userdata.filter(username__icontains=search)[offset: (offset + limit)]
    else:
        count = userdata.count()
        userdata = userdata.all()[offset: (offset + limit)]

    rows = []
    for p in userdata:
        ld = {'id': p.id, 'username': p.username, 'sex': (p.sex - 1 and [u'女'] or [u'男'])[0], 'ip': p.ip,
              'registertime': p.registertime.strftime('%Y-%m-%d %H:%M:%S'),'iswechat': (p.openid and [u'是'] or [u'否'])[0],
              'lastlogintime': p.lastlogintime.strftime('%Y-%m-%d %H:%M:%S'), 'verify': (p.verify and [u'是'] or [u'否'])[0],
              'role': ", ".join(role.name for role in p.role.all())}
        rows.append(ld)
    data = {'total': count, 'rows': rows}
    return HttpResponse(json.dumps(data), content_type="application/json")
