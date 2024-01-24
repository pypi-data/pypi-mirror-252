from typing import Optional, Tuple, List, Union

from ovos_bus_client.client import MessageBusClient
from ovos_plugin_common_play.ocp import OCP_ID
from ovos_plugin_common_play.ocp.status import *
from ovos_plugin_common_play.ocp.utils import ocp_plugins, find_mime
from ovos_utils.json_helper import merge_dict
from ovos_utils.log import LOG
from ovos_bus_client.message import Message
from os.path import join, dirname
from dbus_next.service import Variant


# TODO subclass from dict (?)
class MediaEntry:
    def __init__(self, title="", uri="", skill_id=OCP_ID,
                 image=None, match_confidence=0,
                 playback=PlaybackType.UNDEFINED,
                 status=TrackState.DISAMBIGUATION, phrase=None,
                 position=0, length=None, bg_image=None, skill_icon=None,
                 artist=None, is_cps=False, cps_data=None, javascript="",
                 **kwargs):
        self.match_confidence = match_confidence
        self.title = title
        uri = uri or ""  # handle None
        self.uri = f'file://{uri}' if uri.startswith('/') else uri
        self.artist = artist
        self.skill_id = skill_id
        self.status = status
        self.playback = PlaybackType(playback) if isinstance(playback, int) \
            else playback
        self.image = image or join(dirname(__file__),
                                   "res/ui/images/ocp_bg.png")
        self.position = position
        self.phrase = phrase
        self.length = length  # None -> live stream
        self.skill_icon = skill_icon or join(dirname(__file__),
                                             "res/ui/images/ocp.png")
        self.bg_image = bg_image or join(dirname(__file__),
                                         "res/ui/images/ocp_bg.png")
        self.is_cps = is_cps
        self.data = kwargs
        self.cps_data = cps_data or {}
        self.javascript = javascript  # custom code to run in Webview after page load

    def update(self, entry: dict, skipkeys: list = None, newonly: bool = False):
        """
        Update this MediaEntry object with keys from the provided entry
        @param entry: dict or MediaEntry object to update this object with
        @param skipkeys: list of keys to not change
        @param newonly: if True, only adds new keys; existing keys are unchanged
        """
        skipkeys = skipkeys or []
        if isinstance(entry, MediaEntry):
            entry = entry.as_dict
        entry = entry or {}
        for k, v in entry.items():
            if k not in skipkeys and hasattr(self, k):
                if newonly and self.__getattribute__(k):
                    # skip, do not replace existing values
                    continue
                self.__setattr__(k, v)

    @staticmethod
    def from_dict(data: dict):
        """
        Construct a `MediaEntry` object from dict data.
        @param data: dict information to build the `MediaEntry` for
        @return: MediaEntry object
        """
        if data.get("bg_image") and data["bg_image"].startswith("/"):
            data["bg_image"] = "file:/" + data["bg_image"]
        data["skill"] = data.get("skill_id") or OCP_ID
        data["position"] = data.get("position", 0)
        data["length"] = data.get("length") or \
                         data.get("track_length") or \
                         data.get("duration")  # or get_duration_from_url(url)
        data["skill_icon"] = data.get("skill_icon") or data.get("skill_logo")
        data["status"] = data.get("status") or TrackState.DISAMBIGUATION
        data["playback"] = data.get("playback", PlaybackType.UNDEFINED)
        data["uri"] = data.get("stream") or data.get("uri") or data.get("url")
        data["title"] = data.get("title") or data["uri"]
        data["artist"] = data.get("artist") or data.get("author")
        data["is_cps"] = data.get("is_old_style") or data.get("is_cps", False)
        data["cps_data"] = data.get("cps_data") or {}
        return MediaEntry(**data)

    @property
    def info(self) -> dict:
        """
        Return a dict representation of this MediaEntry + infocard for QML model
        """
        return merge_dict(self.as_dict, self.infocard)

    @property
    def infocard(self) -> dict:
        """
        Return dict data used for a UI display
        """
        return {
            "duration": self.length,
            "track": self.title,
            "image": self.image,
            "album": self.skill_id,
            "source": self.skill_icon,
            "uri": self.uri
        }

    @property
    def mpris_metadata(self) -> dict:
        """
        Return dict data used by MPRIS
        """
        meta = {"xesam:url": Variant('s', self.uri)}
        if self.artist:
            meta['xesam:artist'] = Variant('as', [self.artist])
        if self.title:
            meta['xesam:title'] = Variant('s', self.title)
        if self.image:
            meta['mpris:artUrl'] = Variant('s', self.image)
        if self.length:
            meta['mpris:length'] = Variant('d', self.length)
        return meta

    @property
    def as_dict(self) -> dict:
        """
        Return a dict reporesentation of this MediaEntry
        """
        return {k: v for k, v in self.__dict__.items()
                if not k.startswith("_")}

    @property
    def mimetype(self) -> Optional[Tuple[Optional[str], Optional[str]]]:
        """
        Get the detected mimetype tuple (type, encoding) if it can be determined
        """
        if self.uri:
            return find_mime(self.uri)

    def __eq__(self, other):
        if isinstance(other, MediaEntry):
            other = other.infocard
        # dict compatison
        return other == self.infocard

    def __repr__(self):
        return str(self.as_dict)

    def __str__(self):
        return str(self.as_dict)


