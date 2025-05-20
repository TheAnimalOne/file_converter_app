from PIL import Image
from enum import StrEnum
from pathlib import Path


class ConversionType(StrEnum):
    PNG = 'PNG'
    JPG = 'JPG'
    PDF = 'PDF'
    COMBINED_PDF = 'COMBINED PDF'


class ConversionOutcome(StrEnum):
    SUCCESS = "Success"
    ERROR = "Error"


CONVERSION_TYPE_TO_FILE_FORMAT: dict[ConversionType, str] = {
    ConversionType.PNG: '.png',
    ConversionType.JPG: '.jpg',
    ConversionType.PDF: '.pdf',
    ConversionType.COMBINED_PDF: '.pdf',
}


class FileConverter:

    def __init__(self):
        self.file_paths = []

    def add_file_path(self, new_paths: list[str]) -> None:
        print(f"Adding {new_paths=}")
        for p in new_paths:
            self.file_paths.append(Path(p))

    def delete_file_path(self, indices: list[int]) -> None:
        # delete from back to front, to prevent changing index problems
        print(f"Deleting paths at {indices=}")
        for i in sorted(indices, reverse=True):
            del self.file_paths[i]

    def clear_file_paths(self) -> None:
        print("Files cleared")
        self.file_paths = []

    def switch_order(self, i: int, j: int) -> None:
        print(f"Switching indices {i} and {j}")
        self.file_paths[i], self.file_paths[j] = self.file_paths[j], self.file_paths[i]

    def display_files(self) -> list[str]:
        return [p.name for p in self.file_paths]

    def convert_files(self, c_type: ConversionType, save_loc: str) -> tuple[ConversionOutcome, str]:
        try:
            print("Trying to convert file/s")
            files = self._convert_files(c_type, Path(save_loc))
            print("Success! Returning data...")
            return ConversionOutcome.SUCCESS, f"Successfully saved: {files}"
        except Exception as e:
            print("Error! Returning error data")
            return ConversionOutcome.ERROR, str(e)

    def _convert_files(self, convertion_type_enum: ConversionType, save_location: Path) -> str:
        fmt = CONVERSION_TYPE_TO_FILE_FORMAT[convertion_type_enum]
        match convertion_type_enum:
            case ConversionType.PNG | ConversionType.JPG | ConversionType.PDF:
                print(f"Conversion type {convertion_type_enum}")
                file_paths = []
                for path in self.file_paths:
                    im = Image.open(path)
                    file_name = fr"{save_location}\{path.with_suffix(fmt).name}"
                    file_paths.append(file_name)
                    print(f"Trying to save at {file_name}")
                    im.save(file_name, optimize=True)
                return ", ".join(file_paths)
            case ConversionType.COMBINED_PDF:
                images = [Image.open(p) for p in self.file_paths]
                # for combined pdfs, use directory name as the file name
                file_name = fr"{save_location}\{save_location.with_suffix(fmt).name}"
                print(f"Trying to save at {file_name}")
                images[0].save(file_name, save_all=True, append_images=images[1:], optimize=True)
                return file_name
            case _:
                raise ValueError(f"{convertion_type_enum} is not implemented")
