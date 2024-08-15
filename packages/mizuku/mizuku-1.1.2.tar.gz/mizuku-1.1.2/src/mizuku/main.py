from pathlib import Path
from mizuku.mizu import mizu
from shutil import rmtree


def domain_generator():
    with Path("DOMAINS").open("r") as f:
        for domain in f.read().split("\n"):
            if domain:
                yield domain

def mizu_path_generator():
    for path in Path(".").glob("*.mizu"):
        yield path

def png_path_generator():
    for path in Path(".").glob("*.png"):
        yield path

def main():
    for domain in domain_generator():
        print(f"[+] Processing domain {domain}")
        domain_path = Path(domain)
        if domain_path.exists():
            for path in domain_path.glob("*"):
                if not path.stem.startswith("."):
                    if path.is_dir():
                        rmtree(domain_path)
                    else:
                        path.unlink()
        domain_path.mkdir(parents=True, exist_ok=True)
        with (domain_path / "CNAME").open("w") as f:
            f.write(domain)
        for mizu_path in mizu_path_generator():
            print(f"    [+] Processing {mizu_path}")
            css_path = mizu_path.parent / f"{mizu_path.stem}.css"
            if css_path.exists():
                with css_path.open("r") as f:
                    css = f.read()
            else:
                css = ""
            with mizu_path.open("r") as f:
                mizu_content = f.read()
            html_output_path = domain_path / f"{mizu_path.stem}.html"
            with html_output_path.open("w") as f:
                f.write(mizu(domain, mizu_content, css))
        for png_path in png_path_generator():
            print(f"    [+] Processing {png_path}")
            with png_path.open("rb") as f:
                png_content = f.read()
            png_output_path = domain_path / f"{png_path.stem}.png"
            with png_output_path.open("wb") as f:
                f.write(png_content)
