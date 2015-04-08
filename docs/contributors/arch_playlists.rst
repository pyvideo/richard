============================
Architecture docs: Playlists
============================

Richard is a large index of videos. That's great, but it's hard for users
to go through the index and denote which videos of all the videos they're
interested in watching at some point.

Further, it's probably the case that users want to share a group of
videos for the purposes of education, curation or shenanigans.

The initial playlist structure has the following requirements:

1. a playlist consists of a short summary, a description, an owner,
   and a list of videos in a specific order that belong to the playlist

2. a playlist is owned by a single user

3. users can create multiple playlists

4. users can edit and delete playlists belonging to that user

5. on a video details page, the user can add the video to any of the
   user's playlists

6. on a video listing page, the user can add any of the videos to the
   user's playlists


Implementation details
======================

For now we're going to go with a cheap implementation.

Model::

  id
  summary
  description
  list_of_video_ids


Adding a video to a list:

1. get the playlist instance
2. append the id of the new video to the list
3. save the playlist instance

Removing a video from a list:

1. get the playlist instance
2. remove the video id from the list
3. save the playlist instance

Reordering a video list:

1. get the playlist instance
2. change the order of videos
3. save the playlist instance

User profile lists all playlists the user owns including share links.

Playlist details shows the summary, description, user and then a listing
of videos in the playlist.


Things to think about
=====================

When a user is watching all the videos in a playlist, do we keep track of
where in the playlist they are? How? What happens if the playlist changes
underneath them?
