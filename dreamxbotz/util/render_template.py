import urllib.parse
import aiohttp
import os
from dreamxbotz.Bot import dreamxbotz
from dreamxbotz.util.human_readable import humanbytes
from dreamxbotz.util.file_properties import get_file_ids
from info import *

async def render_page(id, secure_hash):
    file_data = await get_file_ids(dreamxbotz, int(id))
    file_name = file_data.file_name
    file_size = humanbytes(file_data.file_size)
    mime_type = file_data.mime_type
    
    # Links Generation
    if NO_PORT:
        src = f"https://{FQDN}"
    else:
        src = f"https://{FQDN}:{PORT}"

    stream_url = f"{src}/{str(id)}/{urllib.parse.quote(file_name)}?hash={secure_hash}"
    download_url = f"{src}/{str(id)}/{urllib.parse.quote(file_name)}?hash={secure_hash}"

    # HTML Page Design (Popcorn Play Theme)
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{file_name} | Popcorn Play</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/plyr@3.7.8/dist/plyr.css" />
    <style>
        :root {{
            --primary-color: #e50914;
            --bg-color: #141414;
            --card-bg: #1f1f1f;
            --text-color: #ffffff;
        }}
        body {{
            font-family: 'Poppins', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        .container {{
            width: 100%;
            max-width: 900px;
            padding: 20px;
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .logo {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary-color);
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        .video-container {{
            position: relative;
            background: #000;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            margin-bottom: 20px;
        }}
        video {{
            width: 100%;
            height: auto;
        }}
        .file-info {{
            text-align: center;
            margin-bottom: 25px;
            background: var(--card-bg);
            padding: 15px;
            border-radius: 10px;
        }}
        .file-name {{
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 5px;
            color: #fff;
            word-break: break-all;
        }}
        .file-size {{
            color: #aaa;
            font-size: 0.9rem;
        }}
        
        .players-section {{
            text-align: center;
            margin-top: 20px;
        }}
        .warning-text {{
            color: #ffcc00;
            font-size: 0.9rem;
            margin-bottom: 15px;
            font-weight: 500;
        }}
        .button-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 10px;
            margin-bottom: 20px;
        }}
        .btn {{
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 12px 15px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.9rem;
            transition: transform 0.2s, opacity 0.2s;
            color: #fff;
        }}
        .btn:hover {{
            transform: translateY(-2px);
            opacity: 0.9;
        }}
        .btn-download {{ background: var(--primary-color); }}
        .btn-vlc {{ background: #ff8800; }}
        .btn-mx {{ background: #2196f3; }}
        .btn-playit {{ background: #9c27b0; }}
        .btn-km {{ background: #00c851; }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #555;
            font-size: 0.8rem;
        }}
        
        /* Icons */
        .icon {{ margin-right: 8px; width: 20px; height: 20px; }}
    </style>
</head>
<body>

    <div class="container">
        <div class="header">
            <div class="logo">🍿 POPCORN PLAY</div>
        </div>

        <div class="video-container">
            <video id="player" playsinline controls>
                <source src="{stream_url}" type="{mime_type}">
                Your browser does not support the video tag.
            </video>
        </div>

        <div class="file-info">
            <div class="file-name">{file_name}</div>
            <div class="file-size">Size: {file_size}</div>
        </div>

        <div class="players-section">
            <div class="warning-text">⚠️ Audio Problem? Watch on Other Players</div>
            
            <div class="button-grid">
                <a href="{stream_url}" class="btn btn-download">
                    📥 Download / Stream
                </a>
                <a href="vlc://{stream_url}" class="btn btn-vlc">
                    🟠 VLC Player
                </a>
                <a href="intent:{stream_url}#Intent;package=com.mxtech.videoplayer.ad;S.title={file_name};end" class="btn btn-mx">
                    🔵 MX Player
                </a>
                <a href="intent:{stream_url}#Intent;package=com.playit.videoplayer;S.title={file_name};end" class="btn btn-playit">
                    🟣 PlayIt Player
                </a>
                <a href="intent:{stream_url}#Intent;package=com.kmplayer;S.title={file_name};end" class="btn btn-km">
                    🟢 KM Player
                </a>
            </div>
        </div>

        <div class="footer">
            Powered by Popcorn Play | @{script.ADMIN_USERNAME}
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/plyr@3.7.8/dist/plyr.polyfilled.js"></script>
    <script>
        const player = new Plyr('#player', {{
            controls: ['play-large', 'play', 'progress', 'current-time', 'mute', 'volume', 'captions', 'settings', 'pip', 'airplay', 'fullscreen'],
            settings: ['captions', 'quality', 'speed', 'loop']
        }});
    </script>
</body>
</html>
    """
    return html
