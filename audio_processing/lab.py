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
    # check which sound is shorter and pick the shortest as length
    if sound1_length < sound2_length:
        sound_length = sound1_length
    else:
        sound_length = sound2_length

    # check if the sound is stereo
    if "left" in sound1:
        # mix the left and right samples
        left_mix = mix_samples(sound1_left, sound2_left, sound_length, p)
        right_mix = mix_samples(sound1_right, sound2_right, sound_length, p)
        # generate mixed sound from each mixed side
        mix_sound = {"rate": rate, "left": left_mix, "right": right_mix}
        return mix_sound
    # if the sound is mono
    else:
        # mix the samples
        samples_mix = mix_samples(
            sound1_samples, sound2_samples, sound_length, p)
        # generate mixed sound
        mix_sound = {"rate": rate, "samples": samples_mix}
        return mix_sound


def mix_samples(sound_samples1, sound_samples2, length, p):
    """
    Mixes two sample lists into a new sample list combining the original sounds.
    Does not modify inputs.

    Args:
        sound_samples1: a list of floats containing sampled values from a sound
        sound_samples2: a list of floats containing sampled values from another sound
        length: an int representing the desired length of the resulting list
        p: an int parameter determining how much of each sound is mixed

    Returns:
        A new list of floats.
    """
    # create an empty list for samples
    mixed_samples = []
    for i in range(length):
        # determine the amount of each sample mixed
        sample1 = p * sound_samples1[i]
        sample2 = (1 - p) * sound_samples2[i]
        # add samples
        sample_sum = sample1 + sample2
        # add the new sample to the new sound
        mixed_samples.append(sample_sum)
    # return the list
    return mixed_samples


def get_length(sound):
    """
    Gets the length of a sound.
    Does not modify inputs.

    Args:
        sound: A sound dictionary with two key/value pairs:
            * "rate": an int representing the sampling rate, samples per second
            * "samples": a list of floats containing the sampled values

    Returns:
        An int representing the length of the sound.
    """
    # check if the sound is stereo
    if "left" in sound:
        # get the length of the left channel list (same as right)
        length = len(sound["left"])
    # if the sound is mono
    else:
        # get the length of the samples list
        length = len(sound["samples"])
    # return the length
    return length


def convolve(sound, kernel):
    """
    Applies a filter to a sound, resulting in a new sound that is longer than
    the original mono sound by the length of the kernel - 1.
    Does not modify inputs.

    Args:
        sound: A mono sound dictionary with two key/value pairs:
            * "rate": an int representing the sampling rate, samples per second
            * "samples": a list of floats containing the sampled values
        kernel: A list of numbers

    Returns:
        A new mono sound dictionary.
    """
    # get samples from sound
    samples = sound["samples"]
    # create an empty list of the correct length
    convolve_samples = [0] * (len(samples) + len(kernel) - 1)

    # add up each sample and kernel combination
    for i in range(len(kernel)):
        if kernel[i] != 0:
            for j in range(len(samples)):
                convolve_samples[i + j] += kernel[i] * samples[j]

    # return the new sound
    return {"rate": sound["rate"], "samples": convolve_samples}


def echo(sound, num_echoes, delay, scale):
    """
    Compute a new signal consisting of several scaled-down and delayed versions
    of the input sound. Does not modify input sound.

    Args:
        sound: a dictionary representing the original mono sound
        num_echoes: int, the number of additional copies of the sound to add
        delay: float, the amount of seconds each echo should be delayed
        scale: float, the amount by which each echo's samples should be scaled

    Returns:
        A new mono sound dictionary resulting from applying the echo effect.
    """
    sample_delay = round(delay * sound["rate"])
    echo_filter = [0] * (sample_delay * num_echoes + 1)
    echo_filter[0] = 1
    for i in range(num_echoes):
        offset = int((i + 1) * sample_delay)
        echo_filter[offset] = scale ** (i + 1)

    sound_echo = convolve(sound, echo_filter)
    return sound_echo


def pan(sound):
    """
    Applies a filter to a sound, resulting in a new sound
    that pans the sound from the left to the right.
    Does not modify inputs.

    Args:
        sound: A stereo sound dictionary with three key/value pairs:
            * "rate": an int representing the sampling rate, samples per second
            * "left": a list of floats containing the sampled values on the left side
            * "right": a list of floats containing the sampled values on the right side

    Returns:
        A new stereo sound dictionary.
    """
    # get the sampling rate
    rate = sound["rate"]
    # copy the left and right lists into new lists so that the inputs are not modified
    sound_left = sound["left"].copy()
    sound_right = sound["right"].copy()
    # get the length of the sound
    sound_length = len(sound_right)
    # apply the filter to the left and right lists
    for i in range(sound_length):
        sound_right[i] = sound_right[i] * i / (sound_length-1)
        sound_left[i] = sound_left[i] * (1 - i / (sound_length-1))

    # return the new sound dictionary
    return {"rate": rate, "left": sound_left, "right": sound_right}


def remove_vocals(sound):
    """
    Applies a filter to a sound, resulting in a new sound
    that removes the sounds panned to the center.
    Does not modify inputs.

    Args:
        sound: A stereo sound dictionary with three key/value pairs:
            * "rate": an int representing the sampling rate, samples per second
            * "left": a list of floats containing the sampled values on the left side
            * "right": a list of floats containing the sampled values on the right side

    Returns:
        A new mono sound dictionary.
    """
    # get the sampling rate
    rate = sound["rate"]
    # get the left and right samples
    sound_left = sound["left"]
    sound_right = sound["right"]
    # get the length of the sound
    sound_length = len(sound_right)
    # create the new empty mono samples list
    sound_diff = [0] * sound_length
    # apply the filter difference
    for i in range(sound_length):
        sound_diff[i] = sound_left[i] - sound_right[i]

    # return the new sound dictionary
    return {"rate": rate, "samples": sound_diff}


