This note contains malicious URLs that should be rejected:

javascript:alert('XSS')
data:text/html,<script>alert('XSS')</script>
file:///etc/passwd
vbscript:msgbox("XSS")

Only valid URLs like https://example.com should be accepted.