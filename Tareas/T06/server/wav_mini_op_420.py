# SI ven esto los odio y los amo a la vez, aprendi mucho con este pedacito de codigo


def wav_mini(path: str,time=20) -> bytes:
    minimized = b''
    with open(path, "rb") as file:
        audio = file.read()
    metadata = b''
    try:
        metadata = audio[audio.index(b'LIST')+4:audio.index(b'data')]
    except ValueError:
        pass
    music = audio[audio.index(b'data'):audio.index(b'data') + int.from_bytes(audio[28:32], 'little') * time]
    len_data_int = len(metadata)
    total_len = len_data_int + len(music) + len(audio[0:36])
    len_data = len_data_int.to_bytes(4, "little")
    # wav chunk
    minimized += audio[:4]
    minimized += total_len.to_bytes(4, "little")
    minimized += audio[8:36]
    # metadata
    if len_data_int > 0:
        minimized += b'LIST'
        minimized += len_data
        minimized += metadata
    # Audio
    minimized += b'data'
    minimized += (len(music) - 8).to_bytes(7, "little")
    minimized += music[11:]
    return minimized
