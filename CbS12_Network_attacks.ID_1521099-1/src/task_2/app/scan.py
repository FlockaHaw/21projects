import os
import nmap
import sys
from pymongo import MongoClient
from pymongo import errors

def read_iplist():
    FPATH = './ips.txt'
    ip_list = []

    try:
        with open(FPATH, "r") as FILE:
            for line in FILE:
                ip_list.append(line.strip())
        return ip_list
    except Exception as e:
        if "open" in str(e).lower() or "file" in str(e).lower():
            print("Cannot open IP list file (ips.txt)", file=sys.stderr)
        return []

def scan_manually():
    scanning_net = str(input("[?] Enter network to scan (e.g. 127.0.0.1/28) \n > "))
    scanning_ports = str(input("[?] Enter ports to scan (e.g. 27017-27018) \n > "))
    return scan_network(scanning_net, scanning_ports)

def scan_automaticaly():
    ip_list = read_iplist()
    if not ip_list:
        print("[!] No IPs found in ips.txt", file=sys.stderr)
        return []
    
    all_results = []
    for ip in ip_list:
        scanning_net = ip
        scanning_ports = "27017-27018"
        results = scan_network(scanning_net, scanning_ports, single_ip=True)
        if results:  # Добавляем все найденные хосты
            all_results.extend(results)
    
    return all_results

def scan_network(scanning_net, scanning_ports, single_ip=False):
    nm = nmap.PortScanner()
    try:
        local_net = nm.scan(scanning_net, scanning_ports)
    except Exception as e:
        print(f"[!] Scan error: {e}", file=sys.stderr)
        return []
    
    results = []
    for host in local_net['scan']:
        if 'tcp' in local_net['scan'][host]:
            open_ports = [port for port in local_net['scan'][host]['tcp'] 
                         if local_net['scan'][host]['tcp'][port]['state'] == 'open']
            
            if open_ports:
                for port in open_ports:
                    target_ip = host
                    target_port = port
                    target_status = 'open'
                    target_prod = local_net['scan'][host]['tcp'][port].get('product', 'Unknown')
                    target_prod_version = local_net['scan'][host]['tcp'][port].get('version', 'Unknown')
                    results.append((target_ip, target_port, target_status, target_prod, target_prod_version))
        
        # Для single IP режима добавляем хоть какую-то информацию
        elif single_ip:
            target_ip = host
            target_status = local_net['scan'][host]['status']['state']
            results.append((target_ip, None, target_status, None, None))
    
    return results

def connection(target_ip, target_port): # Без аутентификации
    try:
        client = MongoClient(f"mongodb://{target_ip}:{target_port}/", serverSelectionTimeoutMS=5000)
        dbs = client.list_database_names()
        user_dbs = [db for db in dbs if db not in ['admin','local','config']]
        client.close()
        return user_dbs
    except errors.ServerSelectionTimeoutError:
        return "[!] > Timeout"
    except errors.ConnectionFailure as e:
        if "authentication failed" in str(e).lower() or "not authorized" in str(e).lower():
            return "[!] > Auth required"
        return f"[!] > Connection failed: {str(e)[:50]}"
    except Exception as e:
        return f"[!] > Error: {str(e)[:50]}"

def main():
    os.system('clear')
    print("============================")
    print("       MongoDB scanner      ")
    print("============================")
    print("[?] Enter method:\n 1) Manually scan\n 2) Scan via ips.txt file")
    
    try:
        method = int(input(" > "))
    except ValueError:
        print("[!] Invalid input", file=sys.stderr)
        return 1
    
    if method == 1:
        results = scan_manually()
    elif method == 2:
        results = scan_automaticaly()
    else:
        print("[!] Invalid method", file=sys.stderr)
        return 1
    
    if results:
        print(f"\n[+] Found {len(results)} MongoDB instance(s):")
        print("=" * 50)
        
        for i, (target_ip, target_port, target_status, target_prod, target_prod_version) in enumerate(results, 1):
            print(f"\n[{i}] Host: {target_ip}")
            if target_port:
                print(f"    Port: {target_port}")
                print(f"    Status: {target_status}")
                print(f"    Product: {target_prod}, version: {target_prod_version}")
                user_dbs = connection(target_ip, target_port)
                print(f"    User databases: {user_dbs}")
            else:
                print(f"    Status: {target_status} (no open MongoDB ports)")
        
        print("\n" + "=" * 50)
        print(f"Total found: {len(results)}")
    else:
        print("\n[-] No MongoDB instances found")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
