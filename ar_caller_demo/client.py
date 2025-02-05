import asyncio
import websockets
import json
import time

async def connect_with_retry():
    """Connect to WebSocket server with retry logic"""
    uri = "ws://localhost:8765"
    max_retries = 100
    retry_delay = 3  # seconds
    
    for attempt in range(max_retries):
        try:
            return await websockets.connect(uri)
        except (websockets.exceptions.ConnectionClosed, ConnectionRefusedError):
            if attempt < max_retries - 1:
                print(f"Connection attempt {attempt + 1} failed. Retrying in {retry_delay} seconds...")
                await asyncio.sleep(retry_delay)
            else:
                raise Exception("Max retry attempts reached")

async def send_input():
    """Send input from file to WebSocket server"""
    try:
        # Open and read the file
        with open('input.txt', 'r') as file:
            lines = file.readlines()
        
        current_line = 0
        websocket = None
        
        while current_line < len(lines):
            if websocket is None:
                try:
                    websocket = await connect_with_retry()
                    print("Connected to server. Press Enter to send next line (Ctrl+C to quit)")
                except Exception as e:
                    print(f"Failed to connect: {e}")
                    return

            try:
                # Wait for user to press Enter
                input("Press Enter to send next line...")
                
                # Clean the line
                data = lines[current_line].strip()
                if not data:  # Skip empty lines
                    current_line += 1
                    continue
                
                # Send the data
                await websocket.send(data)
                print(f"Sent: {data}")
                
                # Wait for response
                response = await websocket.recv()
                print(f"Server echoed: {response}")
                
                current_line += 1
                
            except (websockets.exceptions.ConnectionClosed, ConnectionRefusedError):
                print("Connection lost. Will retry on next Enter press...")
                websocket = None
                continue
            
        print("Reached end of file")
                
    except FileNotFoundError:
        print("Error: input.txt file not found")
    except KeyboardInterrupt:
        print("\nClient stopped by user")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        if websocket:
            try:
                await websocket.close()
            except:
                pass

if __name__ == "__main__":
    try:
        asyncio.run(send_input())
    except KeyboardInterrupt:
        print("\nClient stopped by user")
