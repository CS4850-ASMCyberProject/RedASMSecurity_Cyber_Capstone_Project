from terminal_run import run_cmd
import json

def expose_url_paths(subdomain):
    WORDLIST = r"~/SecLists/Discovery/DNS/subdomains-top1-million-5000.txt"
    results = []
    try:
        run_cmd("Fuff URL Paths Scan", f"ffuf -u http://{subdomain}/FUZZ -w {WORDLIST} -mc 500 -of json -o ffuf_output.txt")
        
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
                
                results.append(ffuf_payload)
            
            
    except Exception as e:
        print(f"[!] Resolver error: {e}")   
    
    return results