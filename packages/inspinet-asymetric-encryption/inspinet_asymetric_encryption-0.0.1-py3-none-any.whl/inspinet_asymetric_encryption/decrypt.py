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
# Asymetric file decrypt
# Decrypt given file [-i] using provided private key [-k] and save result to a specified location [-o]
# Inspinet.co.uk @2023 v.0.1 -
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

def encrypt(public_key, fin, fout):
    block = k_sizes[public_key.key_size]
    start = time.time()
    print("Start encrypting (" + str(fin) + " -> " + str(fout) + ") ...")
    hasher = hashlib.md5()
    with open(fin, 'rb') as f:
        tmp_content = f.read()
        total_size = len(tmp_content) #read total size of file
    hasher.update(tmp_content)
    print("\t" + str(fin) + " - " + str(total_size) + " bytes (" + convert_bytes(total_size) + ") - MD5 Hash: " + hasher.hexdigest() + "              ") 
    total_chunk = 0
    hasher = hashlib.md5()
    with open(fin, 'rb') as fi, open(fout, 'wb') as fo:
        while True:
            chunk = fi.read(block)
            if len(chunk) == 0:
                break
            total_chunk += len(chunk)
            print("\t" + str(fout) + " ... (encrypting " + str( round( total_chunk / total_size * 100,2) )  + "%)         ", end="\r", flush=True)
            #enc = fernet.encrypt(chunk)
            enc = encrypt_chunk(chunk, public_key)
            fo.write(struct.pack('<I', len(enc)))
            fo.write(enc)
            hasher.update(enc)
            if len(chunk) < block:
                break
    with open(fout, 'rb') as f:
        total_size = len(f.read()) #read total size of file
    print("\t" + str(fout) + " - " + str(total_size) + " bytes (" + convert_bytes(total_size) + ") - MD5 Hash: " + hasher.hexdigest() + "              ")
    finish = time.time()
    print("\tcompleted in ",round(finish-start,2),"s (" + convert_seconds(finish-start) + ")")



## decrypt section STARt


def decrypt_chunk(chunk, private_key):
    return private_key.decrypt(
        chunk,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decrypt(private_key, fin, fout):
    #if private_key.key_size<=1024: block = 4
    #import cryptography.fernet, struct
    #fernet = cryptography.fernet.Fernet(key)
    start = time.time()
    startETA = time.time()
    start_chunk = 0
    avg_speed = "calculate"
    ETA1 = "calculate"
    ETA2 = time.time()
    progress = ""
    print("Start decrypting (" + str(fin) + " -> " + str(fout) + ") ...")
    with open(fin, 'rb') as f:
        total_size = len(f.read()) #read total size of file
    print("\t" + str(fin) + " - " + str(total_size) + " bytes (" + convert_bytes(total_size) + ")") 
    total_chunk = 0
    with open(fin, 'rb') as fi, open(fout, 'wb') as fo:
        while True:
            size_data = fi.read(4)
            if len(size_data) == 0:
                break
            total_chunk += len(size_data)
            if (time.time() - startETA > 5):
                progress = "["
                chunk_processed = total_chunk - start_chunk
                avg_speed = str( round( (total_size / total_chunk) * (60 / (time.time() - startETA)) / (1024 * 1024),3) ) + " MB/min"
                progress += avg_speed + " | "
                progress += str( round(total_chunk / 1024 / 1024,2)) + "MB / " + str(round(total_size/1024/1024,2)) + "MB | "
                ETA1 = (total_size / total_chunk) * (time.time() - startETA)
                ETA2 = datetime.datetime.now()
                time_change = datetime.timedelta(seconds=ETA1)
                ETA2 = ETA2 + time_change
                progress += "ETA: " + str(ETA2) + "]"
                start_chunk = total_chunk
                startETA = time.time()

            print("\t" + str(fout) + " ... (decrypting " + str( round( total_chunk / total_size * 100,2) )  + "%) " + progress + "              ", end="\r", flush=True)
            chunk = fi.read(struct.unpack('<I', size_data)[0])
            #dec = fernet.decrypt(chunk)
            dec = decrypt_chunk(chunk, private_key)
            fo.write(dec)
    with open(fout, 'rb') as f:
        total_size = len(f.read()) #read total size of file

    print("\t" + str(fout) + " - " + str(total_size) + " bytes (" + convert_bytes(total_size) + ")                 ")
    finish = time.time()
    print("\tcompleted in ",round(finish-start,2),"s (" + convert_seconds(finish-start) + ")")


## decrypt section end

if __name__ == "__main__":
    argParser = argparse.ArgumentParser(
        prog='Asymetric file decrypt',
        description='Decrypt given file [-i] using provided private key [-k] and save result to a specified location [-o]',
        epilog='Inspinet.co.uk @2023 v.0.1')
    argParser.add_argument("-i", "--in_file", required=True, help="input file to encrypt, file name or path with file name")
    argParser.add_argument("-o", "--out_file", required=True, help="output file after enrypt, file name or path with file name")
    argParser.add_argument("-k", "--private_key", required=True, help="private key used to decrypt, (.PEM format), file name or path with file name")

    args = argParser.parse_args()
    # print(args)
    # print(args.in_file, args.out_file, args.public_key)
    file_in = check_file_exists(args.in_file)
    file_out = args.out_file
    file_private_key = check_file_exists(args.private_key)

    ##### read public/private file #####
    try:
        print("Loading private key... ", end="")
        with open(file_private_key, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
        )
        print("complete")
    except Exception as err:
        print("Unexpected ", err, " ", type(err))
        sys.exit(str("ERROR: " + str(file_private_key) + " - problem with public key"))

    if private_key.key_size not in k_sizes:
        sys.exit(str("ERROR: " + str(private_key.key_size) + " bits keys are not supported (min 1024 bits required)"))
    
    try:
        decrypt(private_key, file_in, str(file_out))
        print("Decrypted")
    except Exception as err:
        print("Failed - " + str(err) + str(type(err)))
    
    