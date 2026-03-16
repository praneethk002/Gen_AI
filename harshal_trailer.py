"""
Trailer creation for the Harshal podcast (MoviePy 2.x compatible).
"""
from moviepy import (
    VideoFileClip,
    TextClip,
    CompositeVideoClip,
    concatenate_videoclips,
    ColorClip,
)

INPUT_VIDEO = "Demystifying_Fintech_Harshal_Vora.mp4"
OUTPUT_VIDEO = "harshal_trailer_output.mp4"
CROP_RATIO = 0.5  # fraction of width visually reserved for speaker

SEGMENTS = [
    {
        "start": 49.0,
        "end": 57.0,
        "text": "Big banks focus on what start‑ups are doing and learn from them.",
    },
    {
        "start": 57.0,
        "end": 67.0,
        "text": "FinTech and banking: you need a cross‑section of tech, product and finance skills.",
    },
    {
        "start": 1480.0,
        "end": 1489.0,
        "text": "Candidates often focus on the quant stuff and miss the intangibles – think about what you're learning right now.",
    },
    {
        "start": 67.0,
        "end": 81.0,
        "text": "The LBS edge? A supportive community, strong brand and resources for entrepreneurs.",
    },
]

CAPTION_FONT = "Arial-Bold"
CAPTION_FONT_SIZE = 32
CAPTION_COLOR = "white"
CAPTION_STROKE_COLOR = "black"
CAPTION_STROKE_WIDTH = 2
CAPTION_BG_COLOR = (0, 0, 0)
CAPTION_PADDING = 20


def build_trailer(input_video: str, segments: list, output_video: str) -> None:
    video = VideoFileClip(input_video)
    width, height = video.size
    speaker_width = int(width * CROP_RATIO)
    caption_width = width - speaker_width

    clips = []
    for seg in segments:
        start, end, text = seg["start"], seg["end"], seg["text"]

        sub = video.subclipped(start, end)

        layers = []

        # Base black frame
        base = ColorClip(size=(width, height), color=(0, 0, 0)).with_duration(sub.duration)
        layers.append(base)

        # Full video (right side covered by caption panel)
        layers.append(sub.with_position((0, 0)))

        # Caption background panel on the right
        r, g, b = CAPTION_BG_COLOR
        bg = (
            ColorClip(size=(caption_width, height), color=(r, g, b))
            .with_duration(sub.duration)
            .with_position((speaker_width, 0))
        )
        layers.append(bg)

        # Caption text
        txt = TextClip(
            text=text,
            font_size=CAPTION_FONT_SIZE,
            font=CAPTION_FONT,
            color=CAPTION_COLOR,
            stroke_color=CAPTION_STROKE_COLOR,
            stroke_width=CAPTION_STROKE_WIDTH,
            size=(caption_width - 2 * CAPTION_PADDING, None),
            method="caption",
        )
        txt = (
            txt
            .with_start(0)
            .with_end(sub.duration)
            .with_position((speaker_width + CAPTION_PADDING, (height - txt.h) / 2))
        )
        layers.append(txt)

        composite = (
            CompositeVideoClip(layers, size=(width, height))
            .with_duration(sub.duration)
            .with_audio(sub.audio)
        )
        clips.append(composite)

    final_clip = concatenate_videoclips(clips, method="compose")
    final_clip.write_videofile(
        output_video,
        codec="libx264",
        audio_codec="aac",
        fps=24,
        preset="medium",
    )


if __name__ == "__main__":
    build_trailer(INPUT_VIDEO, SEGMENTS, OUTPUT_VIDEO)
