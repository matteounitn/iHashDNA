# iHashDNA
Perceptual hashing library in python (with redis), a wannabe [PhotoDNA](https://en.wikipedia.org/wiki/PhotoDNA)

It uses [phash](https://en.wikipedia.org/wiki/Perceptual_hashing) and [whash](https://fullstackml.com/wavelet-image-hash-in-python-3504fdd282b5?gi=667775a177e2) by checking initially phash, then whash.

By combining these two with a db (redis), you get this library.



You can:

1. **Ban images**: Add the hash of the image to the DB (and checks if already in it). 
   This includes rotations (90 degrees left right 180 up down) of the pictures.
2. **Unban images**: Remove the hash and all the similar hashes from DB;
3. **Whitelist images**: Ignore a picture hash.

---

### Practical examples

Perceptual hashing is a good way to recognize two similar images. If you need to:

* Fast indexing similar images;
* Check for prohibited content without saving it into your DB (child pornography, pornography, porn, gore...);
* Check for watermarked original copyrighted content.

and more...



The library can easily detect an edited photo if it has:

* Color changes;
* Random garbage over it (watermarks, stickers....);
* slight cropping.



### Issues and limitations

Remember that this is not ML-Based. 

It can be easily bypassed by cropping the image. 

This library is a wannabe [PhotoDNA](https://en.wikipedia.org/wiki/PhotoDNA)

## How to use it

### Requirements

1. Install redis

2. Start redis

3. `git clone https://github.com/matteounitn/ihashdna.git`

4. (Optional) create a venv:

   `python3 -m venv venv && source venv/bin/activate`

5. `pip3 install -r requirements.txt`

Then you are good to go!

### Example

Checkout [this example](example.py).