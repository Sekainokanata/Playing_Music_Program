import numpy as np
import sounddevice as sd
import threading

############MAIN PARAMETER############
BPM = 73
bar_line_second = (60/BPM)*4  # 1小節の秒数
Defalt_Volume = 0.1
sample_rate = 88000  # サンプルレート
phase = 0
current_sound_index = 0
played_frames = 0
played_frames_guiter = 0
durations = []#MAIN CODE
frequencies = []#MAIN CODE
duration_guiter = []#GUITAR CODE
frequencies_guiter = []#GUITAR CODE
#####################################



# 音名と周波数の対応表
frequencies_dict = {
    "BR": 0,  # 休符
    "C2": 65.41,  # ド
    "D2": 73.42,  # レ
    "E2": 82.41,  # ミ
    "F2": 87.31,  # ファ
    "G2": 98.00,  # ソ
    "A2": 110.00,  # ラ
    "B2♭": 116.54,  # シ♭
    "B2": 123.47,  # シ
    "C3": 130.81,  # ド
    "D3": 146.83,  # レ
    "E3♭": 155.56,  # ミ♭(レ♯)
    "E3": 164.81,  # ミ
    "F3": 174.61,  # ファ
    "F3#": 185.00,  # ファ♯
    "G3": 196.00,  # ソ
    "A3": 220.00,  # ラ
    "B3♭": 233.08,  # シ♭
    "B3": 246.94,  # シ
    "C4": 261.63,  # ド
    "D4": 293.66,  # レ
    "E4♭": 311.13,  # ミ♭
    "E4": 329.63,  # ミ
    "F4": 349.23,  # ファ
    "F4#": 369.99,  # ファ♯
    "G4": 392.00,  # ソ
    "A4": 440.00,  # ラ
    "B4♭": 466.16,  # シ♭
    "B4": 493.88,  # シ
    "C5": 523.25,  # ド
    "D5": 587.33,  # レ
    "E5♭": 622.25,  # ミ♭(レ♯)
    "E5": 659.25,  # ミ
    "F5": 698.46,  # ファ
    "F5#": 739.99,  # ファ♯
    "G5": 783.99,  # ソ
    "A5": 880.00,  # ラ
}

# コードの周波数リスト
##左から第一弦→第二弦→第三弦→第四弦→第五弦→第六弦(BRは弦を引かない場合)
##開放弦(その弦の一番低い音)は順に、E4→B3→G3→D3→A2→E2
#Em= E minor, Bm= B minor, B7= B7, Efdim= E♭ diminished
#Capo 3なため、３つずらす必要がある


#Capo 0

G = [frequencies_dict["G4"], frequencies_dict["B3"],frequencies_dict["G3"],frequencies_dict["D3"],frequencies_dict["B2"], frequencies_dict["G2"]]
C = [frequencies_dict["E4"],frequencies_dict["C4"], frequencies_dict["G3"],frequencies_dict["E3"],frequencies_dict["C3"], frequencies_dict["BR"]]
D = [frequencies_dict["F4#"], frequencies_dict["D4"], frequencies_dict["A3"],frequencies_dict["D3"],frequencies_dict["BR"],frequencies_dict["BR"]]
Efdim = [frequencies_dict["A4"],frequencies_dict["E4♭"],frequencies_dict["C4"],frequencies_dict["F3#"],frequencies_dict["BR"],frequencies_dict["BR"]]
Em = [frequencies_dict["E4"], frequencies_dict["B3"], frequencies_dict["G3"],frequencies_dict["E3"],frequencies_dict["B2"],frequencies_dict["E2"]]
Bm = [frequencies_dict["F4#"], frequencies_dict["D4"], frequencies_dict["B3"],frequencies_dict["F3#"],frequencies_dict["B2"],frequencies_dict["BR"]]
BonEf = [frequencies_dict["BR"], frequencies_dict["E4♭"], frequencies_dict["B3"],frequencies_dict["F3#"],frequencies_dict["E3♭"],frequencies_dict["BR"]]
Dsus4 = [frequencies_dict["G4"], frequencies_dict["D4"], frequencies_dict["A3"],frequencies_dict["D3"],frequencies_dict["BR"],frequencies_dict["BR"]]

