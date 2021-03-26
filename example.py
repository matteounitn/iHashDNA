from .ihashdna import ihashdna as Idna

idna = Idna("redis://localhost:6379/1")  # set your redis link here

idna.ban_image("/path/to/your/img.png.jpg.whatever")
# this will take some time if the img is big, consider downscaling the sample
print(idna.do_hash_check("/path/to/your/img.png.jpg.whatever"))  # True, it's the same image
print(idna.do_hash_check(
    "/path/to/your/SIMILAR_IMAGE.jpg"))  # True if you set correctly the single threshhold of the PHASH or general bias

idna.unban_image("/path/to/your/img.png.jpg.whatever")
print(idna.do_hash_check("/path/to/your/img.png.jpg.whatever"))  # False, it's the same image
print(idna.do_hash_check(
    "/path/to/your/SIMILAR_IMAGE.jpg"))  # False

print(idna.do_hash_check(
    "/path/to/your/SIMILAR_IMAGE.jpg",
    bounces=1))  # LEARN: if this image is similar with distance 1 (similar to the original), learn and blacklist it.

print(idna.do_hash_check(
    "/path/to/your/SIMILAR_IMAGE.jpg",
    bounces=2))  # LEARN: if this image is similar with distance 2 (similar to the similar to the original),
# learn and blacklist it.
idna.unban_image("/path/to/your/img.png.jpg.whatever")  # WILL remove also the 2 bounces!
