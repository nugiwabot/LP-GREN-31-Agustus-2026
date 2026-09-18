"""
=============================================================================
GREN PROPERTYKOST - MCP SERVER (Model Context Protocol)
=============================================================================
Menyediakan tool native 'gren_market_search' untuk Antigravity IDE via stdio.
Kompatibel dengan spesifikasi resmi Model Context Protocol (JSON-RPC 2.0).
=============================================================================
"""

import sys
import json
import os

# Ensure project root is in python path
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, WORKSPACE_DIR)

import ai_agent_search

def send_response(response):
    """Kirim respon JSON-RPC melalui stdout."""
    data = json.dumps(response)
    sys.stdout.write(f"Content-Length: {len(data.encode('utf-8'))}\r\n\r\n{data}")
    sys.stdout.flush()

def handle_request(req):
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "gren-market-search-server",
                    "version": "1.0.0"
                }
            }
        }

    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "gren_market_search",
                        "description": "Cari data tren pasar sewa kost mahasiswa Jatinangor via Google Custom Search API, proses embedding & reranking dengan AI lokal, dan buat artikel edukasi ramah SEO AI di folder /artikel/.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {
                                    "type": "string",
                                    "description": "Kata kunci atau topik riset pasar (contoh: 'okupansi kost unpad jatinangor 2026')"
                                },
                                "slug": {
                                    "type": "string",
                                    "description": "Nama folder / slug URL artikel opsional"
                                },
                                "top_k": {
                                    "type": "integer",
                                    "description": "Jumlah temuan teratas yang disaring (default: 3)",
                                    "default": 3
                                },
                                "dry_run": {
                                    "type": "boolean",
                                    "description": "Jalankan pencarian dan reranking saja tanpa membuat file artikel fisik",
                                    "default": False
                                }
                            },
                            "required": ["query"]
                        }
                    }
                ]
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "gren_market_search":
            query = args.get("query", "")
            slug = args.get("slug")
            top_k = args.get("top_k", 3)
            dry_run = args.get("dry_run", False)

            try:
                # Execute pipeline
                raw_items = ai_agent_search.fetch_google_search(query, max_results=10)
                top_items = ai_agent_search.rerank_results(query, raw_items, top_k=top_k)

                if dry_run:
                    output_text = f"Pencarian selesai untuk '{query}'. Ditemukan {len(top_items)} referensi unggulan (Mode Dry-run)."
                else:
                    target_file, canonical_url = ai_agent_search.generate_article_html(query, top_items, slug=slug)
                    output_text = (
                        f"Artikel SEO AI berhasil dibuat!\n"
                        f"- File: {target_file}\n"
                        f"- Canonical URL: {canonical_url}\n"
                        f"- Top 3 Referensi: " + ", ".join([it['title'] for it in top_items])
                    )

                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": output_text
                            }
                        ]
                    }
                }
            except Exception as e:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"Gagal mengeksekusi pipeline: {str(e)}"
                            }
                        ],
                        "isError": True
                    }
                }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {
            "code": -32601,
            "message": f"Method '{method}' not found"
        }
    }

def main():
    """Main stdio loop reading JSON-RPC messages."""
    buffer = ""
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        buffer += line
        if "\r\n\r\n" in buffer or "\n\n" in buffer:
            header_part, content_part = buffer.split("\r\n\r\n", 1) if "\r\n\r\n" in buffer else buffer.split("\n\n", 1)
            content_length = None
            for h in header_part.splitlines():
                if h.lower().startswith("content-length:"):
                    content_length = int(h.split(":", 1)[1].strip())
                    break
            
            if content_length is not None:
                while len(content_part.encode("utf-8")) < content_length:
                    more = sys.stdin.readline()
                    if not more:
                        break
                    content_part += more
                
                try:
                    req_json = json.loads(content_part[:content_length])
                    resp = handle_request(req_json)
                    send_response(resp)
                except Exception as ex:
                    sys.stderr.write(f"MCP Error: {ex}\n")
                
                buffer = content_part[content_length:]
            else:
                try:
                    req_json = json.loads(header_part.strip())
                    resp = handle_request(req_json)
                    sys.stdout.write(json.dumps(resp) + "\n")
                    sys.stdout.flush()
                except Exception:
                    pass
                buffer = ""

if __name__ == "__main__":
    main()