#Capo 3
G = [frequencies_dict["B4♭"], frequencies_dict["D4"],frequencies_dict["B3♭"],frequencies_dict["F3"],frequencies_dict["D3"], frequencies_dict["B2♭"]]
C = [frequencies_dict["G4"],frequencies_dict["E4♭"], frequencies_dict["B3♭"],frequencies_dict["G3"],frequencies_dict["E3♭"], frequencies_dict["BR"]]
D = [frequencies_dict["A4"], frequencies_dict["F4"], frequencies_dict["C4"],frequencies_dict["F3"],frequencies_dict["BR"],frequencies_dict["BR"]]
Efdim = [frequencies_dict["A4"],frequencies_dict["E4♭"],frequencies_dict["C4"],frequencies_dict["F3#"],frequencies_dict["BR"],frequencies_dict["BR"]]
Em = [frequencies_dict["G4"], frequencies_dict["D4"], frequencies_dict["B3♭"],frequencies_dict["G3"],frequencies_dict["D3"],frequencies_dict["G2"]]
Bm = [frequencies_dict["A4"], frequencies_dict["F4"], frequencies_dict["D4"],frequencies_dict["A3"],frequencies_dict["D3"],frequencies_dict["BR"]]


###MAIN CODE###
Gakufu1 = ["B3♭","B3♭","B3♭","B3♭","F3","F3","B3♭","B3♭","F3","F3","B3♭","C4","BR","B3♭",
          "C4","C4","C4","C4","C4","B3♭","B3♭","C4","D4","E4♭","D4","C4","C4","B3♭",
          "B3♭","B3♭","B3♭","B3♭","B3♭","G4","G4","F4","E4♭","D4","E4♭","D4","BR","F3",
          "C4","C4","C4","C4","C4","D4","D4","E4♭","D4","C4","D4","C4",
          "B3♭","B3♭","B3♭","B3♭","F3","F3","B3♭","B3♭","F3","F3","B3♭","C4","BR","B3♭",
          "C4","C4","C4","C4","C4","B3♭","C4","D4","E4♭","D4","C4","B3♭",
          "C4","B3♭","B3♭","A4","B4♭","BR","B3♭","B3♭","C4",
          "D4","C4","C4","B3♭","E4♭","D4","C4","B3♭","B3♭",]


Tempo1 =  [1/16,1/16,1/8,1/16,1/16,1/16,1/16,1/16,1/16,1/16,1/16,1/8,1/16,1/16,
          1/16,1/16,1/16,1/16,1/16,1/16,1/16,1/16,1/8,1/8,(1/16)+(1/32),1/32,1/16,1/16,
          1/16,1/16,1/16,1/16,1/16,1/8,1/16,1/16,1/16,1/16,1/16,1/8,1/16,1/16,
          1/16,1/16,1/16,1/16,1/8,1/16,1/16,1/16,1/16,1/16,1/16,1/4,
          1/16,1/16,1/8,1/16,1/16,1/16,1/16,1/16,1/16,1/16,1/16,1/8,1/16,1/16,
          1/16,1/16,1/16,1/16,1/16,1/8,1/16,1/8,1/8,1/8,1/16,1/16,
          1/16,1/8,1/16,(1/8)+(1/16),(1/16)+(1/4),1/16,1/16,1/16,1/16,
          1/8,1/16,(1/16)+(1/8),1/16,(1/16)+(1/8),1/16,(1/16)+(1/16),1/16,(1/16)+(1/2),]
###############

###GUITAR CODE###
Gakufu2 =[G,G,G,G,
          C,C,C,C,C,C,
          D,D,D,D,
          Efdim,Efdim,Efdim,Efdim,Efdim,Efdim,
          Em,Em,Em,Em,
          Bm,Bm,Bm,Bm,Bm,Bm,
          C,C,C,C,
          D,D,D,D,D,D,
          G,G,G,G,
          C,C,C,C,C,C,
          D,D,D,D,
          Efdim,Efdim,Efdim,Efdim,Efdim,Efdim,
          Em,Em,Em,Em,
          Bm,Bm,Bm,Bm,Bm,Bm,
          C,C,C,C,
          D,D,D,D,D,D,
          G,G,G,G,G,G,G,G,G,G]

Tempo2 = [1/4,1/8,1/16,1/16,
          1/16,1/16,1/8,1/8,1/16,1/16,
          1/4,1/8,1/16,1/16,
          1/16,1/16,1/8,1/8,1/16,1/16,
          1/4,1/8,1/16,1/16,
          1/16,1/16,1/8,1/8,1/16,1/16,
          1/4,1/8,1/16,1/16,
          1/16,1/16,1/8,1/8,1/16,1/16,
          1/4,1/8,1/16,1/16,
          1/16,1/16,1/8,1/8,1/16,1/16,
          1/4,1/8,1/16,1/16,
          1/16,1/16,1/8,1/8,1/16,1/16,
          1/4,1/8,1/16,1/16,
          1/16,1/16,1/8,1/8,1/16,1/16,
          1/4,1/8,1/16,1/16,
          1/16,1/16,1/8,1/8,1/16,1/16,
          1/4,1/8,1/16,1/16,1/16,1/16,1/8,1/8,1/16,1,]
