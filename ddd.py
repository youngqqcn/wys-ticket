import ddddocr


if __name__ == '__main__':

    det = ddddocr.DdddOcr(det=False, ocr=False)

    with open('btn.png', 'rb') as f:
        target_bytes = f.read()

    with open('bg.png', 'rb') as f:
        background_bytes = f.read()

    res = det.slide_match(target_bytes, background_bytes, simple_target=True)

    print(res)