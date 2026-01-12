"""
Payload definitions for reflected XSS detection.

Each payload is designed to test a specific 
reflection context without executing JavaScript.
"""

XSS_MARKER = "XSS_CTXT_TEST"

PAYLOADS = {
    "html": [
        {
            "name": "html_script_comment",
            "payload": f"<script>/*{XSS_MARKER}*/</script>",
            "description": "Tests unescaped HTML body reflection"
        },
        {
            "name": "html_tag_marker",
            "payload": f"<div>{XSS_MARKER}</div>",
            "description": "Tests raw HTML tag injection"
        }
    ],
    
    "attribute": [
        {
            "name": "attr_quote_breakout",
            "payload": f"\" onmouseover=\"/*{XSS_MARKER}*/\"",
            "description": "Tests attribute quote breakout and injection"
        }
    ],
    
    "javascript": [
        {
            "name": "js_string_breakout",
            "payload": f"\";/*{XSS_MARKER}*///",
            "description": "Tests reflection inside JavaScript string context"
        }
    ],
    
    "svg": [
        {
            "name": "svg_tag_injection",
            "payload": f"<svg><desc>{XSS_MARKER}</desc></svg>",
            "description": "Tests SVG/tag-based markup reflection"
        }
    ]
}

