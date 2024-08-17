from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from typing import Union
from yta_multimedia.video.edition.effect.moviepy.moviepy_custom_vfx_effect import MoviepyCustomVFXEffect
from yta_multimedia.video.edition.effect.moviepy.moviepy_custom_effect import MoviepyCustomEffect
from yta_multimedia.video.edition.effect.moviepy.moviepy_effect import MoviepyEffect
from yta_general_utils.type_checker import variable_is_type, code_file_is
from yta_general_utils.file_processor import file_is_audio_file

def apply_moviepy_effect_to_video(video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip], effect: Union[MoviepyCustomVFXEffect, MoviepyCustomEffect, MoviepyEffect], **kwargs):
    """
    Applies the provided 'effect' to the provided 'video' and returns it
    with the new effect applied.

    TODO: Maybe add 'output_filename' to be able to write (?)
    """
    if not video:
        return None
    
    if not code_file_is(effect, 'moviepy_custom_vfx_effect.py') and not code_file_is(effect, 'moviepy_custom_effect.py') and not code_file_is(effect, 'moviepy_effect.py'):
        return None
    
    if variable_is_type(video, str):
        if not file_is_audio_file(video):
            return None
        
        video = VideoFileClip(video)

    if code_file_is(effect, 'moviepy_custom_vfx_effect.py'):
        video = video.fl(lambda get_frame, t: effect(get_frame, t, **kwargs))
    elif code_file_is(effect, 'moviepy_effect.py'):
        video = video.fl(effect, **kwargs)
    else:
        # TODO: Apply the custom effect. Remove this comment when working
        video = effect(video, **kwargs)

    # TODO: Add 'output_filename' to write it locally if provided (?)

    return video