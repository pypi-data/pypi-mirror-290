from paddleocr import PaddleOCR
from rich import print


def ocr(img_path: str, text: str) -> tuple[tuple[int, int, int, int]]:
    """ocr 图片，返回指定文本的边缘坐标 tuple(x1, x2, y1, y2)

    Arguments:
        img_path {str} -- 图片路径
        text {str} -- 文本

    Returns:
        tuple[tuple[int, int, int, int]] -- 边缘坐标 tuple(x1, x2, y1, y2)
    """
    ocr = PaddleOCR(lang="ch", use_gpu=True, show_log=False, use_angle_cls=True)
    result = ocr.ocr(img_path, cls=True)
    result = result[0]

    edge_coord = []
    for (
        edge_point_list,
        text_tuple,
    ) in result:
        if text_tuple[0] == text:
            x1 = int(edge_point_list[0][0])
            x2 = int(edge_point_list[1][0])
            y1 = int(edge_point_list[0][1])
            y2 = int(edge_point_list[2][1])
            edge_coord.append((x1, x2, y1, y2))

    return tuple(edge_coord)


if __name__ == "__main__":
    print(ocr(r"C:\Users\qf\Pictures\intel cpu 型号解释.png", "数字越大"))
