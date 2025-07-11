# IELTS Tools

> 一些雅思单词学习工具

``` text
.
├─ielts_gen_vocab_md_tts.py         # list转markdown
├─ielts_vocab_from_text.py          # 文本中提取list
├─ielts_vocab_online_cn_to_en.py    # 听写list，给出中文
├─ielts_vocab_online_en_to_cn.py    # 听写list，给出英文
├─ielts_vocab_online_voice_to_en.py # 听写list，读出英文
└─ttsielts_vocab_radom.py           # 打乱list
```
---

#### ielts_vocab_radom.py
- 用于打乱单词顺序

---

#### ielts_vocab_from_text.py
- 用于从文本提取单词

---

#### ielts_vocab_online_voice_to_en.py
- 读英文，听写单词，用于提升Listening
- 拼写完给出中文
- 统计正确率和错题表

---

#### ielts_vocab_online_cn_to_en.py
- 给出中文，听写单词，用于提升Writing
- 统计正确率和错题表

---

#### ielts_vocab_online_en_to_cn.py
- 给出英文，判断是否认识，用于提升Reading
- 统计正确率和错题表

---

#### ielts_gen_vocab_md_tts.py
- 生成tts input，用于tts听写
- https://ttsreader.com/player/
- 生成单词表markdown table，用于背诵
- 可更改生成文件名称，以及md列数
- md可以通过这个extension转pdf或html
- https://marketplace.visualstudio.com/items?itemName=shd101wyy.markdown-preview-enhanced


---

#### ielts_red_note_comments.py
- 手动复制网页前端body到temp.html
- 从小红书抓评论，整理到markdown
- 给大模型归纳评价（手动）
