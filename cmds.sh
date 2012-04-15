#ffmpeg -r 12 -qscale 2 -i frames/movie_frames_%04d.png two_muons.mp4 # Slower
ffmpeg -r 25 -qscale 2 -i frames/movie_frames_%04d.png two_muons.mp4 # Slow
#ffmpeg -r 64 -qscale 2 -i frames/movie_frames_%04d.png two_muons.mp4 # Faster
