# iHashDNA
Perceptual hashing library in python (with redis), a wannabe [PhotoDNA](https://en.wikipedia.org/wiki/PhotoDNA)

## What is Perceptual Hashing

> **Perceptual hashing** is the use of an [algorithm](https://en.wikipedia.org/wiki/Algorithm) that produces a snippet or [fingerprint](https://en.wikipedia.org/wiki/Fingerprint_(computing)) of various forms of [multimedia](https://en.wikipedia.org/wiki/Multimedia).[[1\]](https://en.wikipedia.org/wiki/Perceptual_hashing#cite_note-1)[[2\]](https://en.wikipedia.org/wiki/Perceptual_hashing#cite_note-2) Perceptual [hash functions](https://en.wikipedia.org/wiki/Hash_function) are analogous if [features](https://en.wikipedia.org/wiki/Feature_vector) of the multimedia are similar, whereas [cryptographic hashing](https://en.wikipedia.org/wiki/Cryptographic_hash_function) relies on the [avalanche effect](https://en.wikipedia.org/wiki/Avalanche_effect) of a small change in input value creating a drastic change in output value. Perceptual hash functions are widely used in finding cases of online [copyright infringement](https://en.wikipedia.org/wiki/Copyright_infringement) as well as in [digital forensics](https://en.wikipedia.org/wiki/Digital_forensics) because of the ability to have a correlation between hashes so similar data can be found (for instance with a differing [watermark](https://en.wikipedia.org/wiki/Digital_watermark)). Based on research at [Northumbria University](https://en.wikipedia.org/wiki/Northumbria_University),[[3\]](https://en.wikipedia.org/wiki/Perceptual_hashing#cite_note-3) it can also be applied to simultaneously identify similar contents for [video copy detection](https://en.wikipedia.org/wiki/Video_copy_detection) and detect malicious manipulations for video authentication. The system proposed performs better than current video hashing techniques in terms of both identification and authentication.
>
> [Wikipedia, Perceptual Hashing](https://en.wikipedia.org/wiki/Perceptual_hashing)

## TLDR: How Perceptual Hashing works

![Why we created 'Imageid' and saved 47% of the moderation effort | by Diego  Essaya | Taringa! | Medium](README.assets/0*zfY4Co3OIXnuJ-96.)

> Pic Source: [Why we created 'Imageid' and saved 47% of the moderation effort | by Diego  Essaya | Taringa! | Medium](https://medium.com/taringa-on-publishing/why-we-built-imageid-and-saved-47-of-the-moderation-effort-b7afb69d068e)

*Perceptual hashing converts an image, by degrading it and turning it into "pixels", into a binary (or hexadecimal) sequence. **Unlike cryptographic hashing**, perceptual hashing **lacks of [avalanche effect](https://en.wikipedia.org/wiki/Avalanche_effect)**, making any change in the image easily perceivable in the hash.*

## What iHashDNA does

It uses [phash](https://en.wikipedia.org/wiki/Perceptual_hashing) and [whash](https://fullstackml.com/wavelet-image-hash-in-python-3504fdd282b5?gi=667775a177e2) by checking initially phash, then whash.

By combining these two with a db (redis), you get this library.

You can:

1. **Ban images**: Add the hash of the image to the DB (and checks if already in it). 
   This includes rotations (90 degrees left right 180 up down) of the pictures.
2. **Unban images**: Remove the hash and all the similar hashes from DB;
3. **Whitelist images**: Ignore a picture hash.

### Practical examples

Perceptual hashing is a good way to recognize *two similar images*. If you need to:

* *Fast indexing similar images;*
* *Check for prohibited content without saving it into your DB (child pornography, pornography, porn, gore...);*
* *Check for watermarked original copyrighted content.*

and **more...**

The library can **easily detect an edited photo** if it has:

* *Color changes;*
* *Random garbage over it (watermarks, stickers....);*
* *slight cropping.*

### Issues and limitations

Remember that <u>this is not ML-Based.</u> 

It can be easily bypassed by cropping the image. 

This library is a wannabe [PhotoDNA](https://en.wikipedia.org/wiki/PhotoDNA).

## How to use it

### Requirements

1. Install redis

2. Start redis

3. `git clone https://github.com/matteounitn/iHashDNA.git`

4. cd into folder

5. (Optional) create a venv:

   `python3 -m venv venv && source venv/bin/activate`

6. `pip3 install -r requirements.txt`

Then you are good to go!

### Example

Checkout [this example](example.py).
