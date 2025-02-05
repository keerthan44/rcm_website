import json

def convert_transcript_to_json():
    try:
        # Read from transcript.txt
        with open('transcript.txt', 'r') as file:
            lines = file.readlines()

        # Open output file
        with open('transcript_output.txt', 'w') as outfile:
            for line in lines:
                # Skip empty lines
                if not line.strip():
                    continue
                
                # Split the line by first colon
                parts = line.split(':', 1)
                if len(parts) == 2:
                    speaker = parts[0].strip()
                    text = parts[1].strip()
                    
                    # Create the JSON structure
                    json_data = {
                        "conversation_transcript": {
                            "speaker": speaker,
                            "conversation_text": text
                        }
                    }
                    
                    # Write to output file
                    outfile.write(json.dumps(json_data) + '\n')

    except FileNotFoundError:
        print("Error: transcript.txt file not found")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    convert_transcript_to_json()
