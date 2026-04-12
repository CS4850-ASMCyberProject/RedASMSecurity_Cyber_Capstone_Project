from terminal_run import run_cmd

import json

def expose_url_paths(subdomain):

    WORDLIST = r"/srv/asm_project/subdomains-top1million-5000.txt"

    results = []

    try:

        run_cmd("Fuff URL Paths Scan", f"ffuf -s -u https://{subdomain}/FUZZ -w {WORDLIST} -mc 500 -of json -o ffuf_output.txt")

        

        with open("ffuf_output.txt", "r") as f:

            data = json.load(f)

            

            for input in data["results"]:

                subdomain = input["host"]

                url_path = input["input"]["FUZZ"]

                status = input["status"]

                size = input["length"]

                words = input["words"]

                line_count = input["lines"]

                duration = input["duration"]/1000000

                duration = int(duration)

            

                ffuf_payload = {

                    "subdomain": subdomain,

                    "url_path": f"/{url_path}",

                    "status": status,

                    "size": size,

                    "words": words,

                    "line_count": line_count,

                    "duration": duration

                }

                print(ffuf_payload)

                results.append(ffuf_payload)

    except Exception as e:

        print(f"[!] Resolver error: {e}")   

    

    return results

if __name__ == "__main__":
    expose_url_paths("shop.redasmsecurity.cloud")
