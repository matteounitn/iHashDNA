from PIL import Image
import imagehash as im
from pottery import RedisDict, Redlock
from redis import Redis
import numpy as np


class imagehash:
    def __init__(self, redis_url):
        self.redis = Redis.from_url(redis_url)
        self.phashdb = RedisDict(redis=self.redis, key='phashdb')  # blacklist
        self.whashdb = RedisDict(redis=self.redis, key='whashdb')  # blacklist
        self.phashdb_clean = RedisDict(redis=self.redis, key='phashdb_clean')  # whitelist
        self.whashdb_clean = RedisDict(redis=self.redis, key='whashdb_clean')  # whitelist

    # chiamata effettiva da fare
    def do_hash_check(self, path: str, bias=0.0, limit=30, whash_treshold=8, phash_threshold=16, bounces=None):
        img = Image.open(path)
        # print(f"[detection]: phash {phash} - whash {whash}")
        phash_check, phash_value = self.check_hash(im.phash(img), True, bias,
                                                   threshold=phash_threshold, bounces=bounces)  # controllo il phash
        if not phash_check:  # se è false
            if 0 <= phash_value <= limit:  # controlla quanto era sotto il limite
                whash_check, whash_value = self.check_hash(im.whash(img), False, bias=bias,
                                                           threshold=whash_treshold, bounces=bounces)
                return whash_check  # ritorna whash_check
            else:
                whash_check, whash_value = self.check_hash(im.whash(img), False, bias=bias,
                                                           threshold=int(whash_treshold / 2), bounces=bounces)
                return whash_check
        else:
            return True

    # ------------------------------------------
    # wrapper method if change of db
    def set_in_db(self, whichdb, key, value, lock=None):
        if lock is not None:
            with lock:
                whichdb[key] = value
        else:
            whichdb[key] = value

    # wrapper method if change of db
    def get_from_db(self, whichdb, key, lock=None):
        if lock is not None:
            with lock:
                return whichdb[key]
        else:
            return whichdb[key]

    # wrapper method if change of db
    def get_keys_from_db(self, whichdb, lock=None):
        if lock is not None:
            with lock:
                return whichdb.keys()
        else:
            return whichdb.keys()

    # wrapper of query select
    def is_in_db(self, whichdb, key, lock=None):
        if lock is not None:
            with lock:
                return key in whichdb
        else:
            return key in whichdb

    # wrapper of del query
    def del_from_db(self, whichdb, key, lock=None):
        if lock is not None:
            with lock:
                del whichdb[key]
        else:
            del whichdb[key]

    # ------------------------------------------

    def ban_image(self, path):
        img = Image.open(path)
        lock_phash_clean = Redlock(key=f'phashdb_clean', masters={self.redis})
        lock_whash_clean = Redlock(key=f'whashdb_clean', masters={self.redis})
        lock_phash = Redlock(key=f'phashdb', masters={self.redis})
        lock_whash = Redlock(key=f'whashdb', masters={self.redis})
        raw_phash = im.phash(img)
        raw_whash = im.whash(img)
        phash = str(raw_phash)
        whash = str(raw_whash)
        self.set_in_db(self.phashdb, phash, 0, lock=lock_phash)
        self.set_in_db(self.whashdb, whash, 0, lock=lock_whash)
        self.exec_similar_hash(self.phashdb_clean, raw_phash, 0, 13, self.del_from_db,
                               lock=lock_phash_clean)  # removing duplicates from the clean phash, if any
        self.exec_similar_hash(self.whashdb_clean, raw_whash, 0, 13, self.del_from_db,
                               lock=lock_whash_clean)  # removing duplicates from the clean whash, if any

    def unban_image(self, path):
        img = Image.open(path)
        lock_phash = Redlock(key=f'phashdb', masters={self.redis})
        lock_whash = Redlock(key=f'whashdb', masters={self.redis})
        raw_phash = im.phash(img)
        raw_whash = im.whash(img)
        self.exec_similar_hash(self.phashdb, raw_phash, 0, 13, self.del_from_db, lock=lock_phash)
        self.exec_similar_hash(self.whashdb, raw_whash, 0, 13, self.del_from_db, lock=lock_whash)

    def whitelist_image(self, path):
        img = Image.open(path)
        lock_phash_clean = Redlock(key=f'phashdb_clean', masters={self.redis})
        lock_whash_clean = Redlock(key=f'whashdb_clean', masters={self.redis})
        self.set_in_db(self.phashdb_clean, str(im.phash(img)), True, lock=lock_phash_clean)
        self.set_in_db(self.whashdb_clean, str(im.whash(img)), True, lock=lock_whash_clean)

    def calc_rotation(self, image: im.ImageHash) -> im.ImageHash:
        return im.ImageHash(np.array(list(zip(*image.hash[::-1]))))

    def get_rotations(self, raw: im.ImageHash) -> list:
        rotations = [raw]
        for i in range(0, 3):
            rotations.append(self.calc_rotation(rotations[i]))
        return rotations

    def calculate_hashes(self, path):
        img = Image.open(path)
        phash = im.phash(img)
        rotations = self.get_rotations(phash)
        toreturn = ['phash of img']
        toreturn.append("\n".join([f"{value}" for value in rotations]))
        whash = im.whash(img)
        rotations = self.get_rotations(whash)
        toreturn.append('whash of img')
        toreturn.append("\n".join([f"{value}" for value in rotations]))
        return "\n".join(toreturn)

    def debug(self, path):
        img = Image.open(path)
        lock_phash = Redlock(key=f'phashdb', masters={self.redis})
        lock_whash = Redlock(key=f'whashdb', masters={self.redis})
        raw_phash = im.phash(img)
        raw_whash = im.whash(img)
        toreturn = [self.calculate_hashes(path)]
        toreturn.append("phashdb")
        print("phashdb")
        toreturn.append(self.debug_similar_hash(self.phashdb, raw_phash, 13, lock=lock_phash))
        print("whashdb")
        toreturn.append("whashdb")
        toreturn.append(self.debug_similar_hash(self.whashdb, raw_whash, 13, lock=lock_whash))
        return "\n".join(toreturn)

    def debug_similar_hash(self, redisdb, raw, threshold, lock=None, rotations=True):
        toreturn = []
        if rotations:
            to_check = self.get_rotations(raw)  # if i want rotation, precompute them
        else:
            to_check = [raw]  # else set the default one
        for key in self.get_keys_from_db(redisdb,
                                         lock=lock):  # check if key. Using SQL it's probabily better
            for raw in to_check:
                value = round(((im.hex_to_hash(key) - raw) / len(raw.hash) ** 2) * 100, 2)  # compute value
                if value <= threshold:
                    toreturn.append(f"[{raw} - {key}] {value}")
                print(f"[{raw} - {key}] {value}")
            toreturn.append("NEXT")
            print("---------------")
        return "\n".join(toreturn)

    def exec_similar_hash(self, redisdb, raw, bias, threshold, execute, lock=None, rotations=True):
        if rotations:
            to_check = self.get_rotations(raw)  # if i want rotation, precompute them
        else:
            to_check = [raw]  # else set the default one
        for key in self.get_keys_from_db(redisdb,
                                         lock=lock):  # check if key. Using SQL it's probabily better
            for raw in to_check:
                value = round(((im.hex_to_hash(key) - raw) / len(raw.hash) ** 2) * 100, 2)  # compute value
                if (value + bias) <= threshold:  # check if less than threshold (+ bias if any)
                    execute(redisdb, key, lock=lock)  # exec on key

    def calc_similar_hash(self, redisdb, raw, raw_str, bias, threshold, bounces=None, lock=None, rotations=True):
        minimum = 1000
        if rotations:
            to_check = self.get_rotations(raw)  # if i want rotation, precompute them
        else:
            to_check = [raw]  # else set the default one
        for key in self.get_keys_from_db(redisdb,
                                         lock=lock):  # check if key. Using SQL it's probabily better
            for raw in to_check:
                value = round(((im.hex_to_hash(key) - raw) / len(raw.hash) ** 2) * 100, 2)  # compute value
                minimum = min(value, minimum)
                if (value + bias) <= threshold:  # check if less than threshold (+ bias if any)
                    if bounces is not None:  # if i set bounces
                        numero = self.get_from_db(redisdb, key, lock=lock)  # get number of jumps
                        if numero <= bounces:  # if it's in the limit
                            self.set_in_db(redisdb, raw_str, numero + 1, lock=lock)  # add with jump+1
                    return True, value  # if found
        return False, minimum  # didn't find

    def check_hash(self, raw, phash: bool, bias=0.0, threshold=13, bounces=None):
        raw_str = str(raw)
        minimum = 1000
        if phash:  # which hash? True phash, false whash
            redisdb = self.phashdb
            redisdb_clean = self.phashdb_clean
            # locks for redis concurrency
            lock = Redlock(key=f'phashdb', masters={self.redis})
            lock_clean = Redlock(key=f'phashdb_clean', masters={self.redis})
            # end of locks
        else:
            redisdb = self.whashdb
            redisdb_clean = self.whashdb_clean
            # locks for redis concurrency
            lock = Redlock(key=f'whashdb', masters={self.redis})
            lock_clean = Redlock(key=f'whashdb_clean', masters={self.redis})
            # end of locks
        if self.is_in_db(redisdb_clean, raw_str, lock=lock_clean):  # if i've processed it, it's not banned
            return False, -2
        elif self.is_in_db(redisdb, raw_str, lock=lock):  # if found
            return True, -2
        else:  # checks for similar hashes
            result, value = self.calc_similar_hash(redisdb, raw, raw_str, bias, threshold, bounces, lock=lock)
            minimum = min(minimum, value)
            if result:
                return result, value  # if it's in the db
            else:
                self.set_in_db(redisdb_clean, raw_str, True, lock=lock_clean)  # set as safe
                return False, minimum  # if it's nott
