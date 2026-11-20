# MasWeb

<div align="center">

```
.___  ___.      ___           _______.____    __    ____  _______ .______   
|   \/   |     /   \         /       |\   \  /  \  /   / |   ____||   _  \  
|  \  /  |    /  ^  \       |   (----` \   \/    \/   /  |  |__   |  |_)  | 
|  |\/|  |   /  /_\  \       \   \      \            /   |   __|  |   _  <  
|  |  |  |  /  _____  \  .----)   |      \    /\    /    |  |____ |  |_)  | 
|__|  |__| /__/     \__\ |_______/        \__/  \__/     |_______||______/  
```

**A multi-threaded web service scanner for common web ports**

</div>

## Overview

MasWeb is a Python-based reconnaissance tool designed to scan multiple domains across common web service ports. It performs HTTP/HTTPS requests, extracts website titles, server banners, response codes, and other metadata from target domains running web services on various ports.

This tool is useful for:
- **Reconnaissance**: Quickly identify web services running on target domains
- **Port Scanning**: Check common web service ports (80, 443, 8080, 8000, 8443, 8081, 9090, 9080)
- **Information Gathering**: Extract titles, server banners, X-Powered-By headers, and cache information
- **Security Testing**: Gather metadata for vulnerability assessment and penetration testing

## Features

✨ **Multi-threaded Scanning**: Scan multiple domains concurrently for faster results
📡 **Common Web Ports**: Checks standard web service ports (80, 443, 8080, 8000, 8443, 8081, 9090, 9080)
🔍 **Detailed Information**: Extracts:
  - HTTP Status Codes
  - Page Titles
  - Server Banners
  - X-Powered-By Headers
  - Cache Headers
  - Redirect Locations
  - Response Content Length
⏱️ **Configurable Timeout**: Set custom connection timeout values
🔒 **HTTPS Support**: Handles both HTTP and HTTPS connections with SSL verification disabled
🧵 **Thread Control**: Adjust the number of worker threads for performance tuning

## Requirements

- Python 2.7+
- `requests` library
- `beautifulsoup4` library
- `urllib3` library (usually included with requests)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/eln1x/masweb.git
cd masweb
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Required packages:
- `requests`
- `beautifulsoup4`

## Usage

### Basic Usage

```bash
python masweb.py --domains list.txt -t 10 -x 5
```

### Command-Line Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--domains` | `-d` | Path to file containing domain list (one domain per line) | Required |
| `--threads` | `-t` | Number of concurrent threads for scanning | 10 |
| `--timeout` | `-x` | Connection timeout in seconds | 5 |

### Examples

**Scan domains with 20 threads and 10-second timeout:**
```bash
python masweb.py -d domains.txt -t 20 -x 10
```

**Scan domains with default settings:**
```bash
python masweb.py --domains targets.txt
```

## Input Format

Create a text file with one domain per line:

**domains.txt:**
```
example.com
google.com
github.com
internal-service.local
api.mycompany.com
```

## Output Explanation

The scanner provides color-coded output for different HTTP status code ranges:

### Status Code Ranges:

**2xx - Success** (Green)
```
[-] 200 Ok: example.com:80 - Banner: Apache/2.4.1 - Title: Home Page - Powered: PHP/7.0.0 Length: 2048
```

**3xx - Redirect** (Yellow)
```
[-] 301 RD: example.com:80 - Banner: nginx/1.14.0 - Length: 512 - Location: https://example.com - Hit: HIT
```

**4xx - Not Found** (Yellow)
```
[-] 404 NF: example.com:8080 - Banner: Apache/2.4.1 - Length: 162
```

**5xx - Server Error** (Yellow)
```
[-] 500 ER: example.com:9090 - Banner: Python/3.6 - Length: 1024
```

## How It Works

1. **Load Domains**: Reads domain names from the specified input file
2. **Queue Processing**: Places each domain into a queue for processing
3. **Thread Workers**: Multiple threads pick domains from the queue
4. **Port Scanning**: For each domain, the tool attempts to connect on 8 common web ports
5. **Data Extraction**: 
   - Retrieves HTTP headers (Server, X-Powered-By, X-Cache, Location)
   - Extracts page title from HTML
   - Records response status code and content length
6. **Result Display**: Prints color-coded results with metadata

## Ports Scanned

The tool scans the following common web service ports:
- **80** - HTTP (standard)
- **443** - HTTPS (standard)
- **8080** - Alternate HTTP
- **8000** - Development/alternate HTTP
- **8443** - Alternate HTTPS
- **8081** - Alternate HTTP
- **9090** - Alternate HTTP (commonly used by Java applications)
- **9080** - Alternate HTTP (commonly used by application servers)

## Error Handling

The tool gracefully handles various connection errors:
- Connection errors
- Too many redirects
- Read timeouts
- Invalid URLs

Failed connections are silently skipped and the scan continues.

## Threading Model

- **Thread-Safe Output**: Uses locks to prevent output corruption from multiple threads
- **Queue-Based Distribution**: Domains are distributed to worker threads via a queue
- **Daemon Threads**: Worker threads run as daemon threads and are terminated after all domains are processed

## Author

**Ahmad Mahfouz** (@eln1x)

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

```
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
```

## Disclaimer

This tool is designed for authorized security testing and reconnaissance only. Users are responsible for ensuring they have permission to scan target domains. Unauthorized scanning may violate laws and regulations. The author assumes no liability for misuse of this tool.

## Tips & Best Practices

🔧 **Performance Tuning**:
- Use 10-20 threads for most scenarios
- Increase threads for larger domain lists
- Adjust timeout based on network conditions

🎯 **Target Preparation**:
- Keep domain lists organized and clean
- Remove duplicates for efficiency
- Test with a small list first

🛡️ **Security Considerations**:
- Run from authorized networks only
- Respect rate limiting and resource usage
- Consider adding delays between requests for large scans

## Troubleshooting

**"Error: please install the requirements"**
```bash
pip install -r requirements.txt
```

**Script hangs or runs slowly**
- Reduce the timeout value with `-x`
- Increase threads with `-t`
- Check your network connection

**No output on target domains**
- Verify domain names are correct
- Check if domains/ports are accessible from your network
- Try with a smaller timeout value

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

<div align="center">

**Made with ❤️ by Ahmad Mahfouz**

</div>
