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
from tastypie.serializers import Serializer

from richard.videos.models import Video, Speaker, Category, Tag, Language


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


def get_id_from_url(url):
    return int(url.rstrip('/').split('/')[-1])


class VideoResource(ModelResource):
    category = fields.ToOneField('richard.videos.api.CategoryResource',
                                 'category')
    speakers = fields.ToManyField('richard.videos.api.SpeakerResource',
                                  'speakers')
    tags = fields.ToManyField('richard.videos.api.TagResource', 'tags')

    class Meta:
        queryset = Video.objects.live()
        resource_name = 'video'
        authentication = get_authentication()
        authorization = AdminAuthorization()
        serializer = Serializer(formats=['json'])

    def hydrate(self, bundle):
        """Hydrate converts the json to an object."""
        # Incoming tags can either be an API url or a tag name.
        tags = bundle.data.get('tags', [])
        for i, tag in enumerate(tags):
            if '/' in tag:
                # If there's a /, we assume it's an API url, pluck the
                # id from the end, and that's the tag.
                tag = get_id_from_url(tag)
                tag = Tag.objects.get(pk=tag)
            else:
                tag = Tag.objects.get_or_create(tag=tag)[0]
            tags[i] = tag
        bundle.data['tags'] = tags

        # Incoming speakers can either be an API url or a speaker
        # name.
        speakers = bundle.data.get('speakers', [])
        for i, speaker in enumerate(speakers):
            if '/' in speaker:
                # If there's a /, we assume it's an API url, pluck the
                # id from the end, and that's the speaker.
                speaker = get_id_from_url(speaker)
                speaker = Speaker.objects.get(pk=speaker)
            else:
                speaker = Speaker.objects.get_or_create(name=speaker)[0]
            speakers[i] = speaker
        bundle.data['speakers'] = speakers

        # Incoming category can be either an API url or a category
        # title (not a name!).
        cat = bundle.data.get('category', None)
        if cat is not None:
            if '/' in cat:
                # If there's a /, we assume it's an API url, pluck the
                # id from the end, and that's the category.
                cat = get_id_from_url(cat)
                cat = Category.objects.get(pk=cat)
            else:
                cat = Category.objects.get_or_create(title=cat)[0]
            bundle.data['category'] = cat

        # Incoming language can only be a language name. We don't
        # allow people to create languages via the API, so if it
        # doesn't exist, we bail.
        lang = bundle.data.get('language', None)
        if lang is not None:
            lang = Language.objects.get(name=lang)
        bundle.obj.language = lang

        return bundle

    def dehydrate(self, bundle):
        """Dehydrate converts the object to json."""
        # Add language name or None
        lang = bundle.obj.language
        if lang == None:
            bundle.data['language'] = None
        else:
            bundle.data['language'] = lang.name
        return bundle

    def apply_authorization_limits(self, request, object_list):
        """Only authenticated users can see videos in draft status."""
        if hasattr(request, 'user') and request.user.is_staff:
            return Video.objects.all()

        return object_list


class SpeakerResource(ModelResource):
    videos = fields.ListField()

    class Meta:
        queryset = Speaker.objects.all()
        resource_name = 'speaker'
        authentication = get_authentication()
        authorization = AdminAuthorization()
        serializer = Serializer(formats=['json'])

    def dehydrate_videos(self, bundle):
        video_set = bundle.obj.video_set
        if hasattr(bundle.request, 'user') and bundle.request.user.is_staff:
            video_set = video_set.all()
        else:
            video_set = video_set.live()

        # TODO: fix url so it's not hard-coded
        return [
            '/api/v1/video/%d/' % vid
            for vid in video_set.values_list('id', flat=True)]


class CategoryResource(ModelResource):
    videos = fields.ListField()

    class Meta:
        queryset = Category.objects.all()
        resource_name = 'category'
        authentication = get_authentication()
        authorization = AdminAuthorization()
        serializer = Serializer(formats=['json'])

    def dehydrate_videos(self, bundle):
        video_set = bundle.obj.video_set
        if hasattr(bundle.request, 'user') and bundle.request.user.is_staff:
            video_set = video_set.all()
        else:
            video_set = video_set.live()

        # TODO: fix url so it's not hard-coded
        return [
            '/api/v1/video/%d/' % vid
            for vid in video_set.values_list('id', flat=True)]


class TagResource(ModelResource):
    videos = fields.ListField()

    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'
        authentication = get_authentication()
        authorization = AdminAuthorization()
        serializer = Serializer(formats=['json'])

    def dehydrate_videos(self, bundle):
        video_set = bundle.obj.video_set
        if hasattr(bundle.request, 'user') and bundle.request.user.is_staff:
            video_set = video_set.all()
        else:
            video_set = video_set.live()

        # TODO: fix url so it's not hard-coded
        return [
            '/api/v1/video/%d/' % vid
            for vid in video_set.values_list('id', flat=True)]