# below are helper functions for converting back-and-forth between WAV files
# and our internal dictionary representation for sounds


def bass_boost_kernel(boost, scale=0):
    """
    Constructs a kernel that acts as a bass-boost filter.

    We start by making a low-pass filter, whose frequency response is given by
    (1/2 + 1/2cos(Omega)) ^ N

    Then we scale that piece up and add a copy of the original signal back in.

    Args:
        boost: an int that controls the frequencies that are boosted (0 will
            boost all frequencies roughly equally, and larger values allow more
            focus on the lowest frequencies in the input sound).
        scale: a float, default value of 0 means no boosting at all, and larger
            values boost the low-frequency content more);

    Returns:
        A list of floats representing a bass boost kernel.
    """
    # make this a fake "sound" so that we can use the convolve function
    base = {"rate": 0, "samples": [0.25, 0.5, 0.25]}
    kernel = {"rate": 0, "samples": [0.25, 0.5, 0.25]}
    for i in range(boost):
        kernel = convolve(kernel, base["samples"])
    kernel = kernel["samples"]

    # at this point, the kernel will be acting as a low-pass filter, so we
    # scale up the values by the given scale, and add in a value in the middle
    # to get a (delayed) copy of the original
    kernel = [i * scale for i in kernel]
    kernel[len(kernel) // 2] += 1

    return kernel


def load_wav(filename, stereo=False):
    """
    Load a file and return a sound dictionary.

    Args:
        filename: string ending in '.wav' representing the sound file
        stereo: bool, by default sound is loaded as mono, if True sound will
            have left and right stereo channels.

    Returns:
        A dictionary representing that sound.
    """
    sound_file = wave.open(filename, "r")
    chan, bd, sr, count, _, _ = sound_file.getparams()

    assert bd == 2, "only 16-bit WAV files are supported"

    out = {"rate": sr}

    left = []
    right = []
    for i in range(count):
        frame = sound_file.readframes(1)
        if chan == 2:
            left.append(struct.unpack("<h", frame[:2])[0])
            right.append(struct.unpack("<h", frame[2:])[0])
        else:
            datum = struct.unpack("<h", frame)[0]
            left.append(datum)
            right.append(datum)

    if stereo:
        out["left"] = [i / (2**15) for i in left]
        out["right"] = [i / (2**15) for i in right]
    else:
        samples = [(ls + rs) / 2 for ls, rs in zip(left, right)]
        out["samples"] = [i / (2**15) for i in samples]

    return out


def write_wav(sound, filename):
    """
    Save sound to filename location in a WAV format.

    Args:
        sound: a mono or stereo sound dictionary
        filename: a string ending in .WAV representing the file location to
            save the sound in
    """
    outfile = wave.open(filename, "w")

    if "samples" in sound:
        # mono file
        outfile.setparams((1, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = [int(max(-1, min(1, v)) * (2**15 - 1)) for v in sound["samples"]]
    else:
        # stereo
        outfile.setparams((2, 2, sound["rate"], 0, "NONE", "not compressed"))
        out = []
        for l_val, r_val in zip(sound["left"], sound["right"]):
            l_val = int(max(-1, min(1, l_val)) * (2**15 - 1))
            r_val = int(max(-1, min(1, r_val)) * (2**15 - 1))
            out.append(l_val)
            out.append(r_val)

    outfile.writeframes(b"".join(struct.pack("<h", frame) for frame in out))
    outfile.close()


if __name__ == "__main__":
    # code in this block will only be run when you explicitly run your script,
    # and not when the tests are being run.  this is a good place to put your
    # code for generating and saving sounds, or any other code you write for
    # testing, etc.

    # here is an example of loading a file (note that this is specified as
    # sounds/hello.wav, rather than just as hello.wav, to account for the
    # sound files being in a different directory than this file)
    hello = load_wav("sounds/hello.wav")
    # write_wav(backwards(hello), "hello_reversed.wav")

    # mystery = load_wav("sounds/mystery.wav")
    # write_wav(backwards(mystery), "mystery_reversed.wav")

    # synth = load_wav("sounds/synth.wav")
    # water = load_wav("sounds/water.wav")
    # write_wav(mix(synth, water, 0.2), "synth_water_mixed.wav")

    # ice_and_chilli = load_wav("sounds/ice_and_chilli.wav")
    # bass_kernel = bass_boost_kernel(1000, 1.5)
    # write_wav(convolve(ice_and_chilli, bass_kernel),
    #           "ice_and_chilli_bass_boosted.wav")

    # chord = load_wav("sounds/chord.wav")
    # write_wav(echo(chord, 5, 0.3, 0.6), "chord_echo.wav")

    # car = load_wav("sounds/car.wav", stereo=True)
    # write_wav(pan(car), "car_panned.wav")

    # lookout_mountain = load_wav("sounds/lookout_mountain.wav", stereo=True)
    # write_wav(remove_vocals(lookout_mountain),
    #           "lookout_mountain_no_vocals.wav")

    # synth = load_wav("sounds/synth.wav", stereo=True)
    # water = load_wav("sounds/water.wav", stereo=True)
    # write_wav(mix(synth, water, 0.3), "synth_water_mixed_stereo.wav")

    print(mix({"rate": 5, "samples": [1, 2, 3, 4, 5]}, {
        "rate": 5, "samples": [2, 3, 4, 5, 6]}, 0.3))
