import os
import pytesseract
from PIL import Image
import pyautogui
import time
import pywinctl as gw

def capture_and_transcribe(output_file, start_page, end_page, delay=2):
    """
    Kindleのページをスクリーンショットし、文字起こしを行い、テキストファイルに保存します。
    :param output_file: 出力するテキストファイルのパス。
    :param start_page: 開始ページ番号。
    :param end_page: 終了ページ番号。
    :param delay: ページ切り替えの間隔（秒）。
    """

    # Kindleウィンドウを特定
    kindle_window = None
    for window in gw.getWindowsWithTitle("Kindle"):
        if "Kindle" in window.title:
            kindle_window = window
            break

    if not kindle_window:
        print("Kindleウィンドウが見つかりません。Kindleを開いてください。")
        return

    print("Kindleウィンドウを見つけました。")
    
    for page in range(start_page, end_page + 1):
        if not kindle_window.isActive:
            print("Kindleウィンドウがアクティブではありません。アクティブにします。")
            kindle_window.activate()
            time.sleep(0.1)
        
        # Kindleウィンドウのスクリーンショットを取得
        screenshot = pyautogui.screenshot(region=(kindle_window.left, kindle_window.top, kindle_window.width, kindle_window.height))
        screenshot_path = "outputs/capture.png"
        screenshot.save(screenshot_path)
        print(f"{screenshot_path} をキャプチャに成功")
        
        print("文字起こしを開始")
        text = pytesseract.image_to_string(Image.open(screenshot_path), lang="jpn")
        os.remove(screenshot_path)  # 処理後にスクリーンショットを削除
        print("文字起こしを完了")

        text_output = []
        text_output.append("\n")
        text_output.append(text)
        text_output.append(f"{page}ページ目 終了")

        with open(output_file, "a", encoding="utf-8") as f:
            f.write("\n".join(text_output))
        
        print(f"{page}ページ目の文字起こしが完了しました。次のページへ進みます。")
        pyautogui.press("right")  # ページをめくる操作をシミュレート
        time.sleep(delay)

if __name__ == "__main__":
    output_file = "outputs/kindle_book_text.txt"
    start_page = 1  # 開始ページ番号
    end_page = 100  # 終了ページ番号
    capture_and_transcribe(output_file, start_page, end_page, delay=0.5)
