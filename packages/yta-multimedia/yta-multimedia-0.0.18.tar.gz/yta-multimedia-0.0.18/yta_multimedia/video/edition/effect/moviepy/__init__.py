from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from typing import Union
from yta_multimedia.video.edition.effect.moviepy.custom_vfx_effect import CustomVFXEffect
from yta_multimedia.video.edition.effect.moviepy.custom_effect import CustomEffect
from yta_general_utils.type_checker import variable_is_type
from yta_general_utils.file_processor import file_is_audio_file

def apply_moviepy_effect_to_video(video: Union[str, VideoFileClip, CompositeVideoClip, ImageClip], effect: Union[CustomVFXEffect, CustomEffect], **kwargs):
    """
    Applies the provided 'effect' to the provided 'video' and returns it
    with the new effect applied.

    TODO: Maybe add 'output_filename' to be able to write (?)
    """
    if not video:
        return None
    
    if not effect:
        return None
    
    if variable_is_type(video, str):
        if not file_is_audio_file(video):
            return None
        
        video = VideoFileClip(video)

    if variable_is_type(effect, CustomVFXEffect):
        video = video.fl(lambda get_frame, t: effect(get_frame, t, **kwargs))
    else:
        # TODO: Apply the custom effect. Remove this comment when working
        video = (lambda t: effect(video, **kwargs))

    # TODO: Add 'output_filename' to write it locally if provided (?)

    return video