import os
import sys
import numpy as np
import load_trace
import fixed_env as env

S_INFO = 8  # bit_rate, buffer_size, next_chunk_size, bandwidth_measurement(throughput and time), chunk_til_video_end, action_vec
S_LEN = 8  # take how many frames in the past
A_DIM = 6
VIDEO_BIT_RATE = [300, 750, 1200, 1850, 2850, 4300]  # Kbps
DEFAULT_QUALITY = 1  # default video quality without agent
TEST_LOG_FOLDER = "/app/results"
LOG_FILE = "/log_"
TEST_TRACES = "/app/traces/"
M_IN_K = 1000.0

# Parâmetros do LOLYPOP
#SIGMA_STAR = 0.02  # Limite de segmentos ignorados
#OMEGA_STAR = 0.1   # Limite de transições de qualidade
SIGMA_STAR = 0.2  # Limite de segmentos ignorados
OMEGA_STAR = 1.0   # Limite de transições de qualidade



class LOLYPOP:
    def __init__(self, sigma_star, omega_star):
        self.sigma_star = sigma_star
        self.omega_star = omega_star
        self.last_quality = DEFAULT_QUALITY  # Qualidade do último segmento

    def select_representation(self, probabilities, current_transitions):
        """
            Seleciona a qualidade para o próximo segmento com base no LOLYPOP.
        """
        # Passo 1: Identificar a qualidade mais alta que atende Σ*
        max_quality = 0
        for j, p in enumerate(probabilities):
            if p >= 1 - self.sigma_star:
                max_quality = j

        # Passo 2: Verificar o limite Ω* para transições de qualidade
        if current_transitions > self.omega_star and max_quality > self.last_quality:
            selected_quality = self.last_quality
        else:
            selected_quality = max_quality

        self.last_quality = selected_quality
        return selected_quality


def main():
    np.random.seed(42)

    all_cooked_time, all_cooked_bw, all_file_names = load_trace.load_trace(TEST_TRACES)
    net_env = env.Environment(all_cooked_time=all_cooked_time, all_cooked_bw=all_cooked_bw)

    if not os.path.exists(TEST_LOG_FOLDER):
        os.makedirs(TEST_LOG_FOLDER)

    log_path = TEST_LOG_FOLDER + LOG_FILE + all_file_names[net_env.trace_idx]
    log_file = open(log_path, "w")
    print(log_file)

    time_stamp = 0
    video_count = 0

    lolypop = LOLYPOP(SIGMA_STAR, OMEGA_STAR)  # Inicializar o algoritmo LOLYPOP
    current_transitions = 0  # Contador de transições de qualidade
    last_bit_rate = DEFAULT_QUALITY
    bit_rate = DEFAULT_QUALITY

    while True:
        (
            delay,
            sleep_time,
            buffer_size,
            rebuf,
            video_chunk_size,
            next_video_chunk_sizes,
            end_of_video,
            video_chunk_remain,
            throughput,
        ) = net_env.get_video_chunk(bit_rate)

        time_stamp += delay
        time_stamp += sleep_time

        # Calcular probabilidades de sucesso de download para todas as qualidades
        probabilities = [
            min(1.0, buffer_size / (next_video_chunk_sizes[j] / throughput)) if throughput > 0 else 0.0
            for j in range(len(VIDEO_BIT_RATE))
        ]

        # Atualizar transições de qualidade se necessário
        if bit_rate != last_bit_rate and video_chunk_remain > 0:
            current_transitions += 1 / video_chunk_remain

        # if bit_rate != last_bit_rate:
        #     current_transitions += 1 / video_chunk_remain

        # Selecionar a próxima qualidade com base no LOLYPOP
        bit_rate = lolypop.select_representation(probabilities, current_transitions)

        # Logar os resultados
        line = (
            f"{time_stamp / M_IN_K},{VIDEO_BIT_RATE[bit_rate]},{buffer_size},"
            f"{rebuf},{video_chunk_size},{delay},{throughput}\n"
        )
        log_file.write(line)
        log_file.flush()

        if end_of_video:
            log_file.write("\n")
            log_file.close()

            last_bit_rate = DEFAULT_QUALITY
            bit_rate = DEFAULT_QUALITY
            current_transitions = 0
            video_count += 1

            print("Video:", video_count)
            if video_count >= len(all_file_names):
                break

            log_path = TEST_LOG_FOLDER + LOG_FILE + all_file_names[net_env.trace_idx]
            log_file = open(log_path, "w")
            print(log_path)


if __name__ == "__main__":
    main()
