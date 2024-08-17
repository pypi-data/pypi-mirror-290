import argparse
from audio_conversion import *
from seam_carving import carve_audio

def main(input_wavfile, n_of_seams, carve_time=False):
    audio, sampling_rate = load_wavfile(input_wavfile)
    matrix = get_stft(audio)
    magnitude, phase = extract_mag_pha(matrix)
    
    # Carve the audio based on the chosen direction
    if carve_time:
        magnitude, phase = carve_audio(n_of_seams, magnitude, phase, is_vertical=True)
        carve_direction = 'time'
    else:
        magnitude, phase = carve_audio(n_of_seams, magnitude, phase, is_vertical=False)
        carve_direction = 'frequency'
    
    # Create the output filename based on carve direction
    output_filename = f'{input_wavfile.split(".")[0]}_carved{carve_direction}_{n_of_seams}.wav'
    
    # Save the carved audio to a new wav file
    sig_to_wav(output_filename, magnitude, phase)
    
    print(f"Processed {input_wavfile} and saved as {output_filename} with {n_of_seams} seams carved in the {carve_direction} domain")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Audio carving script')
    parser.add_argument('input_wavfile', type=str, help='Input WAV file path')
    parser.add_argument('n_of_seams', type=int, help='Number of seams to carve')
    parser.add_argument('--carve_time', action='store_true', help='Perform time domain carving (default is frequency domain)')
    
    args = parser.parse_args()
    
    main(args.input_wavfile, args.n_of_seams, args.carve_time)