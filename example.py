from .ihash import imagehash as Imh

imh = Imh("redis://localhost:6379/1")  # set your redis link here

imh.ban_image("/path/to/your/img.png.jpg.whatever")
# this will take some time if the img is big, consider downscaling the sample
print(imh.do_hash_check("/path/to/your/img.png.jpg.whatever"))  # True, it's the same image
print(imh.do_hash_check(
    "/path/to/your/SIMILAR_IMAGE.jpg"))  # True if you set correctly the single threshhold of the PHASH or general bias

imh.unban_image("/path/to/your/img.png.jpg.whatever")
print(imh.do_hash_check("/path/to/your/img.png.jpg.whatever"))  # False, it's the same image
print(imh.do_hash_check(
    "/path/to/your/SIMILAR_IMAGE.jpg"))  # False

print(imh.do_hash_check(
    "/path/to/your/SIMILAR_IMAGE.jpg",
    bounces=1))  # LEARN: if this image is similar with distance 1 (similar to the original), learn and blacklist it.

print(imh.do_hash_check(
    "/path/to/your/SIMILAR_IMAGE.jpg",
    bounces=2))  # LEARN: if this image is similar with distance 2 (similar to the similar to the original),
# learn and blacklist it.
imh.unban_image("/path/to/your/img.png.jpg.whatever")  # WILL remove also the 2 bounces!
