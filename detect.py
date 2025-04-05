import os
import binascii
from datetime import datetime

# Known file signatures (magic numbers)
SIGNATURES = {
    '.jpg': 'ffd8',              # JPEG (start marker)
    '.png': '89504e47',          # PNG (signature)
    '.exe': '4d5a',              # EXE (MZ header)
    '.pdf': '25504446',          # PDF (%PDF header)
    '.txt': 'efbbbf',            # UTF-8 text (BOM, optional)
    '.mp4': '66747970',          # MP4 (ftyp marker)
    '.gif': '47494638',          # GIF (GIF8 header)
    '.zip': '504b0304',          # ZIP (local file header)
    '.rar': '52617221',          # RAR (Rar! signature)
    '.docx': '504b0304',         # DOCX (ZIP-based, same as .zip)
    '.xlsx': '504b0304',         # XLSX (ZIP-based, same as .zip)
    '.wav': '52494646',          # WAV (RIFF header)
    '.avi': '52494646',          # AVI (RIFF header, with 'AVI ' after)
    '.mov': '6d6f6f76',          # MOV (moov atom, QuickTime)
    '.doc': 'd0cf11e0',          # DOC (OLE compound file)
    '.pptx': '504b0304',         # PPTX (ZIP-based, same as .zip)
    '.bmp': '424d',              # BMP (BM header)
    '.iso': '4344303031',        # ISO (CD001 signature)
    '.flv': '464c56',            # FLV (FLV header)
    '.swf': '465753'             # SWF (FWS or CWS header)
}

def check_signature(file_path):
    
    try:
        with open(file_path, 'rb') as f: #convert file into binary form
            header = f.read(8)  
            return binascii.hexlify(header).decode('utf-8').lower()
    except Exception as e:
        return f"Error: {e}"

def scan_usb(path):
    
    print(f"Scanning USB at: {path}")
    
    # Report file setup
    report_file = "scan_report.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(report_file, "w") as f:
        f.write(f"USB Scan Report\n")
        f.write(f"Scan started at: {timestamp}\n")
        f.write(f"Target path: {path}\n")
        f.write("-" * 50 + "\n")

    # Scan logic with report logging
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            result = ""
            
            if ext in SIGNATURES:
                hex_header = check_signature(file_path)
                if "Error" in hex_header:
                    result = f"Failed to read: {file_path} - {hex_header}"
                elif not hex_header.startswith(SIGNATURES[ext]):
                    result = (f"FAKE DETECTED! {file_path}\n"
                              f"Expected: {SIGNATURES[ext]}, Found: {hex_header[:8]}"
                              f"\n")
                else:
                    result = f"VALID: {file_path} - Signature: {hex_header[:8]}"
            else:
                result = f"UNKNOWN EXTENSION: {file_path}\n"
            
            # Print to console
            print(result)
            # Write to report file
            with open(report_file, "a") as f:
                f.write(result + "\n")

    # Finalize report
    with open(report_file, "a") as f:
        f.write("-" * 50 + "\n")
        f.write(f"Scan completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    print(f"Report saved to {report_file}")

# Run the tool
if __name__ == "__main__":
    usb_path = input("Enter file path (e.g., D:/ or /media/usb): ")
    if os.path.exists(usb_path):
        scan_usb(usb_path)
    else:
        print("Invalid path")
