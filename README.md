# TikTok Video Downloader

A Python-based tool for downloading TikTok videos from URLs or files containing multiple URLs. The tool supports both
command-line arguments and file-based input, with progress tracking and detailed download reports.

---

## Features

- **Multiple URL Support**: Download videos from multiple TikTok URLs at once.
- **File Input**: Process URLs from JSON or text files.
- **Progress Tracking**: Real-time download progress with rich visual feedback.
- **Error Handling**: Detailed error reporting for failed downloads.
- **Customizable**: Set download delay, chunk size, and output directory.
- **Time Saving**: Take a snapshot of your TikTok data and keep it saved forever.
- **No Watermark**: Download videos without a watermark.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/izaan17/TikTock.git
   cd tiktock
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Basic Command-Line Usage

Download videos from one or more TikTok URLs:

```bash
python main.py https://www.tiktok.com/@username/video/1234567890
```

### Download to a Specific Directory

Specify an output directory (it must exist):

```bash
python main.py https://www.tiktok.com/@username/video/1234567890 -o ./videos
```

### Process URLs from a File

Download videos from a file containing TikTok URLs:

```bash
python main.py -r urls.txt
```

### Advanced Options

- **Delay between downloads**: Set a delay (in seconds) between downloads:
  ```bash
  python main.py https://www.tiktok.com/@username/video/1234567890 -d 2
  ```
- **Chunk size**: Adjust the download chunk size (in bytes):
  ```bash
  python main.py https://www.tiktok.com/@username/video/1234567890 -c 2048
  ```

---

### **Log File**:

Save a JSON log of both failed and successfully processed URLs.

**Arguments**:

- `FILE_NAME`: The name of the log file (defaults to `tiktock_log.json`).

**Example Usage**:

```bash
python main.py https://www.tiktok.com/@username/video/1234567890 --log FILE_NAME
```

---

## Supported File Formats

### Text Files (`.txt`)

Plain text files with one TikTok URL per line:

```
https://www.tiktok.com/@username/video/1234567890
https://www.tiktok.com/@username/video/0987654321
```

### JSON Files (`.json`)

TikTok JSON data files (e.g., from TikTok's data export feature):

### Instructions for Downloading Your TikTok Data

To download your TikTok data to get all saved favorites and liked videos, please check out
this [link](https://support.tiktok.com/en/account-and-privacy/personalized-ads-and-data/requesting-your-data). Please
make sure to download the JSON version the txt version is not supported yet.

#### Liked Videos List

```json
{
  "Activity": {
    "Like List": {
      "ItemFavoriteList": [
        {
          "date": "2025-01-01",
          "link": "https://www.tiktok.com/@username/video/1234567890"
        }
      ]
    }
  }
}
```

#### Favorite Videos List

```json
{
  "Activity": {
    "Favorite Videos": {
      "FavoriteVideoList": [
        {
          "Date": "2025-01-01",
          "Link": "https://www.tiktok.com/@username/video/1234567890"
        }
      ]
    }
  }
}
```

#### Custom JSON

```json
{
  "urls": [
    "https://www.tiktok.com/@username/video/1234567890",
    "https://www.tiktok.com/@username/video/0987654321"
  ]
}
```

---

## Requirements

- Python 3.8+
- Dependencies:
    - `requests`
    - `rich`
    - `argparse`

Install dependencies using:

```bash
pip install -r requirements.txt
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request with a detailed description of your changes.

---

## Disclaimer

This tool is for educational purposes only. Ensure you have the right to download and use the content. The developers
are not responsible for any misuse of this tool.
