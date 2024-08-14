from pathlib import Path
from mimul.mimul import mimul
from shutil import rmtree


def domain_generator():
    with Path("DOMAINS").open("r") as f:
        for domain in f.read().split("\n"):
            if domain:
                yield domain

def mimul_path_generator():
    for path in Path(".").glob("*.mimul"):
        yield path

def png_path_generator():
    for path in Path(".").glob("*.png"):
        yield path

def main():
    for domain in domain_generator():
        print(f"[+] Processing domain {domain}")
        domain_path = Path(domain)
        if domain_path.exists():
            rmtree(domain_path)
        domain_path.mkdir(parents=True, exist_ok=True)
        with (domain_path / "CNAME").open("w") as f:
            f.write(f"www.{domain}")
        for mimul_path in mimul_path_generator():
            print(f"    [+] Processing {mimul_path}")
            css_path = mimul_path.parent / f"{mimul_path.stem}.css"
            if css_path.exists():
                with css_path.open("r") as f:
                    css = f.read()
            else:
                css = ""
            with mimul_path.open("r") as f:
                mimul_content = f.read()
            html_output_path = domain_path / f"{mimul_path.stem}.html"
            with html_output_path.open("w") as f:
                f.write(mimul(domain, mimul_content, css))
        for png_path in png_path_generator():
            print(f"    [+] Processing {png_path}")
            with png_path.open("rb") as f:
                png_content = f.read()
            png_output_path = domain_path / f"{png_path.stem}.png"
            with png_output_path.open("wb") as f:
                f.write(png_content)
