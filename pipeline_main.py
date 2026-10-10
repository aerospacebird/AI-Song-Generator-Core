import os
import re
import subprocess
import librosa
import soundfile as sf
from g2pk import G2p

class KoreanLyricsProcessor:
    def __init__(self):
        self.g2p = G2p()

    def convert_to_phonetic(self, lyrics_text):
        tokens = re.split(r'(\[[^\]]+\])', lyrics_text)
        processed_tokens = []
        for token in tokens:
            if token.startswith('[') and token.endswith(']'):
                processed_tokens.append(token)
            elif token.strip() == "":
                processed_tokens.append(token)
            else:
                processed_tokens.append(self.g2p(token))
        return "".join(processed_tokens)

class FullMusicDataPipeline:
    def __init__(self, raw_dir="./raw_data", output_dir="./final_dataset"):
        self.raw_dir = raw_dir
        self.output_dir = output_dir
        self.lyrics_processor = KoreanLyricsProcessor()
        os.makedirs(output_dir, exist_ok=True)

    def separate_vocals_high_qual(self, mp3_path):
        print(f"[*] 분리 시작: {mp3_path}")
        command = f"demucs --two-stems=vocals -n hdemucs_mmi --shifts=10 --overlap=0.25 {mp3_path} -o {self.output_dir}"
        subprocess.run(command, shell=True, check=True)
        
        song_name = os.path.splitext(os.path.basename(mp3_path))[0]
        vocal_path = os.path.join(self.output_dir, "hdemucs_mmi", song_name, "vocals.wav")
        return vocal_path

    def process_song(self, mp3_filename, raw_lyrics):
        mp3_path = os.path.join(self.raw_dir, mp3_filename)
        vocal_wav = self.separate_vocals_high_qual(mp3_path)
        phonetic_lyrics = self.lyrics_processor.convert_to_phonetic(raw_lyrics)
        
        y, sr = librosa.load(vocal_wav, sr=44100)
        chunk_samples = int(15.0 * sr)
        song_name = os.path.splitext(mp3_filename)[0]
        
        for i, start_sample in enumerate(range(0, len(y), chunk_samples)):
            end_sample = min(start_sample + chunk_samples, len(y))
            chunk = y[start_sample:end_sample]
            
            chunk_name = f"{song_name}_chunk_{i:03d}"
            wav_out = os.path.join(self.output_dir, f"{chunk_name}.wav")
            sf.write(wav_out, chunk, sr)
            
            txt_out = os.path.join(self.output_dir, f"{chunk_name}.txt")
            with open(txt_out, "w", encoding="utf-8") as f:
                f.write(phonetic_lyrics)
                
        print(f"[+] 완료: {song_name} 전처리 및 데이터셋 패어 쌍 생성 성공")

if __name__ == "__main__":
    print("Full Music Data Pipeline initialized.")
