def save_page(page: str, save_path: str) -> None:
    """
    保存HTML网页
    """
    with open(save_path, 'w') as f:
        f.write(page)