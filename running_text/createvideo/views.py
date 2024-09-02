import os
from django.http import HttpResponse
from moviepy.editor import TextClip, ColorClip, CompositeVideoClip

from .models import UserRequest


# Параметры видео
width, height = 100, 100
duration = 3


def create_video(request):
    text = request.GET.get('text', 'Бегущая строка')

    # Сохранение запроса в базе данных
    user_request = UserRequest(text=text)
    user_request.save()

    # Создаем текстовый клип
    fontsize = height - 20
    text_clip = TextClip(text, fontsize=fontsize, color='yellow', method='label').set_duration(duration)

    # Получаем ширину текста
    text_width, _ = text_clip.size
    start_position = width
    end_position = -text_width

    # Устанавливаем позицию текста
    text_clip = text_clip.set_position(lambda t: (start_position - (start_position - end_position) * (t / duration), 'center')).set_duration(duration)

    # Создаем фон
    background_clip = ColorClip(size=(width, height), color=(10, 10, 10)).set_duration(duration)

    # Создаем итоговое видео
    video = CompositeVideoClip([background_clip, text_clip])

    # Сохраняем видео во временный файл
    video_file_name = "running_text.mp4"
    video.write_videofile(video_file_name, fps=24, codec='libx264')

    # Отправляем видео пользователю
    with open(video_file_name, 'rb') as f:
        response = HttpResponse(f.read(), content_type='video/mp4')
        response['Content-Disposition'] = 'attachment; filename=' + video_file_name
    os.remove(video_file_name)
    return response
