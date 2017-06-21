# SI ven esto los odio y los amo a la vez aprendi mucho con este pedacito de codigo


def wav_mini(path: str) -> bytes:
    minimized = b''
    with open(path, "rb") as file:
        audio = file.read()
    raw = audio[44:]
    metadata = raw[:raw.index(b'data')]
    music = raw[raw.index(b'data'):raw.index(b'data') + int.from_bytes(audio[28:32], 'little') * 20]
    len_data_int = len(metadata)
    total_len = len_data_int + len(music) + len(audio[0:44])
    len_data = len_data_int.to_bytes(4, "little")
    # wav chunk
    minimized += audio[:4]
    minimized += total_len.to_bytes(4, "little")
    minimized += audio[8:40]
    minimized += len_data
    # metadata
    minimized += metadata
    # Audio
    minimized += b'data'
    minimized += (len(music) - 8).to_bytes(7, "little")
    minimized += music[11:]
    return minimized
