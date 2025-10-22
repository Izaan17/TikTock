<div align="center">

# TikTock - TikTok Video Downloader

A powerful Python tool for downloading TikTok videos efficiently and safely.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![Stars](https://img.shields.io/github/stars/izaan17/TikTock.svg)](https://github.com/izaan17/TikTock/stargazers)
[![Forks](https://img.shields.io/github/forks/izaan17/TikTock.svg)](https://github.com/izaan17/TikTock/network)

[Quick Start](#quick-start) • [Features](#features) • [Installation](#installation) • [Usage](#usage) • [Contributing](#contributing)

</div>

## Overview

TikTock is a robust Python-based command-line tool designed to download TikTok videos efficiently and safely. Whether
you want to save a single video or bulk download from your TikTok data export, TikTock provides an intuitive interface
with powerful features.

## Features

**Multiple Download Methods**

- Single or multiple TikTok URLs
- Bulk download from JSON/text files
- Direct TikTok data export processing

**Advanced Functionality**

- Real-time progress tracking with visual feedback
- Watermark-free video downloads
- Customizable output directories
- Configurable download delays
- Adjustable chunk sizes for optimal performance
- Custom filename templates with dynamic placeholders

**Robust & Reliable**

- Comprehensive error handling
- Detailed download reports and logging
- URL validation before processing

**User Experience**

- Clean CLI with rich formatting
- Progress bars and status indicators
- Organized file management
- Detailed logging capabilities

## Quick Start

```bash
# Download a single video
python main.py https://www.tiktok.com/@username/video/1234567890

# Download multiple videos
python main.py url1 url2 url3 -o ./downloads

# Process from your TikTok data export
python main.py -r liked_videos.json --log download_log.json
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Step-by-step Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/izaan17/TikTock.git
   cd TikTock
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**

   ```bash
   python main.py --help
   ```

## Usage

### Basic Usage

**Download a single video:**

```bash
python main.py https://www.tiktok.com/@username/video/1234567890
```

**Download multiple videos:**

```bash
python main.py url1 url2 url3
```

**Specify output directory:**

```bash
python main.py https://www.tiktok.com/@username/video/1234567890 -o ./my_videos
```

> **Note:** The output directory must exist before running the command.

### File-based Downloads

**From a text file:**

```bash
python main.py -r urls.txt
```

**From TikTok data export:**

```bash
python main.py -r user_data.json
```

### Advanced Options

| Option            | Short | Description                                  | Example                                      |
|-------------------|-------|----------------------------------------------|----------------------------------------------|
| `--output`        | `-o`  | Output directory                             | `-o ./downloads`                             |
| `--recursive`     | `-r`  | Process URLs from file                       | `-r urls.txt`                                |
| `--delay`         | `-d`  | Delay between downloads (seconds)            | `-d 2`                                       |
| `--chunk-size`    | `-c`  | Download chunk size (bytes)                  | `-c 2048`                                    |
| `--log`           |       | Save download log                            | `--log my_log.json`                          |
| `--activity`      |       | Pre-select activity type                     | `--activity liked saved`                     |
| `--name-template` |       | Customize output filename using placeholders | `--name-template "{author}_{index}_{cdate}"` |

### Filename Template Examples

TikTock allows you to customize your downloaded filenames using placeholders:

| Template                                        | Example Output                                         | Description                                             |
|-------------------------------------------------|--------------------------------------------------------|---------------------------------------------------------|
| `{index}`                                       | `1.mp4`                                                | Index of the video in the current download session      |
| `{video_id}`                                    | `7554364340145523999.mp4`                              | TikTok video ID extracted from the URL                  |
| `{author}`                                      | `izaannyc.mp4`                                         | TikTok username of the video's author                   |
| `{cdate}`                                       | `2025-09-27_14-30-05.mp4`                              | Current timestamp in default format `%Y-%m-%d_%H-%M-%S` |
| `{author}_{index}`                              | `izaannyc_1.mp4`                                       | Combines author and index                               |
| `{author}_{video_id}_{cdate}`                   | `izaannyc_7554364340145523999_2025-09-27_14-30-05.mp4` | Combines multiple placeholders                          |
| `{cdate:%Y%m%d-%H%M}`                           | `20250927-1430.mp4`                                    | Custom strftime formatting for timestamp                |
| `{author}_{video_id}_{cdate:%Y-%m-%d_%H-%M-%S}` | `izaannyc_7554364340145523999_2025-09-27_14-30-05.mp4` | Full example with formatted date                        |

> **Tip:** You can mix and match placeholders in any order.
> `{cdate}` supports **Python strftime formatting**, allowing you to change the date format to your preference.

### Example Commands

```bash
# Download with 2-second delay and custom chunk size
python main.py https://tiktok.com/@user/video/123 -d 2 -c 4096

# Process TikTok export with logging
python main.py -r tiktok_data.json --log download_session.json

# Download to specific folder with delay
python main.py url1 url2 -o ./TikTok_Videos -d 1

# Download with custom filename template
python main.py https://tiktok.com/@user/video/123 --name-template "{author}_{index}_{cdate}"
```

## Supported File Formats

### Text Files (`.txt`)

Simple text files with one TikTok URL per line:

```
https://www.tiktok.com/@user1/video/1234567890
https://www.tiktok.com/@user2/video/0987654321
https://www.tiktok.com/@user3/video/1122334455
```

### JSON Files

#### Liked Videos (TikTok Export Format)

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

#### Favorite Videos (TikTok Export Format)

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

#### Custom JSON Format

```json
{
  "urls": [
    "https://www.tiktok.com/@username/video/1234567890",
    "https://www.tiktok.com/@username/video/0987654321"
  ]
}
```

## Getting Your TikTok Data

To download your personal TikTok data for bulk processing:

1. **Request your data**:
   Visit [TikTok's data download page](https://support.tiktok.com/en/account-and-privacy/personalized-ads-and-data/requesting-your-data)
2. **Choose JSON format**: Select JSON format (TXT format is not currently supported)
3. **Wait for email**: TikTok will email you when your data is ready
4. **Download & extract**: Download the zip file and extract it
5. **Use with TikTock**: Use the JSON files with the `-r` option

### System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python Version**: 3.8 or higher
- **Internet**: Stable connection required for downloads

## Supported File Formats

### Text Files (`.txt`)

Simple text files with one TikTok URL per line:

```
https://www.tiktok.com/@user1/video/1234567890
https://www.tiktok.com/@user2/video/0987654321
https://www.tiktok.com/@user3/video/1122334455
```

### JSON Files

#### Liked Videos (TikTok Export Format)

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

#### Favorite Videos (TikTok Export Format)

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

#### Custom JSON Format

```json
{
  "urls": [
    "https://www.tiktok.com/@username/video/1234567890",
    "https://www.tiktok.com/@username/video/0987654321"
  ]
}
```

## Getting Your TikTok Data

To download your personal TikTok data for bulk processing:

1. **Request your data**:
   Visit [TikTok's data download page](https://support.tiktok.com/en/account-and-privacy/personalized-ads-and-data/requesting-your-data)
2. **Choose JSON format**: Select JSON format (TXT format is not currently supported)
3. **Wait for email**: TikTok will email you when your data is ready
4. **Download & extract**: Download the zip file and extract it
5. **Use with TikTock**: Use the JSON files with the `-r` option

### System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python Version**: 3.8 or higher
- **Internet**: Stable connection required for downloads

## Troubleshooting

### Common Issues

#### "Invalid TikTok URL" Error

- Ensure the URL follows the correct TikTok format
- Check that the video is publicly accessible
- Verify the URL is not broken or expired

#### "Directory not found" Error

- Create the output directory before running the command
- Use absolute paths when possible
- Check directory permissions

#### Network/Connection Issues

- Check your internet connection
- Try reducing chunk size: `-c 512`
- Add delay between downloads: `-d 3`

## Contributions

<a href="https://github.com/hatchcanon" style="display: flex; align-items: center; text-decoration: none;">
  <img src="https://avatars.githubusercontent.com/u/10931888?v=4" alt="Hatch canon" width="35" height="35" style="border-radius: 50%;" />
  <span style="margin-left: 10px; color: inherit;">Hatch canon</span>
</a>


Contributions are welcome!

### Bug Reports

Found a bug? Please create an issue with:

- Detailed description of the problem
- Steps to reproduce
- Expected vs actual behavior
- System information (OS, Python version)
- Error messages or logs

## Legal Disclaimer

**Important**: This tool is intended for educational and personal use only.

- **Respect Copyright**: Only download content you have permission to download
- **Follow Terms of Service**: Respect TikTok's Terms of Service
- **Privacy**: Be mindful of privacy when downloading content
- **No Liability**: The developers are not responsible for any misuse of this tool

By using TikTock, you agree to use it responsibly and in accordance with all applicable laws and regulations.

**Made by [Izaan Noman](https://github.com/izaan17)**

If you find this project helpful, please consider giving it a star!
