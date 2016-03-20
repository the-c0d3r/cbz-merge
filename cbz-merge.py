# -*- coding: utf8 -*-
#!/usr/bin/env python
import os
import zipfile
import sys
import logging
import argparse
import shutil
import PIL.Image

class Comic:
    def __init__(self):
        print("CBZ merge\n----------\n")
        if 'nux' in sys.platform:
            self.seperator = "/"
        else:
            self.seperator = "\\"

        self.image_counter = 1 # A counter for renaming JPG files

        self._parseArg()
        self.temp_dir = self.join_path(self.parent_dir,"temp")
        # Creates a temp directory with the name Temp under the comic directory
        # To rename images, and not to mix up with the images already renamed
        self.output_dir = self.join_path(self.parent_dir,os.path.basename(self.parent_dir))
        # Creates an output directory with the same name with parent directory
        # The purpose is to keep all the images here before zipping up
        logging.info("[+] Temp Dir : {}".format(self.temp_dir))
        logging.info("[+] Output Dir : {}".format(self.output_dir))

        self.create_dir(self.temp_dir)
        self.create_dir(self.output_dir)
        # Creates both directories

        self.cbz_files = self.get_cbz_files()
        # Get a list of cbz files


        for cbz in self.cbz_files:
            sys.stdout.write("[+] Extracting : "+cbz+"\r")
            sys.stdout.flush()
            self.extract_cbz(self.join_path(self.parent_dir,cbz))
            # Extracts the cbz content to the temp directory
            self.move_image(self.get_image_files(self.temp_dir))
            # renames the images inside the temporary directory
            # And move them to the output directory

        self.create_cbz()
        # Creates the CBZ with the content of output directory, which is sorted
        # and renamed sequentially, the output file name is the same as 
        # parent directory + ".cbz" will be created under the current directory
        # which means outside the parent_dir
        self.clean_up()
        # Clean up the temp dir and the output dir
        print("\n[+] File Name : ",self.filename)
        print("[+] File Size : ",self.convsize(self.filename))
        print("[+] Directory : ",os.path.abspath("."))
        
    def _parseArg(self):
        parser = argparse.ArgumentParser(description="Combine multiple CBZ to one file")
        parser.add_argument("-d","--directory",help="Directory containing CBZ")
        parser.add_argument("-v","--verbose",help="Enable Verbose Mode",action="store_true")

        args = parser.parse_args()
        if args.verbose:
            logging.basicConfig(format="[%(asctime)s] %(levelname)s: %(message)s", level=logging.DEBUG,datefmt='%H:%M:%S')
            logging.info("Verbose mode activated")
        
        if args.directory == None:
            self.parent_dir = self.join_path(os.getcwd(),input("[?] Enter Directory : "))
            self.check_dir(self.parent_dir)
        elif args.directory:
            if self.seperator in args.directory:
                self.parent_dir = args.directory
                self.check_dir(self.parent_dir)
            else:
                self.parent_dir = self.join_path(os.getcwd(),args.directory)
                self.check_dir(self.parent_dir)


    def join_path(self,*args):
        return self.seperator.join([arg for arg in args])

    def create_dir(self,dir):
        try:
            os.mkdir(dir)
        except FileExistsError:
            logging.info("[-] {} folder already exist".format(os.path.basename(dir)))
            pass

    def check_dir(self,dir):
        if os.path.isdir(dir):
            print("[+] Parent Directory :",self.parent_dir)
        else:
            print("[-] {} did not exist".format(dir))
            exit()

    def get_cbz_files(self):
        getkey = lambda name: float(os.path.basename(os.path.splitext(name)[0])[name.rfind("_c")+2:])
        files = [f for f in os.listdir(self.parent_dir) if f.lower().endswith("cbz")]
        files.sort(key=getkey)
        if len(files) == 0:
            print("[-] No cbz files under [{}]".format(os.path.basename(self.parent_dir)))
        else:
            print("[+] {} cbz files detected".format(len(files)))
            return files

    def get_image_files(self,dir):
        getkey = lambda name: float(os.path.basename(os.path.splitext(name)[0])[name.rfind("_p")+2:])
        files = [f for f in os.listdir(dir) if f.lower().endswith(".jpg") or f.lower.endswith(".png")]
        files.sort(key=getkey)
        logging.info("{} : {} files".format(dir,len(files)))
        return files


    def list_image(self,dir):
        files = [f for f in os.listdir(dir) if f.lower().endswith(".jpg") or f.lower.endswith(".png")]
        files.sort(key=lambda name: int(os.path.basename(os.path.splitext(name)[0])))
        return files

    def extract_cbz(self,cbzfile):
        logging.info(cbzfile)
        with zipfile.ZipFile(cbzfile,"r") as cbz:
            cbz.extractall(self.temp_dir)
        self.verify_jpg(self.get_image_files(self.temp_dir))

    def verify_jpg(self,files):
        for jpg in files:
            try:
                fname = self.join_path(self.temp_dir,jpg)
                im = PIL.Image.open(fname)
                im.verify()
            except Exception as e:
                logging.debug(str(e)+jpg)
                print("[!] File {} is corrupted".format(jpg))
                os.remove(self.join_path(self.temp_dir,jpg))

    def move_image(self,files):
        logging.info("Renaming files to a sequence from temp dir")        

        for i in files:
            filename = str(self.image_counter) + ".jpg"
            oldfile = self.join_path(self.temp_dir,i)
            newfile = self.join_path(self.temp_dir,filename)
            os.rename(oldfile,newfile)
            self.image_counter += 1
        
        logging.info("Moving files to output directory")

        for i in self.list_image(self.temp_dir):
            oldpath = self.join_path(self.temp_dir,i)
            newpath = self.join_path(self.output_dir,i)
            os.rename(oldpath,newpath)
        logging.info("Moved the files to output directory")

    def create_cbz(self):
        print("\n[+] Creating cbz file")
        self.filename = os.path.basename(self.parent_dir)+".cbz"
        cbz = zipfile.ZipFile(self.filename,mode="w")

        filelist = self.list_image(self.output_dir)

        for i in filelist:
            filename = self.join_path(self.output_dir,i)
            cbz.write(filename)
            sys.stdout.write("[+] Writing "+i+"\r")

        cbz.close()
        print("\n[+] {} Written to disk".format(self.filename))

    def clean_up(self):
        print("[+] Cleaning up")
        shutil.rmtree(self.temp_dir)
        shutil.rmtree(self.output_dir)

    def convsize(self,filename):
        """
        This module's purpose is to convert the file size that
        is in Bytes to suitable human readable file size such as
        2 KB instead of 2324 bytes
        2.5 MB instead of 25235436 bytes
        """
        filesize = (os.path.getsize(filename) / (1024.0))
        if len(str(filesize)[:str(filesize).index('.')]) >= 3:
            # if the filesize has 3 or more digits on the left of the decimal place
            # it means it could be converted to MegaBytes
            return "%.2f MB" % (int(filesize) / 1024.0)
        else:
            return "%.2f KB" % (filesize)

if __name__ == "__main__":
    app = Comic()