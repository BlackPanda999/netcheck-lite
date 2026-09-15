#!/usr/bin/env python3
"""NetCheck Lite: a safe, read-only network health checker."""
import argparse, json, socket, ssl, sys, time
from datetime import datetime, timezone
DEFAULT_TARGETS = [{"name":"DNS","host":"example.com","port":443},{"name":"HTTPS","host":"example.com","port":443},{"name":"GitHub","host":"github.com","port":443}]
def check_target(t, timeout):
    started=time.perf_counter(); host=t["host"]; port=int(t.get("port",443)); r={"name":t.get("name",host),"host":host,"port":port,"status":"FAIL"}
    try:
        addresses=socket.getaddrinfo(host,port,type=socket.SOCK_STREAM); r["resolved_addresses"]=sorted({a[4][0] for a in addresses})
        with socket.create_connection((host,port),timeout=timeout) as conn:
            r["tcp"]="reachable"
            if port==443:
                with ssl.create_default_context().wrap_socket(conn,server_hostname=host) as tls: r["tls"]=tls.version(); r["certificate"]="valid"
        r["status"]="PASS"
    except socket.gaierror as e: r["error"]=f"DNS resolution failed: {e}"
    except (socket.timeout,TimeoutError): r["error"]=f"Timed out after {timeout:g}s"
    except ssl.SSLError as e: r["error"]=f"TLS validation failed: {e}"
    except OSError as e: r["error"]=f"Connection failed: {e}"
    r["latency_ms"]=round((time.perf_counter()-started)*1000,1); return r
def main():
    p=argparse.ArgumentParser(description="Read-only DNS, TCP, and TLS network health checker"); p.add_argument("--targets"); p.add_argument("--timeout",type=float,default=3.0); p.add_argument("--json",action="store_true"); a=p.parse_args()
    if a.timeout<=0: p.error("--timeout must be greater than zero")
    try:
        if a.targets:
            with open(a.targets,encoding="utf-8") as f: targets=json.load(f)
            if not isinstance(targets,list) or not targets or any("host" not in x for x in targets): raise ValueError("targets JSON must be a non-empty list containing host")
        else: targets=DEFAULT_TARGETS
    except (OSError,ValueError,json.JSONDecodeError) as e: print(f"Error: {e}",file=sys.stderr); return 2
    checks=[check_target(t,a.timeout) for t in targets]; passed=sum(x["status"]=="PASS" for x in checks); report={"tool":"NetCheck Lite","checked_at":datetime.now(timezone.utc).isoformat(),"passed":passed,"total":len(checks),"checks":checks}
    if a.json: print(json.dumps(report,indent=2))
    else:
        print(f"NetCheck Lite — {passed}/{len(checks)} checks passed")
        for x in checks: print(f"[{x['status']}] {x['name']} ({x['host']}:{x['port']}) — {x['latency_ms']} ms" + (f"\n       {x['error']}" if x.get('error') else ""))
    return 0 if passed==len(checks) else 1
if __name__=="__main__": sys.exit(main())
