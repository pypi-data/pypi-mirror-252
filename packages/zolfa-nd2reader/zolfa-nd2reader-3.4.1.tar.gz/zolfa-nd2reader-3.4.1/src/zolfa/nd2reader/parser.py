# -*- coding: utf-8 -*-
import struct

import array
import warnings
from pims.base_frames import Frame
import numpy as np

from zolfa.nd2reader.common import get_version, read_chunk
from zolfa.nd2reader.label_map import LabelMap
from zolfa.nd2reader.raw_metadata import RawMetadata
from zolfa.nd2reader import stitched


class Parser(object):
    """Parses ND2 files and creates a Metadata and driver object.

    """
    CHUNK_HEADER = 0xabeceda
    CHUNK_MAP_START = b"ND2 FILEMAP SIGNATURE NAME 0001!"
    CHUNK_MAP_END = b"ND2 CHUNK MAP SIGNATURE 0000001!"

    supported_file_versions = {(3, None): True}

    def __init__(self, fh):
        self._fh = fh
        self._label_map = None
        self._raw_metadata = None
        self.metadata = None

        # First check the file version
        self.supported = self._check_version_supported()

        # Parse the metadata
        self._parse_metadata()

    def calculate_image_properties(self, index):
        """Calculate FOV, channels and z_levels

        Args:
            index(int): the index (which is simply the order in which the image was acquired)

        Returns:
            tuple: tuple of the field of view, the channel and the z level

        """
        field_of_view = self._calculate_field_of_view(index)
        channel = self._calculate_channel(index)
        z_level = self._calculate_z_level(index)
        return field_of_view, channel, z_level

    def get_image(self, index):
        """
        Creates an Image object and adds its metadata, based on the index (which is simply the order in which the image
        was acquired). May return None if the ND2 contains multiple channels and not all were taken in each cycle (for
        example, if you take bright field images every minute, and GFP images every five minutes, there will be some
        indexes that do not contain an image. The reason for this is complicated, but suffice it to say that we hope to
        eliminate this possibility in future releases. For now, you'll need to check if your image is None if you're
        doing anything out of the ordinary.

        Args:
            index(int): the index (which is simply the order in which the image was acquired)

        Returns:
            Frame: the image

        """
        field_of_view, channel, z_level = self.calculate_image_properties(index)
        channel_offset = index % len(self.metadata["channels"])
        image_group_number = int(index / len(self.metadata["channels"]))
        frame_number = self._calculate_frame_number(image_group_number, field_of_view, z_level)
        try:
            timestamp, image = self._get_raw_image_data(image_group_number, channel_offset, self.metadata["height"],
                                                        self.metadata["width"])
        except (TypeError):
            return Frame([], frame_no=frame_number, metadata=self._get_frame_metadata())
        else:
            return Frame(image, frame_no=frame_number, metadata=self._get_frame_metadata())

    def get_slice_by_attributes(self, xywh, frame_number, field_of_view, channel, z_level, height, width):
        """Gets a rectangular slice of an image based on its attributes alone

        Args:
            xywh: tuples containing (x, y, w, h) values of the
                  rectangular region to load
            frame_number: the frame number
            field_of_view: the field of view
            channel_name: the color channel name
            z_level: the z level
            height: the height of the image
            width: the width of the image

        Returns:
            Frame: the requested image

        """
        frame_number = 0 if frame_number is None else frame_number
        field_of_view = 0 if field_of_view is None else field_of_view
        channel = 0 if channel is None else channel
        z_level = 0 if z_level is None else z_level

        image_group_number = self._calculate_image_group_number(frame_number, field_of_view, z_level)
        try:
            timestamp, raw_image_data = self._get_raw_slice_data(
                xywh, image_group_number, channel, height, width
            )
        except (TypeError):
            return Frame([], frame_no=frame_number, metadata=self._get_frame_metadata())
        else:
            return Frame(raw_image_data, frame_no=frame_number, metadata=self._get_frame_metadata())

    def get_image_by_attributes(self, frame_number, field_of_view, channel, z_level, height, width):
        """Gets an image based on its attributes alone

        Args:
            frame_number: the frame number
            field_of_view: the field of view
            channel_name: the color channel name
            z_level: the z level
            height: the height of the image
            width: the width of the image

        Returns:
            Frame: the requested image

        """
        frame_number = 0 if frame_number is None else frame_number
        field_of_view = 0 if field_of_view is None else field_of_view
        channel = 0 if channel is None else channel
        z_level = 0 if z_level is None else z_level

        image_group_number = self._calculate_image_group_number(frame_number, field_of_view, z_level)
        try:
            timestamp, raw_image_data = self._get_raw_image_data(image_group_number, channel,
                                                                 height, width)
        except (TypeError):
            return Frame([], frame_no=frame_number, metadata=self._get_frame_metadata())
        else:
            return Frame(raw_image_data, frame_no=frame_number, metadata=self._get_frame_metadata())

    @staticmethod
    def get_dtype_from_metadata():
        """Determine the data type from the metadata.

        For now, always use float64 to prevent unexpected overflow errors when manipulating the data (calculating sums/
        means/etc.)

        """
        return np.float64

    def _check_version_supported(self):
        """Checks if the ND2 file version is supported by this reader.

        Returns:
            bool: True on supported
        """
        major_version, minor_version = get_version(self._fh)
        supported = self.supported_file_versions.get(
            (major_version, minor_version)) or self.supported_file_versions.get((major_version, None))

        if not supported:
            print("Warning: No parser is available for your current ND2 version (%d.%d). " % (
                    major_version, minor_version) + "This might lead to unexpected behaviour.")

        return supported

    def _parse_metadata(self):
        """Reads all metadata and instantiates the Metadata object.

        """
        # Retrieve raw metadata from the label mapping
        self._label_map = self._build_label_map()
        self._raw_metadata = RawMetadata(self._fh, self._label_map)
        self.metadata = self._raw_metadata.__dict__
        self.acquisition_times = self._raw_metadata.acquisition_times

    def _build_label_map(self):
        """
        Every label ends with an exclamation point, however, we can't directly search for those to find all the labels
        as some of the bytes contain the value 33, which is the ASCII code for "!". So we iteratively find each label,
        grab the subsequent data (always 16 bytes long), advance to the next label and repeat.

        Returns:
            LabelMap: the computed label map

        """
        # go 8 bytes back from file end
        self._fh.seek(-8, 2)
        chunk_map_start_location = struct.unpack("Q", self._fh.read(8))[0]
        self._fh.seek(chunk_map_start_location)
        raw_text = self._fh.read(-1)
        return LabelMap(raw_text)

    def _calculate_field_of_view(self, index):
        """Determines what field of view was being imaged for a given image.

        Args:
            index(int): the index (which is simply the order in which the image was acquired)

        Returns:
            int: the field of view
        """
        images_per_cycle = len(self.metadata["z_levels"]) * len(self.metadata["channels"])
        return int((index - (index % images_per_cycle)) / images_per_cycle) % len(self.metadata["fields_of_view"])

    def _calculate_channel(self, index):
        """Determines what channel a particular image is.

        Args:
            index(int): the index (which is simply the order in which the image was acquired)

        Returns:
            string: the name of the color channel

        """
        return self.metadata["channels"][index % len(self.metadata["channels"])]

    def _calculate_z_level(self, index):
        """Determines the plane in the z-axis a given image was taken in.

        In the future, this will be replaced with the actual offset in micrometers.

        Args:
            index(int): the index (which is simply the order in which the image was acquired)

        Returns:
            The z level

        """
        return self.metadata["z_levels"][int(
            ((index - (index % len(self.metadata["channels"]))) / len(self.metadata["channels"])) % len(
                self.metadata["z_levels"]))]

    def _calculate_image_group_number(self, frame_number, fov, z_level):
        """
        Images are grouped together if they share the same time index, field of view, and z-level.

        Args:
            frame_number: the time index
            fov: the field of view number
            z_level: the z level number

        Returns:
            int: the image group number

        """
        z_length = len(self.metadata['z_levels'])
        z_length = z_length if z_length > 0 else 1
        fields_of_view = len(self.metadata["fields_of_view"])
        fields_of_view = fields_of_view if fields_of_view > 0 else 1

        return frame_number * fields_of_view * z_length + (fov * z_length + z_level)

    def _calculate_frame_number(self, image_group_number, field_of_view, z_level):
        """
        Images are in the same frame if they share the same group number and field of view and are taken sequentially.

        Args:
            image_group_number: the image group number (see _calculate_image_group_number)
            field_of_view: the field of view number
            z_level: the z level number

        Returns:

        """
        return (image_group_number - (field_of_view * len(self.metadata["z_levels"]) + z_level)) / (len(self.metadata["fields_of_view"]) * len(self.metadata["z_levels"]))

    @property
    def _channel_offset(self):
        """
        Image data is interleaved for each image set. That is, if there are four images in a set, the first image
        will consist of pixels 1, 5, 9, etc, the second will be pixels 2, 6, 10, and so forth.

        Returns:
            dict: the channel offset for each channel

        """
        return {channel: n for n, channel in enumerate(self.metadata["channels"])}

    # TODO: create missing test cases for slices
    def _get_raw_slice_data(self, xywh, image_group_number, channel, height, width):
        """Reads the raw bytes and the timestamp of a rectangular slice
        of an image.

        Args:
            xywh: tuples containing (x, y, w, h) values of the
                  rectangular region to load
            image_group_number: the image group number (see _calculate_image_group_number)
            channel: the position (int) of the channel to load
            height: the height of the image
            width: the width of the image

        Returns:

        """
        size_c = len(self.metadata["channels"])

        x0, y0, w, h = xywh
        chunk_location = self._label_map.get_image_data_location(image_group_number)
        fh = self._fh

        if chunk_location is None or fh is None:
            return None
        fh.seek(chunk_location)
        # The chunk metadata is always 16 bytes long
        chunk_metadata = fh.read(16)
        header, relative_offset, data_length = struct.unpack("IIQ", chunk_metadata)
        if header != 0xabeceda:
            raise ValueError("The ND2 file seems to be corrupted.")
        # We start at the location of the chunk metadata, skip over the metadata, and then proceed to the
        # start of the actual data field, which is at some arbitrary place after the metadata.
        fh.seek(chunk_location + 16 + relative_offset)

        # Read timestamp (8 bytes)
        timestamp = struct.unpack("d", fh.read(8))[0]

        # Stitched Images: evaluate number of bytes to strip
        # (with stitched images sometimes after each row we have a regular number of extra bytes)
        n_unwanted_bytes = (data_length-8) % (height*width)
        assert 0 == n_unwanted_bytes % height
        rowskip = n_unwanted_bytes // height

        # Read ROI: row-by-row
        image_start_pos = chunk_location + 16 + relative_offset + 8

        line_bytemask = np.zeros(size_c, dtype=bool)
        line_bytemask[channel] = True
        line_bytemask = np.tile(line_bytemask.repeat(2),w)

        def get_line(y):
            fh.seek(image_start_pos + size_c*2*((width)*y+x0) + y*rowskip)
            return np.frombuffer(fh.read(size_c*2*w), np.byte)[line_bytemask]

        data = [get_line(y) for y in range(y0, y0+h)]
        data = bytes().join(data)

        image_group_data = array.array("H", data)
        true_channels_no = int(len(image_group_data) / (h * w))

        image_data = np.reshape(image_group_data, (h, w, true_channels_no))

        missing_channels = ~np.any(image_data, axis=(0, 1))
        image_data[..., missing_channels] = np.full(
            (h, w, missing_channels.sum()), np.nan)

        if np.any(missing_channels):
            warnings.warn(
                "ND2 file contains gap frames which are represented by "
                + "np.nan-filled arrays; to convert to zeros use e.g. "
                + "np.nan_to_num(array)")
        return timestamp, image_data[...,0]


    def _get_raw_image_data(self, image_group_number, channel_offset, height, width):
        """Reads the raw bytes and the timestamp of an image.

        Args:
            image_group_number: the image group number (see _calculate_image_group_number)
            channel_offset: the number of the color channel
            height: the height of the image
            width: the width of the image

        Returns:

        """
        chunk = self._label_map.get_image_data_location(image_group_number)
        data = read_chunk(self._fh, chunk)

        # All images in the same image group share the same timestamp! So if you have complicated image data,
        # your timestamps may not be entirely accurate. Practically speaking though, they'll only be off by a few
        # seconds unless you're doing something super weird.
        timestamp = struct.unpack("d", data[:8])[0]
        image_group_data = array.array("H", data)
        image_data_start = 4 + channel_offset
        image_group_data = stitched.remove_parsed_unwanted_bytes(image_group_data, image_data_start, height, width)

        # The images for the various channels are interleaved within the same array. For example, the second image
        # of a four image group will be composed of bytes 2, 6, 10, etc. If you understand why someone would design
        # a data structure that way, please send the author of this library a message.
        number_of_true_channels = int(len(image_group_data[4:]) / (height * width))
        try:
            image_data = np.reshape(image_group_data[image_data_start::number_of_true_channels], (height, width))
        except ValueError:
            new_width = len(image_group_data[image_data_start::number_of_true_channels]) // height
            image_data = np.reshape(image_group_data[image_data_start::number_of_true_channels], (height, new_width))

        # Skip images that are all zeros! This is important, since NIS Elements creates blank "gap" images if you
        # don't have the same number of images each cycle. We discovered this because we only took GFP images every
        # other cycle to reduce phototoxicity, but NIS Elements still allocated memory as if we were going to take
        # them every cycle.
        if np.any(image_data):
            return timestamp, image_data

        # If a blank "gap" image is encountered, generate an array of corresponding height and width to avoid
        # errors with ND2-files with missing frames. Array is filled with nan to reflect that data is missing.
        else:
            empty_frame = np.full((height, width), np.nan)
            warnings.warn(
                "ND2 file contains gap frames which are represented by np.nan-filled arrays; to convert to zeros use e.g. np.nan_to_num(array)")
            return timestamp, image_data

    def _get_frame_metadata(self):
        """Get the metadata for one frame

        Returns:
            dict: a dictionary containing the parsed metadata

        """
        return self.metadata
