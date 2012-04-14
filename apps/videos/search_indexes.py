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

from haystack import indexes
from videos.models import Video


class VideoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    summary = indexes.CharField(model_attr='summary', indexed=False)
    recorded = indexes.DateTimeField(model_attr='recorded', null=True)
    video_id = indexes.IntegerField(model_attr='id', indexed=False)
    slug = indexes.CharField(model_attr='slug', indexed=False)
    tags = indexes.MultiValueField()
    speakers = indexes.MultiValueField()

    # Used for autocompletion in opensearch
    title_auto = indexes.EdgeNgramField(model_attr='title')

    def prepare(self, obj):
        self.prepared_data = super(VideoIndex, self).prepare(obj)

        self.prepared_data['tags'] = [t.tag for t in obj.tags.all()]
        self.prepared_data['speakers'] = [s.name for s in obj.speakers.all()]

        return self.prepared_data

    def get_model(self):
        return Video

    def index_queryset(self):
        return self.get_model().objects.all()
