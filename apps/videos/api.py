# richard -- video index system
# Copyright (C) 2012 richard contributors.  See AUTHORS.
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

from tastypie import fields
from tastypie.authentication import (ApiKeyAuthentication, Authentication,
                                        MultiAuthentication)
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from videos.models import Video, Speaker, Category, Tag


class AdminAuthorization(Authorization):
    """Only admins get write access to resources."""

    def is_authorized(self, request, object=None):
        # Always allow read-access
        if request.method in ('GET', 'OPTIONS', 'HEAD'):
            return True

        if not hasattr(request, 'user'):
            return False

        return request.user.is_staff


def get_authentication():
    """Authenticate users with API key, but let all others though too.

    Authorization will handle the permissions.
    """
    return MultiAuthentication(ApiKeyAuthentication(), Authentication())


class VideoResource(ModelResource):
    category = fields.ToOneField('videos.api.CategoryResource', 'category')
    speakers = fields.ToManyField('videos.api.SpeakerResource', 'speakers')
    tags = fields.ToManyField('videos.api.TagResource', 'tags')

    class Meta:
        queryset = Video.objects.live()
        resource_name = 'video'
        authentication = get_authentication()
        authorization = AdminAuthorization()

    def hydrate(self, bundle):
        """Allow to pass in the actual names of tags and speakers."""
        bundle.data['tags'] = [Tag.objects.get_or_create(tag=x)[0]
                               for x in bundle.data.get('tags')]

        bundle.data['speakers'] = [Speaker.objects.get_or_create(name=x)[0]
                                   for x in bundle.data.get('speakers')]

        return bundle


class SpeakerResource(ModelResource):

    class Meta:
        queryset = Speaker.objects.all()
        resource_name = 'speaker'
        authentication = get_authentication()
        authorization = AdminAuthorization()


class CategoryResource(ModelResource):

    class Meta:
        queryset = Category.objects.all()
        resource_name = 'category'
        authentication = get_authentication()
        authorization = AdminAuthorization()


class TagResource(ModelResource):

    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'
        authentication = get_authentication()
        authorization = AdminAuthorization()
