"""
6.1010 Spring '23 Lab 0: Audio Processing
"""

import wave
import struct

# No additional imports allowed!


def backwards(sound):
    """
    Applies a filter, resulting in a new sound that is the original sound reversed.
    Does not modify inputs.

    Args:
        sound: A sound dictionary with two key/value pairs:
            * "rate": an int representing the sampling rate, samples per second
            * "samples": a list of floats containing the sampled values

    Returns:
        A new sound dictionary.
    """
    reversed_samples = sound["samples"].copy()
    # reverse the samples from sound
    reversed_samples.reverse()
    reversed_rate = sound["rate"]
    # generate the reversed sound given the rate and samples
    reversed_sound = {"rate": reversed_rate, "samples": reversed_samples}
    return reversed_sound


def mix(sound1, sound2, p):
    """
    Mixes two sounds, resulting in a new sound that combines the original sounds.
    Does not modify inputs.

    Args:
        sound1: A sound dictionary with two key/value pairs:
            * "rate": an int representing the sampling rate, samples per second
            * "samples": a list of floats containing the sampled values
        sound2: A sound dictionary with two key/value pairs:
            * "rate": an int representing the sampling rate, samples per second
            * "samples": a list of floats containing the sampled values
        p: An int parameter determining how much of each sound is mixed

    Returns:
        A new sound dictionary.
    """
    # return None if the sounds have different rates
    if sound1["rate"] != sound2["rate"]:
        return None

    # get the rate for the new sound
    rate = sound1["rate"]
    # get the samples from each sound
    if "left" in sound1:
        sound1_left = sound1["left"]
        sound1_right = sound1["right"]
        sound2_left = sound2["left"]
        sound2_right = sound2["right"]
    else:
        sound1_samples = sound1["samples"]
        sound2_samples = sound2["samples"]
    # determine the length of the new sound, which is the shortest of the two
    sound1_length = get_length(sound1)
    sound2_length = get_length(sound2)
    if sound1_length < sound2_length:
        sound_length = sound1_length
    else:
        sound_length = sound2_length

    if "left" in sound1:
        left_mix = mix_samples(sound1_left, sound2_left, sound_length, p)
        right_mix = mix_samples(sound1_right, sound2_right, sound_length, p)
        mix_sound = {"rate": rate, "left": left_mix, "right": right_mix}
        return mix_sound
    else:
        samples_mix = mix_samples(
            sound1_samples, sound2_samples, sound_length, p)
        mix_sound = {"rate": rate, "samples": samples_mix}
        return mix_sound


def mix_samples(sound_samples1, sound_samples2, length, p):
    mixed_samples = []
    for i in range(length):
        # determine the amount of each sample mixed
        sample1 = p * sound_samples1[i]
        sample2 = (1 - p) * sound_samples2[i]
        # add samples
        sample_sum = sample1 + sample2
        # add the new sample to the new sound
        mixed_samples.append(sample_sum)
    return mixed_samples


def get_length(sound):
    if "left" in sound:
        length = len(sound["left"])
    else:
        length = len("sampels")
    return length


s1 = {
    'rate': 8000,
    'left': [0.00, 0.59, 0.95, 0.95, 0.59, 0.00, -0.59, -0.95, -0.95, -0.59],
    'right': [1.00, 0.91, 0.67, 0.31, -0.10, -0.50, -0.81, -0.98, -0.98, -0.81],
}

s2 = {
    'rate': 8000,
    'left': [1.00, 0.91, 0.67, 0.31, -0.10, -0.50, -0.81, -0.98, -0.98, -0.81],
    'right': [0.00, 0.59, 0.95, 0.95, 0.59, 0.00, -0.59, -0.95, -0.95, -0.59]
}
length = get_length(s1)
print(mix_samples(s1["left"], s2["left"], length, 0.5))
print(mix_samples(s1["right"], s2["right"], length, 0.5))