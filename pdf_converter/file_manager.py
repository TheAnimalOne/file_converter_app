from PIL import Image
from enum import StrEnum
from pathlib import Path


class ConversionType(StrEnum):
    PNG = 'PNG'
    JPG = 'JPG'
    PDF = 'PDF'
    COMBINED_PDF = 'COMBINED PDF'


CONVERSION_TYPE_TO_FILE_FORMAT: dict[ConversionType, str] = {
    ConversionType.PNG: '.png',
    ConversionType.JPG: '.jpg',
    ConversionType.PDF: '.pdf',
    ConversionType.COMBINED_PDF: '.pdf',
}


class FileManager:

    def __init__(self):
        self.file_paths = []

    def add_file_path(self, new_paths: list[str]) -> None:
        for p in new_paths:
            self.file_paths.append(Path(p))

    def delete_file_path(self, indices: list[int]) -> None:
        for i in sorted(indices, reverse=True):
            del self.file_paths[i]

    def clear_file_paths(self) -> None:
        self.file_paths = []

    def switch_order(self, i: int, j: int) -> None:
        self.file_paths[i], self.file_paths[j] = self.file_paths[j], self.file_paths[i]

    def display_files(self) -> list[str]:
        return [p.name for p in self.file_paths]

    def convert_files(self, c_type: ConversionType, save_loc: str) -> tuple[str, str]:
        try:
            files = self._convert_files(c_type, Path(save_loc))
            return "Success", f"Successfully saved: {files}"
        except Exception as e:
            return "Error", str(e)

    def _convert_files(self, convertion_type_enum: ConversionType, save_location: Path) -> str:
        fmt = CONVERSION_TYPE_TO_FILE_FORMAT[convertion_type_enum]
        match convertion_type_enum:
            case ConversionType.PNG | ConversionType.JPG | ConversionType.PDF:
                file_paths = []
                for path in self.file_paths:
                    im = Image.open(path)
                    file_name = fr"{save_location}\{path.with_suffix(fmt).name}"
                    file_paths.append(file_name)
                    im.save(file_name, optimize=True)
                return ", ".join(file_paths)
            case ConversionType.COMBINED_PDF:
                images = [Image.open(p) for p in self.file_paths]
                # for combined pdfs, use parent folder as the file name
                file_name = fr"{save_location}\{save_location.with_suffix(fmt).name}"
                images[0].save(file_name, save_all=True, append_images=images[1:], optimize=True)
                return file_name
            case _:
                raise ValueError(f"{convertion_type_enum} is not implemented")
