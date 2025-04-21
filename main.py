import os
import pytesseract
from PIL import Image
import pyautogui
import time

def capture_and_transcribe(output_file, start_page, end_page, delay=2):
    """
    Kindleのページをスクリーンショットし、文字起こしを行い、テキストファイルに保存します。
    :param output_file: 出力するテキストファイルのパス。
    :param start_page: 開始ページ番号。
    :param end_page: 終了ページ番号。
    :param delay: ページ切り替えの間隔（秒）。
    """
    text_output = []
    for page in range(start_page, end_page + 1, 2):
        screenshot = pyautogui.screenshot()
        page_range_str = f"{page}-{page + 1}"
        screenshot_path = "outputs/capture.png"
        screenshot.save(screenshot_path)
        print(f"{screenshot_path} をキャプチャに成功")
        
        print("文字起こしを開始")
        text = pytesseract.image_to_string(Image.open(screenshot_path), lang="jpn")
        print("文字起こしを完了")

        text_output.append(f"{page_range_str}ページ")
        text_output.append(text)
        
        os.remove(screenshot_path)  # 処理後にスクリーンショットを削除
        pyautogui.press("right")  # ページをめくる操作をシミュレート
        time.sleep(delay)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(text_output))

if __name__ == "__main__":
    # 実行してからKindleを画面いっぱいにするまでちょっと待つ
    time.sleep(3)

    # Example usage
    output_file = "outputs/kindle_book_text.txt"
    start_page = 1  # 開始ページ番号
    end_page = 100  # 終了ページ番号
    capture_and_transcribe(output_file, start_page, end_page, delay=0.1)
