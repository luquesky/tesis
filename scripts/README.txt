'extractStandardAcoustics.praat y voice-analysis.praat extraen atributos
acústicos de un intervalo de un archivo wav.

Modo de uso:

praat SCRIPT WAVFILE START END MIN_PITCH MAX_PITCH

donde:
  SCRIPT: extractStandardAcoustics.praat o voice-analysis.praat.
  WAVFILE: Path al archivo wav.
  START,END: Comienzo y final del intervalo, en segundos.
  MIN_PITCH,MAX_PITCH: Estimación del rango tonal del hablante, en Hz. 
    Para hombres usar 50 y 300, para mujeres usar 75 y 500. El género
    los hablantes lo podés consultar en ../datos/sessions_info.txt.
    Por ejemplo, la sesión 10 tiene dos hablantes mujeres (ids 111 y 103).

extractStandardAcoustics.praat devuelve algo así:

SECONDS:10.000        -->  duration in seconds
F0_MAX:436.790        -->  f0 max
F0_MIN:103.482        -->  f0 min
F0_MEAN:188.553       -->  f0 mean
F0_MEDIAN:175.885     -->  f0 median
F0_STDV:50.528        -->  f0 standard deviation
F0_MAS:264.039        -->  mean absolute f0 slope
ENG_MAX:80.287        -->  energy max (energy=intensity)
ENG_MIN:29.604        -->  energy min
ENG_MEAN:49.815       -->  energy mean
ENG_STDV:15.601       -->  energy standard deviation
VCD2TOT_FRAMES:0.255  -->  ratio of voiced frames to total frames

voice-analysis.praat devuelve algo así:

sound_all_local_jitter:0.008590      --> jitter computado sobre todo el intervalo
sound_all_local_shimmer:0.070114     --> shimmer computado sobre todo el intervalo
noise_to_harmonics_ratio:0.056981    --> relación armónico-ruido
sound_voiced_local_jitter:0.009913   --> jitter computado sobre los voiced frames del intervalo
sound_voiced_local_shimmer:0.053497  --> shimmer computado sobre los voiced frames del intervalo



Ejemplo:

 praat extractStandardAcoustics.praat ../data/s10.objects.1.A.wav 0 10 75 500