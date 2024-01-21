import fire
from colab_easy_ui.ColabEasyUI import ColabEasyUI, JsonApiFunc

import functools
from colab_easy_ui.plugins.download_function.Downloader import DownloadParams
from colab_easy_ui.plugins.download_function.download_function import download

from colab_easy_ui.plugins.unzip_function import unzip

# def downloader_callback(status: str, message: str, port: int, uuid_str: str):
#     import json

#     data = json.dumps(message)
#     requests.get(f"http://localhost:{port}/functions_set_task_status?task_id={uuid_str}&status={status}&data={data}")


# def dummy_downloader_function(port: int, uuid_str: str):
#     downloader_callback_fixed = functools.partial(downloader_callback, port=port, uuid_str=uuid_str)
#     download_weights(downloader_callback_fixed)


# def download(port: int):
#     # UUIDを作成
#     uuid_str = str(uuid.uuid4())

#     server_thread = threading.Thread(target=dummy_downloader_function, args=(port, uuid_str))
#     server_thread.start()

#     try:
#         data = {
#             "status": "ok",
#             "uuid": uuid_str,
#             "description": "easy-file-uploader-py created by wok!",
#         }

#         json_compatible_item_data = jsonable_encoder(data)
#         return JSONResponse(content=json_compatible_item_data)
#     except Exception as e:
#         data = {
#             "status": "error",
#             "message": str(e),
#             "description": "easy-file-uploader-py created by wok!",
#         }
#         print(data)
#         return JSONResponse(content=json_compatible_item_data)


downloadParams = [
    DownloadParams(
        display_name="whisper_tiny.en.pt",
        url="https://openaipublic.azureedge.net/main/whisper/models/d3dd57d32accea0b295c96e26691aa14d8822fac7d9d27d5dc00b4ca2826dd03/tiny.en.pt",
        saveTo="./models/embedder/whisper_tiny.en.pt",
        hash="d3dd57d32accea0b295c96e26691aa14d8822fac7d9d27d5dc00b4ca2826dd03",
    ),
    DownloadParams(
        display_name="whisper_tiny.pt",
        url="https://openaipublic.azureedge.net/main/whisper/models/65147644a518d12f04e32d6f3b26facc3f8dd46e5390956a9424a650c0ce22b9/tiny.pt",
        saveTo="./models/embedder/whisper_tiny.pt",
        hash="65147644a518d12f04e32d6f3b26facc3f8dd46e5390956a9424a650c0ce22b9",
    ),
    DownloadParams(
        display_name="whisper_base.en.pt",
        url="https://openaipublic.azureedge.net/main/whisper/models/25a8566e1d0c1e2231d1c762132cd20e0f96a85d16145c3a00adf5d1ac670ead/base.en.pt",
        saveTo="./models/embedder/whisper_base.en.pt",
        hash="25a8566e1d0c1e2231d1c762132cd20e0f96a85d16145c3a00adf5d1ac670ead",
    ),
    DownloadParams(
        display_name="whisper_base.pt",
        url="https://openaipublic.azureedge.net/main/whisper/models/ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e/base.pt",
        saveTo="./models/embedder/whisper_base.pt",
        hash="ed3a0b6b1c0edf879ad9b11b1af5a0e6ab5db9205f891f668f8b0e6c6326e34e",
    ),
]


def run_server():
    c = ColabEasyUI.get_instance()
    port = c.port
    c.enable_file_uploader("upload", {"abc": "voice.zip"})
    c.enable_colab_internal_fetcher()
    tb_port = c.colabInternalFetcher.start_tensorboard("trainer/amitaro/logs", "TB_LOG")
    print("Tensorflow port:::", tb_port)

    c.register_functions(
        [
            JsonApiFunc("unzip_id", "progress", "unzip_name", "GET", "/unzip", functools.partial(unzip, port=port, zip_path="upload/voice.zip", extract_to="raw_data")),
            # backgroundタスクのパラレル化がむずいので、一つずつ別タスクにする（TOBE IMPROVED）。
            JsonApiFunc("dl_id1", "progress", "dl_name1", "GET", "/download1", functools.partial(download, port=port, downloadParams=downloadParams[0:1])),
            JsonApiFunc("dl_id2", "progress", "dl_name2", "GET", "/download2", functools.partial(download, port=port, downloadParams=downloadParams[1:2])),
            JsonApiFunc("dl_id3", "progress", "dl_name3", "GET", "/download3", functools.partial(download, port=port, downloadParams=downloadParams[2:3])),
            JsonApiFunc("dl_id4", "progress", "dl_name4", "GET", "/download4", functools.partial(download, port=port, downloadParams=downloadParams[3:4])),
        ]
    )
    c.mount_static_folder("/front2", "frontend/dist")
    port = c.start()
    print(port)


def main():
    fire.Fire(run_server)