#################



if Defalt_Volume ==0:
    Volume = float(input("音量を入力してください(0.0~1.0):"))
else:
    Volume = Defalt_Volume

###MAIN CODE###
for i in range(len(Gakufu1)):
    frequencies.append(frequencies_dict[Gakufu1[i]])
for i in range(len(Gakufu1)):
    durations.append(int(bar_line_second * Tempo1[i] * sample_rate))
################

###GUITAR CODE###
for i in range(len(Gakufu2)):#音階
    frequencies_guiter.append(Gakufu2[i])
for i in range(len(Gakufu2)):#音符の長さ
    duration_guiter.append(int(bar_line_second * Tempo2[i] * sample_rate))

cnt_for_stroke = 0

def generate_guitar_wave(frequencies_guiter, duration_guiter):
    global cnt_for_stroke
    wave = np.array([])

    L = 650 * 10**-3#650mm*10^-3=0.65m(弦の長さ)
    x = L * (4/5)#弦の長さの4/5の位置にホールがあると仮定
    T = 70#弦の張力をとりあえず70Nと仮定
    d = 1.0#直径をとりあえず1.0mmと仮定ρ
    ρ = 1150#弦の密度をとりあえず1150kg/m^3と仮定
    μ = np.pi * (((d*10**-3)/2)**2) * ρ
    v = np.sqrt(T/μ)#弦の速度
    A = 1
    B = 1
    for f, d in zip(frequencies_guiter, duration_guiter):
        if d == int((1/16)*sample_rate*bar_line_second):
            cnt_for_stroke += 1
        t = np.linspace(0, d / sample_rate, int(d), endpoint=False)
        tone = 0

        #(https://nose-akira.hatenablog.com/entry/2018/10/14/162306)の資料を基に数値を計算している
        for f_tanon in f:
            #for n in range(1, 24): 
                #tone += A * np.cos((n*np.pi*x)/L)*np.cos(f_tanon*t)+B * np.cos(n*np.pi*x/L)*np.sin(f_tanon*t)
            tone += 1.00 * np.sin(2 * np.pi * f_tanon * t)
            tone += (78/69) * np.sin(2 * np.pi * f_tanon * 2 * t)
            tone += (64/69) * np.sin(2 * np.pi * f_tanon * 3 * t)
            tone += (43/69) * np.sin(2 * np.pi * f_tanon * 4 * t)
            tone += (57/69) * np.sin(2 * np.pi * f_tanon * 5 * t)
            tone += (58/69) * np.sin(2 * np.pi * f_tanon * 6 * t)
            tone += (52/69) * np.sin(2 * np.pi * f_tanon * 7 * t)
            tone += (37/69) * np.sin(2 * np.pi * f_tanon * 8 * t)
            tone += (46/69) * np.sin(2 * np.pi * f_tanon * 9 * t)
            tone += (55/69) * np.sin(2 * np.pi * f_tanon * 10 * t)
            tone += (51/69) * np.sin(2 * np.pi * f_tanon * 11 * t)
            tone += (30/69) * np.sin(2 * np.pi * f_tanon * 12 * t)
            tone += (31/69) * np.sin(2 * np.pi * f_tanon * 13 * t)
            tone += (34/69) * np.sin(2 * np.pi * f_tanon * 14 * t)
            tone += (36/69) * np.sin(2 * np.pi * f_tanon * 15 * t)
            tone += (22/69) * np.sin(2 * np.pi * f_tanon * 16 * t)
            tone += (26/69) * np.sin(2 * np.pi * f_tanon * 17 * t)
            tone += (40/69) * np.sin(2 * np.pi * f_tanon * 18 * t)
            tone += (42/69) * np.sin(2 * np.pi * f_tanon * 19 * t)
            tone += (37/69) * np.sin(2 * np.pi * f_tanon * 20 * t)
            tone += (28/69) * np.sin(2 * np.pi * f_tanon * 21 * t)
            tone += (31/69) * np.sin(2 * np.pi * f_tanon * 22 * t)
            tone += (40/69) * np.sin(2 * np.pi * f_tanon * 23 * t)
        #envelope = np.exp(-3 * t)
        # ADSRエンベロープ
        attack = 0.001#弾いてから音が出るまでの時間
        decay = 0.83#サスティーン・レベルに達するまでの時間
        sustain_level = 0.0#弾いてるあいだの音量
        release = 0.001#音が消えるまでの時間
        attack_samples = int(attack * sample_rate)
        decay_samples = int(decay * sample_rate)
        release_samples = int(release * sample_rate)
        sustain_samples = max(0, d - attack_samples - decay_samples - release_samples)
        envelope = np.concatenate([
            np.linspace(0, 1, attack_samples),  # Attack
            np.linspace(1, sustain_level, decay_samples),  # Decay
            np.full(sustain_samples, sustain_level),  # Sustain
            np.linspace(sustain_level, 0, release_samples)  # Release
        ])
        envelope = np.pad(envelope, (0, max(0, d - len(envelope))), 'constant')
        tone *= envelope[:len(tone)]
        if cnt_for_stroke % 2 == 0:
            tone *= 0.5
        # ノイズの追加
        #noise = np.random.normal(0, 0.005, len(tone))
        #tone += noise
        tone *= 0.1
        wave = np.concatenate((wave, tone))
    wave = wave / np.max(np.abs(wave))
    wave *= 0.5
    return wave

