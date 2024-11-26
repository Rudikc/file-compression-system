# File Compression System

A Python-based file compression system supporting multiple compression algorithms (ZIP, GZIP, LZMA) with optional
encryption. The system provides both a CLI and a GUI for user interaction, enabling efficient file compression and
decompression.

---

## Features

- **Multiple Compression Algorithms**: Supports ZIP, GZIP, and LZMA formats.
- **Encryption Support**: Optionally encrypt compressed files with password protection.
- **Dual Interface**:
    - **CLI**: For users comfortable with command-line operations.
    - **GUI**: User-friendly graphical interface for ease of use.
- **Task History Logging**: Tracks completed compression and decompression tasks.

---

## Requirements

### Minimum System Requirements

- **Processor**: Dual-core CPU
- **Memory**: 4 GB RAM
- **Storage**: 100 MB of free disk space
- **Operating System**: Windows 10, Ubuntu 18.04, or macOS Mojave
- **Python**: 3.8 or higher

---

## Installation

Go to release [page](https://github.com/Rudikc/file-compression-system/releases) and download the latest version of the
application for your operating system.

---

## Usage

### GUI

To run the GUI, just run the executable file. After that, the GUI will open.
Next, you can select the files you want to compress, the compression algorithm, and the encryption option.
GUI lets you to set some default settings like default destination, default compression algorithm, and if the encryption
is enabled by default.

**Example:**

```shell
./file-compression-system
```

### CLI

#### Compression

To compress files, run the executable in the terminal with following arguments:

- To compress, start with the `compress` command.
- `--files` or `-f` flag followed by the path to the files you want to compress. Multiple files can be
  compressed by separating the paths with a space.
- `--algorithm` or `-a` flag to specify the compression algorithm (ZIP, GZIP, or LZMA).
- `--output` or `-o` flag to specify the output file name.
- `--password` or `-p` flag to specify the password for encryption (optional).

**example:**

```shell
./file-compression-system compress -f file1.txt file2.txt -a zip -o compressed_archive -p StrongPassword123
```

#### Decompression

To decompress files, run the executable in the terminal with following arguments:

- To decompress, start with the `decompress` command.
- `--file` or `-f` flag followed by the path to the file you want to decompress.
- `--output` or `-o` flag to specify the output directory.
- `--password` or `-p` flag to specify the password for decryption (optional).

No need to specify the compression algorithm when decompressing, as the system will automatically detect the algorithm

**Example:**

```shell
./file-compression-system decompress -f compressed_archive.zip -o decompressed_files -p StrongPassword123
```




