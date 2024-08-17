import cryptography
import sys, argparse
import os.path
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import cryptography.fernet, struct 
import time
import hashlib
import datetime

##########
# Asymetric file encrypt
# Encrypt given file [-i] using provided public key [-k] and save result to a specified location [-o]
# Inspinet.co.uk @2023 v.0.3
##########

k_sizes = { 1024: 62, 2048: 190, 4096: 446, 8192: 958 }

def check_file_exists(str_filename):
    if not os.path.isfile(str_filename):
        sys.exit(str("ERROR: " + str(str_filename) + " file not found"))
    return str_filename

def convert_bytes(bytes_size):
    if bytes_size < 1024:
        return str(str(bytes_size) + " b")
    elif bytes_size < 1024*1024:
        return str(str(round(bytes_size/1024,2)) + " Kb")
    elif bytes_size < 1024*1024*1024:
        return str(str(round(bytes_size/(1024*1024),2)) + " Mb")
    else:
        return str(str(round(bytes_size/(1024*1024*1024),2)) + " Gb")

def convert_seconds(seconds):
    if seconds<60:
        return str(str(round(seconds,3)) + " s")
    elif seconds<60*60:
        return str(str(round(seconds/60,3)) + " min")
    else:
        return str(str(round(seconds/(60*60),3)) + " hours")
    
def encrypt_chunk(chunk, public_key):
    return public_key.encrypt(
        chunk,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def encrypt(public_key, fin, fout, debug_output = "none"):
    block = k_sizes[public_key.key_size]
    start = time.time()
    if debug_output =="full":
        print("Start encrypting (" + str(fin) + " -> " + str(fout) + ") ...")
    hasher = hashlib.md5()
    with open(fin, 'rb') as f:
        tmp_content = f.read()
        total_size = len(tmp_content) #read total size of file
    hasher.update(tmp_content)
    if debug_output == "full":
        print("\t" + str(fin) + " - " + str(total_size) + " bytes (" + convert_bytes(total_size) + ") - MD5 Hash: " + hasher.hexdigest() + "              ") 
    total_chunk = 0
    hasher = hashlib.md5()
    start = time.time()
    startETA = time.time()
    start_chunk = 0
    avg_speed = "calculate"
    ETA1 = "calculate"
    ETA2 = time.time()
    progress = ""
    with open(fin, 'rb') as fi, open(fout, 'wb') as fo:
        while True:
            chunk = fi.read(block)
            if len(chunk) == 0:
                break
            total_chunk += len(chunk)
            if (time.time() - startETA > 2):
                progress = "["
                chunk_processed = total_chunk - start_chunk
                avg_speed = str( round( (total_size / total_chunk) * (60 / (time.time() - startETA)) / (1024 ),3) ) + " kB/min"
                progress += avg_speed + " | "
                progress += str( round(total_chunk / 1024 ,2)) + "kB / " + str(round(total_size/1024,0)) + "kB | "
                ETA1 = (total_size / total_chunk) * (time.time() - startETA)
                ETA2 = datetime.datetime.now()
                time_change = datetime.timedelta(seconds=ETA1)
                ETA2 = ETA2 + time_change
                progress += "ETA: " + str(ETA2) + "]"
                start_chunk = total_chunk
                startETA = time.time()

            #print("\t" + str(fout) + " ... (encrypting " + str( round( total_chunk / total_size * 100,2) )  + "%) " + progress + "              ", end="\r", flush=True)
            print("\t\t(encrypting " + str( round( total_chunk / total_size * 100,0) )  + "%) " + progress + "              ", end="\r", flush=True)
            #enc = fernet.encrypt(chunk)
            enc = encrypt_chunk(chunk, public_key)
            fo.write(struct.pack('<I', len(enc)))
            fo.write(enc)
            hasher.update(enc)
            if len(chunk) < block:
                break
    with open(fout, 'rb') as f:
        total_size = len(f.read()) #read total size of file
    if debug_output == "full":
        print("\t" + str(fout) + " - " + str(total_size) + " bytes (" + convert_bytes(total_size) + ") - MD5 Hash: " + hasher.hexdigest() + "              ")
    finish = time.time()
    print("\tcompleted in ",round(finish-start,2),"s (" + convert_seconds(finish-start) + ")")


if __name__ == "__main__":
    argParser = argparse.ArgumentParser(
        prog='Asymetric file encrypt',
        description='Encrypt given file [-i] using provided public key [-k] and save result to a specified location [-o]',
        epilog='Inspinet.co.uk @2023 v.0.3')
    argParser.add_argument("-i", "--in_file", required=True, help="input file to encrypt, file name or path with file name")
    argParser.add_argument("-o", "--out_file", required=True, help="output file after enrypt, file name or path with file name")
    argParser.add_argument("-k", "--public_key", required=True, help="public key used to encrypt, (.PEM format), file name or path with file name")

    args = argParser.parse_args()
    # print(args)
    # print(args.in_file, args.out_file, args.public_key)
    file_in = check_file_exists(args.in_file)
    file_out = args.out_file
    file_public_key = check_file_exists(args.public_key)

    ##### read public/private file #####
    try:
        print("Loading public key... ", end="")
        with open(file_public_key, "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
        )
        print("complete")
    except Exception as err:
        print("Unexpected ", err, " ", type(err))
        sys.exit(str("ERROR: " + str(file_public_key) + " - problem with public key"))

    if public_key.key_size not in k_sizes:
        sys.exit(str("ERROR: " + str(public_key.key_size) + " bits keys are not supported (min 1024 bits required)"))

    try:
        encrypt(public_key, file_in, file_out)
        print("Encrypted")
    except Exception as err:
        print("Failed - " + str(err) + str(type(err)))
    
    