# ギターの信号を生成

guitar_signal = generate_guitar_wave(frequencies_guiter, duration_guiter)

def guitar_audio_callback(outdata, frames, time, status):
    global played_frames_guiter

    if status:
        print(status, flush=True)

    # 再生するフレーム数を決定
    frames_to_play_guiter = min(frames, len(guitar_signal) - played_frames_guiter)
    #####
    outdata[:frames_to_play_guiter] = guitar_signal[played_frames_guiter:played_frames_guiter + frames_to_play_guiter].reshape(-1, 1)
    #####
    # バッファの残り部分をゼロ埋め
    if frames_to_play_guiter < frames:
        outdata[frames_to_play_guiter:] = 0

    # 再生済みフレームを更新
    played_frames_guiter += frames_to_play_guiter

def play_guitar_wave():
    global played_frames_guiter
    played_frames_guiter = 0

    with sd.OutputStream(channels=2, callback=guitar_audio_callback, samplerate=sample_rate):
        total_duration = len(guitar_signal) / sample_rate
        sd.sleep(int(total_duration * 1000))  # 全体の再生が終わるまで待つ

def generate_wave(frequency, frames, phase, sample_rate):
    # 時間軸の生成
    t = (np.arange(frames) + phase) / sample_rate
    # 信号の生成
    #wave = Volume * np.sign(np.sin(2 * np.pi * frequency * t)) # 方形波
    #wave = Volume * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1# 三角波
    wave = Volume * np.sin(2 * np.pi * frequency * t)# 正弦波
    #wave = Volume * (2 * (t * frequency - np.floor(t * frequency + 0.5)))# ノコギリ波
    return wave

def apply_fade(wave, fade_in_frames, fade_out_frames):
    fade_in = np.linspace(0, 1, fade_in_frames)
    fade_out = np.linspace(1, 0, fade_out_frames)
    wave[:fade_in_frames] *= fade_in
    wave[-fade_out_frames:] *= fade_out
    return wave    

# すべての信号を生成
signals = []
fade_in_frames = int(sample_rate * 0.005)  # フェードインのフレーム数（0.01秒）
fade_out_frames = int(sample_rate * 0.005)  # フェードアウトのフレーム数（0.01秒）

for i in range(len(Gakufu1)):

    frames = durations[i]
    frequency = frequencies[i]
    

    signal = generate_wave(frequency, frames, 0, sample_rate)

    signal = apply_fade(signal, fade_in_frames, fade_out_frames)
    signals.append(signal)

# すべての信号を結合
full_signal = np.concatenate(signals)

def audio_callback(outdata, frames, time, status):
    global played_frames

    if status:
        print(status, flush=True)

    # 再生するフレーム数を決定
    frames_to_play = min(frames, len(full_signal) - played_frames)

    outdata[:frames_to_play] = full_signal[played_frames:played_frames + frames_to_play].reshape(-1, 1)

    # バッファの残り部分をゼロ埋め
    if frames_to_play < frames:
        outdata[frames_to_play:] = 0

    # 再生済みフレームを更新
    played_frames += frames_to_play

def play_square_wave():
    global played_frames
    played_frames = 0

    with sd.OutputStream(channels=1, callback=audio_callback, samplerate=sample_rate):
        total_duration = len(full_signal) / sample_rate
        sd.sleep(int(total_duration * 1000))  # 全体の再生が終わるまで待つ

# ギターとsquare_waveの音を同時に再生
def play_both_waves():
    guitar_thread = threading.Thread(target=play_guitar_wave)
    square_wave_thread = threading.Thread(target=play_square_wave)
    
    guitar_thread.start()
    square_wave_thread.start()
    
    #guitar_thread.join()
    #square_wave_thread.join()

play_both_waves()