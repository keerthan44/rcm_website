import asyncio
import websockets
import json

# Store connected clients
connected_clients = set()

async def handler(websocket):
    """WebSocket connection handler"""
    client_id = id(websocket)
    try:
        # Add client to set of connected clients
        connected_clients.add(websocket)
        print(f"New client connected. ID: {client_id}")
        print(f"Total clients connected: {len(connected_clients)}")
        
        while True:
            data = await websocket.recv()
            print(f"Received from client {client_id}: {data}")
            
            try:
                # Try to parse as JSON first
                message = {"value": data}
            except json.JSONDecodeError:
                # If not JSON, treat as regular message
                message = {"value": data}
            
            # Broadcast to all connected clients
            for client in connected_clients:
                try:
                    await client.send(json.dumps(message))
                    print(f"Sent to client {id(client)}: {message}")
                except websockets.exceptions.ConnectionClosed:
                    print(f"Failed to send to client {id(client)} - connection closed")
                except Exception as e:
                    print(f"Error sending to client {id(client)}: {e}")
                    
    except websockets.exceptions.ConnectionClosed:
        print(f"Client {client_id} connection closed")
    except Exception as e:
        print(f"Error with client {client_id}: {e}")
    finally:
        connected_clients.remove(websocket)
        print(f"Client {client_id} removed. Total clients: {len(connected_clients)}")

async def main():
    """Start WebSocket server"""
    server = await websockets.serve(handler, "localhost", 8765)
    print("WebSocket server started on ws://localhost:8765")
    await asyncio.Future()  # run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped by user")
