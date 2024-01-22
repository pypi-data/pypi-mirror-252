#!/usr/bin/env python3

"""
** Defines the structure a video frame. **
------------------------------------------
"""

from fractions import Fraction
import numbers
import re
import typing

import numpy as np
import torch

from cutcutcodec.core.classes.frame import Frame



class FrameVideo(Frame):
    """
    ** An image with time information for video context. **

    Behaves like a torch tensor of shape (height, width, nbr_channels).
    The shape is consistent with pyav and cv2.
    The dtype is automaticaly cast into torch.uint8.

    Parameters
    ----------
    channels : int
        The numbers of layers (readonly):

            * 1 -> grayscale
            * 2 -> grayscale, alpha
            * 3 -> blue, green, red
            * 4 -> blue, green, red, alpha
    height : int
        The dimension i (vertical) of the image in pxl (readonly).
    time : Fraction
        The time of the frame inside the video stream in second (readonly).
    width : int
        The dimension j (horizontal) of the image in pxl (readonly).
    """

    def __new__(cls, time: typing.Union[Fraction, numbers.Real, str], *args, **kwargs):
        frame = super().__new__(cls, *args, metadata=time, **kwargs)
        if frame.dtype != torch.uint8:
            frame = frame.to(dtype=torch.uint8, copy=False)
        frame.check_state()
        return frame

    def __repr__(self) -> str:
        """
        ** Compact and complete display of an evaluable version of the video frame. **

        Examples
        --------
        >>> import torch
        >>> from cutcutcodec.core.classes.frame_video import FrameVideo
        >>> FrameVideo("2/4", torch.zeros((480, 720, 3))) # doctest: +ELLIPSIS
        FrameVideo('1/2', [[[0, 0, 0],
                            ...
                            [0, 0, 0]]])
        >>>
        """
        time_str = f"'{self.time}'" if int(self.time) != self.time else f"{self.time}"
        header = f"{self.__class__.__name__}({time_str}, "
        tensor_str = np.array2string(
            self.numpy(force=True), separator=", ", prefix=header, suffix=" "
        )
        if (infos := re.findall(r"\w+=[a-zA-Z0-9_\-.\"']+", torch.Tensor.__repr__(self))):
            infos = [inf for inf in infos if inf != "dtype=torch.uint8"]
        if infos:
            infos = "\n" + " "*len(header) + (",\n" + " "*len(header)).join(infos)
            return f"{header}{tensor_str},{infos})"
        return f"{header}{tensor_str})"

    @property
    def channels(self) -> int:
        """
        ** The numbers of layers. **

        Examples
        --------
        >>> from cutcutcodec.core.classes.frame_video import FrameVideo
        >>> FrameVideo(0, 480, 720, 3).channels
        3
        >>>
        """
        return self.shape[2]

    def check_state(self) -> None:
        """
        ** Apply verifications. **

        Raises
        ------
        AssertionError
            If something wrong in this frame.
        """
        metadata = getattr(self, "metadata", None)
        assert metadata is not None
        assert isinstance(metadata, (Fraction, numbers.Real, str)), metadata.__class__.__name__
        setattr(self, "metadata", Fraction(metadata))
        assert self.ndim == 3, self.shape
        assert self.shape[0] > 0, self.shape
        assert self.shape[1] > 0, self.shape
        assert self.shape[2] in {1, 2, 3, 4}, self.shape
        assert self.dtype == torch.uint8, self.dtype

    def convert(self, channels: int) -> Frame:
        """
        ** Change the numbers of channels of the frame. **

        Returns
        -------
        frame : cutcutcodec.core.classes.frame_video.FrameVideo
            The new frame, be carful, undergroud data can be shared.

        Examples
        --------
        >>> import torch
        >>> from cutcutcodec.core.classes.frame_video import FrameVideo
        >>> _ = torch.manual_seed(0)
        >>> ref_gray = FrameVideo(0, torch.randint(0, 256, (480, 720, 1), dtype=torch.uint8))
        >>> ref_gray_alpha = FrameVideo(0, torch.randint(0, 256, (480, 720, 2), dtype=torch.uint8))
        >>> ref_bgr = FrameVideo(0, torch.randint(0, 256, (480, 720, 3), dtype=torch.uint8))
        >>> ref_bgr_alpha = FrameVideo(0, torch.randint(0, 256, (480, 720, 4), dtype=torch.uint8))
        >>>
        >>> # case 1 -> 2, 3, 4
        >>> gray_alpha = ref_gray.convert(2)
        >>> gray_alpha.channels
        2
        >>> torch.equal(gray_alpha[..., 0], ref_gray[..., 0])
        True
        >>> torch.eq(gray_alpha[..., 1], 255).all()
        tensor(True)
        >>> bgr = ref_gray.convert(3)
        >>> bgr.channels
        3
        >>> torch.equal(bgr[..., 0], ref_gray[..., 0])
        True
        >>> torch.equal(bgr[..., 1], ref_gray[..., 0])
        True
        >>> torch.equal(bgr[..., 2], ref_gray[..., 0])
        True
        >>> bgr_alpha = ref_gray.convert(4)
        >>> bgr_alpha.channels
        4
        >>> torch.equal(bgr_alpha[..., 0], ref_gray[..., 0])
        True
        >>> torch.equal(bgr_alpha[..., 1], ref_gray[..., 0])
        True
        >>> torch.equal(bgr_alpha[..., 2], ref_gray[..., 0])
        True
        >>> torch.eq(bgr_alpha[..., 3], 255).all()
        tensor(True)
        >>>
        >>> # case 2 -> 1, 3, 4
        >>> gray = ref_gray_alpha.convert(1)
        >>> gray.channels
        1
        >>> torch.equal(gray[..., 0],
        ...     torch.where(torch.eq(ref_gray_alpha[..., 1], 0), 0, ref_gray_alpha[..., 0]))
        True
        >>> bgr = ref_gray_alpha.convert(3)
        >>> bgr.channels
        3
        >>> torch.equal(bgr[..., 0],
        ...     torch.where(torch.eq(ref_gray_alpha[..., 1], 0), 0, ref_gray_alpha[..., 0]))
        True
        >>> torch.equal(bgr[..., 1],
        ...     torch.where(torch.eq(ref_gray_alpha[..., 1], 0), 0, ref_gray_alpha[..., 0]))
        True
        >>> torch.equal(bgr[..., 2],
        ...     torch.where(torch.eq(ref_gray_alpha[..., 1], 0), 0, ref_gray_alpha[..., 0]))
        True
        >>> bgr_alpha = ref_gray_alpha.convert(4)
        >>> bgr_alpha.channels
        4
        >>> torch.equal(bgr_alpha[..., 0], ref_gray_alpha[..., 0])
        True
        >>> torch.equal(bgr_alpha[..., 1], ref_gray_alpha[..., 0])
        True
        >>> torch.equal(bgr_alpha[..., 2], ref_gray_alpha[..., 0])
        True
        >>> torch.equal(bgr_alpha[..., 3], ref_gray_alpha[..., 1])
        True
        >>>
        >>> # case 3 -> 1, 2, 4
        >>> gray = ref_bgr.convert(1)
        >>> gray.channels
        1
        >>> gray_alpha = ref_bgr.convert(2)
        >>> gray_alpha.channels
        2
        >>> torch.eq(gray_alpha[..., 1], 255).all()
        tensor(True)
        >>> bgr_alpha = ref_bgr.convert(4)
        >>> bgr_alpha.channels
        4
        >>> torch.equal(bgr_alpha[..., 0], ref_bgr[..., 0])
        True
        >>> torch.equal(bgr_alpha[..., 1], ref_bgr[..., 1])
        True
        >>> torch.equal(bgr_alpha[..., 2], ref_bgr[..., 2])
        True
        >>> torch.eq(bgr_alpha[..., 3], 255).all()
        tensor(True)
        >>>
        >>> # case 4 -> 1, 2, 3
        >>> gray = ref_bgr_alpha.convert(1)
        >>> gray.channels
        1
        >>> gray_alpha = ref_bgr_alpha.convert(2)
        >>> gray_alpha.channels
        2
        >>> torch.equal(gray_alpha[..., 1], ref_bgr_alpha[..., 3])
        True
        >>> bgr = ref_bgr_alpha.convert(3)
        >>> bgr.channels
        3
        >>> torch.equal(bgr[..., 0],
        ...     torch.where(torch.eq(ref_bgr_alpha[..., 3], 0), 0, ref_bgr_alpha[..., 0]))
        True
        >>> torch.equal(bgr[..., 1],
        ...     torch.where(torch.eq(ref_bgr_alpha[..., 3], 0), 0, ref_bgr_alpha[..., 1]))
        True
        >>> torch.equal(bgr[..., 2],
        ...     torch.where(torch.eq(ref_bgr_alpha[..., 3], 0), 0, ref_bgr_alpha[..., 2]))
        True
        >>>
        """
        assert isinstance(channels, int), channels.__class__.__name__

        def get_alpha():
            if self.channels in {2, 4}:
                return torch.unsqueeze(self[..., -1], 2)
            return torch.full((self.height, self.width, 1), 255, dtype=torch.uint8)

        def get_gray():
            if self.channels == 1:
                return self
            if self.channels == 2:
                return torch.unsqueeze(self[..., 0], 2)
            color = self.to(dtype=torch.float32, copy=True) # float16 and round failed, torch 2.0.0
            gray = .114*color[..., 0] + 0.587*color[..., 1] + 0.299*color[..., 2]
            gray = torch.unsqueeze(torch.round(gray, out=gray).to(dtype=torch.uint8), 2)
            return gray

        def get_bgr():
            if self.channels == 3:
                return self
            if self.channels == 4:
                return self[..., :3]
            return torch.tile(get_gray(), (1, 1, 3))

        if self.channels == channels: # optimisation in the case there are alpha channel
            return self

        if channels == 1:
            gray = get_gray()
            if self.channels in {2, 4}:
                gray = torch.where(torch.eq(get_alpha(), 0), 0, gray)
            return FrameVideo(self.time, gray)
        if channels == 2:
            return FrameVideo(self.time, torch.cat((get_gray(), get_alpha()), 2))
        if channels == 3:
            bgr = get_bgr()
            if self.channels in {2, 4}:
                bgr = torch.where(torch.eq(get_alpha(), 0), 0, bgr)
            return FrameVideo(self.time, bgr)
        if channels == 4:
            return FrameVideo(self.time, torch.cat((get_bgr(), get_alpha()), 2))
        raise ValueError(f"channels can only be 1, 2, 3, or 4, not {channels}")

    @property
    def height(self) -> int:
        """
        ** The dimension i (vertical) of the image in pxl. **

        Examples
        --------
        >>> from cutcutcodec.core.classes.frame_video import FrameVideo
        >>> FrameVideo(0, 480, 720, 3).height
        480
        >>>
        """
        return self.shape[0]

    @property
    def time(self) -> Fraction:
        """
        ** The time of the frame inside the video stream in second. **

        Examples
        --------
        >>> from cutcutcodec.core.classes.frame_video import FrameVideo
        >>> FrameVideo(0, 480, 720, 3).time
        Fraction(0, 1)
        >>>
        """
        return self.metadata

    def to_numpy_bgr(self, contiguous=False) -> np.ndarray[np.uint8]:
        """
        ** Returns the 3 channels numpy frame representation. **

        Parameters
        ----------
        contiguous : boolean, default=False
            If True, guaranti that the returned numpy array is c-contiguous.

        Examples
        --------
        >>> from cutcutcodec.core.classes.frame_video import FrameVideo
        >>> frame = FrameVideo(0, 480, 720, 3).to_numpy_bgr() # classical bgr
        >>> type(frame), frame.shape, frame.dtype
        (<class 'numpy.ndarray'>, (480, 720, 3), dtype('uint8'))
        >>> frame = FrameVideo(0, 480, 720, 1).to_numpy_bgr() # grayscale
        >>> type(frame), frame.shape, frame.dtype
        (<class 'numpy.ndarray'>, (480, 720, 3), dtype('uint8'))
        >>> frame = FrameVideo(0, 480, 720, 4).to_numpy_bgr() # alpha channel
        >>> type(frame), frame.shape, frame.dtype
        (<class 'numpy.ndarray'>, (480, 720, 3), dtype('uint8'))
        >>>
        """
        assert isinstance(contiguous, bool), contiguous.__class__.__name__
        frame_np = self.convert(3).numpy(force=True)
        if contiguous:
            return np.ascontiguousarray(frame_np)
        return frame_np

    @property
    def width(self) -> int:
        """
        ** The dimension j (horizontal) of the image in pxl. **

        Examples
        --------
        >>> from cutcutcodec.core.classes.frame_video import FrameVideo
        >>> FrameVideo(0, 480, 720, 3).width
        720
        >>>
        """
        return self.shape[1]
