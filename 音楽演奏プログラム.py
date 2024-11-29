import numpy as np
import sounddevice as sd


#四小節ごとに改行している
Gakufu = []
Tempo =  []
##Gakufuは英語表記、Tempoは何分音符かを分数で記入

BPM = 73
bar_line_second = (60/BPM)*4  # 1小節の秒数

frequencies_dict = {
    "BR": 0,  # 休符
    "C3": 130.81,  # ド
    "D3": 146.83,  # レ
    "E3": 164.81,  # ミ
    "F3": 174.61,  # ファ
    "G3": 196.00,  # ソ
    "A3": 220.00,  # ラ
    "B3♭": 233.08,  # シ♭
    "B3": 246.94,  # シ
    "C4": 261.63,  # ド
    "D4": 293.66,  # レ
    "E4♭": 311.13,  # ミ♭
    "E4": 329.63,  # ミ
    "F4": 349.23,  # ファ
    "G4": 392.00,  # ソ
    "A4": 440.00,  # ラ
    "B4": 493.88,  # シ
    "C5": 523.25,  # ド
    "D5": 587.33,  # レ
    "E5": 659.25,  # ミ
    "F5": 698.46,  # ファ
    "G5": 783.99,  # ソ
}

# パラメータ設定
sample_rate = 44100  # サンプルレート
phase = 0
current_sound_index = 0
played_frames = 0
durations = []
frequencies = []

Volume = float(input("音量を入力してください(0.0~1.0):"))

for i in range(len(Gakufu)):
    durations.append(int(bar_line_second * Tempo[i] * sample_rate))

for i in range(len(Gakufu)):
    frequencies.append(frequencies_dict[Gakufu[i]])

def generate_square_wave(frequency, frames, phase, sample_rate):
    # 時間軸の生成
    t = (np.arange(frames) + phase) / sample_rate
    # 方形波の生成
    wave = Volume * np.sign(np.sin(2 * np.pi * frequency * t))
    return wave

def audio_callback(outdata, frames, time, status):
    global phase, current_sound_index, played_frames

    if status:
        print(status, flush=True)

    # 再生中の音の終了判定
    current_duration_frames = durations[current_sound_index]
    remaining_frames = current_duration_frames - played_frames

    if remaining_frames <= 0:
        # 次の音に切り替え
        current_sound_index += 1
        played_frames = 0
        phase = 0
        if current_sound_index >= len(Gakufu):  # 全ての音を再生し終えたら停止
            raise sd.CallbackStop
        else:
            remaining_frames = durations[current_sound_index]

    # 再生するフレーム数を決定
    frames_to_play = min(frames, remaining_frames)

    waveform = generate_square_wave(frequencies[current_sound_index], frames_to_play, phase, sample_rate)
    outdata[:frames_to_play] = waveform.reshape(-1, 1)
    phase += frames_to_play

    # バッファの残り部分をゼロ埋め
    if frames_to_play < frames:
        outdata[frames_to_play:] = 0

    # 再生済みフレームを更新
    played_frames += frames_to_play

def play_square_wave():
    global current_sound_index, played_frames, phase
    current_sound_index = 0
    played_frames = 0
    phase = 0

    with sd.OutputStream(channels=1, callback=audio_callback, samplerate=sample_rate):
        print("音声再生中...")
        total_duration = sum(durations) / sample_rate
        sd.sleep(int(total_duration * 1000))  # 全体の再生が終わるまで待つ
    print("再生終了！")

play_square_wave()