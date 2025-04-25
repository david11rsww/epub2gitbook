This is README file.


# split4.py

## 目的

本项目的目的在于实现电子书格式的自动化转换，尤其是从EPUB格式到 Gitbook，中间会过渡到 MD 格式；但最难的在于从 MD 格式自动识别并转换为 Gitbook，主要涉及到文件分割、层级识别，以及链接与脚注的自动匹配与转换等功能。如果是手工编辑，时间可能是以月为单位，但是自动化脚本可以在三秒内完成转换。

## Steps

* Pre-Transform: The initial file is EPUB format. Then I transform it to HTML format. And then, to a markdown file.
* With the markdown file, I writed this `split4.py`, and transform it to the *Gitbook* project files.
* The final site is https://book.watersnature.com/onjava8

