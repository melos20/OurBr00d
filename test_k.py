from kokoro import KPipeline
pipe = KPipeline(lang_code='a')
gen = pipe("Hello world", voice='af_heart', speed=1)
for _, _, audio in gen:
    print(type(audio), audio.shape)
