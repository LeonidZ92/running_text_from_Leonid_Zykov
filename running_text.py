from flask import Flask, request, send_file
from moviepy.editor import TextClip, ColorClip, CompositeVideoClip

app = Flask(__name__)

# Параметры видео
width, height = 100, 100  # Размеры видео
duration = 3  # Фиксированная продолжительность 3 секунды

@app.route('/runtext', methods=['GET'])
def create_video():
    text = request.args.get('text', 'Бегущая строка')

    # Создаем текстовый клип
    fontsize = height - 20
    text_clip = TextClip(text, fontsize=fontsize, color='white', method='label').set_duration(duration)

    # Получаем ширину текста
    text_width, _ = text_clip.size
    start_position = width  # Начальная позиция текста за правой границей видео
    end_position = -text_width  # Конечная позиция текста за левой границей видео

    # Устанавливаем позицию текста так, чтобы он начинал за пределами экрана и двигался влево
    text_clip = text_clip.set_position(lambda t: (start_position - (start_position - end_position) * (t / duration), 'center')).set_duration(duration)

    # Создвим фон
    background_clip = ColorClip(size=(width, height), color=(0, 0, 0)).set_duration(duration)

    # Создаем итоговое видео
    video = CompositeVideoClip([background_clip, text_clip])

    # Экспортируем видео
    video_file_name = "running_text.mp4"
    video.write_videofile(video_file_name, fps=24, codec='libx264')

    return send_file(video_file_name, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)