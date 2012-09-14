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

import traceback

from django.conf import settings
from django.core.mail import mail_admins

from tastypie import fields
from tastypie import http
from tastypie.authentication import (ApiKeyAuthentication, Authentication,
                                     MultiAuthentication)
from tastypie.authorization import Authorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from tastypie.utils.mime import build_content_type

from richard.videos.models import (Video, Speaker, Category, Tag, Language,
                                   CategoryKind)


class AdminAuthorization(Authorization):
    """Only admins get write access to resources."""

    def is_authorized(self, request, object=None):
        if request.user.is_staff:
            return True

        # Always allow read-access
        if request.method in ('GET', 'OPTIONS', 'HEAD'):
            return True

        return False


def get_authentication():
    """Authenticate users with API key, but let all others though too.

    Authorization will handle the permissions.
    """
    return MultiAuthentication(ApiKeyAuthentication(), Authentication())


def get_id_from_url(url):
    return int(url.rstrip('/').split('/')[-1])


class EnhancedModelResource(ModelResource):
    def dispatch(self, request_type, request, **kwargs):
        try:
            resp = super(EnhancedModelResource, self).dispatch(
                request_type, request, **kwargs)
        except Exception as exc:
            
            subject = 'API error: %s' % request.path
            try:
                request_repr = repr(request)
            except:
                request_repr = "Request repr() unavailable"
            the_trace = traceback.format_exc()
            resp_repr = 'Unknown response'
            if hasattr(exc, 'response'):
                resp_repr = repr(exc.response.__dict__)

            message = "%s\n\n%s\n\n%s" % (resp_repr, the_trace, request_repr)
            mail_admins(subject, message, fail_silently=True)
            raise

        if not (200 <= resp.status_code <= 299):
            subject = 'API error: %s' % request.path
            try:
                request_repr = repr(request)
            except:
                request_repr = "Request repr() unavailable"
            try:
                resp_repr = repr(resp)
            except:
                resp_repr = "Response repr() unavailable"
            the_trace = '\n'.join(traceback.format_stack())
            message = "%s\n\n%s\n\n%s" % (resp_repr, the_trace, request_repr)
            mail_admins(subject, message, fail_silently=True)
        return resp

    def raise_bad_request(self, bundle, errors):
        desired_format = self.determine_format(bundle.request)
        serialized = self.serialize(bundle.request, errors, desired_format)
        response = http.HttpBadRequest(
            content=serialized,
            content_type=build_content_type(desired_format))
        raise ImmediateHttpResponse(response=response)


class VideoResource(EnhancedModelResource):
    category = fields.ToOneField('richard.videos.api.CategoryResource',
                                 'category')
    speakers = fields.ToManyField('richard.videos.api.SpeakerResource',
                                  'speakers')
    tags = fields.ToManyField('richard.videos.api.TagResource', 'tags')

    class Meta:
        queryset = Video.objects.all()
        resource_name = 'video'
        authentication = get_authentication()
        authorization = AdminAuthorization()
        serializer = Serializer(formats=['json'])

    def hydrate(self, bundle):
        """Hydrate converts the json to an object."""
        errors = {}

        # Check slug
        slug = bundle.data.get('slug')
        if slug is not None:
            if bundle.request.method == 'POST':
                try:
                    Video.objects.get(slug=slug)
                    errors['slug'] = 'slug "%s" is already used.' % slug
                except Video.DoesNotExist:
                    pass
            elif bundle.request.method == 'PUT':
                id_ = bundle.data.get('id')
                if id_ is None:
                    # TODO: Figure out if it's possible to enter this
                    # case.
                    errors['slug'] = 'PUT, but id is None.'
                else:
                    try:
                        Video.objects.get(pk=id_, slug=slug)
                    except Video.DoesNotExist:
                        errors['slug'] = ('Video with id %d does not have '
                                          'slug %s.' % (id_, slug))

        # Check state
        state = bundle.data.get('state')
        if state is not None:
            valid_states = [Video.STATE_LIVE, Video.STATE_DRAFT]
            try:
                state = int(bundle.data['state'])
                if state not in valid_states:
                    errors['state'] = 'state should be in %s' % valid_states
            except ValueError:
                errors['state'] = 'state should be in %s' % valid_states
        else:
            bundle.data['state'] = 1

        # Incoming tags can either be an API url or a tag name.
        tags = bundle.data.get('tags', [])
        for i, tag in enumerate(tags):
            if isinstance(tag, Tag):
                continue
            elif not tag:
                errors.setdefault('tags', []).append(
                    'tags must be list of non-empty strings.')
            elif tag.startswith('/api/v1/'):
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
            if isinstance(speaker, Speaker):
                continue
            elif not speaker:
                errors.setdefault('speakers', []).append(
                    'speakers must be list of non-empty strings.')
            elif speaker.startswith('/api/v1/'):
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
            try:
                if isinstance(cat, Category):
                    pass
                elif cat.startswith('/api/v1/'):
                    cat = get_id_from_url(cat)
                    cat = Category.objects.get(pk=cat)
                else:
                    cat = Category.objects.get(title=cat)
                bundle.data['category'] = cat
            except Category.DoesNotExist:
                errors['category'] = 'category "%s" does not exist.' % cat
                return self.raise_bad_request(bundle, errors)
        else:
            errors['category'] = 'category is a required field.'
            return self.raise_bad_request(bundle, errors)

        # Incoming language can only be a language name. We don't
        # allow people to create languages via the API, so if it
        # doesn't exist, we bail.
        lang = bundle.data.get('language', None)
        if lang is not None:
            try:
                lang = Language.objects.get(name=lang)
                bundle.obj.language = lang
            except Language.DoesNotExist:
                errors['language'] = 'language "%s" does not exist.' % lang
        else:
            bundle.obj.language = lang

        # Nix the 'updated' field since it get saved automatically.
        if 'updated' in bundle.data:
            del bundle.data['updated']

        # If USE_TZ is False, then nix timezone bits---namely the Z at
        # the end which makes Django cross.
        if not settings.USE_TZ:
            for mem in ('added', 'recorded'):
                if mem in bundle.data and bundle.data[mem].endswith('Z'):
                    bundle.data[mem] = bundle.data[mem][:-1]

        if errors:
            bundle.errors = errors

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
        if not request.user.is_staff:
            return object_list.filter(state=Video.STATE_LIVE)

        return object_list


class SpeakerResource(EnhancedModelResource):
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


class CategoryResource(EnhancedModelResource):
    videos = fields.ListField()

    class Meta:
        queryset = Category.objects.all()
        resource_name = 'category'
        authentication = get_authentication()
        authorization = AdminAuthorization()
        serializer = Serializer(formats=['json'])

    def hydrate(self, bundle):
        errors = {}

        if 'kind' not in bundle.data:
            errors['kind'] = 'kind is a required field.'
        else:
            try:
                bundle.obj.kind = CategoryKind.objects.get(
                    pk=bundle.data['kind'])
            except CategoryKind.DoesNotExist:
                    errors['kind'] = ('"%s" is not a valid category kind.' %
                                      bundle.data['kind'])

        if 'slug' in bundle.data:
            slug = bundle.data['slug']
            try:
                Category.objects.get(slug=slug)
                errors['slug'] = 'slug "%s" is already used.' % slug
            except Category.DoesNotExist:
                pass

        if errors:
            bundle.errors = errors

        return bundle

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


class TagResource(EnhancedModelResource):
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
