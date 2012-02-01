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

from django import forms
from parse import ls_ks, languages, timezones

class NameForm(forms.Form):
    """
    Name and template
    """
    select_language = forms.ChoiceField(choices=languages(), initial='en_US')
    select_timezone = forms.ChoiceField(choices=timezones())
    name_of_the_spin = forms.CharField()
    
    # add a specific choice to the list of kickstarts for uploading their own
    kschoices = ((None, 'Use your own!'),) + ls_ks()
    based_on = forms.ChoiceField(choices=kschoices)
    
    # allows for the selection of a different kickstart
    uploaded_kickstart = forms.FileField()
    
    select_language.widget.attrs['class'] = 'forminputdropdown'
    select_timezone.widget.attrs['class'] = 'forminputdropdown'
    name_of_the_spin.widget.attrs['class'] = 'forminputtext'
    based_on.widget.attrs['class'] = 'forminputdropdown'


class BasicForm(forms.Form):
    """
    Name and template
    """
    #TODO fetch tz and lang from kickstart 
    select_language = forms.ChoiceField(choices=languages(), initial='en_US')
    select_timezone = forms.ChoiceField(choices=timezones())

    

