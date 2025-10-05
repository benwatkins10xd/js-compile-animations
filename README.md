## js-compile Animations

Using [`manim`](https://github.com/ManimCommunity/manim/tree/main) for these animations

Requires [`ffmpeg`](https://www.ffmpeg.org/) for creating videos and some kind of LaTeX processor, I'm using [`MiKTeX`](https://miktex.org/) on my Windows machine and it works fine.

To create animations, activate the venv and run:

```
manim -ql path_to_file.py ClassName
```
