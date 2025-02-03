import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
import socketio
from db.model import Note
from api.socket import socket_manager
