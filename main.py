import sys
import os
import re
import requests

sub_output = set()
dir_output = set()
file_output = set()

def check_inner_content(html):
    global dir_output
    html = str(html)

    found_links = re.findall(r"(?<=href=\")([^\"]+)|(?<=src=\")([^\"]+)|(?<=url\()[^\)]+)", html)

    for sub in found_links:
        for l in sub:
            dir_output.add(l)
            print("Added directory: ", l)

def main():
    global sub_output 
    global dir_output 
    global file_output

    args = sys.argv[1:]

    if(len(args) != 1):
        print("Error: Usage => python main.py <target_url>")
        sys.exit(1)

    target_url = args[0]

    print("Target url = ", target_url)

    try:
        requests.get(target_url)
    except Exception as e:
        print("Invalid Url. Use a valid URL to enumerate")
        sys.exit(1)
    
    if "input_files" not in os.listdir("."):
        print("Please provide input_files directory with the correcsponding files")
        sys.exit(1)
    
    subdomains = open("./input_files/subdomains_dictionary.bat", "r").read().splitlines()
    directories = open("./input_files/dirs_dictionary.bat", "r").read().splitlines()


    for sub in subdomains:
        if "https" in target_url:
            sub_target = "https://"+sub+"."+target_url[8:]
        else: sub_target = "http://"+sub+"."+target_url[7:]

        try:
            print("Checking subdomain: ", sub_target)
            req = requests.get(sub_target)
            if req.status == 200 and "404" not in req.text:
                print("Added subdomain: ", sub_target)
                sub_output.add(sub_target)

                check_inner_content(req.txt)
        except Exception as e:
            pass
    for dire in directories:
        if "https" in target_url:
            dir_target = "https://"+target_url[8:]+"/"+dire
        else: dir_target = "http://"+target_url[7:]+"/"+dire

        try:
            print("Checking directory: ", dir_target)
            req = requests.get(dir_target)
            if req.status == 200 and "404" not in req.text:

                if "." in dire:
                    print("Added file: ", dir_target)
                    file_output.add(dir_target)
                
                else:

                    print("Added directory: ", dir_target)
                    dir_output.add(dir_target)
        except Exception as e:
            pass
    
    if "output_directory" not in os.listdir("."):
        os.mkdir("output_directory")
    
    with open("./output_directory/subdomain_output.bat", "w") as f:
        for sub in sub_output:
            f.write(sub)
    with open("./output_directory/directory_output.bat", "w") as f:
        for dir in dir_output:
            f.write(dir)
    with open("./output_directory/files_output.bat", "w") as f:
        for x in file_output:
            f.write(x)
if __name__ == "__main__":
    main()