class Playlist(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._position = 0

    @property
    def position(self) -> int:
        """
        Return the current position in the playlist
        """
        return self._position

    @property
    def entries(self) -> List[MediaEntry]:
        """
        Return a list of MediaEntry objects in the playlist
        """
        entries = []
        for e in self:
            if isinstance(e, dict):
                e = MediaEntry.from_dict(e)
            if isinstance(e, MediaEntry):
                entries.append(e)
        return entries

    @property
    def current_track(self) -> Optional[MediaEntry]:
        """
        Return the current MediaEntry or None if the playlist is empty
        """
        if len(self) == 0:
            return None
        self._validate_position()
        track = self[self.position]
        if isinstance(track, dict):
            track = MediaEntry.from_dict(track)
        return track

    @property
    def is_first_track(self) -> bool:
        """
        Return `True` if the current position is the first track or if the
        playlist is empty
        """
        if len(self) == 0:
            return True
        return self.position == 0

    @property
    def is_last_track(self) -> bool:
        """
        Return `True` if the current position is the last track of if the
        playlist is empty
        """
        if len(self) == 0:
            return True
        return self.position == len(self) - 1

    def goto_start(self) -> None:
        """
        Move to the first entry in the playlist
        """
        self._position = 0

    def clear(self) -> None:
        """
        Remove all entries from the Playlist and reset the position
        """
        super(Playlist, self).clear()
        self._position = 0

    def sort_by_conf(self):
        """
        Sort the Playlist by `match_confidence` with high confidence first
        """
        self.sort(key=lambda k: k.match_confidence
                  if isinstance(k, MediaEntry) else
                  k.get("match_confidence", 0), reverse=True)

    def add_entry(self, entry: MediaEntry, index: int = -1) -> None:
        """
        Add an entry at the requested index
        @param entry: MediaEntry to add to playlist
        @param index: index to insert entry at (default -1 to append)
        """
        assert isinstance(index, int)
        # TODO: Handle index out of range
        if isinstance(entry, dict):
            entry = MediaEntry.from_dict(entry)
        assert isinstance(entry, MediaEntry)
        if index == -1:
            index = len(self)

        if index < self.position:
            self.set_position(self.position + 1)

        self.insert(index, entry)

    def remove_entry(self, entry: Union[int, dict, MediaEntry]) -> None:
        """
        Remove the requested entry from the playlist or raise a ValueError
        @param entry: index or MediaEntry to remove from the playlist
        """
        if isinstance(entry, int):
            self.pop(entry)
            return
        if isinstance(entry, dict):
            entry = MediaEntry.from_dict(entry)
        assert isinstance(entry, MediaEntry)
        for idx, e in self.entries:
            if e == entry:
                self.pop(idx)
                break
        else:
            raise ValueError(f"entry not in playlist: {entry}")

    def replace(self, new_list: List[Union[dict, MediaEntry]]) -> None:
        """
        Replace the contents of this Playlist with new_list
        @param new_list: list of MediaEntry or dict objects to set this list to
        """
        self.clear()
        for e in new_list:
            self.add_entry(e)

    def set_position(self, idx: int):
        """
        Set the position in the playlist to a specific index
        @param idx: Index to set position to
        """
        self._position = idx
        self._validate_position()

    def goto_track(self, track: Union[MediaEntry, dict]) -> None:
        """
        Go to the requested track in the playlist
        @param track: MediaEntry to find and go to in the playlist
        """
        if isinstance(track, MediaEntry):
            requested_uri = track.uri
        else:
            requested_uri = track.get("uri", "")
        for idx, t in enumerate(self):
            if isinstance(t, MediaEntry):
                pl_entry_uri = t.uri
            else:
                pl_entry_uri = t.get("uri", "")
            if requested_uri == pl_entry_uri:
                self.set_position(idx)
                LOG.debug(f"New playlist position: {self.position}")
                return
        LOG.error(f"requested track not in the playlist: {track}")

    def next_track(self) -> None:
        """
        Go to the next track in the playlist
        """
        self.set_position(self.position + 1)

    def prev_track(self) -> None:
        """
        Go to the previous track in the playlist
        """
        self.set_position(self.position - 1)

    def _validate_position(self) -> None:
        """
        Make sure the current position is valid; default `position` to 0
        """
        if self.position < 0 or self.position >= len(self):
            LOG.error(f"Playlist pointer is in an invalid position "
                      f"({self.position}! Going to start of playlist")
            self._position = 0

    def __contains__(self, item):
        if isinstance(item, dict):
            item = MediaEntry.from_dict(item)
        if not isinstance(item, MediaEntry):
            return False
        for e in self.entries:
            if not e.uri and e.data.get("playlist"):
                if e.title == item.title and not item.uri:
                    return True
                # track in playlist
                for t in e.data["playlist"]:
                    if t.get("uri") == item.uri:
                        return True
            elif e.uri == item.uri:
                return True
        return False


class NowPlaying(MediaEntry):
    def __init__(self, *args, **kwargs):
        MediaEntry.__init__(self, *args, **kwargs)
        self._player = None

    @property
    def bus(self) -> MessageBusClient:
        """
        Return the MessageBusClient inherited from the bound OCPMediaPlayer
        """
        return self._player.bus

    @property
    def _settings(self) -> dict:
        """
        Return the dict settings inherited from the bound OCPMediaPlayer
        """
        return self._player.settings

    def as_entry(self) -> MediaEntry:
        """
        Return a MediaEntry representation of this object
        """
        return MediaEntry.from_dict(self.as_dict)

    def bind(self, player):
        """
        Bind an OCPMediaPlayer object to this NowPlaying instance. Registers
        messagebus event handlers and defines `self._player`
        @param player: OCPMediaPlayer instance to bind
        """
        # needs to start with _ to avoid json serialization errors
        self._player = player
        self._player.add_event("ovos.common_play.track.state",
                               self.handle_track_state_change)
        self._player.add_event("ovos.common_play.media.state",
                               self.handle_media_state_change)
        self._player.add_event("ovos.common_play.play",
                               self.handle_external_play)
        self._player.add_event("ovos.common_play.playback_time",
                               self.handle_sync_seekbar)
        self._player.add_event('gui.player.media.service.get.meta',
                               self.handle_player_metadata_request)
        self._player.add_event('mycroft.audio.service.track_info_reply',
                               self.handle_sync_trackinfo)
        self._player.add_event('mycroft.audio.service.play',
                               self.handle_audio_service_play)
        self._player.add_event('mycroft.audio.playing_track',
                               self.handle_audio_service_play_start)

    def shutdown(self):
        """
        Remove NowPlaying events from the MessageBusClient
        """
        self._player.remove_event("ovos.common_play.track.state")
        self._player.remove_event("ovos.common_play.playback_time")
        self._player.remove_event('gui.player.media.service.get.meta')
        self._player.remove_event('mycroft.audio_only.service.track_info_reply')

    def reset(self):
        """
        Reset the NowPlaying MediaEntry to default parameters
        """
        LOG.debug("Resetting NowPlaying")
        self.title = ""
        self.artist = None
        self.skill_icon = None
        self.skill_id = None
        self.position = 0
        self.length = None
        self.is_cps = False
        self.cps_data = {}
        self.data = {}
        self.phrase = None
        self.javascript = ""
        self.playback = PlaybackType.UNDEFINED
        self.status = TrackState.DISAMBIGUATION

    def update(self, entry: dict, skipkeys: list = None, newonly: bool = False):
        """
        Update this MediaEntry and emit `gui.player.media.service.set.meta`
        @param entry: dict or MediaEntry object to update this object with
        @param skipkeys: list of keys to not change
        @param newonly: if True, only adds new keys; existing keys are unchanged
        """
        if isinstance(entry, MediaEntry):
            entry = entry.as_dict
        super().update(entry, skipkeys, newonly)
        # uri updates should not be skipped
        if newonly and entry.get("uri"):
            super().update({"uri": entry["uri"]})
        # sync with gui media player on track change
        if not self._player:
            LOG.error("Instance not bound! Call `bind` before trying to use "
                      "the messagebus.")
            return
        self.bus.emit(Message("gui.player.media.service.set.meta",
                              {"title": self.title,
                               "image": self.image,
                               "artist": self.artist}))

    def extract_stream(self):
        """
        Get metadata from ocp_plugins and add it to this MediaEntry
        """
        uri = self.uri
        if not uri:
            raise ValueError("No URI to extract stream from")
        if self.playback == PlaybackType.VIDEO:
            video = True
        else:
            video = False
        meta = ocp_plugins().extract_stream(uri, video)
        # update media entry with new data
        if meta:
            LOG.info(f"OCP plugins metadata: {meta}")
            self.update(meta, newonly=True)
        elif not any((uri.startswith(s) for s in ["http", "file", "/"])):
            LOG.info(f"OCP WARNING: plugins returned no metadata for uri {uri}")

    # events from gui_player/audio_service
    def handle_external_play(self, message):
        """
        Handle 'ovos.common_play.play' Messages. Update the metadata with new
        data received unconditionally, otherwise previous song keys might
        bleed into the new track
        @param message: Message associated with request
        """
        if message.data.get("tracks"):
            # backwards compat / old style
            playlist = message.data["tracks"]
            media = playlist[0]
        else:
            media = message.data.get("media", {})
        if media:
            self.update(media, newonly=False)

    def handle_player_metadata_request(self, message):
        """
        Handle 'gui.player.media.service.get.meta' Messages. Emit a response for
        the GUI to handle new metadata.
        @param message: Message associated with request
        """
        self.bus.emit(message.reply("gui.player.media.service.set.meta",
                                    {"title": self.title,
                                     "image": self.image,
                                     "artist": self.artist}))

    def handle_track_state_change(self, message):
        """
        Handle 'ovos.common_play.track.state' Messages. Update status
        @param message: Message with updated `state` data
        @return:
        """
        state = message.data.get("state")
        if state is None:
            raise ValueError(f"Got state update message with no state: "
                             f"{message}")
        if isinstance(state, int):
            state = TrackState(state)
        if not isinstance(state, TrackState):
            raise ValueError(f"Expected int or TrackState, but got: {state}")

        if state == self.status:
            return
        self.status = state
        LOG.info(f"TrackState changed: {repr(state)}")

        if state == TrackState.PLAYING_SKILL:
            # skill is handling playback internally
            pass
        elif state == TrackState.PLAYING_AUDIOSERVICE:
            # audio service is handling playback
            pass
        elif state == TrackState.PLAYING_VIDEO:
            # ovos common play is handling playback in GUI
            pass
        elif state == TrackState.PLAYING_AUDIO:
            # ovos common play is handling playback in GUI
            pass

        elif state == TrackState.DISAMBIGUATION:
            # alternative results # TODO its this 1 track or a list ?
            pass
        elif state in [TrackState.QUEUED_SKILL,
                        TrackState.QUEUED_VIDEO,
                        TrackState.QUEUED_AUDIOSERVICE]:
            # audio service is handling playback and this is in playlist
            pass

    def handle_media_state_change(self, message):
        """
        Handle 'ovos.common_play.media.state' Messages. If ended, reset.
        @param message: Message with updated MediaState
        """
        state = message.data.get("state")
        if state is None:
            raise ValueError(f"Got state update message with no state: "
                             f"{message}")
        if isinstance(state, int):
            state = MediaState(state)
        if not isinstance(state, MediaState):
            raise ValueError(f"Expected int or TrackState, but got: {state}")
        # Don't do anything. Let OCP manage this object's state
        # if state == MediaState.END_OF_MEDIA:
        #     # playback ended, allow next track to change metadata again
        #     self.reset()

    def handle_sync_seekbar(self, message):
        """
        Handle 'ovos.common_play.playback_time' Messages sent by audio backend
        @param message: Message with 'length' and 'position' data
        """
        self.length = message.data["length"]
        self.position = message.data["position"]

    def handle_sync_trackinfo(self, message):
        """
        Handle 'mycroft.audio.service.track_info_reply' Messages with current
        media defined in message.data
        @param message: Message with dict MediaEntry data
        """
        self.update(message.data)

    def handle_audio_service_play(self, message):
        """
        Handle 'mycroft.audio.service.play' Messages with list of tracks in data
        @param message: Message with 'tracks' data
        """
        tracks = message.data.get("tracks") or []
        # only present in ovos-core
        skill_id = message.context.get("skill_id") or 'mycroft.audio_interface'
        for idx, track in enumerate(tracks):
            # TODO try to extract metadata from uri (latency ?)
            if idx == 0:
                self.update(
                    {"uri": track,
                     "title": track.split("/")[-1],
                     "status": TrackState.QUEUED_AUDIOSERVICE,
                     'skill_id': skill_id,
                     "playback": PlaybackType.AUDIO_SERVICE}
                )
            else:
                # TODO sync playlist ?
                pass

    def handle_audio_service_play_start(self, message):
        """
        Handle 'mycroft.audio.playing_track' Messages
        @param message: Message notifying playback has started
        """
        self.update(
            {"status": TrackState.PLAYING_AUDIOSERVICE,
             "playback": PlaybackType.AUDIO_SERVICE})


