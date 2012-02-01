# Dorrie - Web interface for building Fedora Spins/Remixes. 
# Copyright (C) 2009 Red Hat Inc.
# Author: Shreyank Gupta <sgupta@redhat.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from forms import NameForm , BasicForm
from helper import new_spin, add_lang_tz, select_helper, get_spin, handle_uploaded_ks
from parse import (get_lang_tz, get_comps, default_selected,
     package_listing, build_ks, livecd_create, get_tail)

import os


def home(request):
    """
    Get the name, base spin, and time defaults
    """
    
    # Set the defaults of the field.
    defaults = {'name_of_the_spin': 'RIT_Remix', \
                'based_on': 'fedora-live-desktop.ks', \
                'select_timezone': 'America/New_York'}
    form = NameForm(initial= defaults)
    return render_to_response('home.html', {'form': form})


def packages(request):
    """
    Select packages and groups
    """
    # if the user is uploading their own kickstart file, toss it in a cache
    if request.FILES:
        handle_uploaded_ks(request.FILES['uploaded_kickstart'])
    
    # Create the spin object here.
    # Some thought the secondary "basic" form  was annoying, so I got rid of it.
    name = request.POST.get('name_of_the_spin')
    base_ks = request.POST.get('based_on')
    
    # Do a simple redirect if they accidentally skipped to this page
    if name == None or base_ks == None:
        return HttpResponseRedirect("/")
    
    # if we hit this, it's because they uploaded their own kickstart file
    uploaded = False
    if base_ks == 'None':
        base_ks = os.path.join(settings.MEDIA_ROOT, request.FILES['uploaded_kickstart']._name)
        uploaded = True
    spin = new_spin(name, base_ks, uploaded)
    
    spin_id = spin.id
    language = request.POST.get('select_language')
    timezone = request.POST.get('select_timezone')
    # These should not be none either.
    if language == None or timezone == None:
        return HttpResponseRedirect("/")
    print spin.uploaded
    spin = add_lang_tz(spin_id, language, timezone)
    print spin.uploaded    
    selected, plus, minus = default_selected(spin.baseks, spin.uploaded)
    c = get_comps()
    groups = package_listing(c)
    categories = c.get_categories()
    return render_to_response('packages.html', {'cats': categories,
        'groups': groups, 'defaults': selected, 'spin': spin,
        'plus': plus, 'minus': minus})
    

def select(request):
    """
    Record to backend when a select box is selected/unselected
    """
    spin_id = request.POST.get('spin_id')
    type = request.POST.get('type')
    action = request.POST.get('action')
    string = request.POST.get('string')
    html = select_helper(spin_id, type, action, string)
    return HttpResponse(html)


def build(request):
    """
    Build KS and later Image
    """
    spin_id = request.POST.get('spin_id')
    
    # if spin_id is None, then they accidentally skipped to this page
    if spin_id == None:
        return HttpResponseRedirect("/")
    
    new_ks = build_ks(spin_id)
    spin = get_spin(spin_id)
    return render_to_response('build.html', {'ks': new_ks, 'spin': spin})
    

def process(request):
    """
    start livecd-creator as a separate process
    """
    spin_id = request.POST.get('spin_id')
    pid = livecd_create(spin_id)
    html = "Process %s started.." % pid
    return HttpResponse(html)


def tail(request):
    """
    Return tail of the log
    """
    spin_id = request.POST.get('spin_id')
    html = get_tail(spin_id)
    return HttpResponse(html)

