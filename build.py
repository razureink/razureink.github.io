# -*- coding: utf-8 -*-
"""静态主页构建脚本：读取 site_data.json，用 Jinja2 渲染 templates/index.html，
输出 index.html 到仓库根目录（覆盖旧文件），并同步 static/ 资源。"""
import glob
import json
import os
import shutil

from jinja2 import Environment, FileSystemLoader, select_autoescape

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

THEMES = {
    'default': '''
        body::before {
            content: '';
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: inherit;
            filter: blur(20px) brightness(0.7);
            z-index: -1;
            transform: scale(1.1);
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 24px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }
    ''',
    'minimal': '''
        body::before {
            content: '';
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: #f5f5f7;
            z-index: -1;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border: none;
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        }
        body {
            color: #1d1d1f;
        }
        .section-title {
            color: #1d1d1f;
            font-weight: 500;
        }
    ''',
    'neumorphism': '''
        body::before {
            content: '';
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: #e0e0e0;
            z-index: -1;
        }
        .glass-card {
            background: #e0e0e0;
            border: none;
            border-radius: 50px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 20px 20px 60px #bebebe, -20px -20px 60px #ffffff;
        }
        body {
            color: #333;
        }
        .tag {
            background: #e0e0e0;
            box-shadow: 5px 5px 10px #bebebe, -5px -5px 10px #ffffff;
            color: #333;
        }
    ''',
}


def get_theme_css(theme_name, custom_css=''):
    if theme_name == 'custom':
        return custom_css
    return THEMES.get(theme_name, THEMES['default'])


def list_music_files():
    """列出 static/music/ 下的音频文件（用于语音与背景音乐）"""
    music_dir = os.path.join(BASE_DIR, 'static', 'music')
    files = []
    for ext in ('*.mp3', '*.wav', '*.ogg', '*.m4a'):
        files.extend(glob.glob(os.path.join(music_dir, ext)))
    return sorted(os.path.basename(f) for f in files)


def main():
    with open(os.path.join(BASE_DIR, 'site_data.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)

    theme_css = get_theme_css(data.get('theme', 'default'), data.get('custom_css', ''))
    music_files = list_music_files()

    env = Environment(
        loader=FileSystemLoader(os.path.join(BASE_DIR, 'templates')),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('index.html')

    html = template.render(
        data=data,
        theme_css=theme_css,
        voice_files=music_files,
        music_files=music_files,
        name_display=data.get('name_display', '青墨雨'),
    )

    out_path = os.path.join(BASE_DIR, 'index.html')
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"[build] 已生成 index.html（{len(html)} 字节，音乐文件 {len(music_files)} 个）")

    # 确保 static 目录结构存在（构建时同步静态资源）
    for sub in ('music', 'fonts', 'uploads'):
        os.makedirs(os.path.join(BASE_DIR, 'static', sub), exist_ok=True)
    print("[build] static/ 目录已就绪（music / fonts / uploads）")


if __name__ == '__main__':
    main()
