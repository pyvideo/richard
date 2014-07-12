# richard -- video index system
# Copyright (C) 2012, 2013 richard contributors.  See AUTHORS.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',

    url(r'^$', 'richard.base.views.home', name='home'),
    url(r'^login-failure$', 'richard.base.views.login_failure',
        name='login_failure'),
    url(r'^new_user$', 'new_user', name='new_user'),
    url(r'^stats/$', 'richard.base.views.stats', name='stats'),
)
