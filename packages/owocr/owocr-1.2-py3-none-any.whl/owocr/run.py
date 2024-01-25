import sys
import time
import threading
import os
import configparser
from pathlib import Path

import fire
import numpy as np
import pyperclipfix
import asyncio
import websockets
import queue
import io

from PIL import Image
from PIL import UnidentifiedImageError
from loguru import logger
from pynput import keyboard
from notifypy import Notify

import inspect
from owocr import *

try:
    import win32gui
    import win32api 
    import win32con
    import win32clipboard
    import ctypes
except ImportError:
    pass


class WindowsClipboardThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.daemon = True

    def process_message(self, hwnd: int, msg: int, wparam: int, lparam: int):
        WM_CLIPBOARDUPDATE = 0x031D
        if msg == WM_CLIPBOARDUPDATE and not (paused or tmp_paused):
            if win32clipboard.IsClipboardFormatAvailable(win32con.CF_BITMAP):
                clipboard_event.set()
        return 0

    def create_window(self):
        className = 'ClipboardHook'
        wc = win32gui.WNDCLASS()
        wc.lpfnWndProc = self.process_message
        wc.lpszClassName = className
        wc.hInstance = win32api.GetModuleHandle(None)
        class_atom = win32gui.RegisterClass(wc)
        return win32gui.CreateWindow(class_atom, className, 0, 0, 0, 0, 0, 0, 0, wc.hInstance, None)

    def run(self):
        hwnd = self.create_window()
        self.thread_id = win32api.GetCurrentThreadId()
        ctypes.windll.user32.AddClipboardFormatListener(hwnd)
        win32gui.PumpMessages()


class WebsocketServerThread(threading.Thread):
    def __init__(self, port, read):
        super().__init__()
        self.daemon = True
        self.loop = asyncio.new_event_loop()
        self.port = port
        self.read = read
        self.clients = set()

    async def send_text_coroutine(self, text):
        for client in self.clients:
            await client.send(text)

    async def server_handler(self, websocket):
        self.clients.add(websocket)
        try:
            async for message in websocket:
                if self.read and not (paused or tmp_paused):
                    websocket_queue.put(message)
                    try:
                        await websocket.send('True')
                    except websockets.exceptions.ConnectionClosedOK:
                        pass
                else:
                    try:
                        await websocket.send('False')
                    except websockets.exceptions.ConnectionClosedOK:
                        pass
        finally:
            self.clients.remove(websocket)

    def send_text(self, text):
        return asyncio.run_coroutine_threadsafe(self.send_text_coroutine(text), self.loop)

    def stop_server(self):
        self.loop.call_soon_threadsafe(self.server.ws_server.close)
        self.loop.call_soon_threadsafe(self.loop.stop)

    def run(self):
        asyncio.set_event_loop(self.loop)
        start_server = websockets.serve(self.server_handler, '0.0.0.0', self.port, max_size=50000000)
        self.server = start_server
        self.loop.run_until_complete(start_server)
        self.loop.run_forever()
        pending = asyncio.all_tasks(loop=self.loop)
        if len(pending) > 0:
            self.loop.run_until_complete(asyncio.wait(pending))
        self.loop.close()


