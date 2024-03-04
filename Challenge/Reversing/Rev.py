def extract(file_path):
    try:
        with open(file_path, 'r') as file:
            output = file.read()
        
        lines = output.split('\n')

        magic_value = None
        start_section_headers = None
        size_section_headers = None

        for line in lines:
            if "Magic:" in line:
                # Split the line and extract the magic value
                parts = line.split()
                if len(parts) > 1:
                    magic_value = ''.join(parts[1:]).replace(' ', '')

            elif "Start of section headers:" in line:
                # Split the line and extract the start of section headers value
                parts = line.split()
                if len(parts) > 4:
                    start_section_headers = int(parts[4])

            elif "Size of section headers:" in line:
                # Split the line and extract the size of section headers value
                parts = line.split()
                if len(parts) > 4:
                    size_section_headers = int(parts[4])
            elif "Number of section headers:" in line:  
                parts = line.split(':')
                if len(parts) > 1:
                    number_of_section_headers = int(parts[1].strip())

        return magic_value, start_section_headers, size_section_headers , number_of_section_headers

    except Exception as e:
        print(f"Error: {str(e)}")

def magicAnalyzer(magic_value):
    data = "MagicAnalyzer:\n"
    #remove padding 
    magic_value = magic_value[:-14]
    #remove magic fixed value
    magic_value = magic_value[8:]
    #extacting values
    class_value = magic_value[:2]
    data_value = magic_value[2:4]
    version_value = magic_value[5:6]
    OS_value = magic_value[6:8]
    #idenify the 32/64 objects
    if class_value == '01':
        data += "  32bit objects"
    else:
        data += "  64bit objects"
    #idenify the LSB/MSB
    if data_value == '01': 
        data += "\n  LSB data"
    else:
        data += "\n  MSB data"
    data += f"\n  Version {version_value}"
    #idenify the OS
    if OS_value == '01': 
        data += "\n  OS is HP-UX"
    elif OS_value == '02':
        data += "\n  OS is NetBSD"
    elif OS_value == '03':
        data += "\n  OS is Linux"
    else:
        data += "\n  OS is None"
    return data

def binarySize(start_section_headers,size_section_headers,number_of_section_headers):
    # calculate the size of the entire binary
    size = start_section_headers + (number_of_section_headers * size_section_headers)
    res = f"the size of the entire binary = {size} bit = {size/8} bytes"
    return res

# Example usage
file_path = 'getting-started/elf'
magic_value, start_section_headers, size_section_headers , number_of_section_headers= extract(file_path)

res = magicAnalyzer(magic_value=magic_value)
print(res)

size = binarySize(start_section_headers,size_section_headers,number_of_section_headers)
print(size)

print("Start section headers: ",start_section_headers)
print("Number of section headers ",number_of_section_headers)
print("Size section headers",size_section_headers)