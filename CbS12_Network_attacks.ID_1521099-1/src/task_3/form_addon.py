import os
import urllib.parse
from mitmproxy import ctx, http

class FormLogger:
    def request(self, flow: http.HTTPFlow):
        # Check if the request method is POST and content type indicates a form
        if flow.request.method == "POST":
            content_type = flow.request.headers.get("Content-Type", "")

            # Try to get parsed form data using mitmproxy's built-in properties
            form_data = None
            if "application/x-www-form-urlencoded" in content_type:
                form_data = flow.request.urlencoded_form
            elif "multipart/form-data" in content_type:
                form_data = flow.request.multipart_form

            # If we successfully obtained form data and it's not empty, save it
            if form_data:
                self.save_form_data(flow.request.url, dict(form_data))
            else:
                ctx.log.info(f"No parsable form data for {flow.request.url}")

    def save_form_data(self, url: str, data: dict):
        """Save form data to text and HTML files in the 'forms' directory."""
        # Sanitize the URL to create a safe filename
        safe_name = self.sanitize_filename(url)
        base_path = os.path.join("forms", safe_name)

        # Ensure the forms directory exists
        os.makedirs("forms", exist_ok=True)

        # Write text file - with values combined per field
        txt_path = base_path + ".txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(f"Form data submitted to: {url}\n\n")
            for key, values in data.items():
                # Combine multiple values into one string (without spaces)
                combined_value = "".join(values)
                f.write(f"{key}: {combined_value}\n")

        # Write HTML file - with values combined per field
        html_path = base_path + ".html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html>\n<html>\n<head>\n")
            f.write(f"<title>Form Data: {url}</title>\n")
            f.write("</head>\n<body>\n")
            f.write(f"<h1>Form submitted to: <a href=\"{url}\">{url}</a></h1>\n")
            f.write("<table border='1'>\n<tr><th>Field</th><th>Value</th></tr>\n")
            for key, values in data.items():
                # Combine multiple values into one string
                combined_value = "".join(values)
                f.write(f"<tr><td>{key}</td><td>{combined_value}</td></tr>\n")
            f.write("</table>\n</body>\n</html>")

        ctx.log.info(f"Saved form data to {txt_path} and {html_path}")

    @staticmethod
    def sanitize_filename(url: str) -> str:
        """Convert a URL into a filesystem-safe string."""
        # Replace common unsafe characters with underscores
        unsafe = ":/?#[]@!$&'()*+,;="
        safe = url
        for ch in unsafe:
            safe = safe.replace(ch, "_")
        # Also replace multiple underscores with a single one for readability
        while "__" in safe:
            safe = safe.replace("__", "_")
        # Limit length to avoid filesystem issues (optional)
        if len(safe) > 200:
            safe = safe[:200]
        return safe


addons = [FormLogger()]
