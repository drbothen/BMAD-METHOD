This note contains malicious content: <script>alert('XSS attack')</script>

It also has an iframe: <iframe src="http://malicious.com/phishing"></iframe>

And an object tag: <object data="malicious.swf"></object>

These should all be sanitized before processing.