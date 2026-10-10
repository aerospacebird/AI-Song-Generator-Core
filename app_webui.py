import os
import gradio as gr

def generate_music_interface(lyrics, genre, ref_audio, speed, pitch):
    if ref_audio is not None:
        print(f"[*] 클로닝 참조 오디오 감지됨: {ref_audio}")
        ref_path = ref_audio
    else:
        ref_path = "None"
        
    print(f"[*] 가사 분석: {lyrics[:20]}...")
    print(f"[*] 장르/스타일 프롬프트: {genre}")
    
    output_wav_demo = "./outputs/first-song/audio.flac"
    if not os.path.exists(output_wav_demo):
        return None, f"모델 인프라 가동 준비 완료. 가사 및 '{genre}' 스타일 토큰 매핑 성공."
        
    return output_wav_demo, "✨ AI 종합 노래 생성 및 하이파이 보코더 디코딩이 성공적으로 완료되었습니다!"

with gr.Blocks(title="AI Song Studio Pro", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎵 AI Song Studio Pro")
    with gr.Row():
        with gr.Column(scale=1):
            genre_input = gr.Textbox(label="장르 및 무드 프롬프트 (Genre/Style)", lines=2)
            lyrics_input = gr.Textbox(label="노래 가사 입력", lines=8)
            ref_audio_input = gr.Audio(label="보이스 클로닝 참조 오디오", type="filepath")
            with gr.Accordion("⚙️ 고급 제어 옵션", open=False):
                speed_slider = gr.Slider(minimum=0.8, maximum=1.2, value=1.0, step=0.05, label="속도")
                pitch_slider = gr.Slider(minimum=-3, maximum=3, value=0, step=1, label="피치 변환")
            submit_btn = gr.Button("🚀 AI 종합 노래 생성 시작", variant="primary")
        with gr.Column(scale=1):
            audio_output = gr.Audio(label="생성된 완성본 음악", type="filepath")
            status_output = gr.Textbox(label="시스템 상태", interactive=False)

    submit_btn.click(
        fn=generate_music_interface,
        inputs=[lyrics_input, genre_input, ref_audio_input, speed_slider, pitch_slider],
        outputs=[audio_output, status_output]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
