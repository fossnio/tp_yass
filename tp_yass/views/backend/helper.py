from pathlib import Path
from tempfile import NamedTemporaryFile

from tp_yass.views.helper.file import get_static_abspath, save_file


def upload_attachment(cgi_field_storage, prefix):
    """將上傳的檔案重新亂數命名後存檔

    Args:
        cgi_field_storage: cgi.FieldStorage 物件
        prefix: 字串，前綴用

    Returns:
        回傳儲存完畢的亂數檔名字串
    """
    upload_file_name = Path(cgi_field_storage.filename)
    with NamedTemporaryFile(dir=str(get_static_abspath() / 'uploads' / 'pages'),
                            prefix=prefix,
                            suffix=upload_file_name.suffix,
                            delete=False) as destination_file:
        save_file(cgi_field_storage, destination_file)
        return str(Path(destination_file.name).name)


def delete_attachment(page_attachment):
    """移除指定的上傳附件實體檔案

    Args:
        page_attachment: PageAttachment 物件
    """
    attachment_abspath = get_static_abspath() / 'uploads' / 'pages' / page_attachment.real_name
    attachment_abspath.unlink()
