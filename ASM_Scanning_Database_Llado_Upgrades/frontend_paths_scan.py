import re

def expose_juice_shop_paths(subdomain):
    pattern = r'(/rest[^`"\s]+)'
    results = []
    
    with open("main.js", "r") as f:
        for line in f:
            data = re.findall(pattern, line)
            
            for path in data:
                results.append(path)
        
    results = set(results)
            
    return results

if __name__ == "__main__":
    expose_juice_shop_paths("shop.redasmsecurity.cloud")
                
    
    