def getchar_thread():
    global user_input
    if sys.platform == 'win32':
        import msvcrt
        while True:
            user_input_bytes = msvcrt.getch()
            try:
                user_input = user_input_bytes.decode()
                if user_input.lower() in 'tq':
                    break
            except UnicodeDecodeError:
                pass
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(sys.stdin.fileno())
            while True:
                user_input = sys.stdin.read(1)
                if user_input.lower() in 'tq':
                    break
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def on_key_press(key):
    global tmp_paused
    global first_pressed
    if first_pressed == None and key in (keyboard.Key.cmd_l, keyboard.Key.cmd_r, keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        first_pressed = key
        tmp_paused = True


def on_key_release(key):
    global tmp_paused
    global just_unpaused
    global first_pressed
    if key == first_pressed:
        tmp_paused = False
        just_unpaused = True
        first_pressed = None


def are_images_identical(img1, img2):
    if None in (img1, img2):
        return img1 == img2

    img1 = np.array(img1)
    img2 = np.array(img2)

    return (img1.shape == img2.shape) and (img1 == img2).all()


def process_and_write_results(engine_instance, engine_color, img_or_path, write_to, notifications):
    t0 = time.time()
    text = engine_instance(img_or_path)
    t1 = time.time()

    logger.opt(ansi=True).info(f'Text recognized in {t1 - t0:0.03f}s using <{engine_color}>{engine_instance.readable_name}</{engine_color}>: {text}')
    if notifications:
        notification = Notify()
        notification.application_name = 'owocr'
        notification.title = 'Text recognized:'
        notification.message = text
        notification.send(block=False)

    if write_to == 'websocket':
        websocket_server_thread.send_text(text)
    elif write_to == 'clipboard':
        pyperclipfix.copy(text)
    else:
        write_to = Path(write_to)
        if write_to.suffix.lower() != '.txt':
            raise ValueError('write_to must be either "clipboard" or a path to a text file')

        with write_to.open('a', encoding='utf-8') as f:
            f.write(text + '\n')


def get_path_key(path):
    return path, path.lstat().st_mtime


def run(read_from='clipboard',
        write_to='clipboard',
        engine='',
        pause_at_startup=False,
        ignore_flag=False,
        delete_images=False
        ):
    """
    Run OCR in the background, waiting for new images to appear either in system clipboard or a directory, or to be sent via a websocket.
    Recognized texts can be either saved to system clipboard, appended to a text file or sent via a websocket.

    :param read_from: Specifies where to read input images from. Can be either "clipboard", "websocket", or a path to a directory.
    :param write_to: Specifies where to save recognized texts to. Can be either "clipboard", "websocket", or a path to a text file.
    :param delay_secs: How often to check for new images, in seconds.
    :param engine: OCR engine to use. Available: "mangaocr", "glens", "gvision", "avision", "azure", "winrtocr", "easyocr", "paddleocr".
    :param pause_at_startup: Pause at startup.
    :param ignore_flag: Process flagged clipboard images (images that are copied to the clipboard with the *ocr_ignore* string).
    :param delete_images: Delete image files after processing when reading from a directory.
    """

    engine_instances = []
    config_engines = []
    engine_keys = []
    default_engine = ''
    logger_format = '<green>{time:HH:mm:ss.SSS}</green> | <level>{message}</level>'
    engine_color = 'cyan'
    delay_secs = 0.5
    websocket_port = 7331
    notifications = False

    config_file = os.path.join(os.path.expanduser('~'),'.config','owocr_config.ini')
    config = configparser.ConfigParser()
    res = config.read(config_file)

    if len(res) != 0:
        try:
            for config_engine in config['general']['engines'].split(','):
                config_engines.append(config_engine.strip().lower())
        except KeyError:
            pass

        try:
            logger_format = config['general']['logger_format'].strip()
        except KeyError:
            pass

        try:
            engine_color = config['general']['engine_color'].strip()
        except KeyError:
            pass

        try:
            delay_secs = float(config['general']['delay_secs'].strip())
        except KeyError:
            pass

        try:
            websocket_port = int(config['general']['websocket_port'].strip())
        except KeyError:
            pass

        try:
            if config['general']['notifications'].strip().lower() == 'true':
                notifications = True
        except KeyError:
            pass

    logger.configure(handlers=[{'sink': sys.stderr, 'format': logger_format}])

    if len(res) != 0:
        logger.info('Parsed config file')
    else:
        logger.warning('No config file, defaults will be used')

    for _,engine_class in sorted(inspect.getmembers(sys.modules[__name__], lambda x: hasattr(x, '__module__') and __package__ + '.ocr' in x.__module__ and inspect.isclass(x))):
        if len(config_engines) == 0 or engine_class.name in config_engines:
            try:
                engine_instance = engine_class(config[engine_class.name])
            except KeyError:
                engine_instance = engine_class()

            if engine_instance.available:
                engine_instances.append(engine_instance)
                engine_keys.append(engine_class.key)
                if engine == engine_class.name:
                    default_engine = engine_class.key

    if len(engine_keys) == 0:
        msg = 'No engines available!'
        raise NotImplementedError(msg)

    engine_index = engine_keys.index(default_engine) if default_engine != '' else 0

    global paused
    global tmp_paused
    global just_unpaused
    global user_input
    global first_pressed
    user_input = ''
    paused = pause_at_startup
    just_unpaused = True
    tmp_paused = False
    first_pressed = None

    user_input_thread = threading.Thread(target=getchar_thread, daemon=True)
    user_input_thread.start()

    tmp_paused_listener = keyboard.Listener(
        on_press=on_key_press,
        on_release=on_key_release)
    tmp_paused_listener.start()

    if read_from == 'websocket' or write_to == 'websocket':
        global websocket_server_thread
        websocket_server_thread = WebsocketServerThread(websocket_port, read_from == 'websocket')
        websocket_server_thread.start()

    if read_from == 'websocket':
        global websocket_queue
        websocket_queue = queue.Queue()
        logger.opt(ansi=True).info(f"Reading from websocket using <{engine_color}>{engine_instances[engine_index].readable_name}</{engine_color}>{' (paused)' if paused else ''}")
    elif read_from == 'clipboard':
        from PIL import ImageGrab
        mac_clipboard_polling = False
        windows_clipboard_polling = False
        generic_clipboard_polling = False
        img = None

        logger.opt(ansi=True).info(f"Reading from clipboard using <{engine_color}>{engine_instances[engine_index].readable_name}</{engine_color}>{' (paused)' if paused else ''}")

        if sys.platform == 'darwin' and 'objc' in sys.modules:
            from AppKit import NSPasteboard, NSPasteboardTypePNG, NSPasteboardTypeTIFF
            pasteboard = NSPasteboard.generalPasteboard()
            count = pasteboard.changeCount()
            mac_clipboard_polling = True
        elif sys.platform == 'win32' and 'win32gui' in sys.modules:
            global clipboard_event
            clipboard_event = threading.Event()
            windows_clipboard_thread = WindowsClipboardThread()
            windows_clipboard_thread.start()
            windows_clipboard_polling = True
        else:
            generic_clipboard_polling = True
    else:
        allowed_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif', '.webp')
        read_from = Path(read_from)
        if not read_from.is_dir():
            raise ValueError('read_from must be either "clipboard" or a path to a directory')

        logger.opt(ansi=True).info(f"Reading from directory {read_from} using <{engine_color}>{engine_instances[engine_index].readable_name}</{engine_color}>{' (paused)' if paused else ''}")

        old_paths = set()
        for path in read_from.iterdir():
            if path.suffix.lower() in allowed_extensions:
                old_paths.add(get_path_key(path))

    while True:
        if user_input != '':
            if user_input.lower() in 'tq':
                if read_from == 'websocket' or write_to == 'websocket':
                    websocket_server_thread.stop_server()
                    websocket_server_thread.join()
                if read_from == 'clipboard' and windows_clipboard_polling:
                    win32api.PostThreadMessage(windows_clipboard_thread.thread_id, win32con.WM_QUIT, 0, 0)
                    windows_clipboard_thread.join()
                user_input_thread.join()
                tmp_paused_listener.stop()
                logger.info('Terminated!')
                break

            old_engine_index = engine_index

            if user_input.lower() == 'p':
                if paused:
                    logger.info('Unpaused!')
                    just_unpaused = True
                else:
                    logger.info('Paused!')
                paused = not paused
            elif user_input.lower() == 's':
                if engine_index == len(engine_keys) - 1:
                    engine_index = 0
                else:
                    engine_index += 1
            elif user_input.lower() in engine_keys:
                engine_index = engine_keys.index(user_input.lower())

            if engine_index != old_engine_index:
                logger.opt(ansi=True).info(f'Switched to <{engine_color}>{engine_instances[engine_index].readable_name}</{engine_color}>!')

            user_input = ''

        if read_from == 'websocket':
            while True:
                try:
                    item = websocket_queue.get(timeout=delay_secs)
                except queue.Empty:
                    break
                else:
                    if not paused and not tmp_paused:
                        img = Image.open(io.BytesIO(item))
                        process_and_write_results(engine_instances[engine_index], engine_color, img, write_to, notifications)
        elif read_from == 'clipboard':
            if windows_clipboard_polling:
                clipboard_changed = clipboard_event.wait(delay_secs)
                if clipboard_changed:
                    clipboard_event.clear()
            elif mac_clipboard_polling:
                if not (paused or tmp_paused):
                    old_count = count
                    count = pasteboard.changeCount()
                    clipboard_changed = not just_unpaused and count != old_count and any(x in pasteboard.types() for x in [NSPasteboardTypePNG, NSPasteboardTypeTIFF])
            else:
                clipboard_changed = not (paused or tmp_paused)


            if clipboard_changed:
                old_img = img

                try:
                    img = ImageGrab.grabclipboard()
                except Exception:
                    pass
                else:
                    if not just_unpaused and isinstance(img, Image.Image) and (ignore_flag or pyperclipfix.paste() != '*ocr_ignore*') and ((not generic_clipboard_polling) or (not are_images_identical(img, old_img))):
                        process_and_write_results(engine_instances[engine_index], engine_color, img, write_to, notifications)

            just_unpaused = False

            if not windows_clipboard_polling:
                time.sleep(delay_secs)
        else:
            for path in read_from.iterdir():
                if path.suffix.lower() in allowed_extensions:
                    path_key = get_path_key(path)
                    if path_key not in old_paths:
                        old_paths.add(path_key)

                        if not paused and not tmp_paused:
                            try:
                                img = Image.open(path)
                                img.load()
                            except (UnidentifiedImageError, OSError) as e:
                                logger.warning(f'Error while reading file {path}: {e}')
                            else:
                                process_and_write_results(engine_instances[engine_index], engine_color, img, write_to, notifications)
                                img.close()
                                if delete_images:
                                    Path.unlink(path)

            time.sleep(delay_secs)

if __name__ == '__main__':
    fire.Fire(run)
