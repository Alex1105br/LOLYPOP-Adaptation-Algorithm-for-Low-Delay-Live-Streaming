import os
import sys

import numpy as np
import load_trace

# import a2c as network
from bb import bb_algo
import fixed_env as env


S_INFO = 8  # bit_rate, buffer_size, next_chunk_size, bandwidth_measurement(throughput and time), chunk_til_video_end, action_vec
S_LEN = 8  # take how many frames in the past
A_DIM = 6
ACTOR_LR_RATE = 0.0001
CRITIC_LR_RATE = 0.001
VIDEO_BIT_RATE = [300, 750, 1200, 1850, 2850, 4300]  # Kbps
BUFFER_NORM_FACTOR = 12.0
BMIN = 4.0
CHUNK_TIL_VIDEO_END_CAP = 48.0
M_IN_K = 1000.0
REBUF_PENALTY = 4.3  # 1 sec rebuffering -> 3 Mbps
SMOOTH_PENALTY = 1
DEFAULT_QUALITY = 1  # default video quality without agent
RANDOM_SEED = 42
RAND_RANGE = 1000
TEST_LOG_FOLDER = "/app/results"
LOG_FILE = "/log_"
TEST_TRACES = "/app/traces/"
# log in format of time_stamp bit_rate buffer_size rebuffer_time chunk_size download_time reward


def main():
    np.random.seed(RANDOM_SEED)

    assert len(VIDEO_BIT_RATE) == A_DIM

    all_cooked_time, all_cooked_bw, all_file_names = load_trace.load_trace(TEST_TRACES)

    net_env = env.Environment(
        all_cooked_time=all_cooked_time, all_cooked_bw=all_cooked_bw
    )

    if not os.path.exists(TEST_LOG_FOLDER):
        os.makedirs(TEST_LOG_FOLDER)

    log_path = TEST_LOG_FOLDER + LOG_FILE + all_file_names[net_env.trace_idx]
    log_file = open(log_path, "w")
    print(log_file)

    time_stamp = 0

    last_bit_rate = DEFAULT_QUALITY
    bit_rate = DEFAULT_QUALITY
    video_count = 0

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

        time_stamp += delay  # in ms
        time_stamp += sleep_time  # in ms

        last_bit_rate = bit_rate

        line = (
            str(time_stamp / M_IN_K)
            + ","
            + str(VIDEO_BIT_RATE[bit_rate])
            + ","
            + str(buffer_size)
            + ","
            + str(rebuf)
            + ","
            + str(video_chunk_size)
            + ","
            + str(delay)
            + ","
            + str(throughput)
            + "\n"
        )

        log_file.write(line)
        log_file.flush()

        # noise = np.random.gumbel(size=len(action_prob))
        bit_rate = bb_algo(buffer_size, VIDEO_BIT_RATE, DEFAULT_QUALITY, M_IN_K, BMIN)

        if end_of_video:
            log_file.write("\n")
            log_file.close()

            last_bit_rate = DEFAULT_QUALITY
            bit_rate = DEFAULT_QUALITY  # use the default action here

            print("Video: ", video_count)
            video_count += 1

            if video_count >= len(all_file_names):
                break

            log_path = TEST_LOG_FOLDER + LOG_FILE + all_file_names[net_env.trace_idx]
            log_file = open(log_path, "w")
            print(log_path)


if __name__ == "__main__":
    main()
