from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip, concatenate_videoclips
from yta_multimedia.video.edition.effect.moviepy.fade_in_moviepy_effect import FadeInMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.fade_out_moviepy_effect import FadeOutMoviepyEffect
from typing import Union

class BlinkMoviepyEffect:
    """
    This method gets the first frame of the provided 'clip' and returns a
    new clip that is an incredible 'sad_moment' effect with black and white
    filter, zoom in and rotating effect and also sad violin music.

    The 'duration' parameter is to set the returned clip duration, but the
    default value is a perfect one.
    """
    __parameters = {}

    def __init__(self, clip: Union[VideoFileClip, CompositeVideoClip, ImageClip], duration = 1):
        self.__clip = clip
        self.__parameters['duration'] = duration

    def __process_parameters(self):
        if not self.__parameters['duration']:
            self.__parameters['duration'] = 1
        else:
            # Zoom is by now limited to [0.1 - 5] ratio
            if self.__parameters['duration'] > 5:
                self.__parameters['duration'] = 5
            elif self.__parameters['duration'] <= 0.1:
                self.__parameters['duration'] = 0.1

        return self.__parameters
    
    def apply(self):
        """
        Applies the effect to the provided 'clip' and with the also
        provided parameters needed by this effect.
        """
        if not self.__clip:
            return None
        
        self.__process_parameters()
        
        half_duration = self.__clip.duration / 2
        self.__clip = concatenate_videoclips([
            FadeOutMoviepyEffect(self.__clip.subclip(0, half_duration), duration = half_duration),
            FadeInMoviepyEffect(self.__clip.subclip(half_duration, self.__clip.duration), duration = half_duration),
        ])

        return self.__clip