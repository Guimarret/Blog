#!/usr/bin/env python3
"""Re-encode the site images as lossless WebP. Nothing else about them changes.

Every image keeps its original pixels and dimensions: WebP lossless decodes byte
for byte identical to the PNG or JPEG it came from, so this is a container swap,
not a quality trade. It is only smaller because PNG is a weak encoder for this
kind of picture.

    python3 scripts/optimize_images.py            # write optimized/ and look at it
    python3 scripts/optimize_images.py --publish  # swap them into the site
    python3 scripts/optimize_images.py --restore  # put the originals back

--publish moves the originals to assets/img-originals/ (kept in the repo, never
published by Hugo), puts the WebP files in static/img/, and repoints the markdown.

Vectors and animations (svg, gif), the blog/ chrome, and anything WebP does not
actually shrink are left exactly as they are.
"""

import io
import json
import os
import shutil
import sys

from PIL import Image

Image.MAX_IMAGE_PIXELS = None

LIVE = "static/img"  # what the site serves
KEEP = "assets/img-originals"  # where the originals go once --publish runs
REVIEW = "optimized"  # scratch output, not part of the site
COPY_AS_IS = {".svg", ".gif", ".webp"}
SKIP_DIRS = {"blog"}  # site chrome, hand-optimised, referenced from CSS
EXCLUDE = {"blog/me_draw.JPG"}  # source drawing, only the derived png is published




def encode(im, **kw):
    buf = io.BytesIO()
    # carry the colour profile across, dropping it would recolour a wide gamut
    # image even though every pixel value stayed the same
    icc = im.info.get("icc_profile")
    if icc:
        kw["icc_profile"] = icc
    im.save(buf, "WEBP", method=5, **kw)
    return buf.getvalue()



def convert(path, rel):
    """Return (webp bytes, info) or (None, reason) when the file is left alone."""
    if rel in EXCLUDE:
        return None, "not published"
    if os.path.splitext(rel)[1].lower() in COPY_AS_IS or rel.split("/")[0] in SKIP_DIRS:
        return None, "left as is"

    im = Image.open(path)
    im.load()
    if im.mode == "P":
        im = im.convert("RGBA")
    elif im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGB")

    data = encode(im, lossless=True)
    if len(data) >= os.path.getsize(path):
        return None, "webp was bigger"

    return data, {"size": im.size}


def walk_images(root):
    for dirpath, _, names in os.walk(root):
        for name in sorted(names):
            if name == ".DS_Store":
                continue
            path = os.path.join(dirpath, name)
            yield path, os.path.relpath(path, root).replace(os.sep, "/")


def build(src):
    out = os.path.join(REVIEW, "img")
    if os.path.isdir(out):
        shutil.rmtree(out)
    manifest, skipped, before, after = [], [], 0, 0
    for path, rel in walk_images(src):
        size = os.path.getsize(path)
        before += size
        data, info = convert(path, rel)
        if data is None:
            after += 0 if info == "not published" else size
            skipped.append((rel, info))
            continue
        dest = os.path.join(out, os.path.splitext(rel)[0] + ".webp")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "wb") as fh:
            fh.write(data)
        after += len(data)
        manifest.append({"src": rel, "out": os.path.splitext(rel)[0] + ".webp",
                         "old": size, "new": len(data), **info})
    return manifest, skipped, before, after


def kb(n):
    return f"{n / 1024:,.0f} KB" if n < 1048576 else f"{n / 1048576:.2f} MB"


def markdown():
    for root, _, names in os.walk("content"):
        for name in names:
            if name.endswith(".md"):
                yield os.path.join(root, name)


def repoint(mapping):
    changed = 0
    for path in markdown():
        text = original = open(path).read()
        for old, new in mapping.items():
            text = text.replace(old, new)
        if text != original:
            open(path, "w").write(text)
            changed += 1
    return changed


def publish(manifest):
    """Swap the optimised files in, keeping the originals under assets/."""
    if os.path.isdir(KEEP):
        shutil.rmtree(LIVE)  # already published once, just refresh from the originals
    else:
        os.makedirs(os.path.dirname(KEEP), exist_ok=True)
        shutil.move(LIVE, KEEP)
    os.makedirs(LIVE, exist_ok=True)
    converted = {m["src"]: m["out"] for m in manifest}
    for path, rel in walk_images(KEEP):
        if rel in EXCLUDE:
            continue
        out = converted.get(rel)
        dest = os.path.join(LIVE, out or rel)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy2(os.path.join(REVIEW, "img", out) if out else path, dest)
    n = repoint({f"/img/{m['src']}": f"/img/{m['out']}" for m in manifest})
    print(f"published {len(converted)} optimised images, repointed {n} markdown files")


def restore():
    if not os.path.isdir(KEEP):
        sys.exit(f"{KEEP} not found, nothing to restore")
    mapping = {}
    for _, rel in walk_images(KEEP):
        stem, ext = os.path.splitext(rel)
        if ext.lower() in (".png", ".jpg", ".jpeg"):
            mapping[f"/img/{stem}.webp"] = f"/img/{rel}"
    shutil.rmtree(LIVE)
    shutil.move(KEEP, LIVE)
    n = repoint(mapping)
    print(f"restored the originals to {LIVE}, repointed {n} markdown files")


def main():
    if "--restore" in sys.argv:
        return restore()

    src = KEEP if os.path.isdir(KEEP) else LIVE
    manifest, skipped, before, after = build(src)

    for m in sorted(manifest, key=lambda m: m["new"] - m["old"])[:8]:
        print(f"  {m['old'] / 1024:7.0f}K -> {m['new'] / 1024:6.0f}K  {m['src']}")
    print(f"\n{len(manifest)} converted losslessly, {len(skipped)} left alone: "
          f"{before / 1048576:.2f} MB -> {after / 1048576:.2f} MB "
          f"({100 * (before - after) / before:.0f}% smaller)")

    with open(os.path.join(REVIEW, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=1)

    if "--publish" in sys.argv:
        publish(manifest)
    else:
        print(f"\nfiles are in {REVIEW}/img, re-run with --publish to use them")


if __name__ == "__main__":
    main()
